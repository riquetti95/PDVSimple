@echo off
echo ========================================
echo Gerando Executavel do SimpleVendas
echo ========================================
echo.

REM Verificar se PyInstaller esta instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nao esta instalado!
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo.
echo Gerando executavel...
echo.

REM Verificar se existe icone, se não, criar
if not exist "icon.ico" (
    echo Criando icone do SimpleVendas...
    python criar_icon.py
)

REM Gerar executavel com icone
if exist "icon.ico" (
    echo Usando icone: icon.ico
    python -m PyInstaller main.py --onefile --windowed --name=SimpleVendas --icon=icon.ico --clean --noconfirm
) else if exist "assets\icon.ico" (
    echo Usando icone: assets\icon.ico
    python -m PyInstaller main.py --onefile --windowed --name=SimpleVendas --icon=assets\icon.ico --clean --noconfirm
) else (
    echo Aviso: Nenhum icone encontrado. Gerando sem icone...
    python -m PyInstaller main.py --onefile --windowed --name=SimpleVendas --clean --noconfirm
)

echo.
echo ========================================
echo Executavel gerado na pasta 'dist'!
echo ========================================
pause

