'''
- Starts the Simulation Server
- Waits for Incoming Connections at port 5000
- When a connection comes in, a Child process is spawned
- Child process handles the simulation & relaying information
'''
import socket 
from multiprocessing import Process
from manager import Manager

class Server:
    def __init__(self,host='127.0.0.1',port=5000,backlog=5):
        self.__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #IPV4 ,TCP socket
        self.__socket.bind((host,port)) #Binding Socket
        self.__socket.listen(backlog) #Queue Size
        print(f'Server Listening At Port : {port}')

    def run(self):
        try :
            while True: #Parent Process Acceptin Conenctions
                client,address = self.__socket.accept()
                print(f'Connection From {address} Accepted')
                client_process = Process(target=Manager(client,address)) #Child Process
                client_process.start() #Calls Manager Instance

        except KeyboardInterrupt:
            print('Server Shutting Down')

        finally :
            self.__socket.close()


if  __name__ ==  "__main__":
    server = Server()
    server.run() 