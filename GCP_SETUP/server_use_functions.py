import json
import warnings

from sqlalchemy.exc import RemovedIn20Warning

from gcp_setup import stock_list, get_pool
from datetime import time, datetime, date
from sqlalchemy import MetaData, Table, Column, String, text
import pandas as pd
import warnings

table_configs = {
    'stocks': {'raw_data': 'stocks.tase_stock_data'},
    'server': {'users': 'server.users', 'actions': 'server.raw_actions'}
}


##general####
def get_100_records_from_table(table_name):
    """
    just a general function to get all records from a table, for testing --should not to use in production
    :param table_name: table name as a string
    :return:
    """
    engine = get_pool()
    with engine.connect() as conn:
        result = conn.execute(
            text(f'SELECT * FROM {table_name} limit 100'))  # Use conn.execute instead of engine.execute
        return result.fetchall()


###stocks function######

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
                from {table_configs['stocks']['raw_data']}
                where index_symbol='{matching_stock_index}' and date>=date('{date}');
          """
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            df = pd.DataFrame(result, columns=['Date', 'Index_Symbol', 'Symbol_Name', 'Open', 'Close', 'High', 'Low'])
            return df, df.shape

    except Exception:
        print("error occurred while running query")
        return None


def check_if_user_exists(user_name: str, email: str):
    """
    Check if a user exists in the database based on their username or email.

    param user_name: The username to check.
    param email: The email address to check.
    return: A dictionary containing a code and a message.
        - code (int): 0 if the user or email is found in the database, 1 otherwise.
        - msg (str): A message indicating whether the user or email is found in the database or not.
    """
    engine = get_pool()
    with engine.connect() as conn:
        result = conn.execute(
            text(
                f"SELECT distinct user_id,email_address FROM {table_configs['server']['users']}"))  # Use conn.execute instead of engine.execute
        df = pd.DataFrame(result, columns=['user_id', 'email_address'])
        if user_name in df['user_id'].values:
            return {'code': 0, 'msg': 'user found in db'}
        if email in df['email_address'].values:
            return {'code': 0, 'msg': 'email_address found in db'}
        return {'code': 1, 'msg': 'user and email not found in db'}


def insert_new_user_to_db(user_id: str, hash_pass: str, email_address: str, install_date: datetime,
                          creation_date: datetime, update_date: datetime):
    """
    Insert a new user into the database if the user ID or email address doesn't already exist.

    Parameters:
    - user_id (str): The user ID.
    - hash_pass (str): The hashed password.
    - email_address (str): The email address.
    - install_date (datetime): The installation date.
    - creation_date (datetime): The creation date.
    - update_date (datetime): The update date.

    Returns:
    - dict or None: A dictionary containing a code and a message if the user is inserted successfully,
      or None if an error occurs during the insertion process.
        - code (int): 0 if the user or email is found in the database, 1 otherwise.
        - msg (str): A message indicating whether the user or email is found in the database or not.
    """
    is_user_exists = check_if_user_exists(user_id, email_address)
    if is_user_exists['code'] == 0:
        return {'code': 0, 'msg': 'user or email found in db'}
    else:
        # noinspection PyBroadException
        try:
            insert_query = (
                f"""
                                       INSERT INTO {table_configs['server']['users']} (user_id,
                                                                       hash_pass,
                                                                       email_address,
                                                                       install_date,
                                                                       creation_date,
                                                                       update_date)
                                       VALUES ('{user_id}','{hash_pass}','{email_address}','{install_date}','{creation_date}','{update_date}' )
                                       """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(insert_query))
                return {'code': 1, 'msg': f" user: {user_id}, {email_address} was inserted to db"}
        except Exception as e:
            print("error occurred while running insert quesry")
            return None


def insert_raw_action(evt_name: str, server_time: datetime, evt_details: dict = None):
    """
    Inserts a raw action record into the database.

    :param evt_name: Name of the event.
    :param server_time: Timestamp representing the time when the event occurred on the server.
    :param evt_details: Additional details about the event, stored as a dictionary. Defaults to None.

    :return: A dictionary containing a code and a message indicating the result of the insertion operation.
        - 'code' (int): Indicates the status of the insertion operation. 1 indicates success, while None indicates an error occurred.
        - 'msg' (str): A message describing the outcome of the insertion operation. If successful, it indicates that the action was listed in the database.
    """
    if evt_details is None:
        evt_details = {}  # Set evt_details to an empty dictionary if None

    server_time_str = server_time.isoformat()

    # Convert evt_details to a JSON string
    evt_details_str = json.dumps(evt_details)

    try:
        insert_query = f"""
            INSERT INTO {table_configs['server']['actions']} (evt_date, evt_time, evt_name, server_time, evt_details)
            VALUES ('{datetime.now().date()}', '{datetime.now()}', '{evt_name}', '{server_time_str}', '{evt_details_str}')
        """

        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(insert_query))
            return {'code': 1, 'msg': f"Action listed in db"}
    except Exception as e:
        print("Error occurred while running insert query:", e)
        return None


# if __name__ == '__main__':
    # # Sample values for insert_raw_action call
    # evt_name = "login"
    # server_time = datetime.now()
    # evt_details = {
    #     "user_id": 123,
    #     "action_type": "login",
    #     "timestamp": datetime.now().isoformat(),
    #     "duration_seconds": 45,
    #     "location": {
    #         "latitude": 37.7749,
    #         "longitude": -122.4194
    #     }
    # }
    # print(insert_raw_action(evt_name, server_time, evt_details))

    # ###Example insert_new_user_to_db call with fake values
    # print(insert_new_user_to_db(user_id='fake_user_id_2',
    #                             hash_pass='fake_hash_pass',
    #                             email_address='fake_email_address_2',
    #                             install_date=datetime.now(),
    #                             creation_date=datetime.now(),
    #                             update_date=datetime.now()))

    #
    # ## get stock data by day example
    # df, shape = get_stock_data_by_date('tel_aviv_35', '2024-05-06')
    # print(df.head(10))
    # print(shape)
