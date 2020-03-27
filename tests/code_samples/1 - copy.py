import math
import sqlite3

'''тест корректной работы с кодом Python - он не должен меняться'''

connection = sqlite3.connect('database.db')
a = 'gfdgd'
for c in a:
    print(c)
RES = connection.execute("SELECT name    FROM users ")
# $ is allowed inside comments
'''$ inside multiline comments too
multiline
'''
for i in range(5):
    pass
e = 500
multiline = 4 + \
    4 + \
    4
math.ceil(e - 23.2)
connection.close()
