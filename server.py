import bottle
from bottle import route, run, request
import sqlite3
import json
import logging
import collections

@route('/', method='GET')
def homepage():
    return 'Hello, I am your main server'
    
@route('/log', method='POST')
def receive_log():
    logging.basicConfig(level=logging.DEBUG)
    data = json.load(request.body)
    logging.info(data)
    
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    for row in data:
        c.execute("INSERT INTO log (hostId, cpu, time) VALUES (?, ?, ?)",row)
        logging.info(row)
    conn.commit()
    c.close()

@route('/host', method='POST')
def receive_host():
    logging.basicConfig(level=logging.DEBUG)
    data = json.load(request.body, object_pairs_hook=collections.OrderedDict)
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute("INSERT INTO clients (hostId, platform, time) VALUES (?, ?, ?)",data.values())
    conn.commit()
    c.close()
    
@route('/showlogs', method='GET')
def show_logs():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute("SELECT hostId, cpu FROM log")
    result = c.fetchall()
    return str(result)

@route('/showhosts', method='GET')
def show_hosts():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute("SELECT hostId, platform FROM clients")
    result = c.fetchall()
    return str(result)

bottle.debug(True) 
bottle.run(host='localhost', port=8081,reloader=True) 
