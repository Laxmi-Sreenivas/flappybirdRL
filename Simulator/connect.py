'''
- Python Doesn't have a Blocking Send 
- Wrapper Class which Implements Blocking Send
'''
class Socket:
    def __init__(self,socket,address):
        #Constants
        self.BUFFER_SIZE = 1024
        self.ENCODING = 'utf-8'

        #Wraps
        self.socket = socket 
        self.address = address

    #Blocking Send
    def sendall(self,data):
        self.socket.sendall(data.encode(self.ENCODING)) #Send Data
        self.socket.recv(self.BUFFER_SIZE).decode(self.ENCODING) #Receiving ACK
    
    #Blocking Recv
    def recv(self):
        data = self.socket.recv(self.BUFFER_SIZE).decode(self.ENCODING) #Receiving Data
        self.socket.sendall("ACK".encode(self.ENCODING)) #Sending Ack
        return data
    
    #Overloading Close
    def close(self):
        self.socket.close()

    #For Printing Purposes
    def __str__(self) -> str:
        return f'Client{self.address}'


    

    
    
