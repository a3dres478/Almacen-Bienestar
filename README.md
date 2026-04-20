# 📦 Gestor de Almacenes - Sistema Asincrónico

Sistema simple e intuitivo para gestionar inventario en pequeños almacenes. Basado en Python con interfaz Tkinter y Excel como base de datos.

## 🎯 Características

✅ **Gestión de Productos**
- Crear nuevos productos con información completa
- Campo opcional de **URL de imagen** para evidencia
- Ver lista actualizada de productos
- **Doble click** en producto para ver detalles completos
- Seguimiento de stock en tiempo real

✅ **Registro de Movimientos**
- **Búsqueda inteligente** de productos (escribe y aparecen sugerencias)
- Registrar entradas y salidas de productos
- Validación estricta: solo números enteros positivos
- Especificar motivos y responsables
- Historial automático de cambios

✅ **Reportes Detallados**
- Historial completo de movimientos
- Reportes por producto
- Resumen general del almacén
- Valor total del inventario

✅ **Importación/Exportación**
- Descargar plantilla Excel para carga masiva
- Importar productos desde Excel
- Exportar datos completos

✅ **Base de Datos Excel**
- Almacenamiento en Excel (no requiere servidor)
- 3 hojas: Productos, Movimientos, Reportes
- Accesible y editable manualmente si es necesario

## 📋 Requisitos

- Python 3.7 o superior
- Tkinter (generalmente incluido con Python)
- openpyxl (para manejo de Excel)

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
python main.py
```

## 📖 Guía de Uso

### 1️⃣ Primera Vez

Al iniciar, el sistema crea automáticamente:
- Carpeta `/data` con el archivo `almacen.xlsx`
- Carpeta `/templates` para plantillas

### 2️⃣ Agregar Productos

1. Ir a la pestaña **"Productos"**
2. Completar los campos:
   - **Nombre**: Nombre del producto (obligatorio)
   - **Descripción**: Detalles del producto
   - **Stock Inicial**: Cantidad inicial (solo números enteros ≥ 0)
   - **Precio Unitario**: Precio por unidad (número decimal ≥ 0)
   - **Unidad Medida**: Unidad (Unidad, Kg, Caja, etc.)
   - **URL Imagen**: Enlace a imagen del producto (opcional)
3. Click en **"✅ Agregar Producto"**

💡 **Tip**: Para ver detalles completos de un producto, **haz doble click** en cualquier fila de la tabla.

### 3️⃣ Registrar Movimientos

1. Ir a la pestaña **"↔️ Movimientos"**
2. **Buscar producto**: Escribe parte del nombre y aparecerán sugerencias automáticamente
   - Ejemplo: escribe "lap" para ver "Lápices", "Laptop", "Lapiceros", etc.
   - Selecciona de la lista o presiona Enter
3. Elegir tipo: **Entrada** o **Salida**
4. Ingresar cantidad (solo números enteros positivos)
5. Especificar motivo y responsable
6. Click en **"✅ Registrar Movimiento"**

⚠️ **Validaciones**:
- Cantidad: Solo números enteros positivos (1, 2, 100...)
- No acepta decimales, negativos ni símbolos
- Todos los campos son obligatorios

El stock se actualiza automáticamente.

### 4️⃣ Ver Historial

1. Pestaña **"📋 Historial"**
2. Seleccionar un producto para filtrar o click en **"🔄 Todos"**
3. Ver todos los movimientos con detalles:
   - Fecha y hora
   - Tipo de movimiento
   - Stock anterior y nuevo
   - Motivo y responsable

### 5️⃣ Generar Reportes

1. Pestaña **"📊 Reportes"**
2. Click en **"📈 Generar Reporte Completo"** para:
   - Resumen general del almacén
   - Detalle por producto
   - Entradas, salidas y movimientos

### 6️⃣ Importar Productos en Lote

#### Descargar plantilla:
1. Pestaña **"📥📤 Importar/Exportar"**
2. Click en **"⬇️ Descargar Plantilla"**
3. Guardar archivo `plantilla_carga.xlsx`

#### Llenar plantilla:
1. Abrir `plantilla_carga.xlsx` en Excel
2. Rellenar con los productos (ejemplo ya incluido)
3. Columnas necesarias:
   - Nombre
   - Descripción
   - Stock Inicial
   - Precio Unitario
   - Unidad Medida

#### Importar archivo:
1. Pestaña **"📥📤 Importar/Exportar"**
2. Click en **"📂 Seleccionar Archivo"**
3. Seleccionar el archivo completado
4. Ver resultado de importación

### 7️⃣ Exportar Datos

1. Pestaña **"📊 Reportes"**
2. Click en **"💾 Exportar a Excel"**
3. Guardar copia de los datos

## 📁 Estructura de Archivos

```
App/
├── main.py                    # Aplicación principal
├── database.py                # Gestión de base de datos
├── requirements.txt           # Dependencias Python
├── README.md                  # Este archivo
├── data/
│   └── almacen.xlsx          # Base de datos (creada automáticamente)
└── templates/
    └── plantilla_carga.xlsx   # Plantilla de carga (creada al descargar)
