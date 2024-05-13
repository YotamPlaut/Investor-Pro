class Stock:
    def __init__(self, name: str, index: int, date: str, open: float, close: float, high: float, low: float):
        self.index = index
        self.name = name
        self.date = date
        self.high = high
        self.low = low
        self.open = open
        self.close = close
