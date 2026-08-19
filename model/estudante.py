from gestorBD import GestorBaseDados
nomeBaseDados="feng_live.db"

class Estudante:
    
    def __init__(self,id:str="",numero_estudante:str="",nome:str="",email:str="",id_curso:int=""):
        self.id_estudante=id
        self.numero_estudante=numero_estudante
        self.nome=nome
        self.email=email
        self.id_curso=id_curso


    
    def autenticarEstudande(self):
        """Verifica se o usuario esta na base de dados e o autentica no sistema"""
        gestorBD= GestorBaseDados(nomeBaseDados)
        comandoSql= "SELECT * FROM usuarios WHERE email = ? and numero_estudante=?"
        resultado=gestorBD.consultarBD(comandoSql,(self.email,self.numero_estudante))
        
       # print(resultado)
        #print("Achei")
        if resultado:
            for estudante in resultado:
        
                self.id=estudante[0]
                self.nome=estudante[2]
                self.curso=estudante[5]
            return self
        else:
            return None
  
    def buscarNotasAluno(self):
        """Busca todas as notas de um aluno com base no seu ID"""
        gestorBD= GestorBaseDados(nomeBaseDados)
        comandoSql=    """
            SELECT d.codigo, d.nome, n.nota1, n.nota2, n.nota3, n.nota_final, n.frequencia, n.semestre, n.ano
            FROM notas n  JOIN disciplinas d ON n.disciplina_id = d.id
            WHERE n.aluno_id = ?
            ORDER BY n.ano DESC, n.semestre DESC
        """
        
        notas= gestorBD.consultarBD(comandoSql,(self.id,))
        print(notas)
        if notas:
            return notas
        else:
            return None
        
    def buscarMediaAluno(self):
        """Calcula média geral do aluno. Faz a busca usando o Id do aluno"""
        gestorBD= GestorBaseDados(nomeBaseDados)
        comandoSql="""
         SELECT AVG(nota_final) as media
            FROM notas
            WHERE aluno_id = ?
        """
        
        media=gestorBD.consultarBD(comandoSql,(self.id,))
        if media:
            media=media[0][0]
            #print(f"Media: {media}")
            return media
        else:
            return 0
        
        
    def buscarRanking(self):
        """Retorna ranking dos alunos"""
        
        gestorBD= GestorBaseDados(nomeBaseDados)
        comandoSql="""
            SELECT u.nome, u.matricula, AVG(n.nota_final) as media
            FROM usuarios u
            JOIN notas n ON u.id = n.aluno_id
            WHERE u.tipo = 'aluno'
            GROUP BY u.id
            ORDER BY media DESC
        """
        
        ranking=gestorBD.consultarBD(comandoSql)
        print(ranking)
        if ranking:
            return ranking
        else:
            return None
    
   
"""
est=Estudante(matricula="2024001",senha="123456")
estudante=est.autenticarEstudande()
estudante.buscarRanking()
#estudante.buscarMediaAluno()
"""


"""
estudante=est.autenticarEstudande() 
print(estudante.curso)    
   #"""         