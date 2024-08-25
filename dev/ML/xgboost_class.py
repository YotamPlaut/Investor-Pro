import json

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from datetime import datetime, timezone, timedelta
from dev.UTILS.utils import get_pool, table_configs,\
    stock_list,get_stock_data_by_date,\
    get_Bar,\
    indices_EoD_by_index_from_date_to_date,\
    securities_EoD_by_index_from_date_to_date,\
    get_matching_stock_name_index,\
    get_matching_is_index

import warnings
from sqlalchemy import text

###CONST####
target = 'close'
feature = ['dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'close_28_before', 'close_7_before',
           'close_3_before', 'close_2_before', 'close_1_before']

# stock_list = [
#     {'index_id': 137, 'name': 'TA-125 Index', 'IsIndex': True},
#     {'index_id': 147, 'name': 'TA-SME 60 Index', 'IsIndex': True},
#     {'index_id': 709, 'name': 'TA-Bond 60 Index', 'IsIndex': True},
#     {'index_id': 662577, 'name': 'Bank Hapoalim', 'IsIndex': False},
#     {'index_id': 691212, 'name': 'Bank Discount', 'IsIndex': False},
# ]

table_configs = {
    'stocks': {
        'raw_data': 'stocks.tase_stock_data',
        'stats': 'stocks.tase_stock_stats'
    },
    'server': {
        'users': 'server.users',
        'actions': 'server.raw_actions'
    }
}


######3
def add_feature(df):
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    return df


def add_lag_feature(df):
    df['close_28_before'] = df['close'].shift(28)
    df['close_7_before'] = df['close'].shift(7)
    df['close_3_before'] = df['close'].shift(3)
    df['close_2_before'] = df['close'].shift(2)
    df['close_1_before'] = df['close'].shift(1)
    return df

def collect_date(stock_name: str,date):
     #get data from the database.
     db_info = json.loads(get_stock_data_by_date(stock_name,date))['price_data']
     df = pd.DataFrame(db_info)
     df['date'] = pd.to_datetime(df['date'])
     df.set_index('date', inplace=True)
     df.rename(columns={'close_price': 'close'}, inplace=True)

     #get the min date of the db data, and the number of days in it
     min_date = df.index.min()
     num_rows = len(df)
     stock_index = get_matching_stock_name_index(stock_name=stock_name)
     stock_isIndex = get_matching_is_index(stock_name=stock_name)
     start_date = min_date + timedelta(days=-1*(403-num_rows))
     if stock_isIndex:
         stock_info = indices_EoD_by_date(current_bearer_token, stock_index, execution_date)
     else:
         stock_info = securities_EoD_by_date(current_bearer_token, stock_index, execution_date)


     print(min_date)
     print(num_rows)
     print(stock_index)
     print(stock_isIndex)
     print(start_date)



    # db_info = get_stock_data_by_date(stock_name, '1970-01-01')
    # return db_info


class xgb_regressor:
    def __init__(self, stock_name, n_estimators: int = 6000, early_stopping_rounds: int = 50,
                 learning_rate: int = 0.001,
                 verbose=100):
        self.stock_name = stock_name
        self.stock_index = get_matching_stock_name_index(self.stock_name)
        self.target = 'close'
        self.feature = ['dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'close_28_before', 'close_7_before',
                        'close_3_before', 'close_2_before', 'close_1_before']
        self.n_estimators = n_estimators
        self.early_stopping_rounds = early_stopping_rounds
        self.learning_rate = learning_rate
        self.verbose = verbose

    def collect_date(self, file_name=None):
        self.df = pd.read_csv("TA_125.csv").drop('Unnamed: 0', axis=1).set_index('date')
        self.df.index = pd.to_datetime(self.df.index)
        self.df = self.df[['close']].astype('float64')

    def train(self):
        ##ading features
        self.df = add_feature(self.df)
        self.df = add_lag_feature(self.df)

        # split test and train
        self.X_all = self.df[feature]
        self.y_all = self.df[target]
        reg = XGBRegressor(n_estimators=self.n_estimators, early_stopping_rounds=self.early_stopping_rounds,
                           learning_rate=self.learning_rate)
        reg.fit(self.X_all, self.y_all,
                eval_set=[(self.X_all, self.y_all)],
                verbose=100
                )
        self.reg = reg

    def add_future_days_to_df(self, future_days):
        self.future_days = future_days
        df = self.df.copy()
        start_date = df.index.max() + pd.DateOffset(days=1)
        end_date = start_date + pd.DateOffset(days=future_days)
        time_span = pd.date_range(start_date, end_date)
        future_df = pd.DataFrame(index=time_span)
        future_df['isFuture'] = True
        df['isFuture'] = False
        df_and_Future = pd.concat([df, future_df])
        df_and_Future = add_feature(df_and_Future)
        df_and_Future = add_lag_feature(df_and_Future)
        self.df = df_and_Future

    def predict(self, future_days):
        self.add_future_days_to_df(future_days)
        future = self.df.query('isFuture').copy()
        predictions = self.reg.predict(future[feature])
        # predictions_dict = zip(future.index, predictions)
        predictions_dict = {str(ts): round(float(val), 2) for ts, val in zip(future.index, predictions)}
        predictions_json = json.dumps(predictions_dict)
        self.predictions = predictions_json

    def store_predictions_into_db(self):
        insert_command = f"""
        INSERT INTO stocks.tase_stock_predictions (index_symbol, symbol_name, predictions, insert_time)
        VALUES ('{self.stock_index}', '{self.stock_name}', '{self.predictions}', '{datetime.now(timezone.utc)}');
        """
        print(insert_command)

        engine = get_pool()
        with engine.connect() as conn:
            with warnings.catch_warnings():
                # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                conn.execute(text(insert_command))
                conn.commit()
