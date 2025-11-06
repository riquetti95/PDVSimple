"""
Módulo de backup automático do banco de dados
"""
import os
import shutil
from datetime import datetime
import sqlite3

def fazer_backup_banco(db_path='data/pdv.db'):
    """
    Cria backup do banco de dados na pasta AppData
    Retorna True se sucesso, False caso contrário
    """
    try:
        # Verificar se o banco existe
        if not os.path.exists(db_path):
            return False
        
        # Obter pasta AppData do usuário
        appdata_path = os.getenv('APPDATA')
        if not appdata_path:
            # Fallback para Linux/Mac
            appdata_path = os.path.expanduser('~/.local/share')
        
        # Criar pasta SimpleVendas no AppData se não existir
        backup_dir = os.path.join(appdata_path, 'SimpleVendas')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Nome do arquivo de backup (sempre o mesmo, sobrescreve)
        backup_file = os.path.join(backup_dir, 'pdv_backup.db')
        
        # Verificar se o banco está acessível (não está em uso)
        try:
            # Tentar conectar para verificar se não está bloqueado
            conn = sqlite3.connect(db_path)
            conn.close()
        except sqlite3.OperationalError:
            # Banco pode estar em uso, tentar mesmo assim
            pass
        
        # Copiar o banco
        shutil.copy2(db_path, backup_file)
        
        # Criar arquivo de informação do backup
        info_file = os.path.join(backup_dir, 'backup_info.txt')
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"Último backup: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Origem: {os.path.abspath(db_path)}\n")
            f.write(f"Destino: {backup_file}\n")
        
        return True
    except Exception as e:
        print(f"Erro ao fazer backup: {str(e)}")
        return False

def get_backup_path():
    """Retorna o caminho do arquivo de backup"""
    appdata_path = os.getenv('APPDATA')
    if not appdata_path:
        appdata_path = os.path.expanduser('~/.local/share')
    
    backup_dir = os.path.join(appdata_path, 'SimpleVendas')
    return os.path.join(backup_dir, 'pdv_backup.db')

def restaurar_backup(backup_path=None, destino='data/pdv.db'):
    """
    Restaura backup do banco de dados
    Retorna True se sucesso, False caso contrário
    """
    try:
        if backup_path is None:
            backup_path = get_backup_path()
        
        if not os.path.exists(backup_path):
            return False
        
        # Criar pasta destino se não existir
        destino_dir = os.path.dirname(destino)
        if destino_dir and not os.path.exists(destino_dir):
            os.makedirs(destino_dir)
        
        # Copiar backup para destino
        shutil.copy2(backup_path, destino)
        return True
    except Exception as e:
        print(f"Erro ao restaurar backup: {str(e)}")
        return False

