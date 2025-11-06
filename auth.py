"""
Módulo de autenticação e controle de acesso
"""
import hashlib
from database import Database

class Auth:
    def __init__(self):
        self.db = Database()
        self.current_user = None
    
    def hash_password(self, password):
        """Cria hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, usuario, senha):
        """Autentica um usuário"""
        senha_hash = self.hash_password(senha)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, usuario, nivel_acesso 
            FROM usuarios 
            WHERE usuario = ? AND senha = ? AND ativo = 1
        ''', (usuario, senha_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.current_user = {
                'id': user[0],
                'nome': user[1],
                'usuario': user[2],
                'nivel_acesso': user[3]
            }
            return True
        return False
    
    def logout(self):
        """Faz logout do usuário atual"""
        self.current_user = None
    
    def get_current_user(self):
        """Retorna o usuário atual"""
        return self.current_user
    
    def has_permission(self, required_level):
        """Verifica se o usuário tem permissão para a ação"""
        if not self.current_user:
            return False
        
        levels = {'Vendedor': 1, 'Conferente': 2, 'Gerente': 3, 'Admin': 4}
        user_level = levels.get(self.current_user['nivel_acesso'], 0)
        required = levels.get(required_level, 0)
        
        return user_level >= required
    
    def create_user(self, nome, usuario, senha, nivel_acesso):
        """Cria um novo usuário (apenas Admin)"""
        if not self.has_permission('Admin'):
            return False
        
        senha_hash = self.hash_password(senha)
        try:
            self.db.execute_insert('''
                INSERT INTO usuarios (nome, usuario, senha, nivel_acesso)
                VALUES (?, ?, ?, ?)
            ''', (nome, usuario, senha_hash, nivel_acesso))
            return True
        except:
            return False
    
    def list_users(self):
        """Lista todos os usuários"""
        if not self.has_permission('Gerente'):
            return []
        
        return self.db.execute_query('''
            SELECT id, nome, usuario, nivel_acesso, ativo 
            FROM usuarios 
            ORDER BY nome
        ''')

