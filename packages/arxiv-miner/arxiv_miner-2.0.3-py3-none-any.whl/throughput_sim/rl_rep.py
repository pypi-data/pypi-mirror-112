import sys
import os
import signal
import time
import multiprocessing  
sys.path.insert(0, os.path.join(os.path.abspath(__file__), "throughput_sim"))
from .structures import *
from .data_workers import ClientThread
from .datasource import get_tcp_server


class Agent:
    def __init__(self):
        pass

    def act(self):
        pass
    
STATES = [
    'SLEEP_STATE'
    'SUCCESS_STATE',
    'FAILURE_STATE',
    'ERROR_STATE'
]

class STATE_SPACE:
    @staticmethod
    def get_onehot_state(state_name):
        if state_name not in STATES:
            raise Exception("%s State Not Present"%state_name)
        oh_vec = [0 for i in range(len(STATES))]
        get_onehot_state = STATES.index(state_name)
        return get_onehot_state

class State:
    number_of_timesteps:None
    last_n_state_ocs = [] # Array of last N ONEHOT STATE VEC
    wait_time:None


class Action:
    def __init__(self):
        self.name = self.__class__.__name__

    def __call__(self):
        raise NotImplementedError()


class Sleep(Action):
    def __call__(self,sleep_time):
        time.sleep(sleep_time)

class MultiAgentWorkers(multiprocessing.Process):
    def __init__(self,host,port,num_workers=100):
        super().__init__()
        
        
    def create_clients(self):
        pass



class ServerProcess(multiprocessing.Process):
    def __init__(self,HOST="localhost", PORT = 9999):
        super().__init__()
        self.server = get_tcp_server(HOST,PORT)

    def shutdown(self):
        self.server.shutdown()

    def run(self):
        self.server.serve_forever()
        

class Environment:
    def __init__(self,episode_length = 100,HOST="localhost", PORT = 9999,  ):

        self.process_manager = multiprocessing.Manager()
        self.exit = multiprocessing.Event()
        self.episode_length = episode_length
        self.server_host = HOST
        self.server_port = PORT
        signal(signal.SIGINT, self.shutdown)
        self.server_process = ServerProcess(HOST=self.server_host,PORT=self.server_port)



    def shutdown(self):
        self.server_process.shutdown()


    def step(self):
        pass