"""
Script para crear un ejecutable portable de Gestor de Almacenes
Requiere: pyinstaller

INSTRUCCIONES:
1. Asegúrate de que logo.png esté en la carpeta raíz
2. Ejecuta: python build_portable.py
3. Obtendrás un archivo en dist/GestorAlmacenes.exe
"""

import subprocess
import sys
import os
import shutil


def instalar_pyinstaller():
    """Instala PyInstaller si no está disponible."""
    try:
        import PyInstaller
        print("[OK] PyInstaller ya está instalado")
    except ImportError:
        print("[...] Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller instalado")


def crear_ejecutable():
    """Crea el ejecutable portable."""
    print("\n" + "="*80)
    print("CREANDO GESTOR DE ALMACENES PORTABLE")
    print("="*80)
    
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Archivos y carpetas a incluir
    archivos_incluir = [
        ("main.py", "main.py"),
        ("database.py", "database.py"),
        ("logo.png" if os.path.exists(os.path.join(ruta_actual, "logo.png")) else None, "logo.png"),
    ]
    
    archivos_incluir = [(src, dst) for src, dst in archivos_incluir if src]
    
    # Comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                                    # Un solo archivo ejecutable
        "--windowed",                                   # Sin ventana de consola
        f"--name=GestorAlmacenes",                     # Nombre del ejecutable
        f"--icon=logo.png" if os.path.exists(os.path.join(ruta_actual, "logo.png")) else "",
        "--hidden-import=openpyxl",                    # Incluir openpyxl
        "--hidden-import=PIL",                          # Incluir Pillow
        "--add-data", f"data{os.pathsep}data",        # Incluir carpeta data
        "--add-data", f"templates{os.pathsep}templates",  # Incluir carpeta templates
        "--add-data", f"logo.png{os.pathsep}.",       # Incluir logo
        "main.py"
    ]
    
    # Filtrar comandos vacíos
    cmd = [c for c in cmd if c]
    
    print(f"\nEjecutando: {' '.join(cmd)}\n")
    
    try:
        subprocess.check_call(cmd, cwd=ruta_actual)
        print("\n" + "="*80)
        print("[OK] EJECUTABLE CREADO EXITOSAMENTE")
        print("="*80)
        print(f"\nArchivo: {os.path.join(ruta_actual, 'dist', 'GestorAlmacenes.exe')}")
        print("\nYa puedes distribuir este archivo sin necesidad de que el usuario instale Python!")
        print("[!] Asegúrate de que data/almacen.xlsx esté en la misma carpeta")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] No se pudo crear el ejecutable: {e}")
        sys.exit(1)


def limpiar():
    """Limpia archivos temporales de build."""
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    
    carpetas_limpiar = [
        os.path.join(ruta_actual, "build"),
        os.path.join(ruta_actual, "__pycache__"),
    ]
    
    archivos_limpiar = [
        os.path.join(ruta_actual, "GestorAlmacenes.spec"),
    ]
    
    for carpeta in carpetas_limpiar:
        if os.path.exists(carpeta):
            print(f"Limpiando {carpeta}...")
            shutil.rmtree(carpeta)
    
    for archivo in archivos_limpiar:
        if os.path.exists(archivo):
            print(f"Eliminando {archivo}...")
            os.remove(archivo)


if __name__ == "__main__":
    # Instalar PyInstaller
    instalar_pyinstaller()
    
    # Crear ejecutable
    crear_ejecutable()
    
    # Limpiar
    print("\nLimpiando archivos temporales...")
    limpiar()
    
    print("\n[*] Proceso completado!")
    print("[*] Tu ejecutable está en: dist/GestorAlmacenes.exe")
