from gestorBD import GestorBaseDados
nomeBaseDados="feng_live.db"

class Professor:
    
    def __init__(self,id:str="",matricula:str="",nome:str="",senha:str="",tipo:str="professor",curso:str=None):
        self.id=id
        self.matricula=matricula
        self.nome=nome
        self.senha=senha
        self.tipo=tipo
        self.curso=curso


    def autenticarProfessor(self):
        """Verifica se o usuario esta na base de dados e o autentica no sistema"""
        gestorBD= GestorBaseDados(nomeBaseDados)
        comandoSql= "SELECT * FROM usuarios WHERE matricula = ? and senha=?"
        resultado=gestorBD.consultarBD(comandoSql,(self.matricula,self.senha))
        
        print(resultado)
        #print("Achei")
        if resultado:
            for professor in resultado:  
                self.id=professor[0]
                self.nome=professor[2]
            return self
        else:
            return None



   
    def lancar_nota(self, aluno_matricula, disciplina_codigo, notas, semestre, ano):
        """Lança nota para um aluno"""
        # Busca aluno
        aluno = self.buscar(aluno_matricula)
        if not aluno:
            return None, "Aluno não encontrado"
        
        # Busca disciplina
        disciplina = self.execute_query(
            "SELECT id FROM disciplinas WHERE codigo = ?",
            (disciplina_codigo,)
        )
        if not disciplina:
            return None, "Disciplina não encontrada"
        
        disciplina_id = disciplina[0]['id']
        
        # Calcula nota final (média)
        nota1, nota2, nota3 = notas
        nota_final = (nota1 + nota2 + nota3) / 3
        
        try:
            # Insere ou atualiza nota
            self.execute_query('''
                INSERT INTO notas 
                (aluno_id, disciplina_id, nota1, nota2, nota3, nota_final, semestre, ano)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(aluno_id, disciplina_id, semestre, ano) 
                DO UPDATE SET 
                    nota1 = excluded.nota1,
                    nota2 = excluded.nota2,
                    nota3 = excluded.nota3,
                    nota_final = excluded.nota_final,
                    updated_at = CURRENT_TIMESTAMP
            ''', (aluno['id'], disciplina_id, nota1, nota2, nota3, nota_final, semestre, ano))
            
            # Cria notificação para o aluno
            self.create_notificacao(
                aluno['id'],
                f"📢 Nova nota lançada em {disciplina_codigo}! "
                f"Média: {nota_final:.1f} (Notas: {nota1}, {nota2}, {nota3})"
            )
            
            return True, "Nota lançada com sucesso!"
            
        except Exception as e:
            return None, f"Erro ao lançar nota: {str(e)}"   




pf =Professor(matricula="P001",senha="123456")
professor=pf.autenticarProfessor()