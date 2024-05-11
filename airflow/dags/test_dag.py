import logging
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


def execute_sql_and_log_result(**kwargs):
    # Connect to PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    query = """
            INSERT INTO stocks.tase_stock_data (index_symbol, symbol_name, date, open, close, high, low)
        VALUES ('142', 'shahar_stock', '2024-05-02', '1941.61', '1939.48', '1945.36', '1930.72'),('184', 'yotam_stock', '2024-05-02', '643.08', '641.18', '650.48', '639.09'),('194', 'ishay_stock', '2024-05-02', '3682.91', '3671.23', '3684.74', '3635.98')
    
    """
    # Execute SQL command
    result = postgres_hook.run(sql=query)
    logging.INFO(result)


def insert_rows_to_test_table(**kwargs):
    # Connect to PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')

    # Insert new rows into test_table
    insert_query = """
    INSERT INTO test_table (first_name, last_name)
    VALUES 
        ('shachar', 'fatran'),
        ('Ishay', 'Balash');
    """
    postgres_hook.run(sql=insert_query)


with DAG(
        dag_id='test_dag',
        start_date=datetime(2024, 2, 28),
        schedule_interval='@daily',
        catchup=False
) as dag:
    insert_data = PythonOperator(
        task_id='insert_data',
        python_callable=execute_sql_and_log_result,
        provide_context=True
    )

insert_data
