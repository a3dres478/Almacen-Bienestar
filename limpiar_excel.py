#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar el archivo Excel almacen.xlsx
- Elimina todos los datos de Productos y Movimientos (mantiene encabezados)
- Elimina la hoja Reportes
"""

import os
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def limpiar_excel():
    """Limpia el archivo Excel."""
    ruta_excel = os.path.join(os.path.dirname(__file__), "data", "almacen.xlsx")
    return limpiar_datos_operativos(ruta_excel)


def limpiar_datos_operativos(ruta_excel):
    """
    Limpia únicamente los datos operativos del archivo Excel indicado.
    No modifica estructura, encabezados, configuraciones ni hojas existentes.
    Puede ser llamada de forma segura desde otros módulos.
    Args:
        ruta_excel (str): Ruta absoluta al archivo Excel a limpiar.
    Returns:
        bool: True si la limpieza fue exitosa, False si hubo error.
    """
    if not os.path.exists(ruta_excel):
        print(f"❌ Error: El archivo {ruta_excel} no existe")
        return False
    try:
        wb = load_workbook(ruta_excel)
        # Limpiar hoja Productos (mantener encabezados)
        if "Productos" in wb.sheetnames:
            ws_productos = wb["Productos"]
            # Eliminar filas de datos (desde fila 2)
            for row in range(2, ws_productos.max_row + 1):
                ws_productos.delete_rows(2)
            print("✅ Hoja 'Productos' limpiada (encabezados mantenidos)")
        # Limpiar hoja Movimientos (mantener encabezados)
        if "Movimientos" in wb.sheetnames:
            ws_movimientos = wb["Movimientos"]
            for row in range(2, ws_movimientos.max_row + 1):
                ws_movimientos.delete_rows(2)
            print("✅ Hoja 'Movimientos' limpiada (encabezados mantenidos)")
        wb.save(ruta_excel)
        print(f"\n✅ Archivo limpiado exitosamente: {ruta_excel}")
        return True
    except Exception as e:
        print(f"❌ Error al limpiar Excel: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Limpiador de Base de Datos Excel")
    print("=" * 60)
    
    if limpiar_excel():
        print("\n✅ La base de datos está lista para nuevas pruebas")
    else:
        print("\n❌ Hubo un problema al limpiar la base de datos")
