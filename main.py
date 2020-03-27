import os
import sqlite3

from src.preprocessor import process_file
from tests.test_queries import create_table, select


def main(file_name):
    path = os.path.dirname(os.path.abspath(__file__))
    testing_folder = os.path.join(path, 'tests', 'code_samples')
    file_path = os.path.join(testing_folder, file_name)
    process_file(file_path, 'connection')
    create_table(path=path,
                 query="CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text NOT NULL, surname text NOT NULL);")
    create_table(path=path, query="CREATE TABLE IF NOT EXISTS blogs (id integer PRIMARY KEY, name text NOT NULL);")
    '''
    name = 'test name'
    surname = 'dfgdfg'
    connection = None
    try:
        connection = sqlite3.connect(os.path.join(path, 'database.db'))
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, surname) VALUES(?, ?)", (name, surname,))
        cursor.execute("INSERT INTO blogs (name) VALUES(?)", (name,))
    finally:
        if connection:
            connection.commit()
            connection.close()
    '''
    select(path=path, query="SELECT u.name, u.surname FROM users u", print_res=True)
    select(path=path, query="SELECT * FROM blogs", print_res=True)


if __name__ == '__main__':
    '''
    to do: 
    сделать, чтобы запросы надо было писать в комментарии, чтобы IDE не считал их ошибкой?
    название connection?
    пробел после $?
    сохранять indent
    '''
    main('2.py')
