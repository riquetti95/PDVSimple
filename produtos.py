"""
Módulo de gerenciamento de produtos
"""
from database import Database

class Produtos:
    def __init__(self):
        self.db = Database()
    
    def create(self, dados):
        """Cria um novo produto"""
        # Validações
        if not dados.get('descricao', '').strip():
            raise ValueError("A descrição do produto é obrigatória!")
        
        preco_venda = dados.get('preco_venda', 0)
        if preco_venda < 0:
            raise ValueError("O preço de venda não pode ser negativo!")
        
        estoque_atual = dados.get('estoque_atual', 0)
        if estoque_atual < 0:
            raise ValueError("O estoque atual não pode ser negativo!")
        
        estoque_minimo = dados.get('estoque_minimo', 0)
        if estoque_minimo < 0:
            raise ValueError("O estoque mínimo não pode ser negativo!")
        
        # Verificar se código já existe (se informado)
        codigo = dados.get('codigo', '').strip()
        if codigo:
            existing = self.db.execute_query('SELECT id FROM produtos WHERE codigo = ?', (codigo,))
            if existing:
                raise ValueError(f"Já existe um produto com o código {codigo}!")
        
        try:
            return self.db.execute_insert('''
                INSERT INTO produtos (
                    codigo, descricao, categoria, unidade, preco_venda,
                    preco_custo, estoque_atual, estoque_minimo, foto_path, ativo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                codigo,
                dados.get('descricao', '').strip(),
                dados.get('categoria', '').strip(),
                dados.get('unidade', 'UN').strip(),
                preco_venda,
                dados.get('preco_custo', 0),
                estoque_atual,
                estoque_minimo,
                dados.get('foto_path', ''),
                dados.get('ativo', 1)
            ))
        except Exception as e:
            raise Exception(f"Erro ao criar produto: {str(e)}")
    
    def update(self, produto_id, dados):
        """Atualiza um produto"""
        # Validações
        if not produto_id:
            raise ValueError("ID do produto não informado!")
        
        # Verificar se produto existe
        produto = self.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado!")
        
        if not dados.get('descricao', '').strip():
            raise ValueError("A descrição do produto é obrigatória!")
        
        preco_venda = dados.get('preco_venda', 0)
        if preco_venda < 0:
            raise ValueError("O preço de venda não pode ser negativo!")
        
        estoque_minimo = dados.get('estoque_minimo', 0)
        if estoque_minimo < 0:
            raise ValueError("O estoque mínimo não pode ser negativo!")
        
        # Verificar se código já existe em outro produto (se informado)
        codigo = dados.get('codigo', '').strip()
        if codigo:
            existing = self.db.execute_query('SELECT id FROM produtos WHERE codigo = ? AND id != ?', (codigo, produto_id))
            if existing:
                raise ValueError(f"Já existe outro produto com o código {codigo}!")
        
        try:
            self.db.execute_query('''
                UPDATE produtos SET
                    codigo = ?,
                    descricao = ?,
                    categoria = ?,
                    unidade = ?,
                    preco_venda = ?,
                    preco_custo = ?,
                    estoque_minimo = ?,
                    foto_path = ?,
                    ativo = ?
                WHERE id = ?
            ''', (
                codigo,
                dados.get('descricao', '').strip(),
                dados.get('categoria', '').strip(),
                dados.get('unidade', 'UN').strip(),
                preco_venda,
                dados.get('preco_custo', 0),
                estoque_minimo,
                dados.get('foto_path', ''),
                dados.get('ativo', 1),
                produto_id
            ))
        except Exception as e:
            raise Exception(f"Erro ao atualizar produto: {str(e)}")
    
    def get_by_id(self, produto_id):
        """Busca produto por ID"""
        result = self.db.execute_query('SELECT * FROM produtos WHERE id = ?', (produto_id,))
        if result:
            row = result[0]
            # Ordem das colunas: id, codigo, descricao, categoria, unidade, 
            # preco_venda, preco_custo, estoque_atual, estoque_minimo, 
            # ativo, created_at, foto_path
            # Verificar quantas colunas existem
            if len(row) >= 12:
                # Banco com foto_path (posição 11)
                foto_path = row[11] if row[11] else ''
                ativo = row[9]
            elif len(row) >= 11:
                # Banco sem foto_path mas com created_at
                foto_path = ''
                ativo = row[9]
            else:
                # Banco antigo
                foto_path = ''
                ativo = row[9] if len(row) > 9 else 1
            
            return {
                'id': row[0],
                'codigo': row[1],
                'descricao': row[2],
                'categoria': row[3],
                'unidade': row[4],
                'preco_venda': row[5],
                'preco_custo': row[6],
                'estoque_atual': row[7],
                'estoque_minimo': row[8],
                'ativo': ativo,
                'foto_path': foto_path
            }
        return None
    
    def get_by_codigo(self, codigo):
        """Busca produto por código"""
        result = self.db.execute_query('SELECT * FROM produtos WHERE codigo = ? AND ativo = 1', (codigo,))
        if result:
            row = result[0]
            # Ordem das colunas: id, codigo, descricao, categoria, unidade, 
            # preco_venda, preco_custo, estoque_atual, estoque_minimo, 
            # ativo, created_at, foto_path
            if len(row) >= 12:
                foto_path = row[11] if row[11] else ''
                ativo = row[9]
            elif len(row) >= 11:
                foto_path = ''
                ativo = row[9]
            else:
                foto_path = ''
                ativo = row[9] if len(row) > 9 else 1
            
            return {
                'id': row[0],
                'codigo': row[1],
                'descricao': row[2],
                'categoria': row[3],
                'unidade': row[4],
                'preco_venda': row[5],
                'preco_custo': row[6],
                'estoque_atual': row[7],
                'estoque_minimo': row[8],
                'ativo': ativo,
                'foto_path': foto_path
            }
        return None
    
    def list_all(self, search='', apenas_ativos=True, incluir_estoque_minimo=False):
        """Lista todos os produtos com busca opcional"""
        if incluir_estoque_minimo:
            # Para estoque, incluir estoque_minimo
            if apenas_ativos:
                if search:
                    return self.db.execute_query('''
                        SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, estoque_minimo, unidade
                        FROM produtos
                        WHERE ativo = 1 AND (codigo LIKE ? OR descricao LIKE ?)
                        ORDER BY descricao
                    ''', (f'%{search}%', f'%{search}%'))
                else:
                    return self.db.execute_query('''
                        SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, estoque_minimo, unidade
                        FROM produtos
                        WHERE ativo = 1
                        ORDER BY descricao
                    ''')
            else:
                if search:
                    return self.db.execute_query('''
                        SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, estoque_minimo, unidade, ativo
                        FROM produtos
                        WHERE codigo LIKE ? OR descricao LIKE ?
                        ORDER BY descricao
                    ''', (f'%{search}%', f'%{search}%'))
                else:
                    return self.db.execute_query('''
                        SELECT id, codigo, descricao, categoria, preco_venda, estoque_atual, estoque_minimo, unidade, ativo
                        FROM produtos
                        ORDER BY descricao
                    ''')
        else:
            # Versão padrão sem estoque_minimo
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

