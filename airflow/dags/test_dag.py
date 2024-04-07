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

    # Execute SQL command
    result = postgres_hook.get_records(sql="SELECT * FROM test_table")

    # Log the result
    for row in result:
        print(row)


def insert_rows_to_test_table(**kwargs):
    # Connect to PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')

    # Insert new rows into test_table
    insert_query = """
    INSERT INTO test_table (first_name, last_name)
    VALUES 
        ('Alice', 'Johnson'),
        ('Bob', 'Smith');
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
        python_callable=insert_rows_to_test_table,
        provide_context=True
    )

    read_data = PythonOperator(
        task_id='read_data',
        python_callable=execute_sql_and_log_result,
        provide_context=True
    )
insert_data >> read_data
