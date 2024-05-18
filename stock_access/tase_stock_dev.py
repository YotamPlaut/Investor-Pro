import http.client
import json
from datetime import datetime, time
import pandas as pd
from sqlalchemy.exc import RemovedIn20Warning
from GCP_SETUP.gcp_setup import get_pool
import warnings
from sqlalchemy import MetaData, Table, Column, String, text

stock_list = [
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


def indices_EoD_by_index_from_date_to_date(bearer: str, index_id: int,start_date: time, end_date: time, stock_name: str = None, insert: bool = False):
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
            #create delete query
            conditions = " OR ".join(
                [f"(index_symbol = '{row['index_symbol']}' AND date = '{row['date']}')" for index, row in
                 df.iterrows()])
            delete_query = f"DELETE FROM {table_configs['stocks']['raw_data']} WHERE {conditions}"

            #create insert quesry
            insert_values = ", ".join([
                                   f"('{row['index_symbol']}', '{row['symbol_name']}', '{row['date']}', {row['open']}, {row['close']}, {row['high']}, {row['low']}, {row['omc']})"
                                   for index, row in df.iterrows()])
            insert_query = f"INSERT INTO {table_configs['stocks']['raw_data']} (index_symbol, symbol_name, date, open, close, high, low, omc) VALUES {insert_values}"

            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    #warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    print(delete_query)
                    conn.execute(text(delete_query))
                    conn.commit()
                    print(insert_query)
                    conn.execute(text(insert_query))
                    conn.commit()
        return df


        #print(dat['indexEndOfDay']['result'])
    except Exception as e:
        print(f"error: {e}")


def indices_EoD_by_one_date(bearer: str, index_id: int, start_date: str):
    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': f"Bearer {bearer}",
        'accept': "application/json"
    }

    conn.request("GET",
                 f"/tase/prod/api/v1/indices/eod/history/ten-years/by-index?indexId={index_id}&fromDate={start_date}&toDate={start_date}",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    try:
        dat = json.loads(data)['indexEndOfDay']['result'][0]  # will only work for one day extraction

        stock_info = {'symbol': dat['indexId'],
                      'date': datetime.strptime(dat['tradeDate'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d'),
                      'open': dat['indexOpeningPrice'],
                      'close': dat['closingIndexPrice'],
                      'high': dat['high'],
                      'low': dat['low'],
                      'omc': dat['overallMarketCap']  ##overallMarketCap
                      }
        # Find the corresponding name for the index
        matching_stock_name = next(
            (stock['name'] for stock in stock_list if stock['index'] == int(stock_info['symbol'])),
            None)
        if matching_stock_name is None:
            raise Exception
        stock_info['symbol_name'] = matching_stock_name
        return stock_info

    except Exception as e:
        print(e)

    # print(data.decode("utf-8"))

    # print(type(data))
    # print(data.decode("utf-8"))


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


if __name__ == '__main__':
    indices_EoD_by_index_from_date_to_date(bearer=get_Bar(), index_id=142, start_date='2024-01-01',
                                           end_date='2024-05-20', insert=True)


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
