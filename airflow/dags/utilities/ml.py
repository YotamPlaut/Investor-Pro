###CONST####
target = 'close'
feature = ['dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'close_28_before', 'close_7_before',
           'close_3_before', 'close_2_before', 'close_1_before']


#####


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
