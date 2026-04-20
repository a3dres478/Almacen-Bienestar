@echo off
REM ============================================================================
REM Crear acceso directo en el escritorio
REM ============================================================================

setlocal enabledelayedexpansion

REM Obtener la ruta actual
set "app_path=%~dp0"
set "desktop=%USERPROFILE%\Desktop"

REM Crear el acceso directo usando PowerShell
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $lnk = $ws.CreateShortcut('%desktop%\Gestor de Almacenes.lnk'); ^
   $lnk.TargetPath = '%app_path%INICIAR.bat'; ^
   $lnk.WorkingDirectory = '%app_path%'; ^
   $lnk.Description = 'Gestor de Almacenes - Sistema Local'; ^
   $lnk.Save();"

if %ERRORLEVEL% equ 0 (
    echo.
    echo Acceso directo creado exitosamente en:
    echo %desktop%\Gestor de Almacenes.lnk
    echo.
    echo Ahora puedes hacer doble click en el escritorio para abrir la aplicacion
) else (
    echo.
    echo ERROR: No se pudo crear el acceso directo
    echo Por favor crea uno manualmente:
    echo 1. Haz click derecho en INICIAR.bat
    echo 2. Elige "Enviar a" - "Escritorio (crear acceso directo)"
)

pause
