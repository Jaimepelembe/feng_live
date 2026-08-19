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
        
    
    
    def criarTabelaCurso(self):
            """Cria a tabela curso""" """Cria uma tabela na BD caso ela nao exista."""
            comandoSql="""
           CREATE TABLE IF NOT EXISTS curso (
                    id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL
                )
                """
    
            return self.executarComandoSql(comandoSql)    
    
    
    def criarTabelaEstudante(self):
        """Cria a tabela Estudante""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
       CREATE TABLE IF NOT EXISTS estudante (
                id_estudante INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_estudante TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                email  TEXT UNIQUE NOT NULL,
                FOREIGN KEY (id_curso) REFERENCES curso(id_curso)
            )
            """

        return self.executarComandoSql(comandoSql)
    

    def criarTabelaCadeira(self):
        """Cria a tabela Cadeira""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
       CREATE TABLE IF NOT EXISTS cadeira (
                id_cadeira INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                semestre INTEGER NOT NULL, 
                FOREIGN KEY (id_curso) REFERENCES curso(id_curso)
            )
            """

        return self.executarComandoSql(comandoSql)
    

    def criarTabelaInscricao(self):
        """Cria a tabela inscricao""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
       CREATE TABLE IF NOT EXISTS inscricao (
                id_inscricao INTEGER PRIMARY KEY AUTOINCREMENT,
                semestre INTEGER NOT NULL, 
                data_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado INTEGER NOT NULL,
                FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante),
                FOREIGN KEY (id_cadeira) REFERENCES cadeira(id_cadeira)
               
            )
            """

        return self.executarComandoSql(comandoSql)

    def criarTabelaDocente(self):
        """Cria a tabela Docente""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
       CREATE TABLE IF NOT EXISTS docente (
                id_docente INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_docente INTEGER NOT NULL, 
                nome TEXT NOT NULL,
                email  TEXT UNIQUE NOT NULL      
            )
            """

        return self.executarComandoSql(comandoSql)



    def criarTabelaTurma(self):
        """Cria a tabela turma""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
       CREATE TABLE IF NOT EXISTS turma (
                id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
                horario TEXT NOT NULL, 
                ano_letivo INTEGER NOT NULL,
                FOREIGN KEY (id_cadeira) REFERENCES cadeira(id_cadeira),
                FOREIGN KEY (id_docente) REFERENCES docente(id_docente)
               
            )
            """
            
        return self.executarComandoSql(comandoSql)

    def criarTabelaNotas(self):
        """Cria a tabela Notas""" """Cria uma tabela na BD caso ela nao exista."""
        comandoSql="""
       CREATE TABLE IF NOT EXISTS notas (
                id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
                nota1 REAL, 
                nota2 REAL, 
                nota3 REAL, 
                frequencia REAL DEFAULT 0,
                FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante),
                FOREIGN KEY (id_docente) REFERENCES docente(id_docente),
                FOREIGN KEY (id_cadeira) REFERENCES cadeira(id_cadeira)
               
            )
            """
            
        return self.executarComandoSql(comandoSql)


     
        
    def criarTabelaNotificacoes(self):
            """Cria a tabela notificacoes""" """Cria uma tabela na BD caso ela nao exista."""
            comandoSql="""
            CREATE TABLE IF NOT EXISTS notificacoes (
            id_notificacao INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            lida INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_estudante) REFERENCES estudante(id_estudante)
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

        if self.conexao == None:
                self.conectarBaseDados()

    
        cursor=self.conexao.cursor() # Utilizamos o cursor para executar comandos sql
        
        #Verificar se existem cursos na base de dados
        self.inserirCursos(cursor)
        
        #Verificar se existem disciplinas na base de dados
        self.inserirCadeiras(cursor)
        #self.inserirEstudantes(cursor)
        #self.inserirDocentes(cursor)
        #self.inserirTurmas(cursor)
        #self.inserirInscricoes(cursor)
        #self.inserirNotas(cursor)
            

               
                

         
         


            

            
            
 


                              

 
            
            
                
            
                
       
        
    
    def gerarNotas(self):
        from random import randint
        notas = []
        for estudante_id in range(1, 19):

            if estudante_id <= 6:
                cadeiras_curso = range(1, 7)

            elif estudante_id <= 12:
                cadeiras_curso = range(7, 13)

            else:
                cadeiras_curso = range(13, 19)

            for cadeira_id in cadeiras_curso:

                docente_id = cadeira_id

                nota1 = randint(12,20)
                nota2 = randint(12,20)
                nota3 = randint(12,20)
                frequencia = randint(85,100)

                notas.append(
                    (
                        nota1,
                        nota2,
                        nota3,
                        frequencia,
                        estudante_id,
                        docente_id,
                        cadeira_id
                    )
                )
        return notas

    def inserirCursos(self,cursor):
        
        try:
            #Verificar se existem cursos na base de dados
            comandoSql= "SELECT COUNT(*) FROM curso"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0] > 0:
                pass
            else:
                cursos = [
                 ("Engenharia Informatica",),
                ("Engenharia Electrica",),
                ("Engenharia Electronica",)]
                
                comandoSql= "INSERT INTO curso (nome) VALUES (?)"
                
                self.inserirVariasLinhas(comandoSql,cursos)
                
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
        
    
    def inserirCadeiras(self,cursor):
        
        try:
                
            #Verificar se existem disciplinas na base de dados
            comandoSql= "SELECT COUNT(*) FROM cadeira"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0] > 0:
                pass
            else:
                cadeiras = [
                # Engenharia Informática
                ("Programação II", 2, 1),
                ("Estruturas de Dados", 2, 1),
                ("Base de Dados", 2, 1),
                ("Sistemas Operativos", 2, 1),
                ("Redes de Computadores I", 2, 1),
                ("Matemática Discreta", 2, 1),

                # Engenharia Eléctrica
                ("Circuitos Eléctricos II", 2, 2),
                ("Electrónica Analógica", 2, 2),
                ("Máquinas Eléctricas I", 2, 2),
                ("Electromagnetismo", 2, 2),
                ("Sistemas Digitais", 2, 2),
                ("Instrumentação Eléctrica", 2, 2),

                # Engenharia Electrónica
                ("Circuitos Electrónicos II", 2, 3),
                ("Microprocessadores", 2, 3),
                ("Electrónica Digital", 2, 3),
                ("Sinais e Sistemas", 2, 3),
                ("Comunicações I", 2, 3),
                ("Sistemas de Controlo", 2, 3)]

                
                comandoSql= "INSERT INTO cadeira (nome, semestre, id_curso) VALUES (?, ?, ?)"          
                self.inserirVariasLinhas(comandoSql,cadeiras)
                
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
    
    
    def inserirEstudantes(self,cursor):
        
        try:
                    
            #Verificar se existem estudantes na base de dados
            comandoSql= "SELECT COUNT(*) FROM estudantes"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0]>0:
                pass
            else:
                estudantes = [
                    # Engenharia Informatica
                    ("202600", "Jaime Fernando", "jaime.fernando@fenglive.com", 1),
                    ("202601", "Carlos Manuel", "carlos.manuel@fenglive.com", 1),
                    ("202602", "Ana Paula", "ana.paula@fenglive.com", 1),
                    ("202603", "Edson Alberto", "edson.alberto@fenglive.com", 1),
                    ("202604", "Marta Isabel", "marta.isabel@fenglive.com", 1),
                    ("202605", "Nelson Antonio", "nelson.antonio@fenglive.com", 1),

                    # Engenharia Electrica
                    ("202606", "Bruno Mateus", "bruno.mateus@fenglive.com", 2),
                    ("202607", "Daniel Jose", "daniel.jose@fenglive.com", 2),
                    ("202608", "Ines Maria", "ines.maria@fenglive.com", 2),
                    ("202609", "Pedro Alberto", "pedro.alberto@fenglive.com", 2),
                    ("202610", "Sofia Manuel", "sofia.manuel@fenglive.com", 2),
                    ("202611", "Antonio Ernesto", "antonio.ernesto@fenglive.com", 2),

                    # Engenharia Electronica
                    ("202612", "Mateus Paulo", "mateus.paulo@fenglive.com", 3),
                    ("202613", "Rui Manuel", "rui.manuel@fenglive.com", 3),
                    ("202614", "Beatriz Alice", "beatriz.alice@fenglive.com", 3),
                    ("202615", "Fernando Luis", "fernando.luis@fenglive.com", 3),
                    ("202616", "Claudia Teresa", "claudia.teresa@fenglive.com", 3),
                    ("202617", "Tomas Antonio", "tomas.antonio@fenglive.com", 3)
                ]
                
                comandoSql= """INSERT INTO estudantes (numero_estudante, nome, email, id_curso) VALUES (?, ?, ?, ?)"""  
                self.inserirVariasLinhas(comandoSql,estudantes)
                
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
    
    
    def inserirDocentes(self,cursor):
        
        try:
                    #Verificar se existem estudantes na base de dados
            comandoSql= "SELECT COUNT(*) FROM docente"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0]>0:
                pass
            else:
                docentes = [
                ("DOC001", "Alberto Joaquim", "alberto.joaquim@fenglive.com"),
                ("DOC002", "Manuel Ernesto", "manuel.ernesto@fenglive.com"),
                ("DOC003", "Carlos Alberto", "carlos.alberto@fenglive.com"),
                ("DOC004", "Paulo Antonio", "paulo.antonio@fenglive.com"),
                ("DOC005", "Fernando Manuel", "fernando.manuel@fenglive.com"),
                ("DOC006", "Joao Carlos", "joao.carlos@fenglive.com"),

                ("DOC007", "Ricardo Jose", "ricardo.jose@fenglive.com"),
                ("DOC008", "Eduardo Paulo", "eduardo.paulo@fenglive.com"),
                ("DOC009", "Armando Luis", "armando.luis@fenglive.com"),
                ("DOC010", "Antonio Manuel", "antonio.manuel@fenglive.com"),
                ("DOC011", "Jose Fernando", "jose.fernando@fenglive.com"),
                ("DOC012", "Miguel Ernesto", "miguel.ernesto@fenglive.com"),

                ("DOC013", "Augusto Pedro", "augusto.pedro@fenglive.com"),
                ("DOC014", "Filipe Antonio", "filipe.antonio@fenglive.com"),
                ("DOC015", "Nelson Manuel", "nelson.manuel@fenglive.com"),
                ("DOC016", "Guilherme Paulo", "guilherme.paulo@fenglive.com"),
                ("DOC017", "Helder Joaquim", "helder.joaquim@fenglive.com"),
                ("DOC018", "Victor Manuel", "victor.manuel@fenglive.com")
            ]
            
                comandoSql= """INSERT INTO docente (numero_docente, nome, email) VALUES (?, ?, ?)"""  
                self.inserirVariasLinhas(comandoSql,docentes)
        
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
    
    
    def inserirTurmas(self,cursor):
        try:
        #Verificar se existem uma turma na base de dados
            comandoSql= "SELECT COUNT(*) FROM turma"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0]>0:
                pass
            else:
                turmas = [
                    # Programacao II
                    ("Laboral", 2026, 1, 1),
                    ("Pos-Laboral", 2026, 1, 1),

                    # Estruturas de Dados
                    ("Laboral", 2026, 2, 2),
                    ("Pos-Laboral", 2026, 2, 2),

                    # Base de Dados
                    ("Laboral", 2026, 3, 3),
                    ("Pos-Laboral", 2026, 3, 3),

                    # Sistemas Operativos
                    ("Laboral", 2026, 4, 4),
                    ("Pos-Laboral", 2026, 4, 4),

                    # Redes de Computadores I
                    ("Laboral", 2026, 5, 5),
                    ("Pos-Laboral", 2026, 5, 5),

                    # Matematica Discreta
                    ("Laboral", 2026, 6, 6),
                    ("Pos-Laboral", 2026, 6, 6),

                    # Circuitos Electricos II
                    ("Laboral", 2026, 7, 7),
                    ("Pos-Laboral", 2026, 7, 7),

                    # Electronica Analogica
                    ("Laboral", 2026, 8, 8),
                    ("Pos-Laboral", 2026, 8, 8),

                    # Maquinas Electricas I
                    ("Laboral", 2026, 9, 9),
                    ("Pos-Laboral", 2026, 9, 9),

                    # Electromagnetismo
                    ("Laboral", 2026, 10, 10),
                    ("Pos-Laboral", 2026, 10, 10),

                    # Sistemas Digitais
                    ("Laboral", 2026, 11, 11),
                    ("Pos-Laboral", 2026, 11, 11),

                    # Instrumentacao Electrica
                    ("Laboral", 2026, 12, 12),
                    ("Pos-Laboral", 2026, 12, 12),

                    # Circuitos Electronicos II
                    ("Laboral", 2026, 13, 13),
                    ("Pos-Laboral", 2026, 13, 13),

                    # Microprocessadores
                    ("Laboral", 2026, 14, 14),
                    ("Pos-Laboral", 2026, 14, 14),

                    # Electronica Digital
                    ("Laboral", 2026, 15, 15),
                    ("Pos-Laboral", 2026, 15, 15),

                    # Sinais e Sistemas
                    ("Laboral", 2026, 16, 16),
                    ("Pos-Laboral", 2026, 16, 16),

                    # Comunicacoes I
                    ("Laboral", 2026, 17, 17),
                    ("Pos-Laboral", 2026, 17, 17),

                    # Sistemas de Controlo
                    ("Laboral", 2026, 18, 18),
                    ("Pos-Laboral", 2026, 18, 18)
                        ]
                comandoSql= """INSERT INTO turma (horario, ano_letivo, id_cadeira,id_docente) VALUES (?, ?, ?, ?)"""  
                self.inserirVariasLinhas(comandoSql,turmas)
                
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
    
    
    def inserirInscricoes(self,cursor):
        
        try:
            #Verificar se existem inscricoes na base de dados
            comandoSql= "SELECT COUNT(*) FROM inscricao"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0]>0: 
                pass
            else:
                inscricoes = []
                for estudante_id in range(1, 19):

                    if estudante_id <= 6:
                        cadeiras_curso = range(1, 7)

                    elif estudante_id <= 12:
                        cadeiras_curso = range(7, 13)

                    else:
                        cadeiras_curso = range(13, 19)

                    for cadeira_id in cadeiras_curso:
                        inscricoes.append(
                            (  2,
                                "1",
                                estudante_id,
                                cadeira_id
                            )
                        )

                comandoSql= """INSERT INTO inscricao (semestre, estado,id_estudante,id_cadeira) VALUES (?, ?, ?, ?)"""  
                self.inserirVariasLinhas(comandoSql,inscricoes)
            
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
    
    
    def inserirNotas(self,cursor):
        try:
        
            #Verificar se existem inscricoes na base de dados
            comandoSql= "SELECT COUNT(*) FROM notas"
            cursor.execute(comandoSql)
            if cursor.fetchone()[0]>0: 
                pass
            else:  
                notas=self.gerarNotas()   
                comandoSql= """INSERT INTO notas (nota1, nota2, nota3, frequencia,
                id_estudante, id_docente, id_cadeira) VALUES (?, ?, ?, ?, ?, ?, ?)"""  
                self.inserirVariasLinhas(comandoSql,notas)    
                
        except TypeError as e:
            print(f"Type Error: {e}")
    
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")
    
        except Exception as e:
            print(f"Error: {e}")
        
    def inicializarTabelas(self):
        """Inicializa a base de dados criando as tabelas e preencheendo os dados de exemplo caso ela esteja vazia."""
        
        self.criarTabelaCurso()
        self.criarTabelaEstudante()
        self.criarTabelaCadeira()
        
        """"
        self.criarTabelaInscricao()
        self.criarTabelaDocente()
        self.criarTabelaTurma()
        self.criarTabelaNotas()
        self.criarTabelaNotificacoes()
        
                """
        self.inserirDadosDeExemplo()  
        

        
           
    def ActualizarLinha(self,comandoSql,parametros:tuple=()):
        """Actualiza uma linha de uma determinada tabela"""

        """Exemplo de comando sql: UPDATE nome_tabela set atributo=? where condicao=?"""
        return self.executarComandoSql(comandoSql,parametros)


    def DeletarLinha(self,comandoSql,parametros:tuple=()):
        """Deleta uma linha de uma determinada tabela"""

        """Exemplo de comando sql: DELETE FROM nome_tabela WHERE condicao=?"""
        return self.executarComandoSql(comandoSql,parametros)


gestor=GestorBaseDados("feng_live.db")
gestor.inicializarTabelas()