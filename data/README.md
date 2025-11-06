# Pasta de Dados

Esta pasta contém os arquivos de banco de dados do sistema.

## Arquivos

- `pdv.db` - Banco de dados SQLite principal do sistema

## Backup

⚠️ **IMPORTANTE**: Faça backup regular desta pasta para evitar perda de dados!

O banco de dados contém:
- Configurações da empresa
- Usuários e senhas
- Clientes
- Produtos
- Estoque
- Vendas
- Orçamentos

## Migração

Se você tinha um banco na raiz do projeto (`pdv.db`), execute:
```bash
python migrate_db.py
```

Isso moverá o banco para esta pasta automaticamente.

