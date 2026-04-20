@echo off
REM ============================================================================
REM GESTOR DE ALMACENES - INSTALACION DE DEPENDENCIAS
REM ============================================================================

echo.
echo ============================================================================
echo INSTALADOR DE DEPENDENCIAS
echo ============================================================================
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar que Python este disponible
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python desde https://www.python.org/downloads/
    echo.
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo Versión de Python:
python --version
echo.

echo Instalando openpyxl...
pip install openpyxl -q

echo Instalando Pillow (para el logo)...
pip install Pillow -q

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: No se pudo instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo Instalacion completada exitosamente!
echo ============================================================================
echo.
echo Proximos pasos:
echo   1. Coloca logo.png en esta carpeta (opcional)
echo   2. Ejecuta INICIAR.bat para abrir la aplicacion
echo   3. (Opcional) Ejecuta CREAR_EJECUTABLE.bat para crear un .exe standalone
echo.
pause
