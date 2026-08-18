import sqlite3
import threading
from datetime import datetime
import os

class Database:
    """Gerenciador da base de dados SQLite3 com thread-safety"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'feng_live.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self._local = threading.local()
        self.init_database()
    
    def _get_connection(self):
        """Obtém conexão thread-safe"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=10
            )
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def init_database(self):
        """Inicializa as tabelas do banco de dados"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('aluno', 'professor', 'coordenador')),
            curso TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Tabela de disciplinas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            professor_id INTEGER,
            creditos INTEGER DEFAULT 4,
            FOREIGN KEY (professor_id) REFERENCES usuarios(id)
        )
        ''')
        
        # Tabela de notas
        cursor.execute('''
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
        ''')
        
        # Tabela de notificações
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            lida INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (aluno_id) REFERENCES usuarios(id)
        )
        ''')
        
        conn.commit()
        self._seed_data()
    
    def _seed_data(self):
        """Insere dados de exemplo se a base estiver vazia"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Verifica se já há dados
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] > 0:
            return
        
        print("📊 Inserindo dados de exemplo...")
        
        # Usuários
        usuarios = [
            ('2024001', 'Alexandre Ntema', '123456', 'aluno', 'Engenharia Informática'),
            ('2024002', 'Henrinques Almeida', '123456', 'aluno', 'Engenharia Civil'),
            ('2024003', 'Afonso Adolfo', '123456', 'aluno', 'Engenharia Elétrica'),
            ('2024004', 'Ana Oliveira', '123456', 'aluno', 'Engenharia Mecânica'),
            ('2024005', 'Carlos Mendes', '123456', 'aluno', 'Engenharia Informática'),
            ('P001', 'Prof. Jaime', '123456', 'professor', None),
            ('P002', 'Prof. Ivone', '123456', 'professor', None),
        ]
        
        cursor.executemany(
            "INSERT INTO usuarios (matricula, nome, senha, tipo, curso) VALUES (?, ?, ?, ?, ?)",
            usuarios
        )
        
        # Disciplinas
        disciplinas = [
            ('INF101', 'Programação I', 6, 4),
            ('MAT101', 'Cálculo I', 6, 4),
            ('FIS101', 'Física I', 7, 4),
            ('INF201', 'Programação II', 6, 4),
            ('MAT201', 'Cálculo II', 7, 4),
        ]
        
        cursor.executemany(
            "INSERT INTO disciplinas (codigo, nome, professor_id, creditos) VALUES (?, ?, ?, ?)",
            disciplinas
        )
        
        # Notas (exemplo)
        notas = [
            (1, 1, 14, 16, 15, 15.0, 85, '2024.1', 2024),
            (1, 2, 10, 8, 12, 10.0, 75, '2024.1', 2024),
            (2, 1, 12, 10, 11, 11.0, 90, '2024.1', 2024),
            (2, 2, 15, 14, 16, 15.0, 85, '2024.1', 2024),
            (3, 2, 13, 12, 14, 13.0, 80, '2024.1', 2024),
        ]
        
        cursor.executemany(
            """INSERT INTO notas 
               (aluno_id, disciplina_id, nota1, nota2, nota3, nota_final, frequencia, semestre, ano)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            notas
        )
        
        conn.commit()
        print("✅ Dados de exemplo inseridos com sucesso!")
    
    def execute_query(self, query, params=None):
        """Executa uma query e retorna resultados"""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
    
    def get_user(self, matricula):
        """Busca usuário por matrícula"""
        result = self.execute_query(
            "SELECT * FROM usuarios WHERE matricula = ?",
            (matricula,)
        )
        return result[0] if result else None
    
    def authenticate(self, matricula, senha):
        """Autentica um usuário"""
        user = self.get_user(matricula)
        if user and user['senha'] == senha:
            return dict(user)
        return None
    
    def get_notas_aluno(self, aluno_id):
        """Busca todas as notas de um aluno"""
        return self.execute_query('''
            SELECT d.codigo, d.nome, n.nota1, n.nota2, n.nota3, n.nota_final, 
                   n.frequencia, n.semestre, n.ano
            FROM notas n
            JOIN disciplinas d ON n.disciplina_id = d.id
            WHERE n.aluno_id = ?
            ORDER BY n.ano DESC, n.semestre DESC
        ''', (aluno_id,))
    
    def get_media_aluno(self, aluno_id):
        """Calcula média geral do aluno"""
        result = self.execute_query('''
            SELECT AVG(nota_final) as media
            FROM notas
            WHERE aluno_id = ?
        ''', (aluno_id,))
        
        return result[0]['media'] if result and result[0]['media'] else 0
    
    def get_ranking(self):
        """Retorna ranking dos alunos"""
        return self.execute_query('''
            SELECT u.nome, u.matricula, AVG(n.nota_final) as media
            FROM usuarios u
            JOIN notas n ON u.id = n.aluno_id
            WHERE u.tipo = 'aluno'
            GROUP BY u.id
            ORDER BY media DESC
        ''')
    
    def lancar_nota(self, aluno_matricula, disciplina_codigo, notas, semestre, ano):
        """Lança nota para um aluno"""
        # Busca aluno
        aluno = self.get_user(aluno_matricula)
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
    
    def create_notificacao(self, aluno_id, mensagem):
        """Cria uma notificação para o aluno"""
        return self.execute_query(
            "INSERT INTO notificacoes (aluno_id, mensagem) VALUES (?, ?)",
            (aluno_id, mensagem)
        )
    
    def get_notificacoes(self, aluno_id, apenas_nao_lidas=True):
        """Busca notificações do aluno"""
        query = "SELECT * FROM notificacoes WHERE aluno_id = ?"
        if apenas_nao_lidas:
            query += " AND lida = 0"
        query += " ORDER BY created_at DESC"
        
        return self.execute_query(query, (aluno_id,))
    
    def marcar_notificacao_lida(self, notificacao_id):
        """Marca notificação como lida"""
        return self.execute_query(
            "UPDATE notificacoes SET lida = 1 WHERE id = ?",
            (notificacao_id,)
        )