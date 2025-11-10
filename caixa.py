"""
Módulo de gerenciamento de caixa (abertura e fechamento)
"""
from database import Database
from datetime import datetime, date
from vendas import Vendas

class Caixa:
    def __init__(self):
        self.db = Database()
        self.vendas = Vendas()
    
    def abrir_caixa(self, usuario_id, valor_inicial=0, observacoes=''):
        """Abre o caixa do dia"""
        # Verificar se já existe caixa aberto para hoje
        caixa_aberto = self.get_caixa_aberto()
        if caixa_aberto:
            return None  # Já existe caixa aberto
        
        # Criar novo caixa
        caixa_id = self.db.execute_insert('''
            INSERT INTO caixa (
                usuario_id, data_abertura, valor_inicial, observacoes, status
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            usuario_id,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            valor_inicial,
            observacoes,
            'Aberto'
        ))
        
        return caixa_id
    
    def fechar_caixa(self, caixa_id, usuario_id, valor_final, observacoes=''):
        """Fecha o caixa e calcula totais"""
        # Verificar se o caixa existe e está aberto
        caixa = self.get_by_id(caixa_id)
        if not caixa or caixa['status'] != 'Aberto':
            return False
        
        # Calcular totais do dia
        totais = self.calcular_totais_dia(caixa['data_abertura'])
        
        # Atualizar caixa
        self.db.execute_query('''
            UPDATE caixa SET
                data_fechamento = ?,
                valor_final = ?,
                total_vendas = ?,
                total_cancelamentos = ?,
                total_descontos = ?,
                observacoes = ?,
                status = 'Fechado'
            WHERE id = ?
        ''', (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            valor_final,
            totais['total_vendas'],
            totais['total_cancelamentos'],
            totais['total_descontos'],
            observacoes,
            caixa_id
        ))
        
        return True
    
    def get_caixa_aberto(self):
        """Retorna o caixa aberto do dia, se existir"""
        hoje = date.today().strftime('%Y-%m-%d')
        result = self.db.execute_query('''
            SELECT c.id, c.usuario_id, c.data_abertura, c.valor_inicial, 
                   c.observacoes, c.status, u.nome as usuario_nome
            FROM caixa c
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE DATE(c.data_abertura) = ? AND c.status = 'Aberto'
            ORDER BY c.data_abertura DESC
            LIMIT 1
        ''', (hoje,))
        
        if result:
            row = result[0]
            return {
                'id': row[0],
                'usuario_id': row[1],
                'data_abertura': row[2],
                'valor_inicial': row[3],
                'observacoes': row[4] if len(row) > 4 else '',
                'status': row[5] if len(row) > 5 else 'Aberto',
                'usuario_nome': row[6] if len(row) > 6 else ''
            }
        return None
    
    def get_by_id(self, caixa_id):
        """Busca caixa por ID"""
        result = self.db.execute_query('''
            SELECT c.id, c.usuario_id, c.data_abertura, c.data_fechamento,
                   c.valor_inicial, c.valor_final, c.total_vendas,
                   c.total_cancelamentos, c.total_descontos, c.observacoes,
                   c.status, u.nome as usuario_nome
            FROM caixa c
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE c.id = ?
        ''', (caixa_id,))
        
        if result:
            row = result[0]
            return {
                'id': row[0],
                'usuario_id': row[1],
                'data_abertura': row[2],
                'data_fechamento': row[3] if row[3] else None,
                'valor_inicial': row[4],
                'valor_final': row[5] if row[5] else 0,
                'total_vendas': row[6] if row[6] else 0,
                'total_cancelamentos': row[7] if row[7] else 0,
                'total_descontos': row[8] if row[8] else 0,
                'observacoes': row[9] if len(row) > 9 else '',
                'status': row[10] if len(row) > 10 else 'Aberto',
                'usuario_nome': row[11] if len(row) > 11 else ''
            }
        return None
    
    def calcular_totais_dia(self, data_abertura):
        """Calcula totais de vendas do dia"""
        data_abertura_date = datetime.strptime(data_abertura, '%Y-%m-%d %H:%M:%S').date()
        data_str = data_abertura_date.strftime('%Y-%m-%d')
        
        # Total de vendas finalizadas
        vendas_result = self.db.execute_query('''
            SELECT COALESCE(SUM(valor_final), 0) as total
            FROM vendas
            WHERE DATE(data_venda) = ? AND status = 'Finalizada'
        ''', (data_str,))
        total_vendas = vendas_result[0][0] if vendas_result and vendas_result[0][0] else 0
        
        # Total de cancelamentos
        cancelamentos_result = self.db.execute_query('''
            SELECT COALESCE(SUM(valor_final), 0) as total
            FROM vendas
            WHERE DATE(data_venda) = ? AND status = 'Cancelada'
        ''', (data_str,))
        total_cancelamentos = cancelamentos_result[0][0] if cancelamentos_result and cancelamentos_result[0][0] else 0
        
        # Total de descontos
        descontos_result = self.db.execute_query('''
            SELECT COALESCE(SUM(desconto), 0) as total
            FROM vendas
            WHERE DATE(data_venda) = ? AND status = 'Finalizada'
        ''', (data_str,))
        total_descontos = descontos_result[0][0] if descontos_result and descontos_result[0][0] else 0
        
        return {
            'total_vendas': total_vendas,
            'total_cancelamentos': total_cancelamentos,
            'total_descontos': total_descontos
        }
    
    def get_resumo_dia(self, data_abertura=None):
        """Retorna resumo do dia"""
        if not data_abertura:
            data_abertura = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data_abertura_date = datetime.strptime(data_abertura, '%Y-%m-%d %H:%M:%S').date()
        data_str = data_abertura_date.strftime('%Y-%m-%d')
        
        totais = self.calcular_totais_dia(data_abertura)
        
        # Contar número de vendas
        num_vendas_result = self.db.execute_query('''
            SELECT COUNT(*) as total
            FROM vendas
            WHERE DATE(data_venda) = ? AND status = 'Finalizada'
        ''', (data_str,))
        num_vendas = num_vendas_result[0][0] if num_vendas_result else 0
        
        # Contar número de cancelamentos
        num_cancelamentos_result = self.db.execute_query('''
            SELECT COUNT(*) as total
            FROM vendas
            WHERE DATE(data_venda) = ? AND status = 'Cancelada'
        ''', (data_str,))
        num_cancelamentos = num_cancelamentos_result[0][0] if num_cancelamentos_result else 0
        
        return {
            'data': data_str,
            'total_vendas': totais['total_vendas'],
            'total_cancelamentos': totais['total_cancelamentos'],
            'total_descontos': totais['total_descontos'],
            'num_vendas': num_vendas,
            'num_cancelamentos': num_cancelamentos
        }
    
    def list_caixas(self, data_inicio=None, data_fim=None):
        """Lista todos os caixas"""
        query = '''
            SELECT c.id, c.data_abertura, c.data_fechamento, c.valor_inicial,
                   c.valor_final, c.total_vendas, c.status, u.nome as usuario_nome
            FROM caixa c
            LEFT JOIN usuarios u ON c.usuario_id = u.id
            WHERE 1=1
        '''
        params = []
        
        if data_inicio:
            query += ' AND DATE(c.data_abertura) >= ?'
            params.append(data_inicio)
        
        if data_fim:
            query += ' AND DATE(c.data_abertura) <= ?'
            params.append(data_fim)
        
        query += ' ORDER BY c.data_abertura DESC'
        
        return self.db.execute_query(query, tuple(params) if params else None)

