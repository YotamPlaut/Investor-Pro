import json
import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from datetime import datetime, date
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from datetime import timedelta
import os
import pickle

from pandas import read_parquet
from utilities.ml import train_xgboost_regressor, predict_on_xgboost_regressor

from utilities.tase_api import (
    stock_list,
    table_configs,
    get_Bar,
    indices_EoD_by_index_from_date_to_date,
    securities_EoD_by_index_from_date_to_date,
)


def store_bearer_token(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    bearer = get_Bar()
    kwargs['ti'].xcom_push(key='bearer', value=bearer)
    logging.info(f"API call for bearer succeeded for date: '{execution_date}'bearer is:{bearer}")


def collect_data(stock_index, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')

    select_query = f"""
        SELECT
            date,
            close
        FROM stocks.tase_stock_data
        WHERE index_symbol = {stock_index}
        AND date <= '{execution_date}'::date;
    """
    logging.info(select_query)

    db_info = postgres_hook.get_pandas_df(sql=select_query)
    db_info['date'] = pd.to_datetime(db_info['date'])
    db_info.set_index('date', inplace=True)
    db_info.sort_index()

    api_end_date = db_info.index.min() - timedelta(days=1)
    db_num_rows = len(db_info)

    api_start_date = api_end_date - timedelta(days=(403 - db_num_rows))
    api_start_date = api_start_date.strftime('%Y-%m-%d')
    api_end_date = api_end_date.strftime('%Y-%m-%d')
    # bearer_token = get_Bar()
    bearer_token = kwargs['ti'].xcom_pull(task_ids='get_bearer_token', key='bearer')

    logging.info(f"---stock_index: {stock_index}")
    logging.info(f"---bearer_token: {bearer_token}")
    logging.info(f"---api_start_date: {api_start_date}")
    logging.info(f"---api_end_date: {api_end_date}")

    is_index = next(
        (stock['IsIndex'] for stock in stock_list if stock['index_id'] == stock_index),
        None
    )
    if is_index:
        api_info = indices_EoD_by_index_from_date_to_date(
            bearer=bearer_token, index_id=stock_index,
            start_date=api_start_date, end_date=api_end_date
        )
    else:
        api_info = securities_EoD_by_index_from_date_to_date(
            bearer=bearer_token, index_id=stock_index,
            start_date=api_start_date, end_date=api_end_date
        )
    logging.info(f"----api_info: {api_info}---")
    api_info = api_info[['date', 'close']]
    api_info['date'] = pd.to_datetime(api_info['date'])
    api_info.set_index('date', inplace=True)
    api_info.sort_index()

    # Merge the two data sources.
    df = pd.concat([api_info, db_info]).sort_index()
    logging.info(f"---final df: {df.head(10)}")

    # save data to temperately location
    os.makedirs('/opt/airflow/temp_data', exist_ok=True)
    df.to_parquet(f'/opt/airflow/temp_data/{stock_index}_temp_{execution_date}.parquet', engine='pyarrow')
    df.to_csv(f'/opt/airflow/temp_data/{stock_index}_temp_{execution_date}.csv')


def train_model(stock_index, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    df = pd.read_parquet(f'/opt/airflow/temp_data/{stock_index}_temp_{execution_date}.parquet')
    reg = train_xgboost_regressor(df)
    os.makedirs('/opt/airflow/temp_regressors', exist_ok=True)
    with open(f'/opt/airflow/temp_regressors/{stock_index}_regressor_{execution_date}.pkl', 'wb') as f:
        pickle.dump(reg, f)
    return


def predict_future_days(stock_index, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')

    df = pd.read_parquet(f'/opt/airflow/temp_data/{stock_index}_temp_{execution_date}.parquet')
    with open(f'/opt/airflow/temp_regressors/{stock_index}_regressor_{execution_date}.pkl', 'rb') as f:
        regressor = pickle.load(f)

    predictions = predict_on_xgboost_regressor(reg=regressor, df=df)
    with open(f'/opt/airflow/temp_predictions/{stock_index}_predictions_{execution_date}.json', 'w') as f:
        f.write(predictions)


default_args = {
    'start_date': datetime(2024, 7, 18),
    'end_date': datetime(2024, 7, 19),
    'schedule_interval': '0 2 * * *',
    'catchup': False,
    'depends_on_past': True,
}
with DAG(
        dag_id='tase_stock_predict',
        default_args=default_args,
        max_active_runs=1
) as dag:
    get_bearer_token = PythonOperator(
        task_id='get_bearer_token',
        python_callable=store_bearer_token,
        provide_context=True
    )

    for stock in stock_list:
        collect_data_task = PythonOperator(
            task_id=f"collect_data_{stock['index_id']}",
            python_callable=collect_data,
            op_args=[stock['index_id']],
            provide_context=True
        )
        train_model_task = PythonOperator(
            task_id=f"train_model_{stock['index_id']}",
            python_callable=train_model,
            op_args=[stock['index_id']],
            provide_context=True
        )
        predict_future_days_task = PythonOperator(
            task_id=f"predict_future_days_{stock['index_id']}",
            python_callable=predict_future_days,
            op_args=[stock['index_id']],
            provide_context=True
        )

        # Define task dependencies
        get_bearer_token >> collect_data_task >> train_model_task >> predict_future_days_task
