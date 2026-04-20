#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GESTOR DE ALMACENES - INSTALADOR Y VERIFICADOR
Verifica dependencias y crea el ambiente de la aplicacion
"""

import subprocess
import sys
import os


def instalar_dependencias():
    """Instala las dependencias necesarias."""
    print("\n" + "="*80)
    print("INSTALADOR DE DEPENDENCIAS")
    print("="*80 + "\n")
    
    # Verificar openpyxl
    try:
        import openpyxl
        print("[OK] openpyxl ya esta instalado")
        return True
    except ImportError:
        print("[ERROR] openpyxl no esta instalado")
        print("\nInstalando openpyxl...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
            print("\n[OK] openpyxl instalado correctamente")
            return True
        except Exception as e:
            print(f"\n[ERROR] No se pudo instalar openpyxl: {e}")
            print("\nIntenta instalar manualmente con:")
            print("  pip install openpyxl")
            return False


def iniciar_aplicacion():
    """Inicia la aplicacion principal."""
    print("\n" + "="*80)
    print("INICIANDO APLICACION")
    print("="*80 + "\n")
    
    try:
        from main import main
        main()
    except Exception as e:
        print(f"[ERROR] Error al iniciar la aplicacion: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Cambiar al directorio del script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Verificar dependencias
    if instalar_dependencias():
        # Iniciar aplicacion
        iniciar_aplicacion()
    else:
        print("\n[ERROR] No se pudo completar la instalacion")
        sys.exit(1)
