"""
Módulo de gerenciamento de produtos
"""
from database import Database

class Produtos:
    def __init__(self):
        self.db = Database()
    
    def create(self, dados):
        """Cria um novo produto"""
        return self.db.execute_insert('''
            INSERT INTO produtos (
                codigo, descricao, categoria, unidade, preco_venda,
                preco_custo, estoque_atual, estoque_minimo, ativo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados.get('codigo', ''),
            dados.get('descricao', ''),
            dados.get('categoria', ''),
            dados.get('unidade', 'UN'),
            dados.get('preco_venda', 0),
            dados.get('preco_custo', 0),
            dados.get('estoque_atual', 0),
            dados.get('estoque_minimo', 0),
            dados.get('ativo', 1)
        ))
    
    def update(self, produto_id, dados):
        """Atualiza um produto"""
        self.db.execute_query('''
            UPDATE produtos SET
                codigo = ?,
                descricao = ?,
                categoria = ?,
                unidade = ?,
                preco_venda = ?,
                preco_custo = ?,
                estoque_minimo = ?,
                ativo = ?
            WHERE id = ?
        ''', (
            dados.get('codigo', ''),
            dados.get('descricao', ''),
            dados.get('categoria', ''),
            dados.get('unidade', 'UN'),
            dados.get('preco_venda', 0),
            dados.get('preco_custo', 0),
            dados.get('estoque_minimo', 0),
            dados.get('ativo', 1),
            produto_id
        ))
    
    def get_by_id(self, produto_id):
        """Busca produto por ID"""
        result = self.db.execute_query('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        if result:
            return {
                'id': result[0][0],
                'codigo': result[0][1],
                'descricao': result[0][2],
                'categoria': result[0][3],
                'unidade': result[0][4],
                'preco_venda': result[0][5],
                'preco_custo': result[0][6],
                'estoque_atual': result[0][7],
                'estoque_minimo': result[0][8],
                'ativo': result[0][9]
            }
        return None
    
    def get_by_codigo(self, codigo):
        """Busca produto por código"""
        result = self.db.execute_query('SELECT * FROM produtos WHERE codigo = ? AND ativo = 1', (codigo,))
        if result:
            return {
                'id': result[0][0],
                'codigo': result[0][1],
                'descricao': result[0][2],
                'categoria': result[0][3],
                'unidade': result[0][4],
                'preco_venda': result[0][5],
                'preco_custo': result[0][6],
                'estoque_atual': result[0][7],
                'estoque_minimo': result[0][8],
                'ativo': result[0][9]
            }
        return None
    
    def list_all(self, search='', apenas_ativos=True):
        """Lista todos os produtos com busca opcional"""
        if apenas_ativos:
            if search:
                return self.db.execute_query('''
                    SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, unidade
                    FROM produtos
                    WHERE ativo = 1 AND (codigo LIKE ? OR descricao LIKE ?)
                    ORDER BY descricao
                ''', (f'%{search}%', f'%{search}%'))
            else:
                return self.db.execute_query('''
                    SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, unidade
                    FROM produtos
                    WHERE ativo = 1
                    ORDER BY descricao
                ''')
        else:
            if search:
                return self.db.execute_query('''
                    SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, unidade, ativo
                    FROM produtos
                    WHERE codigo LIKE ? OR descricao LIKE ?
                    ORDER BY descricao
                ''', (f'%{search}%', f'%{search}%'))
            else:
                return self.db.execute_query('''
                    SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, unidade, ativo
                    FROM produtos
                    ORDER BY descricao
                ''')
    
    def atualizar_estoque(self, produto_id, quantidade, tipo='Ajuste'):
        """Atualiza o estoque de um produto"""
        produto = self.get_by_id(produto_id)
        if not produto:
            return False
        
        if tipo == 'Entrada':
            novo_estoque = produto['estoque_atual'] + quantidade
        elif tipo == 'Saida':
            novo_estoque = produto['estoque_atual'] - quantidade
        elif tipo == 'Cancelamento':
            novo_estoque = produto['estoque_atual'] + quantidade
        else:  # Ajuste
            novo_estoque = quantidade
        
        self.db.execute_query('''
            UPDATE produtos SET estoque_atual = ? WHERE id = ?
        ''', (novo_estoque, produto_id))
        
        return True

