# db.py
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname='covid',
        user='postgres',
        password=12345,
        host='localhost'
    )
    return conn
