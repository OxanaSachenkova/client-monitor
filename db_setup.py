import sqlite3
con = sqlite3.connect('logs.db') # Warning: This file is created in the current directory
con.execute("CREATE TABLE log (id INTEGER PRIMARY KEY, hostId INTEGER NOT NULL, cpu char(100) NOT NULL,time char(100) NOT NULL)")
con.execute("CREATE TABLE clients (id INTEGER PRIMARY KEY, hostId INTEGER NOT NULL, platform char(100) NOT NULL, time char(100) NOT NULL)")
#con.execute("INSERT INTO log (hostId,cpu,time) VALUES (111,'0.0','2011-10-11')")
con.commit()