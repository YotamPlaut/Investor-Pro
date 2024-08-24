import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

###CONST####
target = 'close'
feature = ['dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'close_28_before', 'close_7_before',
           'close_3_before', 'close_2_before', 'close_1_before']


######3


class xgb_regressor:
    def __init__(self, n_estimators: int = 6000, early_stopping_rounds: int = 50, learning_rate: int = 0.001,
                 verbose=100):
        self.target = 'close'
        self.feature = ['dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'close_28_before', 'close_7_before',
                        'close_3_before', 'close_2_before', 'close_1_before']
        self.n_estimators = n_estimators
        self.early_stopping_rounds = early_stopping_rounds
        self.learning_rate = learning_rate
        self.verbose = verbose

    def collect_date(self, file_name=None):
        self.df = pd.read_csv("TA_125.csv")

    def add_feature(self):
        df = self.df.copy()
        df['dayofweek'] = df.index.dayofweek
        df['quarter'] = df.index.quarter
        df['month'] = df.index.month
        df['year'] = df.index.year
        df['dayofyear'] = df.index.dayofyear
        self.df = df

    def add_lag_feature(self):
        df = self.df.copy()
        df['close_28_before'] = df['close'].shift(28)
        df['close_7_before'] = df['close'].shift(7)
        df['close_3_before'] = df['close'].shift(3)
        df['close_2_before'] = df['close'].shift(2)
        df['close_1_before'] = df['close'].shift(1)
        self.df = df

    def train(self):
        ##ading features
        self.add_feature()
        self.add_lag_feature()

        # split test and train
        self.X_all = self.df[feature]
        self.y_all = self.df[target]
        reg = xgb.XGBRegressor(n_estimators=self.n_estimators, early_stopping_rounds=self.early_stopping_rounds,
                               learning_rate=self.learning_rate)
        reg.fit(self.X_all, self.y_all,
                eval_set=[(self.X_all, self.y_all)],
                verbose=100
                )
        self.reg = reg

    def predict(self, future_days=7):
        pass