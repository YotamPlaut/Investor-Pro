#######tase key###########
# key: ecbcee894a91d47a30cfca5560769288
# password:4e418f5616c8f30f0d23420d31e8c670
#####################

import http.client
import json
from datetime import datetime

curr_barr = "AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODgLTHu8aTr12FQhHw5a9BbZGIxTxNgRKG2-CCgpVsBY4wD0cVp1YnIHvhoNaaYSMZ7sF9DJ7yPxa8zuHftsuJc0K5JnzorIF-iPy0xyEYEjuFXBHUJG0-9FrG8ADwWZLQE"

stock_list = [
    {'index': 142, 'name': 'tel_aviv_35'},
    {'index': 143, 'name': 'tel_aviv_90'},
    {'index': 147, 'name': 'semi_60'},
    {'index': 148, 'name': 'finaces'},
    {'index': 169, 'name': 'top_100_tech'},
    {'index': 601, 'name': 'all_bonds'}
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
    json_obj = indices_EoD_by_date(bearer=get_Bar(),
                                   index_id=142,
                                   start_date='2024-05-01')
    print(json_obj)
    print(json_obj['symbol'])
    matching_stock_name = next((stock['name'] for stock in stock_list if stock['index'] == int(json_obj['symbol'])), None)
    print(matching_stock_name)
    json_obj['symbol_name'] = matching_stock_name
    print(json_obj)