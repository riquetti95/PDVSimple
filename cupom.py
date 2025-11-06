"""
Módulo de geração de cupom não fiscal
"""
from database import Database
from empresa_config import EmpresaConfig
from datetime import datetime

class Cupom:
    def __init__(self):
        self.db = Database()
        self.empresa = EmpresaConfig()
    
    def gerar_cupom(self, venda_id):
        """Gera o texto do cupom não fiscal"""
        venda = self.db.execute_query('''
            SELECT v.id, v.numero, v.cliente_id, v.usuario_id, v.data_venda,
                   v.valor_total, v.desconto, v.valor_final,
                   c.nome as cliente_nome, c.cpf_cnpj, c.endereco, c.cidade, c.estado,
                   u.nome as vendedor
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.id = ?
        ''', (venda_id,))
        
        if not venda:
            return None
        
        ven = venda[0]
        empresa_config = self.empresa.get_config()
        
        # Buscar itens
        itens = self.db.execute_query('''
            SELECT p.descricao, vi.quantidade, vi.preco_unitario, vi.subtotal
            FROM venda_itens vi
            JOIN produtos p ON vi.produto_id = p.id
            WHERE vi.venda_id = ?
        ''', (venda_id,))
        
        # Montar cupom
        cupom = []
        cupom.append("=" * 50)
        cupom.append("SIMPLEVENDAS - CUPOM NÃO FISCAL")
        cupom.append("=" * 50)
        cupom.append("")
        
        if empresa_config:
            if empresa_config.get('nome_fantasia'):
                cupom.append(empresa_config['nome_fantasia'])
            if empresa_config.get('razao_social'):
                cupom.append(empresa_config['razao_social'])
            if empresa_config.get('cnpj'):
                cupom.append(f"CNPJ: {empresa_config['cnpj']}")
            if empresa_config.get('endereco'):
                endereco = empresa_config['endereco']
                if empresa_config.get('numero'):
                    endereco += f", {empresa_config['numero']}"
                cupom.append(endereco)
                if empresa_config.get('bairro'):
                    cupom.append(empresa_config['bairro'])
                cidade = empresa_config.get('cidade', '')
                if empresa_config.get('estado'):
                    cidade += f" - {empresa_config['estado']}"
                if cidade:
                    cupom.append(cidade)
                if empresa_config.get('cep'):
                    cupom.append(f"CEP: {empresa_config['cep']}")
            if empresa_config.get('telefone'):
                cupom.append(f"Tel: {empresa_config['telefone']}")
        
        cupom.append("")
        cupom.append("-" * 50)
        cupom.append(f"Venda: {ven[1]}")  # numero
        try:
            data_str = datetime.strptime(ven[4], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
        except:
            data_str = str(ven[4])
        cupom.append(f"Data: {data_str}")
        cupom.append(f"Vendedor: {ven[13] if len(ven) > 13 else 'N/A'}")
        cupom.append("-" * 50)
        cupom.append("")
        
        if ven[2]:  # cliente_id
            cupom.append(f"Cliente: {ven[8] if len(ven) > 8 else 'N/A'}")
            if len(ven) > 9 and ven[9]:  # cpf_cnpj
                cupom.append(f"CPF/CNPJ: {ven[9]}")
            cupom.append("")
        
        cupom.append("ITENS:")
        cupom.append("-" * 50)
        
        total = 0
        for item in itens:
            descricao = item[0][:30] if item[0] else ""  # Limitar tamanho
            quantidade = item[1]
            preco_unit = item[2]
            subtotal = item[3]
            total += subtotal
            
            cupom.append(f"{descricao}")
            cupom.append(f"  {quantidade} x R$ {preco_unit:.2f} = R$ {subtotal:.2f}")
        
        cupom.append("-" * 50)
        cupom.append(f"SUBTOTAL: R$ {ven[5]:.2f}")  # valor_total
        
        if len(ven) > 6 and ven[6] > 0:  # desconto
            cupom.append(f"DESCONTO: R$ {ven[6]:.2f}")
        
        cupom.append(f"TOTAL: R$ {ven[7]:.2f}")  # valor_final
        cupom.append("")
        cupom.append("=" * 50)
        cupom.append("OBRIGADO PELA PREFERÊNCIA!")
        cupom.append("=" * 50)
        
        return "\n".join(cupom)
    
    def salvar_cupom(self, venda_id, caminho=None):
        """Salva o cupom em um arquivo de texto"""
        cupom_texto = self.gerar_cupom(venda_id)
        if not cupom_texto:
            return False
        
        if not caminho:
            caminho = f"cupons/cupom_{venda_id}.txt"
        
        import os
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(cupom_texto)
        
        return True
    
    def imprimir_cupom(self, venda_id):
        """Imprime o cupom (pode ser adaptado para impressora)"""
        cupom_texto = self.gerar_cupom(venda_id)
        if not cupom_texto:
            return False
        
        # Por enquanto, apenas retorna o texto
        # Pode ser adaptado para usar biblioteca de impressão
        return cupom_texto

