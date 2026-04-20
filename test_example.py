"""
Script de ejemplo para probar el Gestor de Almacenes sin interfaz gráfica
Útil para verificar que todo funciona correctamente
"""

from database import GestorAlmacen
from datetime import datetime

def main():
    print("=" * 80)
    print("GESTOR DE ALMACENES - SCRIPT DE PRUEBA")
    print("=" * 80)
    
    # Inicializar base de datos
    db = GestorAlmacen("data/almacen.xlsx")
    print("\n[OK] Base de datos inicializada")
    
    # Agregar productos de ejemplo
    print("\n[PRODUCTOS] Agregando productos de ejemplo...")
    
    productos_ejemplo = [
        ("Laptop Dell", "Laptop 15 pulgadas Intel i7", 10, 1200.00, "Unidad"),
        ("Mouse Logitech", "Mouse inalambrico USB", 50, 25.50, "Unidad"),
        ("Teclado Mecanico", "Teclado RGB con switches MX", 30, 85.00, "Unidad"),
        ("Monitor LG", "Monitor Full HD 24 pulgadas", 15, 200.00, "Unidad"),
        ("Cable HDMI", "Cable HDMI 2.0 de 2 metros", 100, 8.50, "Unidad"),
    ]
    
    ids_productos = []
    for nombre, desc, stock, precio, unidad in productos_ejemplo:
        id_prod = db.agregar_producto(nombre, desc, stock, precio, unidad)
        ids_productos.append(id_prod)
        print(f"  OK - {nombre} (ID: {id_prod})")
    
    # Registrar movimientos de ejemplo
    print("\n[MOVIMIENTOS] Registrando movimientos de ejemplo...")
    
    movimientos_ejemplo = [
        (ids_productos[0], "Entrada", 5, "Compra a proveedor", "Juan Perez"),
        (ids_productos[1], "Salida", 10, "Venta a cliente", "Maria Garcia"),
        (ids_productos[2], "Entrada", 20, "Devolucion de stock", "Pedro Lopez"),
        (ids_productos[3], "Salida", 2, "Venta a cliente", "Juan Perez"),
        (ids_productos[4], "Entrada", 50, "Compra a proveedor", "Maria Garcia"),
        (ids_productos[0], "Salida", 3, "Venta a cliente", "Pedro Lopez"),
    ]
    
    for id_prod, tipo, cant, motivo, responsable in movimientos_ejemplo:
        resultado = db.registrar_movimiento(id_prod, tipo, cant, motivo, responsable)
        if resultado:
            print(f"  OK - {tipo}: {cant} unidades")
        else:
            print(f"  ERROR - Movimiento fallido")
    
    # Obtener y mostrar productos actualizados
    print("\n" + "=" * 80)
    print("[PRODUCTOS ACTUALIZADOS]")
    print("=" * 80)
    
    productos = db.obtener_productos()
    for prod in productos:
        print(f"\nID: {prod['id']} | {prod['nombre']}")
        print(f"  Stock: {prod['stock']} {prod['unidad']}")
        print(f"  Precio: ${prod['precio']:.2f}")
        print(f"  Valor Total: ${prod['stock'] * prod['precio']:,.2f}")
    
    # Mostrar historial
    print("\n" + "=" * 80)
    print("[HISTORIAL DE MOVIMIENTOS]")
    print("=" * 80)
    
    movimientos = db.obtener_movimientos()
    print(f"\nTotal de movimientos registrados: {len(movimientos)}\n")
    
    for mov in movimientos[-10:]:  # Mostrar ultimos 10
        print(f"{mov['fecha']} | {mov['tipo']:7} | {mov['nombre_producto']:20} | {mov['cantidad']:3} | {mov['responsable']}")
    
    # Generar reporte
    print("\n" + "=" * 80)
    print("[GENERANDO REPORTE]")
    print("=" * 80)
    
    db.generar_reporte()
    print("\n[OK] Reporte generado")
    
    # Resumen final
    print("\n" + "=" * 80)
    print("[OK] PRUEBA COMPLETADA CON EXITO")
    print("=" * 80)
    print("\nAhora puedes ejecutar: python main.py")
    print("Para abrir la interfaz grafica")
    
    # Exportar plantilla
    print("\n[PLANTILLA] Creando plantilla de carga...")
    db.exportar_plantilla_carga("templates/plantilla_carga.xlsx")
    print("[OK] Plantilla creada en: templates/plantilla_carga.xlsx")


if __name__ == "__main__":
    main()
