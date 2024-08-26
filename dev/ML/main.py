from xgboost_class import xgb_regressor, collect_date
from dev.UTILS.utils import  get_Bar

current_bar = "AAIgZWNiY2VlODk0YTkxZDQ3YTMwY2ZjYTU1NjA3NjkyODgKXxmzO_lOTZ94MZbaF1aMSFS6MNmD8ev_ho27IdYtPyTfkF_EpNU2Df0kf1hRgfmnOVZyLGkkH_SGQGgqqFDv0h4Qy3V0RRaEHCcr5wPE28_7l1k9g1N5TMKmjamiXiY"

if __name__ == '__main__':
    collect_date(stock_name='TA-125 Index',bearer_token=current_bar)
    # collect_date(stock_name='TA-125 Index',date='1970-01-01')

    # regressor = xgb_regressor(stock_name='TA-125 Index')
    # regressor.collect_date()
    # regressor.train()
    # regressor.predict(future_days=7)
    # regressor.store_predictions_into_db()
