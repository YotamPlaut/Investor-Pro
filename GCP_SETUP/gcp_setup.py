from datetime import time

import pandas as pd
from sqlalchemy import MetaData, Table, Column, String, text
import sqlalchemy
import pg8000

# from sqlalchemy.dialects.postgresql import pg8000

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
        future=True
        # Additional options if needed
    )
    return pool