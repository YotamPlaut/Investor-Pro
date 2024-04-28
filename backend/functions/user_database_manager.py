from backend.classes_backend.user import User
from GCD_SETUP.gcp_setup import get_pool
from datetime import datetime
import hashlib
from sqlalchemy import text


class UserDatabaseManager():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def is_username_exists(self, username: str):
        engine = get_pool()
        with engine.connect() as conn:
            print(username)
            result = conn.execute(text(f'SELECT * FROM {table_name}'))
            print(result)
            #data = conn.execute(text(f'SELECT COUNT(*) FROM server.user_logins WHERE user_id = {username}'))
            print(data)
            exists = data.fetchone()[0] > 0
            return exists


    def load_new_user_to_database(self, user: User):
        # Hash the password using SHA-256
        hash_pass = hashlib.sha256(user.password.encode()).hexdigest()

        engine = get_pool()
        with engine.connect() as conn:
            insert_query = text(
                f"""
                INSERT INTO server.user_logins (user_id,
                                                hash_pass,
                                                email_address,
                                                install_date,
                                                creation_date,
                                                update_date)
                VALUES ('{user.username}','{hash_pass}','{user.email_address}','{datetime.now()}','{datetime.now()}','{datetime.now()}' )

                """
            )
            conn.execute(insert_query)
            conn.commit()


if __name__ == '__main__':
    user_db_manager = UserDatabaseManager()
    user = User(username='test', email='faharshatran@gmail.com', password='123456')
    user_db_manager.load_new_user_to_database(user)
