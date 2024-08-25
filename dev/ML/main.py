from xgboost_class import xgb_regressor, collect_date

if __name__ == '__main__':
    collect_date(stock_name='TA-125 Index',date='1970-01-01')

    # regressor = xgb_regressor(stock_name='TA-125 Index')
    # regressor.collect_date()
    # regressor.train()
    # regressor.predict(future_days=7)
    # regressor.store_predictions_into_db()
