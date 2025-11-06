"""
Módulo de gerenciamento do banco de dados SQLite
"""
import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path=None):
        # Se não especificado, usar data/pdv.db
        if db_path is None:
            # Criar pasta data se não existir
            data_dir = 'data'
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            db_path = os.path.join(data_dir, 'pdv.db')
        
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa o banco de dados criando todas as tabelas necessárias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de configuração da empresa
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empresa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                razao_social TEXT NOT NULL,
                nome_fantasia TEXT,
                cnpj TEXT,
                inscricao_estadual TEXT,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                numero TEXT,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                logo_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nivel_acesso TEXT NOT NULL CHECK(nivel_acesso IN ('Vendedor', 'Conferente', 'Gerente', 'Admin')),
                ativo INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf_cnpj TEXT,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                numero TEXT,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                observacoes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de produtos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE,
                descricao TEXT NOT NULL,
                categoria TEXT,
                unidade TEXT DEFAULT 'UN',
                preco_venda REAL NOT NULL DEFAULT 0,
                preco_custo REAL DEFAULT 0,
                estoque_atual REAL DEFAULT 0,
                estoque_minimo REAL DEFAULT 0,
                ativo INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de orçamentos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orcamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                cliente_id INTEGER,
                usuario_id INTEGER,
                data_orcamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_validade TIMESTAMP,
                valor_total REAL DEFAULT 0,
                status TEXT DEFAULT 'Aberto' CHECK(status IN ('Aberto', 'Aprovado', 'Cancelado', 'Vendido')),
                observacoes TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabela de itens do orçamento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orcamento_itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orcamento_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade REAL NOT NULL,
                preco_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id) ON DELETE CASCADE,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        
        # Tabela de vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT UNIQUE NOT NULL,
                cliente_id INTEGER,
                usuario_id INTEGER NOT NULL,
                orcamento_id INTEGER,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                valor_total REAL DEFAULT 0,
                desconto REAL DEFAULT 0,
                valor_final REAL DEFAULT 0,
                status TEXT DEFAULT 'Finalizada' CHECK(status IN ('Finalizada', 'Cancelada')),
                observacoes TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (orcamento_id) REFERENCES orcamentos(id)
            )
        ''')
        
        # Tabela de itens da venda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS venda_itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade REAL NOT NULL,
                preco_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        ''')
        
        # Tabela de movimentação de estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque_movimentacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('Entrada', 'Saida', 'Ajuste', 'Cancelamento')),
                quantidade REAL NOT NULL,
                venda_id INTEGER,
                observacao TEXT,
                usuario_id INTEGER,
                data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES produtos(id),
                FOREIGN KEY (venda_id) REFERENCES vendas(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Criar usuário admin padrão se não existir
        cursor.execute('SELECT COUNT(*) FROM usuarios')
        if cursor.fetchone()[0] == 0:
            # Hash da senha padrão
            import hashlib
            senha_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO usuarios (nome, usuario, senha, nivel_acesso)
                VALUES (?, ?, ?, ?)
            ''', ('Administrador', 'admin', senha_hash, 'Admin'))
        else:
            # Migração: atualizar senha do admin se não estiver hasheada
            import hashlib
            cursor.execute('SELECT senha FROM usuarios WHERE usuario = ?', ('admin',))
            result = cursor.fetchone()
            if result:
                senha_atual = result[0]
                # Se a senha não tem 64 caracteres (tamanho do hash SHA256), precisa ser atualizada
                if len(senha_atual) != 64:
                    senha_hash = hashlib.sha256('admin123'.encode()).hexdigest()
                    cursor.execute('''
                        UPDATE usuarios SET senha = ? WHERE usuario = ? AND senha = ?
                    ''', (senha_hash, 'admin', 'admin123'))
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """Executa uma query e retorna o resultado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    
    def execute_insert(self, query, params):
        """Executa um INSERT e retorna o ID do registro inserido"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return last_id

