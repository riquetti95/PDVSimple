"""
Módulo de gerenciamento de clientes
"""
from database import Database

class Clientes:
    def __init__(self):
        self.db = Database()
    
    def create(self, dados):
        """Cria um novo cliente"""
        return self.db.execute_insert('''
            INSERT INTO clientes (
                nome, cpf_cnpj, telefone, email, endereco, numero,
                complemento, bairro, cidade, estado, cep, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados.get('nome', ''),
            dados.get('cpf_cnpj', ''),
            dados.get('telefone', ''),
            dados.get('email', ''),
            dados.get('endereco', ''),
            dados.get('numero', ''),
            dados.get('complemento', ''),
            dados.get('bairro', ''),
            dados.get('cidade', ''),
            dados.get('estado', ''),
            dados.get('cep', ''),
            dados.get('observacoes', '')
        ))
    
    def update(self, cliente_id, dados):
        """Atualiza um cliente"""
        self.db.execute_query('''
            UPDATE clientes SET
                nome = ?,
                cpf_cnpj = ?,
                telefone = ?,
                email = ?,
                endereco = ?,
                numero = ?,
                complemento = ?,
                bairro = ?,
                cidade = ?,
                estado = ?,
                cep = ?,
                observacoes = ?
            WHERE id = ?
        ''', (
            dados.get('nome', ''),
            dados.get('cpf_cnpj', ''),
            dados.get('telefone', ''),
            dados.get('email', ''),
            dados.get('endereco', ''),
            dados.get('numero', ''),
            dados.get('complemento', ''),
            dados.get('bairro', ''),
            dados.get('cidade', ''),
            dados.get('estado', ''),
            dados.get('cep', ''),
            dados.get('observacoes', ''),
            cliente_id
        ))
    
    def get_by_id(self, cliente_id):
        """Busca cliente por ID"""
        result = self.db.execute_query('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
        if result:
            return {
                'id': result[0][0],
                'nome': result[0][1],
                'cpf_cnpj': result[0][2],
                'telefone': result[0][3],
                'email': result[0][4],
                'endereco': result[0][5],
                'numero': result[0][6],
                'complemento': result[0][7],
                'bairro': result[0][8],
                'cidade': result[0][9],
                'estado': result[0][10],
                'cep': result[0][11],
                'observacoes': result[0][12]
            }
        return None
    
    def list_all(self, search=''):
        """Lista todos os clientes com busca opcional"""
        if search:
            return self.db.execute_query('''
                SELECT id, nome, cpf_cnpj, telefone, email, cidade
                FROM clientes
                WHERE nome LIKE ? OR cpf_cnpj LIKE ? OR telefone LIKE ?
                ORDER BY nome
            ''', (f'%{search}%', f'%{search}%', f'%{search}%'))
        else:
            return self.db.execute_query('''
                SELECT id, nome, cpf_cnpj, telefone, email, cidade
                FROM clientes
                ORDER BY nome
            ''')

