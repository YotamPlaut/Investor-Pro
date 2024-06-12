import http.client
import json
from datetime import datetime, time
import numpy as np
import pandas as pd

############### tase configurations    ##################
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


##########################################################
############### tase api functions    ##################

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


##########################################################


def run_stock_stats_sharp_ratio(stock_data: pd.DataFrame, index_id: int, start_date: datetime = datetime(1970, 1, 1),
                                risk_free_rate_annual=0.045,
                                trading_days_per_year: int = 252):
    try:
        stock_data = stock_data.copy()
        stock_data = stock_data[stock_data['date'] >= start_date]

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
        return res_json

    except Exception as e:
        print(e)
