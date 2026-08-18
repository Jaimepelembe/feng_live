import socket
import threading
import json
from gestorBD import GestorBaseDados
nomeBaseDados="pessoal.db"

class Server:

    def __init__(self,host:str="localhost",port:int=5000,format:str="utf-8"):
        """Initialize a server Object"""

        self.HOST=host  # socket.gethostbyname(socket.gethostname()) this gets the current host ip address by his name
        self.PORT=port 
        self.FORMAT=format
        self.serverSocket=None
        self.gestorBD=GestorBaseDados(nomeBaseDados)

    def start(self):
        """Starts the server."""

        self.serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # IPv4 and TCP
        ADDR= (self.HOST,self.PORT) # Address
        self.serverSocket.bind(ADDR)

        print(f"[Starting] The server is running in {self.HOST}:{self.PORT}")
        print("Wainting for connection...")

        self.serverSocket.listen() # Start listening for new connections

        while True:
            connection,addr=self.serverSocket.accept() # Returns the connection and the address of the host(host ip and port)
            thread=threading.Thread(target=self.handleClient, args=(connection,addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}") # print the number of clients connected

    def handleClient(self,connection,addr:tuple):
        """Handle the individual connection between the client and the server"""
        
        print(F"[NEW CONNECTION] {addr} connected.")
        try:
            connected=True
            while connected:
                message=connection.recv(1024)#decode(self.FORMAT) #buffer size is 1024 bits
                message=json.loads(message)
                
                if message: # is not None
                    

                    if message == "disconnect":
                        self.closeConnection(connection)
                        connected=False

                    print(f"{addr}: {message}")

                    operacao=message.get("type")
                    messageToSend=""
                    
                    if operacao=="add_usuario":
                        comandoSql=message["sql"]
                        usuario=message["value"]
                        resultado=self.gestorBD.inserirLinha(comandoSql,usuario)
                        if resultado== True:
                            messageToSend="Usuario adicionado com sucesso"

                    elif operacao=="remove_usuario":
                        comandoSql=message["sql"]
                        valor=message["value"]
                        resultado=self.gestorBD.DeletarLinha(comandoSql,valor)
                        if resultado== True:
                            messageToSend="Usuario removido com sucesso"

                    elif operacao =="buscar_todos":
                        comandoSql=message["sql"]
                        resultado=self.gestorBD.consultarBD(comandoSql)
                        #print(f"Resultado da consulta: {resultado}")
                        if resultado:
                                messageToSend=resultado

                        else:
                            messageToSend="A base de dados nao tem nenhum registo."

                    #Send Message to the client
                    messageToSend=json.dumps(messageToSend).encode(self.FORMAT)# Converts the object into a string of bytes .encode(self.FORMAT)
                    connection.sendall(messageToSend)


        except AttributeError as e:
            print(f"Error:{e}")

        except Exception as e:
                    print(f"Error:{e}")


    def closeConnection(self,connection):
        """"Closes the connection between the server and the user"""
        connection.close()


if __name__ == '__main__':
    server = Server()
    server.start()
    #print(server.somar(3,4))