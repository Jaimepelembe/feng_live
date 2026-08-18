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
        
        
    def inserirDadosDeExemplo():
        pass



    def inserirLinha(self,comandoSql:str,parametros:tuple=()):
        """Insere uma linha em uma determinada tabela da base de dados"""
        #Exemplo: INSERT INTO nome_tabela colunas VALUES {values}
        return self.executarComandoSql(comandoSql,parametros)
       
         
         
    def inserirVariasLinhas(comandoSql:str,parametros:list[tuple]=[]):
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
         
         
    def ActualizarLinha(self,comandoSql,parametros:tuple=()):
        """Actualiza uma linha de uma determinada tabela"""

        """Exemplo de comando sql: UPDATE nome_tabela set atributo=? where condicao=?"""
        return self.executarComandoSql(comandoSql,parametros)


    def DeletarLinha(self,comandoSql,parametros:tuple=()):
        """Deleta uma linha de uma determinada tabela"""

        """Exemplo de comando sql: DELETE FROM nome_tabela WHERE condicao=?"""
        return self.executarComandoSql(comandoSql,parametros)

