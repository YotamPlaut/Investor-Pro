import http.client
import json
import math
from datetime import datetime, time

import numpy as np
import pandas as pd
from sqlalchemy.exc import RemovedIn20Warning
from GCP_SETUP.gcp_setup import get_pool
import warnings
from sqlalchemy import MetaData, Table, Column, String, text

## add days of increase/decrease.
## for each stock-add recommendation. (strong buy/drop/hold ex...)


stock_list = [
    {'index_id': 137, 'name': 'TA_125', 'IsIndex': True},
    {'index_id': 147, 'name': 'TA_SME_60', 'IsIndex': True},
    {'index_id': 709, 'name': 'TA_Bond_60', 'IsIndex': True},
    {'index_id': 662577, 'name': 'Bank_Hapoalim', 'IsIndex': False},
    {'index_id': 691212, 'name': 'Bank_Discont', 'IsIndex': False},

]
table_configs = {
    'stocks': {
        'raw_data': 'stocks.tase_stock_data',
        'stats': 'stocks.tase_stock_stats'
    },
    'server': {
        'users': 'server.users',
        'actions': 'server.raw_actions'
    }
}


def get_Bar():
    conn = http.client.HTTPSConnection("openapigw.tase.co.il")
    payload = 'grant_type=client_credentials&scope=tase'
    headers = {
        'Authorization': 'Basic ZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODg6NGU0MThmNTYxNmM4ZjMwZjBkMjM0MjBkMzFlOGM2NzA=',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/tase/prod/oauth/oauth2/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_dict = json.loads(data)
    return json_dict['access_token']


def indices_EoD_by_index_from_date_to_date(bearer: str, index_id: int, start_date: time, end_date: time,
                                           stock_name: str = None, insert: bool = False):
    """
    Retrieves End of Day (EoD) data for a specified stock index -for Index stocks (TA_125...) within a given date range from the Tel Aviv Stock Exchange (TASE) API.

    param bearer: (str) The bearer token for authentication with the TASE API.
    param index_id: (int) The ID of the stock index for which EoD data is to be retrieved.
    param start_date: (time) The start date of the date range for which EoD data is to be retrieved.
    param end_date: (time) The end date of the date range for which EoD data is to be retrieved.
    param stock_name: (str, optional) The name of the stock. If not provided, the function will attempt to find it based on the `index_id`.
    param insert: (bool, default=False) If `True`, the retrieved data will be inserted into a database table.
    return: DataFrame: A Pandas DataFrame containing the retrieved EoD data.

    """

    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': f"Bearer {bearer}",
        'accept': "application/json"
    }
    conn.request("GET",
                 f"/tase/prod/api/v1/indices/eod/history/ten-years/by-index?indexId={index_id}&fromDate={start_date}&toDate={end_date}",
                 headers=headers)
    res = conn.getresponse()
    data = res.read()
    try:
        dat = json.loads(data)
        if stock_name is None:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(index_id)), None)
            if symbol_name is None:
                raise ValueError("symbol_name was not provided and was not found in stock list,operation can't be done")
        else:
            symbol_name = stock_name
        df = pd.DataFrame(dat['indexEndOfDay']['result'])
        df['symbol_name'] = symbol_name
        df = df.rename(columns={
            'indexId': 'index_symbol',
            'tradeDate': 'date',
            'indexOpeningPrice': 'open',
            'closingIndexPrice': 'close',
            'high': 'high',
            'low': 'low',
            'overallMarketCap': 'omc'
        })

        # Reorder columns
        df = df[['index_symbol', 'symbol_name', 'date', 'open', 'close', 'high', 'low', 'omc']]
        if insert:
            # create delete query
            conditions = " OR ".join(
                [f"(index_symbol = '{row['index_symbol']}' AND date = '{row['date']}')" for index, row in
                 df.iterrows()])
            delete_query = f"DELETE FROM {table_configs['stocks']['raw_data']} WHERE {conditions}"

            # create insert query
            insert_values = ", ".join([
                f"('{row['index_symbol']}', '{row['symbol_name']}', '{row['date']}', {row['open']}, {row['close']}, {row['high']}, {row['low']}, {row['omc']})"
                for index, row in df.iterrows()])
            insert_query = f"INSERT INTO {table_configs['stocks']['raw_data']} (index_symbol, symbol_name, date, open, close, high, low, omc) VALUES {insert_values}"

            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    print(delete_query)
                    conn.execute(text(delete_query))
                    conn.commit()
                    print(insert_query)
                    conn.execute(text(insert_query))
                    conn.commit()
        return df

        # print(dat['indexEndOfDay']['result'])
    except Exception as e:
        print(f"error: {e}")


