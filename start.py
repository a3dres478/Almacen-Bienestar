#!/usr/bin/env python
"""
============================================================================
GESTOR DE ALMACENES - ARCHIVO DE INICIO
============================================================================

Ejecuta este script para iniciar la aplicacion de manera facil
"""

import os
import sys
import subprocess

def main():
    print("\n" + "="*80)
    print("GESTOR DE ALMACENES - INICIO")
    print("="*80 + "\n")
    
    # Verificar si openpyxl está instalado
    try:
        import openpyxl
        print("[OK] Dependencias verificadas")
    except ImportError:
        print("[ERROR] openpyxl no está instalado")
        print("\nInstalando dependencias...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[OK] Dependencias instaladas\n")
    
    # Mensaje de inicio
    print("\nIniciando aplicacion...")
    print("-" * 80)
    
    try:
        # Importar y ejecutar la aplicacion
        from main import main as run_app
        run_app()
    except Exception as e:
        print(f"\n[ERROR] Error al iniciar la aplicacion: {e}")
        print("\nIntentando solucionar...")
        print("1. Verifica que openpyxl este instalado: pip install openpyxl")
        print("2. Verifica que tkinter este disponible en tu sistema")
        print("3. Si el problema persiste, ejecuta: python test_example.py")


if __name__ == "__main__":
    main()
