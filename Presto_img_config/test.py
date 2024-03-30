import psycopg2
import pandas as pd

# Database connection parameters
dbname = 'AppDataBase'
user = 'InvestorPro'
password = '123456!@'
host = 'localhost'  # Hostname of the PostgreSQL service in Docker Compose
port = '5432'  # Port number for PostgreSQL


def create_table(conn):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS test_table (
            name VARCHAR(50),
            last_name VARCHAR(50)
        )
    '''

    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()


def insert_data(conn):
    insert_query = '''
        INSERT INTO public.test_table (name, last_name) VALUES (%s, %s)
    '''
    data = [('Johna', 'Doea')]
    cur = conn.cursor()
    cur.executemany(insert_query, data)
    conn.commit()


def print_all_records(conn):
    select_query = '''
            SELECT * FROM public.test_table
        '''
    cur = conn.cursor()
    cur.execute(select_query)
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
    print(df)




if __name__ == '__main__':
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connected to the database")
        #create_table(conn=conn)
        #print('created table')
        #insert_data(conn=conn)
        #print('inserted data')
        print_all_records(conn=conn)


##hi shachar

    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
        exit()

