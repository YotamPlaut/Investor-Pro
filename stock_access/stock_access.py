#######tase key###########
#key: ecbcee894a91d47a30cfca5560769288
#password:4e418f5616c8f30f0d23420d31e8c670
#####################


import http.client
import json


def indices_EoD_by_date():
    conn = http.client.HTTPSConnection("openapigw.tase.co.il")

    headers = {
        'Authorization': "Bearer AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODgmvyHqhlEQVFAiIAvKkztHku_1GRCpQiGNNG4FvrOodOVGDg6m62eA1ZLPBKXBt67YQrUoKgpVi2aoLBESZMvAxfENqj9Lz_LFadfIniIfGuIMdFn_ShJ9dfNzyT9T_Ak",
        'accept': "application/json"
    }

    conn.request("GET",
                 "/tase/prod/api/v1/indices/eod/history/ten-years/by-index?indexId=142&fromDate=2024-01-01&toDate=2024-01-03",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))




    #print(type(data))
    #print(data.decode("utf-8"))



if __name__ == '__main__':
    indices_EoD_by_date()
