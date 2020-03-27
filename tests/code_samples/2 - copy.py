import sqlite3


connection = sqlite3.connect('database.db')
name = 'test name'
surname = 'dfgdfg'
res = connection.execute("SELECT name    FROM users    ;")
connection.execute("INSERT INTO blogs (name) VALUES(?);", (name, ))
connection.execute("CREATE TABLE comments (id integer PRIMARY KEY, content text NOT NULL);")
connection.execute("INSERT INTO users (name, surname) VALUES(?, ?);", (name, surname, ))
i = 1
new_name = 'John'
connection.execute("UPDATE users SET name=?, surname = 'Doe' WHERE id = ?;", (new_name, i, ))
connection.execute("DELETE FROM users WHERE id=?;", (i, ))
res = connection.execute("SELECT name FROM users ;").fetchall()
