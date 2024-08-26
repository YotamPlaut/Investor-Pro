from datetime import datetime, timedelta


class Stock:
    def __init__(self, data):
        # this is int representation
        self.symbol = data.get("index_symbol")
        self.name = data.get("symbol_name")
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

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "description": self.description,
            "num_days": self.num_days,
            #"last_access_date": self.last_access_date.strftime("%Y-%m-%d"),  # Convert datetime to string
            "price_data": [
                {
                    "date": item["date"].strftime("%Y-%m-%d"),  # Convert datetime to string
                    "close_price": item["close_price"]
                } for item in self.price_data
            ]
        }