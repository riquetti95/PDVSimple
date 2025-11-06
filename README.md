# SimpleVendas - Sistema de Vendas para Lojas de Conserto de Moto

Sistema completo de vendas desenvolvido em Python para lojas de conserto de moto, com controle de vendas, estoque, orçamentos e cupom não fiscal.

## Características

- ✅ **Configuração da Empresa**: Cadastro completo com dados, logo e endereço
- ✅ **Sistema de Login**: Autenticação de usuários
- ✅ **Níveis de Acesso**: Vendedor, Conferente, Gerente e Admin
- ✅ **Controle de Orçamentos**: Criação, aprovação e conversão em vendas
- ✅ **Controle de Estoque**: Saída automática na venda, reversão no cancelamento
- ✅ **Cadastro de Clientes**: Gestão completa de clientes
- ✅ **Cadastro de Produtos**: Gestão de produtos com controle de estoque
- ✅ **Cupom Não Fiscal**: Geração e impressão de cupons
- ✅ **Banco de Dados Offline**: SQLite local, não requer conexão

## Requisitos

- Python 3.7 ou superior
- Bibliotecas padrão do Python (tkinter, sqlite3)

## Instalação

1. Clone ou baixe o repositório
2. Certifique-se de ter Python instalado
3. Execute o arquivo `main.py`:

```bash
python main.py
```

## Primeiro Acesso

**Usuário padrão:**
- Usuário: `admin`
- Senha: `admin123`
- Nível: Admin

⚠️ **Importante**: Altere a senha padrão após o primeiro acesso!

## Estrutura do Projeto

```
PDVSimple/
├── main.py                 # Arquivo principal
├── database.py             # Gerenciamento do banco de dados
├── auth.py                 # Autenticação e controle de acesso
├── empresa_config.py       # Configuração da empresa
├── clientes.py             # Gerenciamento de clientes
├── produtos.py             # Gerenciamento de produtos
├── estoque.py              # Controle de estoque
├── orcamentos.py           # Controle de orçamentos
├── vendas.py               # Gerenciamento de vendas
├── cupom.py                # Geração de cupom não fiscal
├── data/                   # Pasta de dados (banco de dados)
│   └── pdv.db              # Banco SQLite (criado automaticamente)
├── assets/                 # Recursos (logos, ícones)
├── migrate_db.py           # Script de migração do banco
├── ui_login.py             # Tela de login
├── ui_main.py              # Tela principal
├── ui_cadastros_panel.py   # Painel de cadastros
├── ui_vendas_panel.py      # Painel de vendas
├── ui_orcamentos_panel.py  # Painel de orçamentos
├── ui_estoque_panel.py     # Painel de estoque
├── ui_config_empresa.py    # Configuração da empresa
├── ui_usuarios.py          # Gerenciamento de usuários
└── ui_*.py                 # Outras telas auxiliares
```

## Funcionalidades por Nível de Acesso

### Vendedor
- Realizar vendas
- Criar orçamentos
- Consultar produtos e clientes
- Visualizar estoque

### Conferente
- Todas as funções do Vendedor
- Ajustar estoque
- Visualizar movimentações

### Gerente
- Todas as funções do Conferente
- Configurar dados da empresa
- Aprovar orçamentos
- Cancelar vendas

### Admin
- Todas as funções do Gerente
- Gerenciar usuários
- Acesso total ao sistema

## Controle de Estoque

O sistema possui controle automático de estoque:
- **Venda**: Estoque é baixado automaticamente
- **Cancelamento de Venda**: Estoque é revertido automaticamente
- **Ajustes Manuais**: Disponível para conferentes e superiores

## Geração de Executável (.exe)

### Método 1: Usando o script automático (Recomendado)

**Windows:**
```bash
build.bat
```
O script criará automaticamente o ícone se não existir!

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

**Python:**
```bash
python build_exe.py
```

### Criar o Ícone do SimpleVendas

Para criar o ícone personalizado:
```bash
python criar_icon.py
```

Isso criará um arquivo `icon.ico` com:
- Fundo azul gradiente
- Carrinho de compras branco
- Iniciais "SV" (SimpleVendas)
- Múltiplos tamanhos (16x16 até 256x256)

### Método 2: Manual

1. Instale o PyInstaller:
```bash
pip install pyinstaller
```

2. Coloque um ícone (opcional):
   - Crie um arquivo `icon.ico` na raiz do projeto, OU
   - Coloque em `assets/icon.ico`

3. Gere o executável:
```bash
# Com ícone
pyinstaller --onefile --windowed --name="SimpleVendas" --icon=icon.ico main.py

# Sem ícone
pyinstaller --onefile --windowed --name="SimpleVendas" main.py
```

O executável estará na pasta `dist/`.

### Criando um ícone (.ico)

Para criar um ícone:
1. Use uma imagem PNG ou JPG
2. Converta para .ico usando ferramentas online como:
   - https://convertio.co/pt/png-ico/
   - https://www.icoconverter.com/
3. Salve como `icon.ico` na raiz do projeto ou em `assets/icon.ico`
4. Tamanho recomendado: 256x256 pixels

## Banco de Dados

O sistema utiliza SQLite como banco de dados local. O arquivo `data/pdv.db` é criado automaticamente na primeira execução na pasta `data/`.

**Estrutura Organizada**: O banco de dados está organizado na pasta `data/` para manter o projeto limpo.

**Migração**: Se você tinha um banco na raiz (`pdv.db`), execute:
```bash
python migrate_db.py
```

**Backup**: ⚠️ Faça backup regular da pasta `data/` para evitar perda de dados!

## Suporte

Para problemas ou dúvidas, verifique:
1. Se o Python está instalado corretamente
2. Se todas as dependências estão disponíveis
3. Se o banco de dados não está corrompido

## Licença

Este projeto é de código aberto e pode ser modificado conforme necessário.

## Desenvolvido com

- Python 3.x
- Tkinter (Interface Gráfica)
- SQLite (Banco de Dados)

---

**Versão**: 1.0
**Data**: 2024
