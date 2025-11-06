"""
Script de migração do banco de dados
Move o banco da raiz para a pasta data/
"""
import os
import shutil

def migrate_database():
    """Move o banco de dados da raiz para data/"""
    old_path = 'pdv.db'
    data_dir = 'data'
    new_path = os.path.join(data_dir, 'pdv.db')
    
    # Criar pasta data se não existir
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✓ Pasta '{data_dir}' criada")
    
    # Verificar se o banco antigo existe
    if os.path.exists(old_path):
        # Verificar se já existe na nova localização
        if os.path.exists(new_path):
            print(f"⚠ Aviso: O banco já existe em '{new_path}'")
            resposta = input("Deseja substituir? (s/N): ").lower()
            if resposta != 's':
                print("Migração cancelada.")
                return False
        
        # Mover o banco
        try:
            shutil.move(old_path, new_path)
            print(f"✓ Banco de dados movido de '{old_path}' para '{new_path}'")
            return True
        except Exception as e:
            print(f"✗ Erro ao mover banco: {str(e)}")
            return False
    else:
        print(f"ℹ Banco '{old_path}' não encontrado na raiz.")
        print(f"  O sistema usará '{new_path}' (será criado automaticamente)")
        return True

if __name__ == "__main__":
    print("=" * 50)
    print("Migração do Banco de Dados")
    print("=" * 50)
    print()
    migrate_database()
    print()
    print("Migração concluída!")

