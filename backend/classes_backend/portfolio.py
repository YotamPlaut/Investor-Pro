class Portfolio:
    def __init__(self, port_name: str, stock_list: list):
        self.port_name = port_name
        self.stocks = stock_list

    def to_dict(self):
        return {
            "port_name": self.port_name,
            "stock_list": self.stocks
        }
