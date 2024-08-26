class StockData:
    _stock_list = [
        {'index_id': 137, 'name': 'TA_125', 'IsIndex': True},
        {'index_id': 147, 'name': 'TA_SME_60', 'IsIndex': True},
        {'index_id': 709, 'name': 'TA_Bond_60', 'IsIndex': True},
        {'index_id': 662577, 'name': 'Bank_Hapoalim', 'IsIndex': False},
        {'index_id': 691212, 'name': 'Bank_Discount', 'IsIndex': False},
    ]

    @classmethod
    def get_stock_list(cls):
        return cls._stock_list
