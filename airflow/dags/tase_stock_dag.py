from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import logging
from utilities.tase_api import get_Bar, indices_EoD_by_date
from utilities.stock_list import stock_list
from sqlalchemy import text


def store_bearer_token(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    bearer = get_Bar()
    kwargs['ti'].xcom_push(key='bearer', value=bearer)
    logging.info(f"API call for bearer succeeded for date: '{execution_date}'bearer is:{bearer}")


def extract_stock_data(stock_index, **kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    current_bearer_token = kwargs['ti'].xcom_pull(task_ids='get_bearer_token', key='bearer')
    logging.info(f"using current_bearer_token: {current_bearer_token}")
    logging.info(f"going to run on stock: {stock_index}, on date: {execution_date}")
    stock_info = indices_EoD_by_date(current_bearer_token, stock_index, execution_date)
    logging.info(f'Stock info for index {stock_index}: {stock_info}')
    kwargs['ti'].xcom_push(key=f'{stock_index}', value=stock_info)


def store_stock_info(**kwargs):
    execution_date = kwargs['execution_date'].strftime('%Y-%m-%d')
    postgres_hook = PostgresHook(postgres_conn_id='investor_pro')
    all_stock_info = []
    for stock in stock_list:
        stock_info = kwargs['ti'].xcom_pull(task_ids=f"extract_{stock['name']}_info", key=f"{stock['index']}")
        if stock_info is None:
            pass
        else:
            stock_info['symbol_name'] = stock['name']
            all_stock_info.append(stock_info)
            logging.info(f"for stock {stock['index']}, info is :{stock_info}")

    if len(all_stock_info) == 0:
        logging.info(f"no record data for date: {execution_date}")
    else:
        delete_values = ", ".join([f"('{info['symbol']}', '{info['date']}')" for info in all_stock_info])
        delete_query = f"DELETE FROM stocks.tase_stock_data WHERE (index_symbol, date) IN ({delete_values});"
        logging.info(f"running delete_query: {delete_query}")
        postgres_hook.run(sql=delete_query)

        ##insert command
        logging.info("""!!!!!!!!!!!!!!!!!!!!! {}
        """.format(",".join(["('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            info['symbol'], info['symbol_name'], info['date'], info['open'],
            info['close'], info['high'], info['low'], info['omc']) for info in all_stock_info])))

        logging.info("""!!!!!!!!!!!@@@@!!!!!!!!!! {}
                """.format(info['omc']) for info in all_stock_info)

        insert_query = """
            INSERT INTO stocks.tase_stock_data (index_symbol, symbol_name, date, open, close, high, low, omc)
            VALUES {}
            """.format(",".join(["('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            info['symbol'], info['symbol_name'], info['date'], info['open'],
            info['close'], info['high'], info['low'], info['omc']) for info in all_stock_info]))
        logging.info(f"running insert query : {insert_query}")

        ##run  postgres_hook.run(sql=delete_query)
        postgres_hook.run(sql=insert_query)
        logging.info(f"done")


with DAG(
        dag_id='tase_stock_extract',
        start_date=datetime(2024, 4, 28),
        # end_date=datetime(2024, 5, 2),
        schedule_interval='@daily',
        # catchup=False,
) as dag:
    start_dummy = DummyOperator(
        task_id='start_dummy'
    )
    get_bearer_token = PythonOperator(
        task_id='get_bearer_token',
        python_callable=store_bearer_token
        # trigger_rule = 'one_success'
    )

    store_stock_info = PythonOperator(
        task_id='store_stock_info',
        python_callable=store_stock_info
        # trigger_rule='one_success'

    )

    start_dummy >> get_bearer_token

    for stock in stock_list:
        extract_stock_data_task = PythonOperator(
            task_id=f"extract_{stock['name']}_info",
            python_callable=extract_stock_data,
            op_args=[stock['index']]
            # trigger_rule='one_success'
        )

        get_bearer_token >> extract_stock_data_task >> store_stock_info