def securities_EoD_by_index_from_date_to_date(bearer: str, index_id: int, start_date: time, end_date: time,
                                              stock_name: str = None, insert: bool = False):
    """
    Retrieves End of Day (EoD) data for a specified stock index -for actual stocks (bank_hapoim.....) within a given date range from the Tel Aviv Stock Exchange (TASE) API.

    param bearer: (str) The bearer token for authentication with the TASE API.
    param index_id: (int) The ID of the stock index for which EoD data is to be retrieved.
    param start_date: (time) The start date of the date range for which EoD data is to be retrieved.
    param end_date: (time) The end date of the date range for which EoD data is to be retrieved.
    param stock_name: (str, optional) The name of the stock. If not provided, the function will attempt to find it based on the `index_id`.
    param insert: (bool, default=False) If `True`, the retrieved data will be inserted into a database table.
    return: DataFrame: A Pandas DataFrame containing the retrieved EoD data.

    """
    import http.client

    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': f"Bearer {bearer}",
        'accept': "application/json"
    }

    conn.request("GET",
                 f"/tase/prod/api/v1/securities/trading/eod/history/ten-years/by-security?securityId={index_id}&fromDate={start_date}&toDate={end_date}",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    try:
        dat = json.loads(data)
        if stock_name is None:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == int(index_id)), None)
            if symbol_name is None:
                raise ValueError("symbol_name was not provided and was not found in stock list,operation can't be done")
        else:
            symbol_name = stock_name
        df = pd.DataFrame(dat['securitiesEndOfDayTradingData']['result'])
        df['symbol_name'] = symbol_name
        df = df.rename(columns={
            'securityId': 'index_symbol',
            'tradeDate': 'date',
            'openingPrice': 'open',
            'closingPrice': 'close',
            'high': 'high',
            'low': 'low',
            'marketCap': 'omc',
            'volume': 'volume'
        })
        df = df[['index_symbol', 'symbol_name', 'date', 'open', 'close', 'high', 'low', 'omc', 'volume']]
        if insert:
            # create delete query
            conditions = " OR ".join(
                [f"(index_symbol = '{row['index_symbol']}' AND date = '{row['date']}')" for index, row in
                 df.iterrows()])
            delete_query = f"DELETE FROM {table_configs['stocks']['raw_data']} WHERE {conditions}"

            # create insert query
            insert_values = ", ".join([
                f"('{row['index_symbol']}', '{row['symbol_name']}', '{row['date']}', {row['open']}, {row['close']}, {row['high']}, {row['low']}, {row['omc']}, {row['volume']})"
                for index, row in df.iterrows()])
            insert_query = f"INSERT INTO {table_configs['stocks']['raw_data']} (index_symbol, symbol_name, date, open, close, high, low, omc,volume ) VALUES {insert_values}"

            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    print(delete_query)
                    conn.execute(text(delete_query))
                    conn.commit()
                    print(insert_query)
                    conn.execute(text(insert_query))
                    conn.commit()
        return df
    except Exception as e:
        pass


# todo need to add this function
def update_table_stocks(bearer: str, start_date: time, end_date):
    """
    This function is used to update the stock tables for all stocks in the stock_list for a specific time range

    param bearer: (str)  param bearer: (str) The bearer token for authentication with the TASE API.
    param start_date: (time) The start date of the date range for which EoD data is to be retrieved.
    param end_date: (time) The end date of the date range for which EoD data is to be retrieved.
    :return: nothing
    """
    pass


