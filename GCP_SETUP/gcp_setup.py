from datetime import time

import pandas as pd
from sqlalchemy import MetaData, Table, Column, String, text
import sqlalchemy
import pg8000

# from sqlalchemy.dialects.postgresql import pg8000

########################### GCDS SETUP PARAMS #########################
INSTANCE_CONNECTION_NAME = 'investor-pro-418817:us-west1:investorprodb'
DB_USER = 'investorpro_mng'
DB_PASS = 'admin'
DB_NAME = 'app_db'
DB_HOST = '34.168.210.93'

############################################################################

##### list of stocks #####
stock_list = [
    {'index': 142, 'name': 'tel_aviv_35'},
    {'index': 143, 'name': 'tel_aviv_90'},
    {'index': 147, 'name': 'semi_60'},
    {'index': 148, 'name': 'finaces'},
    {'index': 169, 'name': 'top_100_tech'},
    {'index': 601, 'name': 'all_bonds'}
]


def getconn() -> pg8000.Connection:
    conn: pg8000.Connection = pg8000.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
    )
    return conn


def get_pool():
    pool = sqlalchemy.create_engine(
        f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
        creator=getconn,
        # Additional options if needed
    )
    return pool


def get_all_records_from_table(table_name):
    engine = get_pool()
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT * FROM {table_name}'))  # Use conn.execute instead of engine.execute
        return result.fetchall()


def get_stock_data_by_date(stock_name: str, date: time):
    """
    :param stock_name: stock name as a string, need to be one out of the stock_list
    :param date: stat date, the function will retuen all records from this start date- in the format of yyyy-mm-dd
    :return: return a pandas data frame with this cols: Date  Index_Symbol  Symbol_Name     Open    Close     High      Low
             plus is return the shape of the data frame as a tupple, (number of rows, number of cols).
             In case some error occured, we will return None.
    """
    matching_stock_index = next(
        (stock['index'] for stock in stock_list if stock['name'] == stock_name),
        None)
    if matching_stock_index is None:
        print(f"didnt found maching index for stock: {stock_name}")
        return None
    try:
        engine = get_pool()
        query = f"""
                 select 
                    date,
                    index_symbol,
                    symbol_name,
                    open,
                    close,
                    high,
                    low
                from stocks.tase_stock_data
                where index_symbol='{matching_stock_index}' and date>=date('{date}');
          """
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            df = pd.DataFrame(result, columns=['Date', 'Index_Symbol', 'Symbol_Name', 'Open', 'Close', 'High', 'Low'])
            return df, df.shape

    except Exception:
        print("error occurred while running query")
        return None


# def insert_test_user(user_id, password, email_address):
#         # Hash the password using SHA-256
#         hash_pass = hashlib.sha256(password.encode()).hexdigest()
#
#         engine = get_pool()
#         with engine.connect() as conn:
#             insert_query = text(
#                 f"""
#                 INSERT INTO server.user_logins (user_id,
#                                                 hash_pass,
#                                                 email_adress,
#                                                 install_date,
#                                                 creation_date,
#                                                 update_date)
#                 VALUES ('{user_id}','{hash_pass}','{email_address}','{datetime.now()}','{datetime.now()}','{datetime.now()}' )
#
#                 """
#             )
#             conn.execute(insert_query)
#             conn.commit()
#
if __name__ == '__main__':
    #     # insert_test_user('test_user_ishay_2', '1234567', 'ishay6411@gmail.zibi.com')
    #     # # insert_into_test()
    df, shape = get_stock_data_by_date('tel_aviv_35', '2024-05-06')
    print(df.head(10))
    print(shape)

    # rows = get_all_records_from_table('server.user_logins')
    # print(rows)
#     has_pass=hashlib.sha256('1234567'.encode()).hexdigest()
#
#     engine = get_pool()
#     with engine.connect() as conn:
#         result = conn.execute(text(f"SELECT * FROM server.user_logins where hash_pass='{has_pass}'"))  # Use conn.execute instead of engine.execute
#         print(result.fetchall())
#
#
#
