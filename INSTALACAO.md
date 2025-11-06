# Guia de Instalação e Compilação

## Instalação do Sistema

### Requisitos
- Python 3.7 ou superior
- Windows, Linux ou Mac

### Passo a Passo

1. **Baixe ou clone o projeto**

2. **Execute o sistema:**
```bash
python main.py
```

3. **Primeiro acesso:**
   - Usuário: `admin`
   - Senha: `admin123`

## Gerar Executável (.exe)

### Opção 1: Script Automático (Mais Fácil)

**Windows:**
- Clique duas vezes em `build.bat`
- O executável será gerado na pasta `dist/`

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

### Opção 2: Manual

1. **Instale o PyInstaller:**
```bash
pip install pyinstaller
```

2. **Adicione um ícone (opcional):**
   - Crie um arquivo `icon.ico` na raiz do projeto
   - Ou coloque em `assets/icon.ico`
   - Tamanho recomendado: 256x256 pixels

3. **Gere o executável:**
```bash
    # Com ícone
    pyinstaller --onefile --windowed --name="SimpleVendas" --icon=icon.ico main.py

    # Sem ícone
    pyinstaller --onefile --windowed --name="SimpleVendas" main.py
```

### Onde encontrar o executável?

Após a compilação, o arquivo `SimpleVendas.exe` (Windows) estará em:
```
dist/SimpleVendas.exe
```

## Adicionar Ícone ao Executável

### Como criar um arquivo .ico:

1. **Tenha uma imagem:**
   - Formato: PNG, JPG ou qualquer imagem
   - Tamanho recomendado: 256x256 pixels ou maior

2. **Converta para .ico:**
   - Use ferramentas online:
     - https://convertio.co/pt/png-ico/
     - https://www.icoconverter.com/
     - https://icoconvert.com/
   
3. **Salve o arquivo:**
   - Nome: `icon.ico`
   - Localização: Raiz do projeto (mesma pasta do `main.py`)
   - OU em: `assets/icon.ico`

4. **Gere o executável novamente:**
   - O script `build.bat` detectará automaticamente o ícone
   - Ou use: `pyinstaller --icon=icon.ico ...`

## Estrutura de Arquivos Recomendada

```
PDVSimple/
├── main.py
├── icon.ico          ← Ícone do executável (opcional)
├── build.bat         ← Script de compilação Windows
├── build.sh          ← Script de compilação Linux/Mac
├── build_exe.py      ← Script de compilação Python
├── assets/
│   └── icon.ico      ← Ícone alternativo (opcional)
└── dist/
    └── SimpleVendas.exe       ← Executável gerado aqui
```

## Solução de Problemas

### Erro: "PyInstaller não encontrado"
```bash
pip install pyinstaller
```

### Ícone não aparece no executável
- Verifique se o arquivo é realmente .ico (não .png renomeado)
- Use um conversor online para garantir formato correto
- Tamanho recomendado: 256x256 pixels

### Executável muito grande
- Normal para aplicações Python
- Use `--onefile` para um único arquivo
- O executável inclui o Python e todas as bibliotecas

### Erro ao executar o .exe
- Verifique se todas as dependências estão instaladas
- Teste primeiro com `python main.py`
- Verifique se o banco de dados está acessível

