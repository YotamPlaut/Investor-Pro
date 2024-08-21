import datetime

from GCD_SETUP.gcp_setup import get_pool
from backend.classes_backend.stock_info import StockData
from sqlalchemy import text
from sqlalchemy.exc import InterfaceError
import json


class StockManager:
    _instance = None
    table_name = 'stocks.tase_stock_data'

    def __init__(self):
        self.stock_list = StockData.get_stock_list()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_stock_data_by_date(self, stock_name: str, date: datetime.date):
        """
         Fetches stock data for a given stock name starting from a specific date.
        :param stock_name: The name of the stock, which must be present in the stock_list.
        :param date: The start date for fetching the stock records, in the format of yyyy-mm-dd.
        :return: A JSON string containing:
                 - 'info': A dictionary where keys are dates and values are dictionaries of stock data (fields: Index_Symbol, Symbol_Name, Open, Close, High, Low, OMC, Volume).
                 - 'num_days': The number of unique dates in the data.
                 - 'Index_Symbol': The index symbol of the stock.
                 - 'Symbol_Name': The name of the stock.
                 If an error occurs, None is returned.
        """
        matching_stock_index = next(
            (stock['index_id'] for stock in self.stock_list if stock['name'] == stock_name),
            None)
        if matching_stock_index is None:
            print(f"didnt found maching index for stock: {stock_name}")
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
                stock_data_dict = {'info': {}}
                for row in result:
                    # date_str = row['date'].strftime('%Y-%m-%d')  # Ensure date is in string format for JSON compatibility
                    stock_data_dict['info'][row[0].strftime('%Y-%m-%d')] = {
                        'Index_Symbol': row[1],
                        'Symbol_Name': row[2],
                        'Open': row[3],
                        'Close': row[4],
                        'High': row[5],
                        'Low': row[6],
                        'OMC': row[7],
                        'Volume': row[8]
                    }
                # Add the number of unique dates to the JSON object
                num_days = len(stock_data_dict['info'])
                stock_data_dict['num_days'] = num_days
                stock_data_dict['index_symbol'] = matching_stock_index
                stock_data_dict['symbol_name'] = stock_name

                # Convert dictionary to JSON
                return stock_data_dict

        except InterfaceError:
            return {'error': 'error while fetching data'}
        except Exception as e:
            print(f"error occurred while running query: {e}")
            return None

    def is_valid_index(self, stock_index: int):
        for stock in self.stock_list:
            if stock['index_id'] == stock_index:
                return True
        return False


if __name__ == '__main__':
    st_manager = StockManager()
    data = st_manager.get_stock_data_by_date('Bank_Hapoalim', '2024-05-06')
    for key in data['info'].keys():
        print(key)
        print(data['info'][key])
