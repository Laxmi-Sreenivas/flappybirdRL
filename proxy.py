'''
- Jupyter Notebooks Don't Support pyGame
- Acts as a Proxy Simulator
- Notebook Talks to Proxy Simulator
- Which Interacts with The Server where Simulation is Done
'''
import socket
from connect import Socket
import json

class Proxy:
    def __init__(self,level,server_ip='127.0.0.1',server_port=5000):
        #Connecting to Server
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((server_ip,server_port))

        #Extracting Host Info
        hostname = socket.gethostname()
        client_ip = socket.gethostbyname(hostname)
        
        #For Blocking Sends & Recvs
        self.client = Socket(client_socket,client_ip)

        #Initial Level
        self.client.sendall(json.dumps(level))

    def levelUp(self,level):
        #Sending Level Info The Simulator
        #Need to be Called When When Level Start
        self.client.sendall("LvlUp")
        self.client.sendall(json.dumps(level))

    def update(self,action):
        self.client.sendall("Continue")
        self.client.sendall(action) #Action Send
        state = self.client.recv() #State Received
        return json.loads(state) #Converting String to Json

    def exit(self):
        #Closing Connection
        self.client.sendall("Exit")
        self.client.close()
