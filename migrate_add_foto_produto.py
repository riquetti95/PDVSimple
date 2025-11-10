"""
Script de migração para adicionar campo de foto aos produtos
"""
import sqlite3
import os

def migrate():
    """Adiciona campo foto_path à tabela produtos se não existir"""
    db_path = os.path.join('data', 'pdv.db')
    
    if not os.path.exists(db_path):
        print("Banco de dados não encontrado!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar se a coluna já existe
        cursor.execute("PRAGMA table_info(produtos)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'foto_path' not in columns:
            print("Adicionando coluna foto_path a tabela produtos...")
            cursor.execute('ALTER TABLE produtos ADD COLUMN foto_path TEXT')
            conn.commit()
            print("Coluna foto_path adicionada com sucesso!")
        else:
            print("Coluna foto_path ja existe!")
        
        # Criar pasta para fotos se não existir
        fotos_dir = os.path.join('data', 'fotos_produtos')
        if not os.path.exists(fotos_dir):
            os.makedirs(fotos_dir)
            print(f"Pasta {fotos_dir} criada!")
        
    except Exception as e:
        print(f"Erro na migração: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()

