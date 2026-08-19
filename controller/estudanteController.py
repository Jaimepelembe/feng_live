from controller.client import Client
import threading

class EstudanteController(Client):

    def __init__(self,nome:str):
        """Initialize a new CTA Object"""

        super().__init__() # Initialize the client
        self.nome=nome

    def autenticarEstudande(self,email:str,numero_estudante:int):
        
        
        mensagem={}
        mensagem["tipo_usuario"]="estudante"
        mensagem["operacao"]="autenticar_estudante"
        mensagem["valor"]=(email,numero_estudante)
        #mensagem["sql"]=comandoSql
        print(mensagem)
        self.sendMessage(mensagem)
        dados=self.receiveMessage()
        
        return dados # Retorna os dados enviados pelo servidor


    def buscarNotasAluno(self,id_aluno):
        
        pass




    def removerPessoa(self):

        comandoSql="DELETE FROM usuarios WHERE id=?"
        Id=int(input("Digite o ID da pessoa: "))
        mensagem={}
        mensagem["type"]="remove_usuario"
        mensagem["value"]=(Id,)
        mensagem["sql"]=comandoSql
        print(mensagem)
        self.sendMessage(mensagem)


    def buscarTodos(self)-> list:
        """Retorna a lista de todos os usuarios do sistema"""
        comandoSql="SELECT * FROM usuarios"
        mensagem={}
        mensagem["type"]="buscar_todos"
        mensagem["sql"]=comandoSql
        print(mensagem)
        self.sendMessage(mensagem)   
        data=self.receiveMessage()
       # if self.dataReceived ==None:
        #    self.buscarTodos()
       # data=self.dataReceived  
        
        print(f"Dados recebido do servidor:\n{data}")
        """
        for dado in data:
            print(f"ID: {dado[0]}")        
            print(f"Nome: {dado[1]}")        
            print(f"Email: {dado[2]}")        
        """
        return data




