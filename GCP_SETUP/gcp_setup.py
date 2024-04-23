import hashlib
from datetime import datetime

from sqlalchemy import MetaData, Table, Column, String, text
import pg8000
import sqlalchemy

########################### GCDS SETUP PARAMS #########################
INSTANCE_CONNECTION_NAME = 'investor-pro-418817:us-west1:investorprodb'
DB_USER = 'investorpro_mng'
DB_PASS = 'admin'
DB_NAME = 'app_db'
DB_HOST = '34.168.210.93'


############################################################################

def getconn() -> pg8000.Connection:
    conn: pg8000.Connection = pg8000.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
    )
    return conn


def get_pool():
    pool = sqlalchemy.create_engine(
        f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
        creator=getconn,
        # Additional options if needed
    )
    return pool

#
# def get_all_records_from_table(table_name):
#     engine = get_pool()
#     with engine.connect() as conn:
#         result = conn.execute(text(f'SELECT * FROM {table_name}'))  # Use conn.execute instead of engine.execute
#         return result.fetchall()
#
#
#
#
#
# def insert_test_user(user_id, password, email_address):
#         # Hash the password using SHA-256
#         hash_pass = hashlib.sha256(password.encode()).hexdigest()
#
#         engine = get_pool()
#         with engine.connect() as conn:
#             insert_query = text(
#                 f"""
#                 INSERT INTO server.user_logins (user_id,
#                                                 hash_pass,
#                                                 email_adress,
#                                                 install_date,
#                                                 creation_date,
#                                                 update_date)
#                 VALUES ('{user_id}','{hash_pass}','{email_address}','{datetime.now()}','{datetime.now()}','{datetime.now()}' )
#
#                 """
#             )
#             conn.execute(insert_query)
#             conn.commit()
#
# if __name__ == '__main__':
#     # insert_test_user('test_user_ishay_2', '1234567', 'ishay6411@gmail.zibi.com')
#     # # insert_into_test()
#     # rows = get_all_records_from_table('server.server_test')
#     # #print(rows)
#     has_pass=hashlib.sha256('1234567'.encode()).hexdigest()
#
#     engine = get_pool()
#     with engine.connect() as conn:
#         result = conn.execute(text(f"SELECT * FROM server.user_logins where hash_pass='{has_pass}'"))  # Use conn.execute instead of engine.execute
#         print(result.fetchall())
#
#
#
