"""
Módulo de configuração da empresa
"""
from database import Database
import os
import shutil

class EmpresaConfig:
    def __init__(self):
        self.db = Database()
    
    def get_config(self):
        """Retorna a configuração da empresa"""
        result = self.db.execute_query('SELECT * FROM empresa LIMIT 1')
        if result:
            config = {
                'id': result[0][0],
                'razao_social': result[0][1],
                'nome_fantasia': result[0][2],
                'cnpj': result[0][3],
                'inscricao_estadual': result[0][4],
                'telefone': result[0][5],
                'email': result[0][6],
                'endereco': result[0][7],
                'numero': result[0][8],
                'complemento': result[0][9],
                'bairro': result[0][10],
                'cidade': result[0][11],
                'estado': result[0][12],
                'cep': result[0][13],
                'logo_path': result[0][14]
            }
            return config
        return None
    
    def save_config(self, dados, logo_path=None):
        """Salva ou atualiza a configuração da empresa"""
        config = self.get_config()
        
        # Se houver logo, copiar para pasta de assets
        if logo_path and os.path.exists(logo_path):
            assets_dir = 'assets'
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
            
            logo_filename = os.path.basename(logo_path)
            dest_path = os.path.join(assets_dir, logo_filename)
            shutil.copy2(logo_path, dest_path)
            dados['logo_path'] = dest_path
        elif config and config.get('logo_path'):
            dados['logo_path'] = config['logo_path']
        
        if config:
            # Atualizar
            self.db.execute_query('''
                UPDATE empresa SET
                    razao_social = ?,
                    nome_fantasia = ?,
                    cnpj = ?,
                    inscricao_estadual = ?,
                    telefone = ?,
                    email = ?,
                    endereco = ?,
                    numero = ?,
                    complemento = ?,
                    bairro = ?,
                    cidade = ?,
                    estado = ?,
                    cep = ?,
                    logo_path = ?
                WHERE id = ?
            ''', (
                dados.get('razao_social', ''),
                dados.get('nome_fantasia', ''),
                dados.get('cnpj', ''),
                dados.get('inscricao_estadual', ''),
                dados.get('telefone', ''),
                dados.get('email', ''),
                dados.get('endereco', ''),
                dados.get('numero', ''),
                dados.get('complemento', ''),
                dados.get('bairro', ''),
                dados.get('cidade', ''),
                dados.get('estado', ''),
                dados.get('cep', ''),
                dados.get('logo_path', ''),
                config['id']
            ))
        else:
            # Inserir
            self.db.execute_insert('''
                INSERT INTO empresa (
                    razao_social, nome_fantasia, cnpj, inscricao_estadual,
                    telefone, email, endereco, numero, complemento,
                    bairro, cidade, estado, cep, logo_path
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dados.get('razao_social', ''),
                dados.get('nome_fantasia', ''),
                dados.get('cnpj', ''),
                dados.get('inscricao_estadual', ''),
                dados.get('telefone', ''),
                dados.get('email', ''),
                dados.get('endereco', ''),
                dados.get('numero', ''),
                dados.get('complemento', ''),
                dados.get('bairro', ''),
                dados.get('cidade', ''),
                dados.get('estado', ''),
                dados.get('cep', ''),
                dados.get('logo_path', '')
            ))

