'''
- Interpret the Messages of Clients
- Message Type : 
    - Chnage Environment Type
    - Exit Simulation
    - Update Existing Environment
- Passes down Necessary Info to Simulator
'''
import Simulator
from connect import Socket
from Simulator.simulator import Simulator
import json

class Manager:
    def __init__(self,client,address):
        self.__client = Socket(client,address) #wrapper Socket Instance
        
    def __call__(self): #Called by Server
        level,flag = 0,True

        try :
            while flag: #Level Loop
                info = self.__client.recv()
                print(f'{self.__client} Executing Level-{level} with {info}')

                #Environment Creation & Simulation
                #Converting Info String to Json Before Sending
                environment = Simulator(json.loads(info),f'{self.__client}')
                flag = self.__simulationLoop(environment)

                del environment
                    
                #Update Level
                level += 1

        except Exception as e :
            print(f'Bad request from {self.__client}: {e}')

        finally: 
            self.__client.close()
            print(f'Connection with {self.__client} closed')
        

    def __simulationLoop(self,environment):
        while True : 
            actionType = self.__client.recv() #Decide Move

            if actionType == "Continue":
                action = self.__client.recv() #Fetch Action From Client
                state = environment.update(action) #Update State
                self.__client.sendall(json.dumps(state)) #Send Back the New State Info [String] to Client
            
            elif actionType == "Exit" : #Exit the Level Loop 
                return False 
            
            elif actionType == "LvlUp": #Exit Current Simulation & Enter New Level
                return True