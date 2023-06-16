import os
import mysql.connector
from sqlalchemy import create_engine


HOST = "localhost"
USER = os.getenv('MYSQL_USERNAME')
PASSWORD = os.environ.get('MYSQL_PASSWORD')
DATABASE = "hush_hush"


def get_database_connection():
    return mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)


def get_sql_engine():
    return create_engine(f'mysql://{USER}:{PASSWORD}@localhost/{DATABASE}')


if __name__ == '__main__':
    database = get_database_connection()
    if database.is_connected():
        print("Connected successfully to MySQL Database!")

    engine = get_sql_engine()
    if engine:
        print("Connected successfully through SQLAlchemy!")
