from datetime import time
from GCD_SETUP.gcp_setup import get_pool
from sqlalchemy import text
import pandas as pd


class StockManager:
    _instance = None
    table_name = 'stocks.tase_stock_data'
    stock_list = [
        {'index_id': 137, 'name': 'TA_125', 'IsIndex': True},
        {'index_id': 147, 'name': 'TA_SME_60', 'IsIndex': True},
        {'index_id': 709, 'name': 'TA_Bond_60', 'IsIndex': True},
        {'index_id': 662577, 'name': 'Bank_Hapoalim', 'IsIndex': False},
        {'index_id': 691212, 'name': 'Bank_Discont', 'IsIndex': False},

    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_stock_data_by_date(self, stock_name: str, date: str):
        """
        :param stock_name: stock name as a string, need to be one out of the stock_list
        :param date: stat date, the function will return all records from this start date, in the format of yyyy-mm-dd
        :return: return a pandas data frame with these cols: Date  Index_Symbol  Symbol_Name   Open    Close     High      Low
                 plus is return the shape of the data frame as a tuple, (number of rows, number of cols).
                 In case some error occurred, we will return None.
        """
        matching_stock_index = next(
            (stock['index_id'] for stock in self.stock_list if stock['name'] == stock_name),
            None)
        if matching_stock_index is None:
            print(f"did not found matching index for stock: {stock_name}")
            return None
        try:
            engine = get_pool()
            query = f"""
                     select 
                        date,
                        index_symbol,
                        symbol_name,
                        open,
                        close,
                        high,
                        low,
                        omc,
                        volume
                    from {self.table_name}
                    where index_symbol='{matching_stock_index}' and date>=date('{date}');
              """
            with engine.connect() as conn:
                result = conn.execute(text(query)).fetchall()
                df = pd.DataFrame(result,
                                  columns=['Date', 'Index_Symbol', 'Symbol_Name', 'Open', 'Close', 'High', 'Low', 'omc',
                                           'volume'])
                return df, df.shape
        except Exception:
            print("error occurred while running query")
            return None

    def is_valid_index(self, stock_index: int):
        for stock in self.stock_list:
            if stock['index_id'] == stock_index:
                return True
        return False


if __name__ == '__main__':
    st_manager = StockManager()
    df, shape = st_manager.get_stock_data_by_date('Bank_Hapoalim', '2024-05-06')
    print(df.to_json())