```

## 📊 Estructura de Excel

### Hoja: Productos
| ID | Nombre | Descripción | Stock Actual | Precio Unitario | Unidad Medida | Fecha Creación | URL Imagen |
|----|--------|-------------|--------------|-----------------|--------------|-----------------|------------|
| 1  | Lápices| Lápices HB  | 50           | 2.50           | Unidad       | 2024-01-15     | https://... |

### Hoja: Movimientos
| ID Mov. | Fecha | Tipo | ID Prod | Nombre Prod | Cantidad | Stock Anterior | Stock Nuevo | Motivo | Responsable |
|---------|-------|------|---------|-------------|----------|-----------------|-------------|--------|-------------|

### Hoja: Reportes
| Fecha Reporte | Producto | Movimientos | Entradas | Salidas | Stock Final | Valor Stock |
|---------------|----------|-------------|----------|---------|-------------|-------------|

## 🔒 Consideraciones de Seguridad

- La aplicación es **asincrónica** (no tiempo real)
- No hay control de acceso por usuario
- Los datos se basan en confianza en los responsables
- Se recomienda generar respaldos regulares

## 💾 Respaldos

Se recomienda:
1. Hacer copias periódicas del archivo `data/almacen.xlsx`
2. Exportar reportes mensuales
3. Mantener un registro de cambios importantes

## 🐛 Solución de Problemas

### Error: "No se puede encontrar module 'tkinter'"
**Solución**: Tkinter viene con Python. En algunos Linux puede necesitar:
```bash
sudo apt-get install python3-tk
```

### Error: "No se puede encontrar 'openpyxl'"
**Solución**: Instalar manualmente:
```bash
pip install openpyxl
```

### El archivo Excel se ve dañado
**Solución**: 
1. Exportar datos en un nuevo archivo
2. Eliminar `data/almacen.xlsx`
3. Reiniciar la aplicación (creará nuevo archivo)

## 📝 Notas Técnicas

- **Lenguaje**: Python 3
- **Interfaz**: Tkinter (GUI nativa de Python)
- **Base de Datos**: Excel con openpyxl
- **Modelo**: Asincrónico (actualización después de eventos)
- **Escalabilidad**: Óptimo para 1000-10000 productos

## 🎓 Ejemplos de Uso

### Caso 1: Compra de Stock
1. Recibir mercancía con documento de compra
2. Ir a "Movimientos"
3. Tipo: "Entrada"
4. Motivo: "Compra a Proveedor XYZ"
5. Responsable: Nombre de quien recibió
6. Stock se actualiza automáticamente

### Caso 2: Devolución de Cliente
1. Ir a "Movimientos"
2. Tipo: "Salida"
3. Motivo: "Devolución Cliente - Número de Factura"
4. Responsable: Quien procesó la devolución

### Caso 3: Reportes Mensuales
1. Fin de mes ir a "Reportes"
2. Click en "Generar Reporte Completo"
3. Exportar a Excel
4. Guardar con nombre: `Reporte_Almacen_YYYYMM.xlsx`

## 📞 Soporte

Para errores o preguntas:
1. Verificar que `data/almacen.xlsx` no esté abierto en Excel
2. Cerrar y reiniciar la aplicación
3. Verificar que tengas los permisos de escritura en la carpeta

## 📄 Licencia

Libre para uso personal y comercial.

---

**Versión**: 1.0  
**Última actualización**: Abril 2026
