import sqlite3

connection = sqlite3.connect('site_db.sqlite')
cursor = connection.cursor()

with open('create_db.sql', 'r') as f:
    script = f.read()

cursor.executescript(script)
cursor.close()
connection.close()
