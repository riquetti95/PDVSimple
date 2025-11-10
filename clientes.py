"""
Módulo de gerenciamento de clientes
"""
from database import Database

class Clientes:
    def __init__(self):
        self.db = Database()
    
    def create(self, dados):
        """Cria um novo cliente"""
        # Validações
        nome = dados.get('nome', '').strip()
        if not nome:
            raise ValueError("O nome do cliente é obrigatório!")
        
        if len(nome) < 3:
            raise ValueError("O nome do cliente deve ter pelo menos 3 caracteres!")
        
        # Validar email se informado
        email = dados.get('email', '').strip()
        if email and '@' not in email:
            raise ValueError("Email inválido!")
        
        try:
            return self.db.execute_insert('''
                INSERT INTO clientes (
                    nome, cpf_cnpj, telefone, email, endereco, numero,
                    complemento, bairro, cidade, estado, cep, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nome,
                dados.get('cpf_cnpj', '').strip(),
                dados.get('telefone', '').strip(),
                email,
                dados.get('endereco', '').strip(),
                dados.get('numero', '').strip(),
                dados.get('complemento', '').strip(),
                dados.get('bairro', '').strip(),
                dados.get('cidade', '').strip(),
                dados.get('estado', '').strip(),
                dados.get('cep', '').strip(),
                dados.get('observacoes', '').strip()
            ))
        except Exception as e:
            raise Exception(f"Erro ao criar cliente: {str(e)}")
    
    def update(self, cliente_id, dados):
        """Atualiza um cliente"""
        # Validações
        if not cliente_id:
            raise ValueError("ID do cliente não informado!")
        
        # Verificar se cliente existe
        cliente = self.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado!")
        
        nome = dados.get('nome', '').strip()
        if not nome:
            raise ValueError("O nome do cliente é obrigatório!")
        
        if len(nome) < 3:
            raise ValueError("O nome do cliente deve ter pelo menos 3 caracteres!")
        
        # Validar email se informado
        email = dados.get('email', '').strip()
        if email and '@' not in email:
            raise ValueError("Email inválido!")
        
        try:
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
                nome,
                dados.get('cpf_cnpj', '').strip(),
                dados.get('telefone', '').strip(),
                email,
                dados.get('endereco', '').strip(),
                dados.get('numero', '').strip(),
                dados.get('complemento', '').strip(),
                dados.get('bairro', '').strip(),
                dados.get('cidade', '').strip(),
                dados.get('estado', '').strip(),
                dados.get('cep', '').strip(),
                dados.get('observacoes', '').strip(),
                cliente_id
            ))
        except Exception as e:
            raise Exception(f"Erro ao atualizar cliente: {str(e)}")
    
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

