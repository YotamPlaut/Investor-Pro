import json
import logging
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from airflow import DAG

from utilities.tase_api import stock_list
from utilities.tase_stock_stats import calc_stock_stats_sharp_ratio


def extract_stock_data_from_db(stock_index, start_date: datetime = datetime(1970, 1, 1), **kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    select_query = f"SELECT * FROM stocks.tase_stock_data WHERE date >= '{start_date}' and index_symbol={stock_index};"
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(select_query)
    records = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    stock_info = pd.DataFrame(records, columns=column_names)
    logging.info(f"done querying data for index: {stock_index}")
    logging.info(f"df results\n: {stock_info}")

    stock_info_json = stock_info.to_json(orient='split')
    # Push the JSON string to XCom
    if stock_info_json:
        kwargs['ti'].xcom_push(key=f'{stock_index}', value=stock_info_json)
        logging.info(f"succeed to push data to XCom: stock_info_json {stock_info_json}")
    else:
        logging.error("Failed to push data to XCom: stock_info_json is None")


def run_stock_stats_sharp_ratio(stock_index, **kwargs):
    symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(stock_index)), None)
    stock_info_json = kwargs['ti'].xcom_pull(task_ids=f"extract_{symbol_name}_info", key=f'{stock_index}')
    if stock_info_json:
        stock_info = pd.read_json(stock_info_json, orient='split')
        logging.info(f"Processing data for index: {stock_index}")
        logging.info(f"df results\n: {stock_info}")
    else:
        logging.error(f"can't find data for for symbol_name: {symbol_name}")
        return
    sharp_ratio_json = calc_stock_stats_sharp_ratio(stock_data=stock_info)
    logging.info(f"sharp_ratio_dict: {sharp_ratio_json}")
    if sharp_ratio_json:
        kwargs['ti'].xcom_push(key=f'{stock_index}_sharp_ratio', value=sharp_ratio_json)
        logging.info(f"succeed to push data to XCom: {stock_index}_sharp_ratio: {sharp_ratio_json}")
    else:
        logging.error("Failed to push data to XCom: stock_info_json is None")





default_args = {
    'start_date': datetime(2024, 6, 11),
    'schedule_interval': '0 2 * * *',
    'catchup': False,
    'depends_on_past': True,
}
with DAG(
        dag_id='tase_stock_stats',
        default_args=default_args,
        max_active_runs=1
) as dag:
    start_dummy = DummyOperator(
        task_id='start_dummy'
    )
    for stock in stock_list:
        extract_stock_data_from_db_task = PythonOperator(
            task_id=f"extract_{stock['name']}_info",
            python_callable=extract_stock_data_from_db,
            op_args=[stock['index_id']],
            provide_context=True
            # trigger_rule='one_success'
        )
        run_stock_stats_sharp_ratio_task = PythonOperator(
            task_id=f"run_stats_{stock['name']}_sharp_ratio",
            python_callable=run_stock_stats_sharp_ratio,
            op_args=[stock['index_id']],
            provide_context=True
        )

        start_dummy >> extract_stock_data_from_db_task >> run_stock_stats_sharp_ratio_task