##stocks statistics
def run_stock_stats_daily_increase(index_id: int, start_date: datetime = datetime(1970, 1, 1), insert: bool = False):
    ## get stock needed info from db:
    try:
        engine = get_pool()
        query = f"""
                 select 
                    date,
                    index_symbol,
                    open,
                    close
                from {table_configs['stocks']['raw_data']}
                where index_symbol='{index_id}' and date>=date('{start_date}');
          """
        df = pd.DataFrame()
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            df = pd.DataFrame(result, columns=['date', 'index_Symbol', 'open', 'close'])

        if df.empty:
            raise ValueError('data frame is empty, something is wrong with query')

        # CALC STATS
        df['increase_val'] = (df['close'] - df['open']) / df['open']
        buckets = [-float('inf'), -0.2, -0.1, -0.05, -0.03, -0.01, 0.01, 0.03, 0.05, 0.1, 0.2, float('inf')]

        bucket_counts = pd.cut(df['increase_val'], bins=buckets).value_counts().sort_index()
        total_days = df.shape[0]
        bucket_percentages = (bucket_counts / total_days) * 100

        res_dict = {
            "total_days_in_view": int(total_days),
            "buckets": []
        }
        for bucket_range, count, percentage in zip(bucket_counts.index, bucket_counts.values,
                                                   bucket_percentages.values):
            if count > 0:
                bucket_start, bucket_end = bucket_range.left, bucket_range.right
                bucket_info = {
                    "bucket_start": float(bucket_start),
                    "bucket_end": float(bucket_end),
                    "count": int(count),
                    "percentage_of_total": float(percentage)
                }
                res_dict["buckets"].append(bucket_info)
        res_json = json.dumps(res_dict)
        if insert:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == index_id), None)
            insert_stock_stats_to_db(index_symbol=index_id,
                                     symbol_name=symbol_name,
                                     stats_name="daily_increase",
                                     stats_info=res_json
                                     )
        return res_json

    except Exception as e:
        print(f"error: {e}")


def run_correlation_coefficient(index_id_1: int, index_id_2: int, start_date: time):
    try:
        engine = get_pool()
        query = f"""
                    select 
                       date,
                       index_symbol,
                       open,
                       close
                   from {table_configs['stocks']['raw_data']}
                   where index_symbol in('{index_id_1}',{index_id_2}) and date>=date('{start_date}');
             """
        df = pd.DataFrame()
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            df = pd.DataFrame(result, columns=['date', 'index_symbol', 'open', 'close'])

        first_stock_data = df[df['index_symbol'] == index_id_1].copy()
        second_stock_data = df[df['index_symbol'] == index_id_2].copy()

        ##calc daily return
        first_stock_data['date'] = pd.to_datetime(first_stock_data['date'])
        second_stock_data['date'] = pd.to_datetime(second_stock_data['date'])

        # Sort DataFrame by date (just in case it's not already sorted)
        first_stock_data = first_stock_data.sort_values(by='date')
        second_stock_data = second_stock_data.sort_values(by='date')

        # Calculate the daily return
        first_stock_data['daily_return'] = (first_stock_data['close'].shift(-1) - first_stock_data['close']) / \
                                           first_stock_data['close']
        second_stock_data['daily_return'] = (second_stock_data['close'].shift(-1) - second_stock_data['close']) / \
                                            second_stock_data['close']

        # calc the mean of Return
        index_1_mean_daily_return = first_stock_data['daily_return'].mean()
        index_2_mean_daily_return = second_stock_data['daily_return'].mean()

        # Drop the last row with NaN daily return
        first_stock_data = first_stock_data.dropna(subset=['daily_return'])
        second_stock_data = second_stock_data.dropna(subset=['daily_return'])

        # Merge the two DataFrames on 'date' to align the daily returns
        merged_data = pd.merge(first_stock_data[['date', 'daily_return']],
                               second_stock_data[['date', 'daily_return']],
                               on='date',
                               suffixes=('_1', '_2'))

        # Calculate the covariance between the daily returns
        covariance = merged_data[['daily_return_1', 'daily_return_2']].cov().iloc[0, 1]

        # calc the std of the daily return for each stock
        first_stock_daily_return_std = first_stock_data['daily_return'].std()
        second_stock_daily_return_std = second_stock_data['daily_return'].std()

        correlation_coefficient = covariance / (first_stock_daily_return_std * second_stock_daily_return_std)
        return correlation_coefficient
        if df.empty:
            raise ValueError('data frame is empty, something is wrong with query')
    except Exception as e:
        print(f"error: {e}")


