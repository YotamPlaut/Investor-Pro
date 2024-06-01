import http.client
import json
from datetime import datetime, time
import pandas as pd
from sqlalchemy.exc import RemovedIn20Warning
from GCP_SETUP.gcp_setup import get_pool
import warnings
from sqlalchemy import MetaData, Table, Column, String, text

stock_list = [
    {'index': 137, 'name': 'tel_aviv_125'},
    {'index': 142, 'name': 'tel_aviv_35'},
    {'index': 143, 'name': 'tel_aviv_90'},
    {'index': 147, 'name': 'semi_60'},
    {'index': 148, 'name': 'finaces'},
    {'index': 169, 'name': 'top_100_tech'},
    {'index': 601, 'name': 'all_bonds'}
]
table_configs = {
    'stocks': {'raw_data': 'stocks.tase_stock_data'},
    'server': {'users': 'server.users', 'actions': 'server.raw_actions'}
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
    Retrieves End of Day (EoD) data for a specified stock index within a given date range from the Tel Aviv Stock Exchange (TASE) API.

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
            symbol_name = next((stock['name'] for stock in stock_list if stock['index'] == int(index_id)), None)
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

            # create insert quesry
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


def run_stock_stat_daily_increase(index_id: int, start_date: time):
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

        sats_dict = {
            "total_days": total_days,
            "buckets": []
        }
        for bucket_range, count, percentage in zip(bucket_counts.index, bucket_counts.values,
                                                   bucket_percentages.values):
            if count > 0:
                bucket_start, bucket_end = bucket_range.left, bucket_range.right
                bucket_info = {
                    "bucket_start": bucket_start,
                    "bucket_end": bucket_end,
                    "count": count,
                    "percentage_of_total": percentage
                }
                sats_dict["buckets"].append(bucket_info)
        print(sats_dict)




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


def run_sharp_index(index_id: int, start_date: time):
    try:
        engine = get_pool()
        query = f"""
                    select 
                       date,
                       index_symbol,
                       open,
                       close
                   from {table_configs['stocks']['raw_data']}
                   where index_symbol in('{index_id}','601') and date>=date('{start_date}'); 
             """
        df = pd.DataFrame()

        with engine.connect() as conn:
            result = conn.execute(text(query)).fetchall()
            df = pd.DataFrame(result, columns=['date', 'index_symbol', 'open', 'close'])
        stock_data = df[df['index_symbol'] == index_id].copy()
        bond_data = df[df['index_symbol'] == 601].copy()

        # Calculate daily returns
        stock_data['daily_return'] = stock_data['close'].pct_change()
        bond_data['daily_return'] = bond_data['close'].pct_change()

        # Calculate the average daily return of the stock
        average_daily_return = stock_data['daily_return'].mean()



        # Estimate the annual risk-free rate from the bond's daily returns
        annual_risk_free_rate = bond_data['daily_return'].mean() * 252



        # Convert the annual risk-free rate to a daily rate
        daily_risk_free_rate = (1 + annual_risk_free_rate) ** (1 / 252) - 1

        # Calculate the standard deviation of daily returns for the stock
        std_dev_daily_return = stock_data['daily_return'].std()

        sharpe_ratio = (average_daily_return - daily_risk_free_rate) / std_dev_daily_return
        print(f"Sharpe Ratio: {sharpe_ratio}")
    except Exception as e:
        print(f"error: {e}")


def securities_Eod_by_by_date():
    import http.client

    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': "Bearer AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODhkwLtQpJb76r6dkVbgo3okAKwY2NJnyC-Jf31uCsN-u6fAUz3veqYrQ1YucL36s5CxNMMVSTRpzvnvc6Wd_yadSNvTTMZgklxrgQWVAZHvkGKenVAJWakdnfhDbCXvg9g",
        'accept': "application/json"
    }

    conn.request("GET",
                 "/tase/prod/api/v1/securities/trading/eod/history/ten-years/by-security?securityId=604611&fromDate=2024-05-01&toDate=2024-05-20",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))



if __name__ == '__main__':
    securities_Eod_by_by_date()
    #print(get_Bar())
    #df=indices_EoD_by_index_from_date_to_date(bearer='AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODhkwLtQpJb76r6dkVbgo3okAKwY2NJnyC-Jf31uCsN-u6fAUz3veqYrQ1YucL36s5CxNMMVSTRpzvnvc6Wd_yadSNvTTMZgklxrgQWVAZHvkGKenVAJWakdnfhDbCXvg9g',
    #                                       index_id=142,
    #                                       start_date='2024-05-27',
    #                                       end_date='2024-05-28',
    #                                       insert=False
    #                                       )
    #print(df.head(10))









    # print(get_Bar())
    # pass
    #run_sharp_index(index_id=142, start_date='2024-01-01')

    # print(run_correlation_coefficient(index_id_1=142, index_id_2=148, start_date='2024-01-01'))

    #run_stock_stat_daily_increase(index_id=142, start_date='2024-05-01')

    # indices_EoD_by_index_from_date_to_date(bearer=get_Bar(), index_id=137, start_date='2024-01-01',
    #                                        end_date='2024-05-20', insert=True)

    # json_obj = indices_EoD_by_one_date(bearer=get_Bar(),
    #                                    index_id=142,
    #                                    start_date='2024-05-01')
    # print(json_obj)
    # print(json_obj['symbol'])
    # matching_stock_name = next((stock['name'] for stock in stock_list if stock['index'] == int(json_obj['symbol'])),
    #                            None)
    # print(matching_stock_name)
    # json_obj['symbol_name'] = matching_stock_name
    # print(json_obj)
