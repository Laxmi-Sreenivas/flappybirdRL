'''
- Interpret the Messages of Clients
- Message Type : 
    - Chnage Environment Type
    - Exit Simulation
    - Update Existing Environment
- Passes down Necessary Info to Simulator
'''
from simulator import Simulator

#Constants
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

class Manager:
    def __init__(self,client,address):
        self.__client = client #Client Instance
        self.__address = address #Client Address

    def __call__(self): #Called by Server
        level,flag = 0,True

        try :
            while flag: #Level Loop
                info = self.__client.recv(BUFFER_SIZE).decode(ENCODING).split(',')
                print(f'Client{self.__address} Executing Level-{level} with {info}')

                #Environment Creation & Simulation
                environment = Simulator(info)
                flag = self.__simuationLoop(environment)
                    
                #Update Level
                level += 1

        except Exception as e :
            print(f'Bad request from client{self.__address}: {e}')

        finally: 
            self.__client.close()
            print(f'Connection with client{self.__address} closed')
        

    def __simulationLoop(self,environment):
        while True : 
            actionType = self.__client.recv(BUFFER_SIZE).decode(ENCODING)

            if actionType == "Continue":
                action = self.__client.recv(BUFFER_SIZE).decode(ENCODING) #Fetch Action From Client
                state = environment.update(action) #Update State
                self.__client.send(state.encode(ENCODING)) #Send Back the New State Info to Client
            
            elif actionType == "Exit" : #Exit the Level Loop 
                return False 
            
            elif actionType == "LvlUp": #Exit Current Simulation & Enter New Level
                return True