def run_stock_stats_sharp_ratio(index_id: int, start_date: datetime = datetime(1970, 1, 1), risk_free_rate_annual=0.045,
                                trading_days_per_year: int = 252, insert: bool = False):
    try:
        engine = get_pool()
        query = f"""
                    select 
                       date,
                       index_symbol,
                       close
                   from {table_configs['stocks']['raw_data']}
                   where index_symbol='{index_id}' and date>=date('{start_date}'); 
             """
        stock_data = None
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            stock_data = pd.DataFrame(result, columns=['date', 'index_symbol', 'close'])
            stock_data.set_index('date', inplace=True)

        # Calculate daily returns
        stock_data['daily_returns'] = stock_data['close'].pct_change().dropna()

        # Calculate the daily risk-free rate
        daily_risk_free_rate = (1 + risk_free_rate_annual) ** (1 / trading_days_per_year) - 1

        # Calculate the excess returns
        stock_data['excess_returns'] = stock_data['daily_returns'] - daily_risk_free_rate

        # Calculate the average of excess returns
        avg_excess_return = stock_data['excess_returns'].mean()

        # Calculate the standard deviation of excess returns
        std_excess_return = stock_data['excess_returns'].std()

        # Calculate the Sharpe Ratio
        sharpe_ratio = avg_excess_return / std_excess_return

        # Annualize the Sharpe Ratio
        annualized_sharpe_ratio = sharpe_ratio * np.sqrt(trading_days_per_year)

        total_days = stock_data.shape[0]
        res_json = json.dumps({'total_days_in_view': total_days, 'sharp_ratio': annualized_sharpe_ratio})

        if insert:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == index_id), None)
            insert_stock_stats_to_db(index_symbol=index_id,
                                     symbol_name=symbol_name,
                                     stats_name="sharp_ratio",
                                     stats_info=res_json
                                     )
        return res_json
    except Exception as e:
        print(f"error: {e}")


def run_stock_stats_norn_distribution(index_id: int, start_date: datetime = datetime(1970, 1, 1), insert: bool = False):
    try:
        engine = get_pool()
        query = f"""
                       select 
                          date,
                          index_symbol,
                          close
                      from {table_configs['stocks']['raw_data']}
                      where index_symbol='{index_id}' and date>=date('{start_date}'); 
                """
        stock_data = None
        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            stock_data = pd.DataFrame(result, columns=['date', 'index_symbol', 'close'])
            stock_data.set_index('date', inplace=True)

        # Calculate daily returns
        stock_data['daily_returns'] = stock_data['close'].pct_change().dropna()

        # Calculate the average of excess returns
        avg_daily_returns = stock_data['daily_returns'].mean()

        # Calculate the standard deviation of excess returns
        std_daily_returns = stock_data['daily_returns'].std()

        total_days = stock_data.shape[0]

        res_json = json.dumps({'total_days_in_view': total_days, 'avg_daily_returns': avg_daily_returns,
                               'std_daily_returns': std_daily_returns})
        if insert:
            symbol_name = next((stock['name'] for stock in stock_list if stock['index_id'] == index_id), None)
            insert_stock_stats_to_db(index_symbol=index_id,
                                     symbol_name=symbol_name,
                                     stats_name="norn_distribution",
                                     stats_info=res_json
                                     )
        return res_json

    except Exception as e:
        print(f"error: {e}")


def insert_stock_stats_to_db(index_symbol: int, symbol_name: str, stats_name: str, stats_info: json,
                             insert_time: datetime = datetime.now()):
    # insert_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_query = f"""
               INSERT INTO {table_configs['stocks']['stats']} (index_symbol, symbol_name, stats_name, stats_info, insert_time)
               VALUES ('{index_symbol}', '{symbol_name}', '{stats_name}','{stats_info}','{insert_time.strftime('%Y-%m-%d %H:%M:%S')}')
           """
    engine = get_pool()
    with engine.connect() as conn:
        with warnings.catch_warnings():
            # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
            conn.execute(text(insert_query))
            conn.commit()


if __name__ == '__main__':
    print(f"sharp ratio:\n  {run_stock_stats_sharp_ratio(index_id=691212, insert=True)}")
    print(f"increase_buckets:\n {run_stock_stats_daily_increase(index_id=691212, insert=True)}")
    print(f"norm_distribution:\n {run_stock_stats_norn_distribution(index_id=691212, insert=True)}")
