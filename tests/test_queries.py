import os
import sqlite3

'''Вспомогательный код для тестирования корректности генерируемых запросов'''


def connect_to_db(execute_query):
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = sqlite3.connect(os.path.join(kwargs.pop('path'), 'database.db'))
            cursor = connection.cursor()
            return execute_query(cursor, kwargs.pop('query'), *args, **kwargs)
        finally:
            if connection:
                connection.commit()
                connection.close()
    return wrapper


@connect_to_db
def select(cursor, query, *args, **kwargs):
    cursor.execute(query)
    if kwargs.get('print_res'):
        records = cursor.fetchall()
        print(records)
    return cursor


@connect_to_db
def create_table(cursor, query, *args, **kwargs):
    cursor.execute(query)


@connect_to_db
def insert(cursor, query, *args, **kwargs):
    cursor.execute(query)
