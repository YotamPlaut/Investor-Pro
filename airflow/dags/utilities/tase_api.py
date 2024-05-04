#######tase key###########
# key: ecbcee894a91d47a30cfca5560769288
# password:4e418f5616c8f30f0d23420d31e8c670
#####################

import http.client
import json
from datetime import datetime


curr_barr = "AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODgLTHu8aTr12FQhHw5a9BbZGIxTxNgRKG2-CCgpVsBY4wD0cVp1YnIHvhoNaaYSMZ7sF9DJ7yPxa8zuHftsuJc0K5JnzorIF-iPy0xyEYEjuFXBHUJG0-9FrG8ADwWZLQE"


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
                      'low': dat['low']
                      }
        print(stock_info)
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
