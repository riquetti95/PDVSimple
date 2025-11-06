#!/bin/bash

echo "========================================"
echo "Gerando Executável do SimpleVendas"
echo "========================================"
echo ""

# Verificar se PyInstaller está instalado
python3 -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyInstaller não está instalado!"
    echo "Instalando PyInstaller..."
    pip3 install pyinstaller
fi

echo ""
echo "Gerando executável..."
echo ""

# Verificar se existe ícone
if [ -f "icon.ico" ]; then
    python3 -m PyInstaller main.py --onefile --windowed --name=SimpleVendas --icon=icon.ico --clean --noconfirm
elif [ -f "assets/icon.ico" ]; then
    python3 -m PyInstaller main.py --onefile --windowed --name=SimpleVendas --icon=assets/icon.ico --clean --noconfirm
else
    echo "Aviso: Nenhum ícone encontrado. Use icon.ico ou assets/icon.ico"
    python3 -m PyInstaller main.py --onefile --windowed --name=SimpleVendas --clean --noconfirm
fi

echo ""
echo "========================================"
echo "Executável gerado na pasta 'dist'!"
echo "========================================"

