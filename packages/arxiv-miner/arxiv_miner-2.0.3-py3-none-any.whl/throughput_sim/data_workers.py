import threading
import socket
import sys
import uuid
import json
import random 
import os

import time
sys.path.insert(0, os.path.join(os.path.abspath(__file__), "throughput_sim"))
from .structures import *


class ClientThread(threading.Thread):
    def __init__(self,host,port):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.identity = uuid.uuid1()
        self.status = None
        self.running = False

    def success(self):
        if self.status is None:
            return False
        return self.status.success_bool 

    def run(self):
        self.running = True
        identity_str = json.dumps({
            'identity':str(self.identity)
        })
        try:
            self.sock.connect((self.host,self.port))
            self.sock.sendall(bytes(identity_str, "utf-8"))
            received = str(self.sock.recv(1024), "utf-8")
            self.status = Status(**json.loads(received))
        except:
            return

if  __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("give probability as arg")
    compare_prob = float(sys.argv[1])
    max_threads = int(sys.argv[2])
    HOST, PORT = "localhost", 9999 
    threads = []
    start_time = time.time()
    for i in range(max_threads):
        t = ClientThread(host=HOST,port=PORT)
        prob = random.random()
        if  prob < compare_prob:
            time.sleep(0.2)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    
    succ = 0
    end_time = time.time()
    for t in threads:
        if t.status:
            if t.status.success_bool:
                succ+=1
    
    print("DONE WORKING Covered : %d From %d In Time %d Seconds"%(succ,len(threads),end_time-start_time))