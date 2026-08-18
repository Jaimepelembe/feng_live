import sqlite3
from  pathlib import Path

#Organize the directories
BASE_DIRECTORY=Path(__file__).resolve().parent
BASE_DIRECTORY=BASE_DIRECTORY
print(f"Directorio {BASE_DIRECTORY}")



class GestorBaseDados:

    def __init__(self,nomeBD:str):
        self.nomeBD=nomeBD
        self.conexao=None
        self.inicializarTabelas()
        



    def conectarBaseDados(self):
        """Cria a conexao com a base de dados. Caso a BD nao exista cria uma nova."""
        self.conexao=sqlite3.connect(BASE_DIRECTORY/self.nomeBD)


    def executarComandoSql(self,comandoSql:str,parameters=()) ->bool:
        """Executa um comando Sql. Retorna True se alguma linha foi afectada pela operacao e False caso contrario"""
        try:
            if self.conexao == None:
                self.conectarBaseDados()

            cursor=self.conexao.cursor() # Utilizamos o cursor para executar comandos sql
            cursor.execute(comandoSql,parameters)

        except TypeError as e:
            print(f"Type Error: {e}")

        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")

        except Exception as e:
                    print(f"Error: {e}")

        else:
            self.conexao.commit() # Salva as alteracoes na BD

            linhasAfectadas=cursor.rowcount # Numero de linhas afectadas pera operacao
            if linhasAfectadas>0:
                    return True  # O comando foi executado com sucesso
            else:
                    return False 

        finally:
            self.conexao.close()
            self.conexao=None
        

    def criarTabelaUsuarios(self):
        """Cria a tabela usuarios""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
       CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('aluno', 'professor', 'coordenador')),
                curso TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """

        return self.executarComandoSql(comandoSql)
    
    def criarTabelaDisciplinas(self):
        """Cria a tabela disciplinas""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            professor_id INTEGER,
            creditos INTEGER DEFAULT 4,
            FOREIGN KEY (professor_id) REFERENCES usuarios(id)
        )
            """

        return self.executarComandoSql(comandoSql)
    
    
    def criarTabelaNotas(self):
            """Cria a tabela notas""" """Cria uma tabela na BD caso ela nao exista."""
            comandoSql="""
                 CREATE TABLE IF NOT EXISTS notas (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       aluno_id INTEGER NOT NULL,
                       disciplina_id INTEGER NOT NULL,
                       nota1 REAL,
                       nota2 REAL,
                       nota3 REAL,
                       nota_final REAL,
                       frequencia REAL DEFAULT 0,
                       semestre TEXT NOT NULL,
                       ano INTEGER NOT NULL,
                       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY (aluno_id) REFERENCES usuarios(id),
                       FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
                       UNIQUE(aluno_id, disciplina_id, semestre, ano)
                   )
                """
    
            return self.executarComandoSql(comandoSql)
        
        
    def criarTabelaNotificacoes(self):
            """Cria a tabela notificacoes""" """Cria uma tabela na BD caso ela nao exista."""
            comandoSql="""
            CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            lida INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
        )
            """
    
            return self.executarComandoSql(comandoSql)
        
        
 

    def inserirLinha(self,comandoSql:str,parametros:tuple=()):
        """Insere uma linha em uma determinada tabela da base de dados"""
        #Exemplo: INSERT INTO nome_tabela colunas VALUES {values}
        return self.executarComandoSql(comandoSql,parametros)
       
         
         
    def inserirVariasLinhas(self,comandoSql:str,parametros:list[tuple]=[]):
        """Executa um comando Sql. Retorna True se alguma linha foi afectada pela operacao e False caso contrario"""
       
        try:
            if self.conexao == None:
                self.conectarBaseDados()

            cursor=self.conexao.cursor() # Utilizamos o cursor para executar comandos sql
            cursor.executemany(comandoSql,parametros)
            
        except TypeError as e:
            print(f"Type Error: {e}")

        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")

        except Exception as e:
            print(f"Error: {e}")        
        else:
            self.conexao.commit() # Salva as alteracoes na BD

    



    def consultarBD(self,comandoSql:str,parametros:tuple=())-> list[tuple] | None:
        """Executa uma consulta na base de dados."""
        try:
            if self.conexao == None:
                self.conectarBaseDados()

            cursor=self.conexao.cursor() # Utilizamos o cursor para executar comandos sql
            cursor.execute(comandoSql,parametros)
            
        except TypeError as e:
            print(f"Type Error: {e}")

        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")

        except Exception as e:
                    print(f"Error: {e}")

        else:
            resultado=cursor.fetchall()
            return resultado
      
        finally:
            self.conexao.close()
            self.conexao=None


    def inserirDadosDeExemplo(self):
        """Insere varios dados de exemplo na base de dados, caso ela esteja vazia."""
        try:
            if self.conexao == None:
                    self.conectarBaseDados()

        
            cursor=self.conexao.cursor() # Utilizamos o cursor para executar comandos sql
            
            #Verificar se existem estudantes na base de dados
            comandoSql= "SELECT COUNT(*) FROM usuarios"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0] > 0:
                pass
            else:
                usuarios = [
                        ('2024001', 'Alexandre Ntema', '123456', 'aluno', 'Engenharia Informática'),
                        ('2024002', 'Henrinques Almeida', '123456', 'aluno', 'Engenharia Civil'),
                        ('2024003', 'Afonso Adolfo', '123456', 'aluno', 'Engenharia Elétrica'),
                        ('2024004', 'Ana Oliveira', '123456', 'aluno', 'Engenharia Mecânica'),
                        ('2024005', 'Carlos Mendes', '123456', 'aluno', 'Engenharia Informática'),
                        ('P001', 'Prof. Jaime', '123456', 'professor', None),
                        ('P002', 'Prof. Ivone', '123456', 'professor', None),
                    ]
                comandoSql= "INSERT INTO usuarios (matricula, nome, senha, tipo, curso) VALUES (?, ?, ?, ?, ?)"
                
                self.inserirVariasLinhas(comandoSql,usuarios)
               
                
            #Verificar se existem disciplinas na base de dados
            comandoSql= "SELECT COUNT(*) FROM disciplinas"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0] > 0:
                pass
            else:
                disciplinas = [
                ('INF101', 'Programação I', 6, 4),
                ('MAT101', 'Cálculo I', 6, 4),
                ('FIS101', 'Física I', 7, 4),
                ('INF201', 'Programação II', 6, 4),
                ('MAT201', 'Cálculo II', 7, 4),]
                
                comandoSql= "INSERT INTO disciplinas (codigo, nome, professor_id, creditos) VALUES (?, ?, ?, ?)"
                
                self.inserirVariasLinhas(comandoSql,disciplinas)
         
            
            #Verificar se existem notas na base de dados
            comandoSql= "SELECT COUNT(*) FROM notas"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0]>0:
                pass
            else:
                notas = [
                (1, 1, 14, 16, 15, 15.0, 85, '2024.1', 2024),
                (1, 2, 10, 8, 12, 10.0, 75, '2024.1', 2024),
                (2, 1, 12, 10, 11, 11.0, 90, '2024.1', 2024),
                (2, 2, 15, 14, 16, 15.0, 85, '2024.1', 2024),
                (3, 2, 13, 12, 14, 13.0, 80, '2024.1', 2024),]   
                #print("Dados de exemplo inseridos com sucesso!") 
                
                comandoSql= """INSERT INTO notas (aluno_id, disciplina_id, nota1, nota2, nota3, nota_final, frequencia, semestre, ano) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""  
                self.inserirVariasLinhas(comandoSql,notas)
            
           # print("Dados de exemplo inseridos com sucesso!")
            
    
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
        
    
    def inicializarTabelas(self):
        """Inicializa a base de dados criando as tabelas e preencheendo os dados de exemplo caso ela esteja vazia."""
        
        self.criarTabelaUsuarios()
        self.criarTabelaDisciplinas()
        self.criarTabelaNotas()
        self.criarTabelaNotificacoes()
        self.inserirDadosDeExemplo()
        
        
        
           
    def ActualizarLinha(self,comandoSql,parametros:tuple=()):
        """Actualiza uma linha de uma determinada tabela"""

        """Exemplo de comando sql: UPDATE nome_tabela set atributo=? where condicao=?"""
        return self.executarComandoSql(comandoSql,parametros)


    def DeletarLinha(self,comandoSql,parametros:tuple=()):
        """Deleta uma linha de uma determinada tabela"""

        """Exemplo de comando sql: DELETE FROM nome_tabela WHERE condicao=?"""
        return self.executarComandoSql(comandoSql,parametros)


