import http.client
import json
from datetime import datetime, time



table_configs = {
    'stocks': {'raw_data': 'stocks.tase_stock_data'},
    'server': {'users': 'server.users', 'actions': 'server.raw_actions'}
}

stock_list = [
    {'index_id': 137, 'name': 'TA_125', 'IsIndex': True},
    {'index_id': 147, 'name': 'TA_SME_60', 'IsIndex': True},
    {'index_id': 709, 'name': 'TA_Bond_60', 'IsIndex': True},
    {'index_id': 662577, 'name': 'Bank_Hapoalim', 'IsIndex': False},
    {'index_id': 691212, 'name': 'Bank_Discont', 'IsIndex': False},

]


def indices_EoD_by_date(bearer: str, index_id: int, start_date: str):
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
                      'omc': round(dat['overallMarketCap']),  ##overallMarketCap
                      'volume': None
                      }
        # Find the corresponding name for the index
        matching_stock_name = next(
            (stock['name'] for stock in stock_list if stock['index_id'] == int(stock_info['symbol'])),
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


def securities_EoD_by_date(bearer: str, index_id: int, start_date: str):
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
    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': f"Bearer {bearer}",
        'accept': "application/json"
    }

    conn.request("GET",
                 f"/tase/prod/api/v1/securities/trading/eod/history/ten-years/by-security?securityId={index_id}&fromDate={start_date}&toDate={start_date}",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    try:
        dat = json.loads(data)['securitiesEndOfDayTradingData']['result'][0]  # will only work for one day extraction
        stock_info = {'symbol': dat['securityId'],
                      'date': datetime.strptime(dat['tradeDate'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d'),
                      'open': dat['openingPrice'],
                      'close': dat['closingPrice'],
                      'high': dat['high'],
                      'low': dat['low'],
                      'omc': round(dat['marketCap']),
                      'volume': round(dat['volume'])
                      }
        matching_stock_name = next(
            (stock['name'] for stock in stock_list if stock['index_id'] == int(stock_info['symbol'])),
            None)
        stock_info['symbol_name'] = matching_stock_name
        if matching_stock_name is None:
            raise Exception
        return stock_info
    except Exception as e:
        print(e)


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
