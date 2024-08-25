from datetime import datetime, timedelta


class Stock:
    def __init__(self, data):
        self.index_symbol = data.get("Index_Symbol")
        self.symbol_name = data.get("Symbol_Name")
        self.description = data.get("description")
        self.num_days = data.get("num_days")
        self.last_access_date = datetime.today()
        # Convert date strings to datetime objects and sort the price_data by date
        self.price_data = sorted(
            [
                {"date": datetime.strptime(item["date"], "%Y-%m-%d"), "close_price": item["close_price"]}
                for item in data.get("price_data", [])
            ],
            key=lambda x: x["date"]
        )

    def validate_price_data(self):
        for entry in self.price_data:
            assert isinstance(entry["date"], datetime), f"Date {entry['date']} is not a datetime object"
        print("Price data validation passed.")

    def __repr__(self):
        return f"StockCacheItem(Symbol: {self.symbol_name}, Index: {self.index_symbol}, Days: {self.num_days})"

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
    