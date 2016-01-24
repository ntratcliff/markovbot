import sqlite3 as sql
import os

#create caching db
dbLoc = os.path.join(os.path.dirname(__file__), 'msg-cache.db')
print('Creating file ' + dbLoc + '...');

conn = sql.connect(dbLoc)

cur = conn.cursor()

#create messages table
cur.execute('''CREATE TABLE messages (
		message_text text, 
		channel text, 
		timestamp text, 
		user text)''')

conn.commit()
conn.close()
