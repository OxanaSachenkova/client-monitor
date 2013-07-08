import bottle
from bottle import route, run, request, template
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
        import ast
        row[1] = ast.literal_eval(row[1])["cpu"]
        c.execute("INSERT INTO log (hostId, cpu, time) VALUES (?, ?, ?)",row)
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
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT hostId, cpu FROM log")
    result = c.fetchall()

    logging.basicConfig(level=logging.DEBUG)
    logging.info(result)
    return template('logs_template', logs=result)

@route('/showhosts', method='GET')
def show_hosts():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute("SELECT hostId, platform FROM clients")
    result = c.fetchall()
    return str(result)

bottle.debug(True) 
bottle.run(host='localhost', port=8081,reloader=True)
bottle.TEMPLATE_PATH.insert(0,'/Users/merenlin/client-monitor/views') 
