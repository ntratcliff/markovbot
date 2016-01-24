from slacksocket import SlackSocket
import os
import json
import sqlite3 as sql

#get api configuration file
confLoc = os.path.join(os.path.dirname(__file__), 'api.conf')
with open(confLoc) as conf_file:
	apiconf = json.load(conf_file)

socket = SlackSocket(apiconf['slack']['api-key'], 
			translate=False,
			event_filters = ['message'])

#open database
dbLoc = os.path.join(os.path.dirname(__file__), 'msg-cache.db')
conn = sql.connect(dbLoc)
cur = conn.cursor()

def cacheEvent(json):
	entry = (json['text'], json['channel'], json['ts'], json['user'])
	cur.execute('INSERT INTO messages VALUES (?,?,?,?)', entry)
	conn.commit()

def updateEvent(json):
	#todo: handle message updating
	return

for event in socket.events():
	if 'subtype' in event.event:
		updateEvent(event.event)
	else:
		cacheEvent(event.event)
