

class CacheItem:
    def __init__(self, first_date, last_date, stock_index: int, data: dict):
        self.first_date = first_date
        self.last_date = last_date
        self.stock_index = stock_index
        self.data = data
