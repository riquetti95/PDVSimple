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
        # Validações
        if not itens or len(itens) == 0:
            raise ValueError("A venda deve conter pelo menos um item!")
        
        if not usuario_id:
            raise ValueError("Usuário não informado!")
        
        # Validar estoque antes de criar a venda
        from produtos import Produtos
        produtos = Produtos()
        
        for item in itens:
            produto = produtos.get_by_id(item['produto_id'])
            if not produto:
                raise ValueError(f"Produto ID {item['produto_id']} não encontrado!")
            
            if not produto.get('ativo', 1):
                raise ValueError(f"Produto {produto.get('descricao', '')} está inativo!")
            
            if produto.get('estoque_atual', 0) < item['quantidade']:
                raise ValueError(f"Estoque insuficiente para o produto {produto.get('descricao', '')}! "
                               f"Estoque disponível: {produto.get('estoque_atual', 0)}")
        
        # Validar desconto
        valor_total = sum(item['subtotal'] for item in itens)
        if desconto < 0:
            desconto = 0
        if desconto > valor_total:
            raise ValueError(f"Desconto não pode ser maior que o valor total da venda!")
        
        valor_final = valor_total - desconto
        if valor_final < 0:
            valor_final = 0
        
        # Gerar número da venda
        numero = self.gerar_numero()
        
        try:
            # Criar venda
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
        except Exception as e:
            # Se houver erro, tentar reverter (se a venda foi criada)
            raise Exception(f"Erro ao criar venda: {str(e)}")
    
    def cancelar(self, venda_id, usuario_id):
        """Cancela uma venda e reverte o estoque"""
        # Validações
        if not venda_id:
            raise ValueError("ID da venda não informado!")
        
        if not usuario_id:
            raise ValueError("Usuário não informado!")
        
        # Verificar se a venda existe e não está cancelada
        venda = self.get_by_id(venda_id)
        if not venda:
            raise ValueError("Venda não encontrada!")
        
        if venda['status'] == 'Cancelada':
            raise ValueError("Esta venda já foi cancelada!")
        
        try:
            # Reverter estoque
            self.estoque.reverter_estoque_venda(venda_id, usuario_id)
            
            # Atualizar status
            self.db.execute_query('''
                UPDATE vendas SET status = 'Cancelada' WHERE id = ?
            ''', (venda_id,))
            
            return True
        except Exception as e:
            raise Exception(f"Erro ao cancelar venda: {str(e)}")
    
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

