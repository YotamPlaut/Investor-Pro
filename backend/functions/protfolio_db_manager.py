from GCD_SETUP.gcp_setup import get_pool
from sqlalchemy import text


class PortfolioDatabaseManager:

    _instance = None
    table_name = 'server.portfolios'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_username_and_portfolio_name_exists(self, username: str, portfolio_name):
        engine = get_pool()
        with engine.connect() as conn:
            query = text(f"SELECT COUNT(*) FROM {self.table_name} WHERE user_id = '{username}' "
                         f"AND portfolio_id = '{portfolio_name}' ")
            result = conn.execute(query)
            exists = result.scalar() is not None
            return exists
