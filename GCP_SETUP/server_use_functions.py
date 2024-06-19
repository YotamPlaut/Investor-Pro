import json
import warnings

from sqlalchemy.exc import RemovedIn20Warning

from gcp_setup import get_pool
from datetime import time, datetime, date
from sqlalchemy import MetaData, Table, Column, String, text
import pandas as pd
import warnings

table_configs = {
    'stocks': {'raw_data': 'stocks.tase_stock_data'},
    'server': {'users': 'server.users', 'actions': 'server.raw_actions', 'portfolio': 'server.portfolios'}
}
stock_list = [
    {'index_id': 137, 'name': 'TA_125', 'IsIndex': True},
    {'index_id': 147, 'name': 'TA_SME_60', 'IsIndex': True},
    {'index_id': 709, 'name': 'TA_Bond_60', 'IsIndex': True},
    {'index_id': 662577, 'name': 'Bank_Hapoalim', 'IsIndex': False},
    {'index_id': 691212, 'name': 'Bank_Discont', 'IsIndex': False},

]


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
     Fetches stock data for a given stock name starting from a specific date.

    :param stock_name: The name of the stock, which must be present in the stock_list.
    :param date: The start date for fetching the stock records, in the format of yyyy-mm-dd.
    :return: A JSON string containing:
             - 'info': A dictionary where keys are dates and values are dictionaries of stock data (fields: Index_Symbol, Symbol_Name, Open, Close, High, Low, OMC, Volume).
             - 'num_days': The number of unique dates in the data.
             - 'Index_Symbol': The index symbol of the stock.
             - 'Symbol_Name': The name of the stock.
             If an error occurs, None is returned.
    """
    matching_stock_index = next(
        (stock['index_id'] for stock in stock_list if stock['name'] == stock_name),
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
                    low,
                    omc,
                    volume
                from {table_configs['stocks']['raw_data']}
                where index_symbol='{matching_stock_index}' and date>=date('{date}');
          """
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            # df = pd.DataFrame(result,
            #                   columns=['Date', 'Index_Symbol', 'Symbol_Name', 'Open', 'Close', 'High', 'Low', 'omc', 'volume'])
            # return df, df.shape
            stock_data_dict = {'info': {}}
            for row in result:
                date_str = row['date'].strftime('%Y-%m-%d')  # Ensure date is in string format for JSON compatibility
                stock_data_dict['info'][date_str] = {
                    'Index_Symbol': row['index_symbol'],
                    'Symbol_Name': row['symbol_name'],
                    'Open': row['open'],
                    'Close': row['close'],
                    'High': row['high'],
                    'Low': row['low'],
                    'OMC': row['omc'],
                    'Volume': row['volume']
                }

                # Add the number of unique dates to the JSON object
            num_days = len(stock_data_dict['info'])
            stock_data_dict['num_days'] = num_days
            stock_data_dict['Index_Symbol'] = matching_stock_index
            stock_data_dict['Symbol_Name'] = stock_name

            # Convert dictionary to JSON
            stock_data_json = json.dumps(stock_data_dict)
            return stock_data_json
    except Exception as e:
        print(f"error occurred while running query: {e}")
        return None


