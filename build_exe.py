"""
Script para gerar executável (.exe) do SimpleVendas
"""
import PyInstaller.__main__
import os

# Verificar se PyInstaller está instalado
try:
    import PyInstaller
except ImportError:
    print("PyInstaller não está instalado!")
    print("Instale com: pip install pyinstaller")
    exit(1)

# Caminho do ícone (se existir, senão criar)
icon_path = None
if os.path.exists("icon.ico"):
    icon_path = "icon.ico"
elif os.path.exists("assets/icon.ico"):
    icon_path = "assets/icon.ico"
else:
    # Tentar criar o ícone
    try:
        from criar_icon import criar_icone
        print("Criando ícone do SimpleVendas...")
        if criar_icone():
            icon_path = "icon.ico"
    except:
        pass

# Parâmetros do PyInstaller
params = [
    'main.py',
    '--onefile',                    # Um único arquivo executável
    '--windowed',                    # Sem console (interface gráfica)
    '--name=SimpleVendas',          # Nome do executável
    '--clean',                       # Limpar cache antes de construir
    '--noconfirm',                   # Não pedir confirmação
]

# Adicionar ícone se existir
if icon_path:
    params.append(f'--icon={icon_path}')
    print(f"Usando ícone: {icon_path}")
else:
    print("Aviso: Nenhum ícone encontrado. Use icon.ico ou assets/icon.ico")

# Adicionar arquivos de dados se necessário
if os.path.exists("assets"):
    params.append('--add-data=assets;assets')

# Executar PyInstaller
print("Gerando executável...")
PyInstaller.__main__.run(params)

print("\nExecutável gerado na pasta 'dist'!")

