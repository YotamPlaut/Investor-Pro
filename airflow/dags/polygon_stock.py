from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime


with DAG(
        dag_id='polygon_stock_extract',
        start_date=datetime(2024, 1, 1),
        schedule_interval='@daily',
        catchup=False
) as dag:
    pass