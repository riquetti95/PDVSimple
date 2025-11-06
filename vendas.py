"""
Módulo de gerenciamento de vendas
"""
from database import Database
from estoque import Estoque

class Vendas:
    def __init__(self):
        self.db = Database()
        self.estoque = Estoque()
    
    def gerar_numero(self):
        """Gera número único para a venda"""
        result = self.db.execute_query('SELECT COUNT(*) FROM vendas')
        count = result[0][0] if result else 0
        numero = f'VEN{str(count + 1).zfill(6)}'
        return numero
    
    def create(self, cliente_id, usuario_id, itens, orcamento_id=None, desconto=0, observacoes=''):
        """Cria uma nova venda e baixa o estoque automaticamente"""
        numero = self.gerar_numero()
        
        valor_total = sum(item['subtotal'] for item in itens)
        valor_final = valor_total - desconto
        
        venda_id = self.db.execute_insert('''
            INSERT INTO vendas (
                numero, cliente_id, usuario_id, orcamento_id, valor_total, desconto, valor_final, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (numero, cliente_id, usuario_id, orcamento_id, valor_total, desconto, valor_final, observacoes))
        
        # Inserir itens
        for item in itens:
            self.db.execute_insert('''
                INSERT INTO venda_itens (
                    venda_id, produto_id, quantidade, preco_unitario, subtotal
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                venda_id,
                item['produto_id'],
                item['quantidade'],
                item['preco_unitario'],
                item['subtotal']
            ))
        
        # Baixar estoque automaticamente
        self.estoque.baixar_estoque_venda(venda_id, usuario_id)
        
        return venda_id
    
    def cancelar(self, venda_id, usuario_id):
        """Cancela uma venda e reverte o estoque"""
        # Verificar se a venda existe e não está cancelada
        venda = self.get_by_id(venda_id)
        if not venda or venda['status'] == 'Cancelada':
            return False
        
        # Reverter estoque
        self.estoque.reverter_estoque_venda(venda_id, usuario_id)
        
        # Atualizar status
        self.db.execute_query('''
            UPDATE vendas SET status = 'Cancelada' WHERE id = ?
        ''', (venda_id,))
        
        return True
    
    def get_by_id(self, venda_id):
        """Busca venda por ID"""
        result = self.db.execute_query('''
            SELECT v.id, v.numero, v.cliente_id, v.usuario_id, v.orcamento_id, 
                   v.data_venda, v.valor_total, v.desconto, v.valor_final, 
                   v.status, v.observacoes, c.nome as cliente_nome
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.id = ?
        ''', (venda_id,))
        
        if result:
            ven = result[0]
            return {
                'id': ven[0],
                'numero': ven[1],
                'cliente_id': ven[2],
                'usuario_id': ven[3],
                'orcamento_id': ven[4],
                'data_venda': ven[5],
                'valor_total': ven[6],
                'desconto': ven[7],
                'valor_final': ven[8],
                'status': ven[9] if ven[9] else 'Finalizada',
                'observacoes': ven[10] if len(ven) > 10 else '',
                'cliente_nome': ven[11] if len(ven) > 11 else ''
            }
        return None
    
    def get_itens(self, venda_id):
        """Busca itens de uma venda"""
        return self.db.execute_query('''
            SELECT vi.*, p.descricao, p.codigo
            FROM venda_itens vi
            JOIN produtos p ON vi.produto_id = p.id
            WHERE vi.venda_id = ?
        ''', (venda_id,))
    
    def list_all(self, data_inicio=None, data_fim=None, cliente_id=None):
        """Lista todas as vendas"""
        query = '''
            SELECT v.id, v.numero, v.data_venda, v.valor_final, v.status,
                   c.nome as cliente_nome
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE 1=1
        '''
        params = []
        
        if data_inicio:
            query += ' AND DATE(v.data_venda) >= ?'
            params.append(data_inicio)
        
        if data_fim:
            query += ' AND DATE(v.data_venda) <= ?'
            params.append(data_fim)
        
        if cliente_id:
            query += ' AND v.cliente_id = ?'
            params.append(cliente_id)
        
        query += ' ORDER BY v.data_venda DESC'
        
        return self.db.execute_query(query, tuple(params) if params else None)

