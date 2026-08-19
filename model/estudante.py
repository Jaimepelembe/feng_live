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
        comandoSql= "SELECT * FROM estudante WHERE email = ? and numero_estudante=?"
        resultado=gestorBD.consultarBD(comandoSql,(self.email,self.numero_estudante))
        
       # print(resultado)
        #print("Achei")
        if resultado:
            for estudante in resultado:
        
                self.id=estudante[0]
                self.nome=estudante[2]
                self.id_curso=estudante[4]
            return self
        else:
            return None
  
    def buscarNotasAluno(self,id_estudante):
        """Busca todas as notas de um aluno com base no seu ID"""
        gestorBD= GestorBaseDados(nomeBaseDados)
        comandoSql=    f"""
                        SELECT 
                    cadeira.nome AS disciplina,
                    notas.nota1,
                    notas.nota2,
                    notas.nota3,
                    ROUND((notas.nota1 + notas.nota2 + notas.nota3) / 3.0, 2) AS media,
                    notas.frequencia AS frequencia,  
                    cadeira.semestre
                FROM 
                    estudante
                    INNER JOIN inscricao ON estudante.id_estudante = inscricao.id_estudante
                    INNER JOIN cadeira ON inscricao.id_cadeira = cadeira.id_cadeira
                    INNER JOIN notas ON notas.id_estudante = estudante.id_estudante 
                                    AND notas.id_cadeira = cadeira.id_cadeira
                WHERE 
                    estudante.id_estudante = ?;   -- substitua o 1 pelo ID do estudante desejado
                        """
        
        notas= gestorBD.consultarBD(comandoSql,(id_estudante,))
        print("Notas da BD {notas}")
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