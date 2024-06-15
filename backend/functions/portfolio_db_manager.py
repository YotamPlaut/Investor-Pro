from GCD_SETUP.gcp_setup import get_pool
from sqlalchemy import text
import warnings


class PortfolioDatabaseManager:

    _instance = None
    table_name = 'server.portfolios'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # test this one:
    def is_username_and_portfolio_name_exists(self, username: str, portfolio_name):
        engine = get_pool()
        with engine.connect() as conn:
            query = text(f"SELECT COUNT(*) FROM {self.table_name} WHERE user_id = '{username}' "
                         f"AND portfolio_id = '{portfolio_name}' ")
            result = conn.execute(query)
            exists = result.scalar() > 0
            return exists

    def insert_new_portfolio(self, user_id: str, portfolio_id: str, stock_array: set = None):
        try:
            insert_query = (
                f"""
                   INSERT INTO {self.table_name} (user_id,
                                                  portfolio_id,
                                                  stock_array
                                                  )
                   VALUES ('{user_id}','{portfolio_id}','{stock_array}')
                """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(insert_query))
                    conn.commit()
                return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was inserted to db"}
        except Exception as e:
            print("error occurred while running insert query")
            return None

    def remove_portfolio(self, user_id: str, portfolio_id: str):
        try:
            delete_query = (
                f"""
                    DELETE FROM {self.table_name}
                            WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';

                 """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(delete_query))
                    conn.commit()
                return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was removed from db"}
        except Exception as e:
            print("error occurred while running delete query")
            return None

    def add_new_stock_to_portfolio(self, user_id: str, portfolio_id: str, stock_int: int):
        try:
            update_query = (
                f"""
                   UPDATE {self.table_name}
                   SET stock_array = CASE
                                    WHEN NOT ({stock_int} = ANY(stock_array)) THEN stock_array || {stock_int}
                                    ELSE stock_array END
                   WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
                """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    # warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(update_query))
                    conn.commit()
            return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was was updated"}

        except Exception as e:
            print("error occurred while running update query ")
        return None

    def remove_stock_from_portfolio(self, user_id: str, portfolio_id: str, stock_int: int):
        try:
            update_query = (
                f"""
                   UPDATE {self.table_name}
                   SET stock_array = array_remove(stock_array, {stock_int})
                   WHERE user_id = '{user_id}' AND portfolio_id = '{portfolio_id}';
                """
            )
            engine = get_pool()
            with engine.connect() as conn:
                with warnings.catch_warnings():
                    #warnings.filterwarnings("ignore", category=RemovedIn20Warning)
                    conn.execute(text(update_query))
                    print(update_query)
                    conn.commit()
            return {'code': 1, 'msg': f" portfolio : {portfolio_id}, for user:  {user_id} was was updated"}

        except Exception as e:
            print("error occurred while running update query ")
        return None

    def get_all_portfolios(self):
        engine = get_pool()
        with engine.connect() as conn:
            result = conn.execute(
                text(f'SELECT * FROM {self.table_name}'))  # Use conn.execute instead of engine.execute
            return result.fetchall()
