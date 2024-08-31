import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from datetime import datetime,date
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
import pandas as pd

from pandas import read_parquet
from utilities.ml import add_feature, add_lag_feature
from utilities.tase_api import (
    stock_list,
    table_configs,
    get_Bar,
    indices_EoD_by_index_from_date_to_date,
    securities_EoD_by_index_from_date_to_date,
    )


def collect_data(index_symbol, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')

    select_query = """
        SELECT 
            date,
            close
        FROM stocks.tase_stock_data    
        WHERE index_symbol = 137
        AND date <= '2024-07-18'::date;
    """


    db_info = postgres_hook.get_pandas_df(sql=select_query)
    db_info['date'] = pd.to_datetime(db_info['date'])
    db_info.set_index('date', inplace=True)

    api_end_date = db_info.index.min() - timedelta(days=1)
    db_num_rows = len(db_info)

    api_start_date = api_end_date - timedelta(days=(403 - db_num_rows))
    api_start_date = api_start_date.strftime('%Y-%m-%d')
    api_end_date = api_end_date.strftime('%Y-%m-%d')

    bearer_token = get_Bar()
    is_index = next(
        (stock['IsIndex'] for stock in stock_list if stock['index_id'] == index_symbol),
        None
    )

    logging.info(f"bearer_token: {bearer_token}")
    logging.info(f"index_symbol: {index_symbol}")
    logging.info(f"api_start_date: {api_start_date}")
    logging.info(f"api_end_date: {api_end_date}")
    logging.info(f"is_index: {is_index}")

    if is_index:
        logging.info("here")
        api_info = indices_EoD_by_index_from_date_to_date(
            bearer=bearer_token, index_id=index_symbol,
            start_date='2023-05-24', end_date='2024-05-19'
        )
    else:
        logging.info("in there")
        api_info = securities_EoD_by_index_from_date_to_date(
            bearer=bearer_token, index_id=index_symbol,
            start_date=api_start_date, end_date=api_end_date
        )
    logging.info(f"api_info: {api_info}")

    api_info = api_info[['date', 'close']]
    api_info['date'] = pd.to_datetime(api_info['date'])
    api_info.set_index('date', inplace=True)

    # Merge the two data sources.
    df = pd.concat([api_info, db_info]).sort_index()
    df.to_parquet(f'{index_symbol}_temp.parquet', engine='pyarrow')
    df.to_csv(f'{index_symbol}_temp.csv')


default_args = {
    'start_date': datetime(2024, 7, 18),
    'end_date': datetime(2024, 8, 1),
    'schedule_interval': '0 2 * * *',
    'catchup': False,
    'depends_on_past': True,
}
with DAG(
        dag_id='test_dag',
        default_args=default_args,
        max_active_runs=1
) as dag:
    collect_data = PythonOperator(
        task_id=f"collect_data",
        python_callable=collect_data,
        op_args=[137],
        provide_context=True
    )
