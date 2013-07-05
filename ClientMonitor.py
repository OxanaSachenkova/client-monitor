import psutil
import time
import json, requests
from datetime import datetime

class ClientMonitor:
    "getting data on the client and sending it to the server"
    
    def get_process_id(self, pname):
        for proc in psutil.process_iter():
            if proc.name == pname:
                return proc.pid

    def get_process_status(self, pid):
        status={}
        p = psutil.Process(pid)
        status["cpu"] = p.get_cpu_percent(interval= 0.1 )
        return status

    def send_to_server(self):
        status = [x.split(",") for x in self.log] 
        print json.dumps(status)
        print "request"
        requests.post('http://localhost:8081/info', data=json.dumps(status))
        # TODO: erase only of got 200 OK from the server
        self.log = []
        print "sent"

    def run(self, interval):
        pid = self.get_process_id(self.pname)   
        while True:
            status = self.get_process_status(pid)
            ts = time.time()
            timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            self.log.append(str(self.hostId) + "," + str(status) + "," + str(timestamp))
            #TODO: send to server only once per hour or smth
            self.send_to_server()
            time.sleep(interval)

    def __init__(self, hostId, pname):
        self.hostId = hostId
        self.pname = pname
        self.log = []