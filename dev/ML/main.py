from xgboost_class import XgbRegressor
from dev.UTILS.utils import stock_list,get_Bar

current_bar = "AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODhg5KDT7kNU55GUECKYaRAotae76wkDjrYTRtPzHUKsTN8nZx2bevI7WJlj7VainyGGxCrVW726u0fgC5CZSF_GRI5huVcjyTaIX97_ipV37gaieJ-V4JJoRTU5TBODkTg"


def update_stock_predictions(stock_name,bearer_token):
    regressor = XgbRegressor(stock_name=stock_name, bearer_token=bearer_token)
    regressor.collect_date()
    regressor.train()
    regressor.predict(future_days=7)
    regressor.store_predictions_into_db()


if __name__ == '__main__':

    # df = collect_date(stock_name='TA-125 Index',bearer_token=current_bar)
    # print(df.head(100))
    # collect_date(stock_name='TA-125 Index',date='1970-01-01')
    for stock in stock_list:
        update_stock_predictions(stock_name=stock['name'],bearer_token=current_bar)
