import socket
import json


class Client:

    def __init__(self,host:str="localhost",port:int=5000):
        """Initialize a new client object"""
        self.SERVERADDRESS= host # Address of the server
        self.PORT=port
        self.FORMAT="utf-8"
        self.ADDR=(self.SERVERADDRESS,self.PORT) 
        self.ClientSocket=None
        self.dataReceived=None


    def start(self):
        """Starts the client"""

        self.ClientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ClientSocket.connect(self.ADDR) # Client Address


    def sendMessage(self,message):
        """Sends a message to the server"""
        encodedMessage=json.dumps(message).encode(self.FORMAT) # Converts a string into a bytes object
        self.ClientSocket.sendall(encodedMessage)
 


    def receiveMessage(self):
        """Recebe mensagens do servidor"""
        connected=True
        while connected:
            try:
        
                data = self.ClientSocket.recv(1024)#.decode('utf-8')
                data=json.loads(data)
                if data==None:
                    print("Nao ha dados recebidos do servidor.")
                    break
                else:
                    #self.dataReceived=data
                    return data
                #connected=False

            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    client=Client()
    client.start()