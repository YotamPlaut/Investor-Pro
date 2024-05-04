from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
from airflow.operators.python import PythonOperator

import logging
from utilities.tase_api import get_Bar, indices_EoD_by_date


def store_bearer_token(**kwargs):
    bearer = get_Bar()
    kwargs['ti'].xcom_push(key='bearer', value=bearer)


with DAG(
        dag_id='tase_stock_extract',
        start_date=datetime(2024, 5, 1),
        schedule_interval='@daily',
        catchup=False
) as dag:
    get_Bearer_token = PythonOperator(
        task_id='get_bearer_token',
        python_callable=store_bearer_token
    )
get_Bearer_token
