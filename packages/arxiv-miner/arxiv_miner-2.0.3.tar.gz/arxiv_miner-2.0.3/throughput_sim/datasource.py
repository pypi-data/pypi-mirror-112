import socketserver
from expiringdict import ExpiringDict
import random
import math
import json
import time
import sys
from functools import partialmethod
import os
sys.path.insert(0, os.path.join(os.path.abspath(__file__), "throughput_sim"))
from .structures import *

MAX_CONNS = 100
CONN_DEATH_TTL = 30
MAX_REQ_TIMEOUT = 10


class ERRORCODES:
    
    SOCKET_OVERLOAD = '[ERROR][SOCKET_OVERLOAD]'



class RESPONSECODES:
    FAILURE = '[RESPONSE][FAILURE]'
    SUCCESS = '[RESPONSE][SUCCESS]'


class DecayLimiter:
    """ DecayLimiter

    Adaptive DecayLimiter based on Cos Function going from 0 -> pi split by conn_limt
    return goes from 1->0 based on 0->pi
    """
    
    def __init__(self,max_conn_lim = MAX_CONNS):
        self.max_conn_lim = max_conn_lim
    
    def _adapted_flux(self,curr_conn):    
        if self.max_conn_lim <= curr_conn:
            return 0
        return math.cos(math.pi*(curr_conn/self.max_conn_lim)/2)

    def __call__(self,num_conns):
        return self._adapted_flux(num_conns)


class GrowthLimiter:
    """ GrowthLimiter

    Adaptive GrowthLimiter based on sin Function going from 0 -> pi split by conn_limt
    return goes from 0->1 based on 0->pi
    """
    
    def __init__(self,max_conn_lim = MAX_CONNS):
        self.max_conn_lim = max_conn_lim
    
    def _adapted_flux(self,curr_conn):    
        if self.max_conn_lim <= curr_conn:
            return 0
        return math.sin(math.pi*(curr_conn/self.max_conn_lim)/2)

    def __call__(self,num_conns):
        return self._adapted_flux(num_conns)


    
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def __init__(self,request, client_address, server,max_conns=MAX_CONNS,max_request_timeout=MAX_REQ_TIMEOUT,inmemory_connection_ttl=CONN_DEATH_TTL):
        self.rate_limiter = DecayLimiter(max_conn_lim=max_conns)
        self.current_conn_set = ExpiringDict(max_conns,max_age_seconds=CONN_DEATH_TTL)    
        self.timeout_limiter = DecayLimiter(max_conn_lim=max_request_timeout)
        socketserver.BaseRequestHandler.__init__(self,request, client_address, server)    
        

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # todo : mark exact identity
        self.current_conn_set[self.client_address] = 1
        print("started ",self.client_address,len(self.current_conn_set))
        
        positive_resp_prob = self.rate_limiter(len(self.current_conn_set))
        if positive_resp_prob == 0:
            status = Status(message=ERRORCODES.SOCKET_OVERLOAD,wait_time=0)
            self.request.sendall(bytes(status.json_string,'utf-8'))
            return 

        succ_chance = random.random()
        wait_time = self.timeout_limiter(positive_resp_prob * \
                                self.timeout_limiter.max_conn_lim\
                                ) * self.timeout_limiter.max_conn_lim
        time.sleep(wait_time)
        if  succ_chance <= positive_resp_prob: # this means success
            status = Status(success_bool=True,message=RESPONSECODES.SUCCESS,wait_time=wait_time)
        else:
            status = Status(message=RESPONSECODES.FAILURE,wait_time=wait_time)

        # just send back the same data, but upper-cased
        self.request.sendall(bytes(status.json_string,'utf-8'))

    def finish(self):
        # todo : remove exact identity
        if self.client_address in self.current_conn_set:
            del self.current_conn_set[self.client_address]
            print("Finished ",self.client_address,len(self.current_conn_set))


def partialclass(cls, *args, **kwds):

    class NewCls(cls):
        __init__ = partialmethod(cls.__init__, *args, **kwds)

    return NewCls  

def get_tcp_server(host,port,max_conns=MAX_CONNS,max_request_timeout=MAX_REQ_TIMEOUT,inmemory_connection_ttl=CONN_DEATH_TTL):
    handler = partialclass(MyTCPHandler)
    server = socketserver.ThreadingTCPServer((host, port), handler) 
    return server

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = get_tcp_server(HOST,PORT)
    server.serve_forever()