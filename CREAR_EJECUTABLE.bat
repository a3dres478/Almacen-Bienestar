@echo off
REM ============================================================================
REM CREAR EJECUTABLE PORTABLE
REM ============================================================================

echo.
echo ============================================================================
echo CONSTRUCTOR DE GESTOR DE ALMACENES PORTABLE
echo ============================================================================
echo.
echo Este script creara un ejecutable independiente (no necesita Python)
echo.

cd /d "%~dp0"

REM Verificar Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

REM Instalar PyInstaller
echo Instalando PyInstaller...
python -m pip install pyinstaller -q

REM Instalar Pillow
echo Instalando Pillow...
python -m pip install Pillow -q

REM Crear ejecutable
echo.
echo Creando ejecutable... (esto puede tomar tiempo)
echo.

python -m PyInstaller --onefile --windowed --name=GestorAlmacenes ^
    --hidden-import=openpyxl --hidden-import=PIL ^
    --add-data "data;data" --add-data "templates;templates" ^
    --add-data "logo.png;." ^
    main.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================================
    echo EXITO! Ejecutable creado
    echo ============================================================================
    echo.
    echo Ubicacion: dist\GestorAlmacenes.exe
    echo.
    echo Puedes distribuir este archivo sin necesidad de que el usuario instale Python
    echo.
) else (
    echo.
    echo ERROR: No se pudo crear el ejecutable
    echo.
)

pause
