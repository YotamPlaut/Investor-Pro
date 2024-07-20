from datetime import datetime


class Stock:
    def __init__(self, stock: dict):
        self.index = stock['index_symbol']
        self.name = stock['symbol_name']
        self.info = stock['info']
        self.num_days = stock['num_days']
        self.begin_date = self.find_min_date(self.info)
        self.end_date = self.find_max_date(self.info)

    @staticmethod
    def find_min_date(data):
        # Convert the keys to date objects and find the minimum date
        dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in data.keys()]
        min_date = min(dates)
        return min_date.strftime('%Y-%m-%d')

    @staticmethod
    def find_max_date(data):
        # Convert the keys to date objects and find the maximum date
        dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in data.keys()]
        max_date = max(dates)
        return max_date.strftime('%Y-%m-%d')
    