import sqlite3


connection = sqlite3.connect('database.db')
name = 'test name'
surname = 'dfgdfg'
SELECT name\
    FROM users\
    $into res;
INSERT INTO blogs (name) VALUES($name);
$(CREATE TABLE comments (id integer PRIMARY KEY, content text NOT NULL);)
INSERT INTO users (name, surname) VALUES($name, $surname);
i = 1
new_name = 'John'
UPDATE users SET name=$new_name, surname = 'Doe' WHERE id = $i;
DELETE FROM users WHERE id=$i;
SELECT name FROM users $into res bulk;
