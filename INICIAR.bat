@echo off
REM ============================================================================
REM GESTOR DE ALMACENES - INICIAR APLICACION
REM ============================================================================

cd /d "%~dp0"

echo.
echo ============================================================================
echo GESTOR DE ALMACENES
echo ============================================================================
echo.
echo Iniciando aplicacion...
echo.

REM Intentar ejecutar con python
python main.py

REM Si hay error, mostrar mensaje
if %ERRORLEVEL% neq 0 (
    echo.
    echo ============================================================================
    echo ERROR: No se pudo iniciar la aplicacion
    echo ============================================================================
    echo.
    echo Por favor verifica que:
    echo 1. Python este instalado correctamente
    echo 2. Las dependencias esten instaladas (ejecuta INSTALAR.bat)
    echo 3. Tkinter este disponible en tu sistema
    echo.
    echo Para mas informacion, revisa el archivo README.md
    echo.
    pause
)

