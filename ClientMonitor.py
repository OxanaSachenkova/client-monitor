import threading
import psutil
import time
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

    def save_to_log(self,status,timestamp):
        print "saved", status, timestamp

    def run(self, interval):
        pid = self.get_process_id(self.pname)   
        while True:
            status = self.get_process_status(pid)
            ts = time.time()
            timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            self.save_to_log(status,timestamp)
            time.sleep(interval)

    def __init__(self, pname):
        self.pname = pname