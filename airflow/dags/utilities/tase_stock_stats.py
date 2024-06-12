import json
from datetime import datetime
import numpy as np
import pandas as pd


def calc_stock_stats_sharp_ratio(stock_data: pd.DataFrame,
                                 risk_free_rate_annual=0.045,
                                 trading_days_per_year: int = 252):
    try:
        stock_data = stock_data.copy()

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
