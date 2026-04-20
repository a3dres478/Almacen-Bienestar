"""
Módulo de gestión de base de datos en Excel para el gestor de almacenes.
Maneja la creación, lectura y actualización de datos en archivos Excel.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
import os
from difflib import SequenceMatcher


class GestorAlmacen:
    def __init__(self, ruta_bd="data/almacen.xlsx"):
        """
        Inicializa el gestor de almacén.
        
        Args:
            ruta_bd (str): Ruta del archivo Excel de base de datos
        """
        self.ruta_bd = ruta_bd
        self.ruta_dir = os.path.dirname(ruta_bd)
        
        # Crear directorio si no existe
        if self.ruta_dir and not os.path.exists(self.ruta_dir):
            os.makedirs(self.ruta_dir)
        
        # Crear BD si no existe
        if not os.path.exists(ruta_bd):
            self._crear_bd()
        else:
            # Verificar y actualizar esquema si es necesario
            self._verificar_actualizar_esquema()
    
    def _crear_bd(self):
        """Crea un nuevo archivo Excel con la estructura inicial."""
        wb = openpyxl.Workbook()
        wb.remove(wb.active)  # Eliminar hoja por defecto
        
        # Crear hoja de productos
        self._crear_hoja_productos(wb)
        
        # Crear hoja de movimientos
        self._crear_hoja_movimientos(wb)
        
        # Crear hoja de reportes
        self._crear_hoja_reportes(wb)
        
        wb.save(self.ruta_bd)
    
    def _verificar_actualizar_esquema(self):
        """Verifica y actualiza el esquema de la base de datos existente."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            
            # Verificar hoja de productos
            if "Productos" in wb.sheetnames:
                ws_productos = wb["Productos"]
                
                # Leer encabezados actuales
                encabezados_actuales = []
                if ws_productos.max_row >= 1:
                    for cell in ws_productos[1]:
                        if cell.value:
                            encabezados_actuales.append(cell.value)
                
                # Encabezados esperados
                encabezados_esperados = ["ID", "Nombre", "Descripción", "Stock Actual", "Unidad Medida", "Fecha Creación", "URL Imagen"]
                
                # Verificar si faltan columnas
                columnas_faltantes = []
                for encabezado in encabezados_esperados:
                    if encabezado not in encabezados_actuales:
                        columnas_faltantes.append(encabezado)
                
                # Agregar columnas faltantes
                if columnas_faltantes:
                    print(f"Actualizando esquema: agregando columnas {columnas_faltantes}")
                    
                    # Para cada columna faltante, agregarla al final
                    col_actual = len(encabezados_actuales) + 1
                    for columna in columnas_faltantes:
                        ws_productos.cell(row=1, column=col_actual, value=columna)
                        col_actual += 1
                    
                    # Aplicar estilo a los nuevos encabezados
                    self._estilizar_encabezado(ws_productos, 1, len(encabezados_esperados))
                    
                    # Ajustar ancho de la nueva columna
                    if "URL Imagen" in columnas_faltantes:
                        ws_productos.column_dimensions['H'].width = 25
            
            wb.save(self.ruta_bd)
            wb.close()
            
        except Exception as e:
            print(f"Error al verificar/actualizar esquema: {e}")
    
    def _crear_hoja_productos(self, wb):
        """Crea la hoja de productos con encabezados."""
        ws = wb.create_sheet("Productos")
        
        encabezados = ["ID", "Nombre", "Descripción", "Stock Actual", "Unidad Medida", "Fecha Creación", "URL Imagen"]
        ws.append(encabezados)
        
        # Estilo de encabezado
        self._estilizar_encabezado(ws, 1, len(encabezados))
        
        # Ajustar ancho de columnas
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 30
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 25
    
    def _crear_hoja_movimientos(self, wb):
        """Crea la hoja de movimientos (entradas y salidas)."""
        ws = wb.create_sheet("Movimientos")
        
        encabezados = ["ID Movimiento", "Fecha", "Mes", "Año", "Tipo", "ID Producto", "Nombre Producto", 
                       "Cantidad", "Stock Anterior", "Stock Nuevo", "Motivo", "Responsable"]
        ws.append(encabezados)
        
        self._estilizar_encabezado(ws, 1, len(encabezados))
        
        # Ajustar ancho
        for col, ancho in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'], 1):
            ws.column_dimensions[ancho].width = 15
    
    def _crear_hoja_reportes(self, wb):
        """Crea la hoja de reportes (historial resumido)."""
        ws = wb.create_sheet("Reportes")
        
        encabezados = ["Fecha Reporte", "Producto", "Movimientos", "Entradas Totales", 
                       "Salidas Totales", "Stock Final", "Valor Stock"]
        ws.append(encabezados)
        
        self._estilizar_encabezado(ws, 1, len(encabezados))
        
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            ws.column_dimensions[col].width = 18
    
    def _estilizar_encabezado(self, ws, fila, num_columnas):
        """Aplica estilos a la fila de encabezado."""
        fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        font = Font(bold=True, color="FFFFFF")
        alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        for col in range(1, num_columnas + 1):
            cell = ws.cell(row=fila, column=col)
            cell.fill = fill
            cell.font = font
            cell.alignment = alignment
    
    def obtener_productos(self):
        """Obtiene la lista de todos los productos."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Productos"]
            
            productos = []
            for fila in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
                if fila[0]:  # Si hay ID
                    productos.append({
                        "id": fila[0],
                        "nombre": fila[1],
                        "descripcion": fila[2],
                        "stock": fila[3],
                        "unidad": fila[4],
                        "fecha_creacion": fila[5],
                        "url_imagen": fila[6] if len(fila) > 6 else ""
                    })
            
            wb.close()
            return productos
        except Exception as e:
            return []
    
    def obtener_producto_por_id(self, id_producto):
        """Obtiene un producto específico por ID."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Productos"]
            
            for fila in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
                if fila[0] == id_producto:
                    wb.close()
                    return {
                        "id": fila[0],
                        "nombre": fila[1],
                        "descripcion": fila[2],
                        "stock": fila[3],
                        "unidad": fila[4],
                        "fecha_creacion": fila[5],
                        "url_imagen": fila[6] if len(fila) > 6 else ""
                    }
            
            wb.close()
            return None
        except Exception as e:
            return None
    
    def obtener_proximo_id_producto(self):
        """Obtiene el próximo ID disponible para productos."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Productos"]
            
            max_id = 0
            for fila in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
                if fila[0] and isinstance(fila[0], (int, float)):
                    max_id = max(max_id, int(fila[0]))
            
            wb.close()
            return max_id + 1
        except Exception as e:
            return 1
    
    def obtener_proximo_id_movimiento(self):
        """Obtiene el próximo ID disponible para movimientos."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Movimientos"]
            
            max_id = 0
            for fila in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
                if fila[0] and isinstance(fila[0], (int, float)):
                    max_id = max(max_id, int(fila[0]))
            
            wb.close()
            return max_id + 1
        except Exception as e:
            return 1
    
    def agregar_producto(self, nombre, descripcion, stock_inicial, unidad_medida, url_imagen=""):
        """Agrega un nuevo producto a la BD."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Productos"]
            
            id_producto = self.obtener_proximo_id_producto()
            fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            ws.append([id_producto, nombre, descripcion, stock_inicial, unidad_medida, fecha_creacion, url_imagen])
            
            wb.save(self.ruta_bd)
            wb.close()
            
            return id_producto
        except Exception as e:
            print(f"Error al agregar producto: {e}")
            return False
    
    def registrar_movimiento(self, id_producto, tipo_movimiento, cantidad, motivo, responsable):
        """
        Registra una entrada o salida de producto.
        
        Args:
            id_producto: ID del producto
            tipo_movimiento: "Entrada" o "Salida"
            cantidad: Cantidad a registrar
            motivo: Motivo del movimiento
            responsable: Usuario responsable
        
        Returns:
            bool: True si fue exitoso, False si no
        """
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws_productos = wb["Productos"]
            ws_movimientos = wb["Movimientos"]
            
            # Buscar el producto y obtener stock actual
            stock_anterior = None
            fila_producto = None
            
            for idx, fila in enumerate(ws_productos.iter_rows(min_row=2, max_row=ws_productos.max_row), start=2):
                if fila[0].value == id_producto:
                    stock_anterior = fila[3].value if fila[3].value else 0
                    fila_producto = idx
                    nombre_producto = fila[1].value
                    break
            
            if stock_anterior is None:
                wb.close()
                return False
            
            # Calcular nuevo stock
            if tipo_movimiento.lower() == "entrada":
                stock_nuevo = stock_anterior + cantidad
            elif tipo_movimiento.lower() == "salida":
                if stock_anterior < cantidad:
                    wb.close()
                    return False  # No hay suficiente stock
                stock_nuevo = stock_anterior - cantidad
            else:
                wb.close()
                return False
            
            # Registrar movimiento
            id_movimiento = self.obtener_proximo_id_movimiento()
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mes = datetime.now().strftime("%m")
            año = datetime.now().strftime("%Y")
            
            ws_movimientos.append([
                id_movimiento,
                fecha,
                mes,
                año,
                tipo_movimiento,
                id_producto,
                nombre_producto,
                cantidad,
                stock_anterior,
                stock_nuevo,
                motivo,
                responsable
            ])
            
            # Actualizar stock en productos
            ws_productos.cell(row=fila_producto, column=4).value = stock_nuevo
            
            wb.save(self.ruta_bd)
            wb.close()
            
            return True
        except Exception as e:
            print(f"Error al registrar movimiento: {e}")
            return False
    
    def obtener_movimientos(self, id_producto=None):
        """Obtiene los movimientos. Si id_producto es None, obtiene todos."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Movimientos"]
            
            movimientos = []
            for fila in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
                if fila[0]:  # Si hay ID
                    if id_producto is None or fila[5] == id_producto:
                        # Extraer mes y año de la fecha
                        fecha_str = str(fila[1]) if fila[1] else ""
                        mes = ""
                        año = ""
                        if fecha_str and len(fecha_str) >= 10:  # Formato YYYY-MM-DD
                            try:
                                año = fecha_str[:4]
                                mes = fecha_str[5:7]
                            except:
                                pass
                        
                        movimientos.append({
                            "id": fila[0],
                            "fecha": fila[1],
                            "mes": mes,
                            "año": año,
                            "tipo": fila[4],
                            "id_producto": fila[5],
                            "nombre_producto": fila[6],
                            "cantidad": fila[7],
                            "stock_anterior": fila[8],
                            "stock_nuevo": fila[9],
                            "motivo": fila[10],
                            "responsable": fila[11]
                        })
            
            wb.close()
            return movimientos
        except Exception as e:
            return []
    
    def exportar_plantilla_carga(self, ruta_salida="templates/plantilla_carga.xlsx"):
        """Crea una plantilla Excel para cargar datos masivos."""
        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Cargar Productos"
            
            encabezados = ["Nombre", "Descripción", "Stock Inicial", "Unidad Medida"]
            ws.append(encabezados)
            
            self._estilizar_encabezado(ws, 1, len(encabezados))
            
            # Ajustar ancho
            ws.column_dimensions['A'].width = 20
            ws.column_dimensions['B'].width = 30
            ws.column_dimensions['C'].width = 15
            ws.column_dimensions['D'].width = 15
            
            # Agregar filas de ejemplo
            ws.append(["Producto Ejemplo", "Descripción ejemplo", 100, "Unidad"])
            
            # Crear directorio si no existe
            if not os.path.exists(os.path.dirname(ruta_salida)):
                os.makedirs(os.path.dirname(ruta_salida))
            
            wb.save(ruta_salida)
            wb.close()
            
            return True
        except Exception as e:
            print(f"Error al exportar plantilla: {e}")
            return False
    
    def cargar_productos_desde_excel(self, ruta_archivo):
        """Carga productos desde un archivo Excel externo."""
        try:
            wb = openpyxl.load_workbook(ruta_archivo)
            ws = wb.active

            productos_agregados = 0
            errores = []

            # Leer encabezados de la primera fila
            encabezados = [str(celda).strip().lower() if celda is not None else "" 
                        for celda in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]

            # Detectar si el archivo trae columna ID al inicio
            tiene_id = len(encabezados) > 0 and encabezados[0] == "id"

            for idx, fila in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True), start=2):
                try:
                    # Si trae ID, empezamos desde la columna 1
                    if tiene_id:
                        nombre = fila[1] if len(fila) > 1 else None
                        descripcion = fila[2] if len(fila) > 2 else ""
                        stock = int(fila[3]) if len(fila) > 3 and fila[3] not in (None, "") else 0
                        unidad = fila[4] if len(fila) > 4 else "Unidades"
                    else:
                        nombre = fila[0] if len(fila) > 0 else None
                        descripcion = fila[1] if len(fila) > 1 else ""
                        stock = int(fila[2]) if len(fila) > 2 and fila[2] not in (None, "") else 0
                        unidad = fila[3] if len(fila) > 3 else "Unidades"

                    # Solo agregar si hay nombre
                    if nombre:
                        self.agregar_producto(nombre, descripcion, stock, unidad)
                        productos_agregados += 1

                except Exception as e:
                    errores.append(f"Fila {idx}: {str(e)}")

            wb.close()
            return productos_agregados, errores

        except Exception as e:
            print(f"Error al cargar archivo: {e}")
            return 0, [str(e)]

    
    def generar_reporte(self):
        """Genera un reporte completo del estado del almacén."""
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws_productos = wb["Productos"]
            ws_movimientos = wb["Movimientos"]
            ws_reportes = wb["Reportes"]
            
            # Limpiar reportes anteriores
            for fila in ws_reportes.iter_rows(min_row=2, max_row=ws_reportes.max_row):
                for cell in fila:
                    cell.value = None
            
            fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Procesar cada producto
            for fila_prod in ws_productos.iter_rows(min_row=2, max_row=ws_productos.max_row):
                id_prod = fila_prod[0].value
                nombre_prod = fila_prod[1].value
                stock_actual = fila_prod[3].value or 0
                
                if id_prod:
                    # Contar movimientos
                    entrada_total = 0
                    salida_total = 0
                    cantidad_mov = 0
                    
                    for fila_mov in ws_movimientos.iter_rows(min_row=2, max_row=ws_movimientos.max_row, values_only=True):
                        if fila_mov[5] == id_prod:  # ID del producto (posición 5)
                            cantidad_mov += 1
                            cantidad = fila_mov[7]  # Cantidad (posición 7)
                            if fila_mov[4].lower() == "entrada":  # Tipo (posición 4)
                                entrada_total += cantidad
                            else:
                                salida_total += cantidad
                    
                    valor_stock = stock_actual  # Sin precio, solo cantidad
                    
                    ws_reportes.append([
                        fecha_reporte,
                        nombre_prod,
                        cantidad_mov,
                        entrada_total,
                        salida_total,
                        stock_actual,
                        valor_stock
                    ])
            
            wb.save(self.ruta_bd)
            wb.close()
            
            return True
        except Exception as e:
            print(f"Error al generar reporte: {e}")
            return False
    
    def calcular_similitud(self, str1, str2):
        """Calcula la similitud entre dos strings usando SequenceMatcher."""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def encontrar_productos_similares(self, nombre_producto, umbral=0.8):
        """
        Encuentra productos similares al nombre ingresado.
        Retorna una tupla (producto_encontrado, similitud) o (None, 0) si no hay coincidencia
        """
        try:
            productos = self.obtener_productos()
            mejor_coincidencia = None
            mejor_similitud = 0
            
            for producto in productos:
                similitud = self.calcular_similitud(nombre_producto, producto['nombre'])
                if similitud > mejor_similitud:
                    mejor_similitud = similitud
                    mejor_coincidencia = producto
            
            # Retornar solo si supera el umbral
            if mejor_similitud >= umbral:
                return mejor_coincidencia, mejor_similitud
            return None, 0
            
        except Exception as e:
            print(f"Error al encontrar productos similares: {e}")
            return None, 0
    
    def limpiar_movimientos_antiguos(self, fecha_limite="2026-04-17"):
        """
        Elimina todos los movimientos anteriores a la fecha especificada (17 de abril de 2026).
        """
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Movimientos"]
            
            filas_a_eliminar = []
            
            # Identificar filas a eliminar
            for idx, fila in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row), start=2):
                if fila[1].value:  # Si hay fecha (posición 1)
                    fecha_str = str(fila[1].value).split()[0]  # Extraer solo la fecha
                    if fecha_str < fecha_limite:
                        filas_a_eliminar.append(idx)
            
            # Eliminar filas (desde la última hacia la primera para no afectar índices)
            for idx in reversed(filas_a_eliminar):
                ws.delete_rows(idx)
            
            wb.save(self.ruta_bd)
            wb.close()
            
            print(f"Se eliminaron {len(filas_a_eliminar)} movimientos anteriores a {fecha_limite}")
            return True
            
        except Exception as e:
            print(f"Error al limpiar movimientos antiguos: {e}")
            return False
    
    def obtener_movimientos_por_rango_fechas(self, fecha_inicio, fecha_fin, id_producto=None):
        """
        Obtiene movimientos dentro de un rango de fechas.
        fecha_inicio y fecha_fin deben estar en formato "YYYY-MM-DD"
        """
        try:
            wb = openpyxl.load_workbook(self.ruta_bd)
            ws = wb["Movimientos"]
            
            movimientos = []
            
            for fila in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
                if fila[1]:  # Si hay fecha
                    fecha_str = str(fila[1]).split()[0]
                    
                    # Verificar si está en el rango
                    if fecha_inicio <= fecha_str <= fecha_fin:
                        # Filtrar por producto si se especifica
                        if id_producto is None or fila[5] == id_producto:
                            movimientos.append({
                                "id_movimiento": fila[0],
                                "fecha": fila[1],
                                "mes": fila[2],
                                "año": fila[3],
                                "tipo": fila[4],
                                "id_producto": fila[5],
                                "nombre_producto": fila[6],
                                "cantidad": fila[7],
                                "stock_anterior": fila[8],
                                "stock_nuevo": fila[9],
                                "motivo": fila[10],
                                "responsable": fila[11]
                            })
            
            wb.close()
            return movimientos
            
        except Exception as e:
            print(f"Error al obtener movimientos por rango de fechas: {e}")
            return []

