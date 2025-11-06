"""
Módulo de controle de orçamentos
"""
from database import Database
from datetime import datetime, timedelta

class Orcamentos:
    def __init__(self):
        self.db = Database()
    
    def gerar_numero(self):
        """Gera número único para o orçamento"""
        result = self.db.execute_query('SELECT COUNT(*) FROM orcamentos')
        count = result[0][0] if result else 0
        numero = f'ORC{str(count + 1).zfill(6)}'
        return numero
    
    def create(self, cliente_id, usuario_id, itens, data_validade_dias=30, observacoes=''):
        """Cria um novo orçamento"""
        numero = self.gerar_numero()
        data_validade = (datetime.now() + timedelta(days=data_validade_dias)).strftime('%Y-%m-%d')
        
        valor_total = sum(item['subtotal'] for item in itens)
        
        orcamento_id = self.db.execute_insert('''
            INSERT INTO orcamentos (
                numero, cliente_id, usuario_id, data_validade, valor_total, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (numero, cliente_id, usuario_id, data_validade, valor_total, observacoes))
        
        # Inserir itens
        for item in itens:
            self.db.execute_insert('''
                INSERT INTO orcamento_itens (
                    orcamento_id, produto_id, quantidade, preco_unitario, subtotal
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                orcamento_id,
                item['produto_id'],
                item['quantidade'],
                item['preco_unitario'],
                item['subtotal']
            ))
        
        return orcamento_id
    
    def get_by_id(self, orcamento_id):
        """Busca orçamento por ID"""
        result = self.db.execute_query('''
            SELECT o.id, o.numero, o.cliente_id, o.usuario_id, o.data_orcamento,
                   o.data_validade, o.valor_total, o.status, o.observacoes,
                   c.nome as cliente_nome
            FROM orcamentos o
            LEFT JOIN clientes c ON o.cliente_id = c.id
            WHERE o.id = ?
        ''', (orcamento_id,))
        
        if result:
            orc = result[0]
            return {
                'id': orc[0],
                'numero': orc[1],
                'cliente_id': orc[2],
                'usuario_id': orc[3],
                'data_orcamento': orc[4],
                'data_validade': orc[5],
                'valor_total': orc[6],
                'status': orc[7],
                'observacoes': orc[8] if len(orc) > 8 else '',
                'cliente_nome': orc[9] if len(orc) > 9 else ''
            }
        return None
    
    def get_itens(self, orcamento_id):
        """Busca itens de um orçamento"""
        return self.db.execute_query('''
            SELECT oi.*, p.descricao, p.codigo
            FROM orcamento_itens oi
            JOIN produtos p ON oi.produto_id = p.id
            WHERE oi.orcamento_id = ?
        ''', (orcamento_id,))
    
    def list_all(self, status=None, cliente_id=None):
        """Lista todos os orçamentos"""
        query = '''
            SELECT o.id, o.numero, o.data_orcamento, o.data_validade, o.valor_total, o.status,
                   c.nome as cliente_nome
            FROM orcamentos o
            LEFT JOIN clientes c ON o.cliente_id = c.id
            WHERE 1=1
        '''
        params = []
        
        if status:
            query += ' AND o.status = ?'
            params.append(status)
        
        if cliente_id:
            query += ' AND o.cliente_id = ?'
            params.append(cliente_id)
        
        query += ' ORDER BY o.data_orcamento DESC'
        
        return self.db.execute_query(query, tuple(params) if params else None)
    
    def atualizar_status(self, orcamento_id, status):
        """Atualiza o status do orçamento"""
        self.db.execute_query('''
            UPDATE orcamentos SET status = ? WHERE id = ?
        ''', (status, orcamento_id))
    
    def converter_para_venda(self, orcamento_id, usuario_id):
        """Converte um orçamento aprovado em venda"""
        orcamento = self.get_by_id(orcamento_id)
        if not orcamento or orcamento['status'] != 'Aprovado':
            return None
        
        itens = self.get_itens(orcamento_id)
        venda_itens = []
        for item in itens:
            venda_itens.append({
                'produto_id': item[2],
                'quantidade': item[3],
                'preco_unitario': item[4],
                'subtotal': item[5]
            })
        
        from vendas import Vendas
        vendas = Vendas()
        venda_id = vendas.create(
            orcamento['cliente_id'],
            usuario_id,
            venda_itens,
            orcamento_id=orcamento_id
        )
        
        # Atualizar status do orçamento
        self.atualizar_status(orcamento_id, 'Vendido')
        
        return venda_id

