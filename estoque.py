"""
Módulo de controle de estoque
"""
from database import Database
from datetime import datetime

class Estoque:
    def __init__(self):
        self.db = Database()
    
    def registrar_movimentacao(self, produto_id, tipo, quantidade, venda_id=None, observacao='', usuario_id=None):
        """Registra uma movimentação de estoque"""
        from produtos import Produtos
        produtos = Produtos()
        
        # Atualizar estoque do produto
        produtos.atualizar_estoque(produto_id, quantidade, tipo)
        
        # Registrar movimentação
        self.db.execute_insert('''
            INSERT INTO estoque_movimentacao (
                produto_id, tipo, quantidade, venda_id, observacao, usuario_id
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (produto_id, tipo, quantidade, venda_id, observacao, usuario_id))
    
    def baixar_estoque_venda(self, venda_id, usuario_id):
        """Baixa estoque de todos os itens de uma venda"""
        # Buscar itens da venda
        itens = self.db.execute_query('''
            SELECT produto_id, quantidade
            FROM venda_itens
            WHERE venda_id = ?
        ''', (venda_id,))
        
        for item in itens:
            produto_id, quantidade = item
            self.registrar_movimentacao(
                produto_id, 'Saida', quantidade,
                venda_id=venda_id,
                observacao=f'Baixa automática da venda #{venda_id}',
                usuario_id=usuario_id
            )
    
    def reverter_estoque_venda(self, venda_id, usuario_id):
        """Reverte o estoque de uma venda cancelada"""
        # Buscar itens da venda
        itens = self.db.execute_query('''
            SELECT produto_id, quantidade
            FROM venda_itens
            WHERE venda_id = ?
        ''', (venda_id,))
        
        for item in itens:
            produto_id, quantidade = item
            self.registrar_movimentacao(
                produto_id, 'Cancelamento', quantidade,
                venda_id=venda_id,
                observacao=f'Cancelamento da venda #{venda_id}',
                usuario_id=usuario_id
            )
    
    def list_movimentacoes(self, produto_id=None, data_inicio=None, data_fim=None):
        """Lista movimentações de estoque"""
        query = '''
            SELECT em.id, em.tipo, em.quantidade, em.data_movimentacao, em.observacao,
                   p.descricao, u.nome
            FROM estoque_movimentacao em
            LEFT JOIN produtos p ON em.produto_id = p.id
            LEFT JOIN usuarios u ON em.usuario_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if produto_id:
            query += ' AND em.produto_id = ?'
            params.append(produto_id)
        
        if data_inicio:
            query += ' AND DATE(em.data_movimentacao) >= ?'
            params.append(data_inicio)
        
        if data_fim:
            query += ' AND DATE(em.data_movimentacao) <= ?'
            params.append(data_fim)
        
        query += ' ORDER BY em.data_movimentacao DESC'
        
        return self.db.execute_query(query, tuple(params) if params else None)
    
    def get_produtos_estoque_baixo(self):
        """Retorna produtos com estoque abaixo do mínimo"""
        return self.db.execute_query('''
            SELECT id, codigo, descricao, estoque_atual, estoque_minimo
            FROM produtos
            WHERE ativo = 1 AND estoque_atual <= estoque_minimo AND estoque_minimo > 0
            ORDER BY (estoque_atual - estoque_minimo) ASC
        ''')

