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


def get_all_records_from_table(table_name):
    engine = get_pool()
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT * FROM {table_name}'))  # Use conn.execute instead of engine.execute
        return result.fetchall()


if __name__ == '__main__':
    # insert_into_test()
    rows = get_all_records_from_table('test_table')
    print(rows)