def get_all_stocks():
    """
    Retrieves all distinct stocks from the database.
    :return: A list of dictionaries where each dictionary contains 'index_symbol' and 'symbol_name' keys.
             Returns an empty list if no stocks are found or if an error occurs.
    """
    try:
        select_query = (
            f"""
               select distinct index_symbol,symbol_name from {table_configs['stocks']['raw_data']}
            """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                result = conn.execute(text(select_query)).fetchall()
                stock_list = [{res[0]: res[1]} for res in result]
        return stock_list
    except Exception as e:
        print(f"error occurred while running query: {e}")


##server functions
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


def insert_new_portfolio(user_id: str, portfolio_id: str, stock_array: {} = None):
    try:
        insert_query = (
            f"""
                                   INSERT INTO {table_configs['server']['portfolio']} (user_id,
                                                                  portfolio_id,
                                                                  stock_array
                                                                  )
                                   VALUES ('{user_id}','{portfolio_id}','{stock_array}')
                                   """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(insert_query))
                conn.commit()
            return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was inserted to db"}
    except Exception as e:
        print("error occurred while running insert query")
        return None


def remove_portfolio(user_id: str, portfolio_id: str):
    try:
        delete_query = (
            f"""
                DELETE FROM {table_configs['server']['portfolio']}
                        WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
            
             """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(delete_query))
                conn.commit()
            return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was removed from db"}
    except Exception as e:
        print("error occurred while running delete query")
        return None


def add_new_stock_to_portfolio(user_id: str, portfolio_id: str, stock_int: int):
    try:
        update_query = (
            f"""
               UPDATE {table_configs['server']['portfolio']}
               SET stock_array = CASE
                                WHEN NOT ({stock_int} = ANY(stock_array)) THEN stock_array || {stock_int}
                                ELSE stock_array END
               WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
            """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(update_query))
                conn.commit()
        return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was was updated"}

    except Exception as e:
        print("error occurred while running update query ")
    return None


def remove_stock_from_portfolio(user_id: str, portfolio_id: str, stock_int: int):
    try:
        update_query = (
            f"""
               UPDATE {table_configs['server']['portfolio']}
               SET stock_array = array_remove(stock_array, {stock_int})
               WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
            """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(update_query))
                conn.commit()
        return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was was updated"}

    except Exception as e:
        print("error occurred while running update query ")
    return None


def get_all_portfolios(user_id: str):
    try:
        select_query = (
            f"""
               select distinct portfolio_id from {table_configs['server']['portfolio']}
               WHERE user_id = '{user_id}';
            """
        )
        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                result = conn.execute(text(select_query)).fetchall()
                portfolios_list = [portfolio[0] for portfolio in result]
        return portfolios_list
    except Exception as e:
        print(f"error occurred while running query: {e}")


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
                    conn.commit()
                return {'code': 1, 'msg': f" user: {user_id}, {email_address} was inserted to db"}
        except Exception as e:
            print("error occurred while running insert quesry")
            return None


def insert_raw_action(evt_name: str, server_time: datetime, user_id: str, evt_details: dict = None):
    """
    Inserts a raw action record into the database.

    :param user_id: user id- needs to be from server.users!
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
            INSERT INTO {table_configs['server']['actions']} (evt_date, evt_time, evt_name, server_time, evt_details, user_id)
            VALUES ('{datetime.now().date()}', '{datetime.now()}', '{evt_name}', '{server_time_str}', '{evt_details_str}' ,'{user_id}')
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


if __name__ == '__main__':
    pass
    # print(insert_new_portfolio(user_id='ishay_balach',portfolio_id='my portfolio', stock_array={142, 11192, 125}))
    # print(add_new_stock_to_portfolio(user_id='ishay_balach', portfolio_id='my portfolio', stock_int=145))
    # print(remove_stock_from_portfolio(user_id='ishay_balach', portfolio_id='my portfolio', stock_int=125))
    # print(remove_portfolio(user_id='ishay_balach',portfolio_id='my portfolio'))

    # # Sample values for insert_raw_action call
    # evt_name = "login"
    # server_time = datetime.now()
    # evt_details = {
    #     "action_type": "login",
    #     "timestamp": datetime.now().isoformat(),
    #     "duration_seconds": 45,
    #     "location": {
    #         "latitude": 37.7749,
    #         "longitude": -122.4194
    #     }
    # }
    # print(insert_raw_action(evt_name=evt_name, server_time=server_time, user_id='test_users', evt_details=evt_details))

    ###Example insert_new_user_to_db call with fake values
    # print(insert_new_user_to_db(user_id='fake_user_id_ishay',
    #                             hash_pass='fake_hash_pass',
    #                             email_address='fake_email_address_3',
    #                             install_date=datetime.now(),
    #                             creation_date=datetime.now(),
    #                             update_date=datetime.now()))

    #
    # get stock data by day example
    # print(get_stock_data_by_date('Bank_Discont', '2024-05-06'))
    # print(get_all_portfolios(user_id='shahar_tst'))
    # df, shape = get_stock_data_by_date('Bank_Discont', '2024-05-06')
    # print(df.head(10))
    # print(shape)
    print(get_all_stocks())
