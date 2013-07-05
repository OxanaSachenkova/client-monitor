import bottle
from bottle import route, run, request
import sqlite3
import json
import logging

@route('/', method='GET')
def homepage():
    return 'Hello, I am your main server'
    
@route('/info', method='POST')
def receive_info():
    #get json
    #parse json 
    logging.basicConfig(level=logging.DEBUG)
    data = json.load(request.body)
    #print Data
    logging.info(data)
    
    #data = many rows
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    for row in data:
        logging.info(row)
        c.execute("INSERT INTO log (hostId, cpu,time) VALUES (?, ?, ?)",row)

    new_id = c.lastrowid

    conn.commit()
    c.close()
    

@route('/logs', method='GET')
def show_logs():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute("SELECT hostId, cpu FROM log")
    result = c.fetchall()
    return str(result)


bottle.debug(True) 
bottle.run(host='localhost', port=8081,reloader=True) 
