"""
Gestor de Almacenes - Aplicación principal con interfaz Tkinter
Sistema simple e intuitivo para gestionar inventario en pequeños almacenes
"""
"Hecho por Choco, Andrés y David - Bienestar Ciencias 2026"

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
import sys
import shutil

# --- Diálogo personalizado de tres opciones ---
def dialogo_tres_opciones(parent, titulo, mensaje, opcion1="Sí", opcion2="No", opcion3="Agregar de todas formas"):
    """
    Muestra un diálogo modal con tres botones personalizados.
    Retorna el texto del botón presionado.
    """
    import tkinter as tk
    from tkinter import ttk

    resultado = {"valor": None}
    win = tk.Toplevel(parent)
    win.title(titulo)
    win.transient(parent)
    win.grab_set()  # Modal

    ttk.Label(win, text=mensaje, wraplength=350).pack(padx=20, pady=(20,10))

    frame_btns = ttk.Frame(win)
    frame_btns.pack(pady=(0, 20))

    def set_valor(val):
        resultado["valor"] = val
        win.destroy()

    ttk.Button(frame_btns, text=opcion1, command=lambda: set_valor(opcion1)).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_btns, text=opcion2, command=lambda: set_valor(opcion2)).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_btns, text=opcion3, command=lambda: set_valor(opcion3)).pack(side=tk.LEFT, padx=5)

    win.wait_window()
    return resultado["valor"]

# Intentar importar PIL para soportar imágenes
try:
    from PIL import Image, ImageTk
    PILLOW_DISPONIBLE = True
except ImportError:
    PILLOW_DISPONIBLE = False

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import GestorAlmacen
from datetime import datetime


class DropdownConBusqueda(tk.Frame):
    """Widget personalizado de dropdown con búsqueda en tiempo real."""
    
    def __init__(self, parent, items=None, on_select=None, width=50, max_height=6, **kwargs):
        """
        Inicializa el dropdown con búsqueda.
        
        Args:
            parent: Frame padre
            items: Lista de items para mostrar
            on_select: Función callback cuando se selecciona un item
            width: Ancho del entry
            max_height: Altura máxima del listbox en filas
        """
        super().__init__(parent, **kwargs)
        
        self.items = items or []
        self.on_select = on_select
        self.width = width
        self.max_height = max_height
        self.valor_seleccionado = tk.StringVar()
        self.lista_popup = None
        self.frame_popup = None
        self.root_window = None
        
        # Colores
        self.COLOR_PRIMARIO = "#1b5e20"
        self.COLOR_SECUNDARIO = "#4caf50"
        self.COLOR_CLARO = "#81c784"
        self.COLOR_BLANCO = "#ffffff"
        self.COLOR_FONDO = "#f1f8e9"
        self.COLOR_TEXTO = "#1b5e20"
        
        # Crear Entry
        self.entry = tk.Entry(self, 
                             textvariable=self.valor_seleccionado,
                             width=width,
                             font=('Arial', 9),
                             relief=tk.SOLID,
                             borderwidth=1,
                             fg=self.COLOR_TEXTO,
                             bg=self.COLOR_BLANCO)
        self.entry.pack(fill=tk.X, expand=True)
        
        # Bindings
        self.entry.bind('<Button-1>', self._on_click)
        self.entry.bind('<KeyRelease>', self._on_key_release)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<Up>', self._on_up_arrow)
        self.entry.bind('<Down>', self._on_down_arrow)
        self.entry.bind('<Return>', self._on_return)
        self.entry.bind('<Escape>', self._close_popup)
        
        self.parent = parent
        self._selected_index = -1
    
    def set_items(self, items):
        """Actualiza la lista de items."""
        self.items = items
        if self.frame_popup and self.frame_popup.winfo_exists():  # Si el popup está abierto
            self._filtrar_items()
    
    def get(self):
        """Retorna el valor seleccionado."""
        return self.valor_seleccionado.get()
    
    def set(self, valor):
        """Establece el valor."""
        self.valor_seleccionado.set(valor)
    
    def _on_click(self, event):
        """Se ejecuta cuando se hace click en el entry."""
        if not self.lista_popup:
            self._mostrar_popup()
        return "break"
    
    def _on_key_release(self, event):
        """Se ejecuta mientras se escribe en el entry."""
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Return', 'Escape'):
            return
        # Solo filtrar si el popup está abierto
        if self.lista_popup:
            self._filtrar_items()
    
    def _filtrar_items(self):
        """Filtra los items según el texto escrito."""
        # Solo filtrar si el popup está abierto
        if not self.lista_popup or not self.lista_popup.winfo_exists():
            return
        
        texto = self.valor_seleccionado.get().lower().strip()
        
        # Limpiar listbox
        self.lista_popup.delete(0, tk.END)
        
        # Filtrar items
        items_filtrados = []
        for item in self.items:
            if texto == "" or texto in item.lower():
                items_filtrados.append(item)
        
        # Mostrar items filtrados (máximo max_height)
        for i, item in enumerate(items_filtrados[:self.max_height]):
            self.lista_popup.insert(tk.END, item)
    
    def _mostrar_popup(self):
        """Muestra el popup con la lista de productos."""
        if not self.lista_popup:
            # Crear ventana flotante (Toplevel) para la lista
            self.frame_popup = tk.Toplevel(self.entry)
            self.frame_popup.wm_overrideredirect(True)
            self.frame_popup.wm_attributes('-topmost', True)  # Mantener al frente
            
            # Agregar scrollbar
            frame_interno = tk.Frame(self.frame_popup, relief=tk.SOLID, borderwidth=1)
            frame_interno.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(frame_interno)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.lista_popup = tk.Listbox(frame_interno,
                                         height=self.max_height,
                                         font=('Arial', 9),
                                         relief=tk.FLAT,
                                         borderwidth=0,
                                         bg=self.COLOR_BLANCO,
                                         fg=self.COLOR_TEXTO,
                                         selectmode=tk.SINGLE,
                                         yscrollcommand=scrollbar.set,
                                         activestyle='none')
            scrollbar.config(command=self.lista_popup.yview)
            self.lista_popup.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Bindings para el listbox
            self.lista_popup.bind('<Button-1>', self._on_listbox_click)
            self.lista_popup.bind('<Return>', self._on_return)
            self.lista_popup.bind('<Escape>', self._close_popup)
            self.lista_popup.bind('<FocusOut>', self._on_listbox_focus_out)
            self.lista_popup.bind('<Motion>', self._on_listbox_motion)
            
            # Cargar todos los items inicialmente
            for item in self.items[:self.max_height]:
                self.lista_popup.insert(tk.END, item)
            
            # Posicionar el popup debajo del entry
            self.entry.after(10, self._posicionar_popup)
            
            # Traer al frente y darle el foco al listbox
            self.frame_popup.lift()
            
            # Detectar clicks fuera del popup
            self.root_window = self.entry.winfo_toplevel()
            self.root_window.bind('<Button-1>', self._on_root_click, add=True)
    
    def _on_listbox_motion(self, event):
        """Resalta el item bajo el mouse sin seleccionar."""
        try:
            index = self.lista_popup.index(f"@{event.x},{event.y}")
            if index is not None:
                self.lista_popup.selection_clear(0, tk.END)
                self.lista_popup.selection_set(index)
        except:
            pass
    
    def _on_root_click(self, event):
        """Detecta clicks fuera del dropdown y lo cierra."""
        if not self.frame_popup or not self.frame_popup.winfo_exists():
            return
        
        # Obtener coordenadas del popup
        popup_x1 = self.frame_popup.winfo_x()
        popup_y1 = self.frame_popup.winfo_y()
        popup_x2 = popup_x1 + self.frame_popup.winfo_width()
        popup_y2 = popup_y1 + self.frame_popup.winfo_height()
        
        # Obtener coordenadas del entry
        entry_x1 = self.entry.winfo_rootx()
        entry_y1 = self.entry.winfo_rooty()
        entry_x2 = entry_x1 + self.entry.winfo_width()
        entry_y2 = entry_y1 + self.entry.winfo_height()
        
        # Coordenadas del click
        click_x = event.x_root
        click_y = event.y_root
        
        # Si el click está fuera del entry y del popup, cerrar
        click_en_entry = entry_x1 <= click_x <= entry_x2 and entry_y1 <= click_y <= entry_y2
        click_en_popup = popup_x1 <= click_x <= popup_x2 and popup_y1 <= click_y <= popup_y2
        
        if not click_en_entry and not click_en_popup:
            self._close_popup()
    
    def _posicionar_popup(self):
        """Posiciona el popup debajo del entry."""
        if self.frame_popup:
            # Obtener posición del entry
            x = self.entry.winfo_rootx()
            y = self.entry.winfo_rooty() + self.entry.winfo_height()
            
            # Ancho del popup = ancho del entry
            ancho = self.entry.winfo_width()
            if ancho < 1:
                ancho = self.width * 7  # Aproximación
            
            altura = self.max_height * 20 + 2  # Altura aproximada
            
            self.frame_popup.geometry(f"{ancho}x{altura}+{x}+{y}")
    
    def _close_popup(self, event=None):
        """Cierra el popup."""
        # Desvincular el binding de click global
        try:
            if hasattr(self, 'root_window') and self.root_window:
                self.root_window.unbind('<Button-1>', None)
        except:
            pass
        
        # Destruir el popup
        try:
            if self.frame_popup and self.frame_popup.winfo_exists():
                self.frame_popup.destroy()
        except:
            pass
        finally:
            self.frame_popup = None
            self.lista_popup = None
        
        if event:
            return "break"
    
    def _on_listbox_click(self, event):
        """Se ejecuta cuando se hace click en un item de la lista."""
        selection = self.lista_popup.curselection()
        if selection:
            item = self.lista_popup.get(selection[0])
            self.valor_seleccionado.set(item)
            self._close_popup()
            if self.on_select:
                self.on_select(item)
        return "break"
    
    def _on_return(self, event):
        """Se ejecuta cuando se presiona Enter."""
        if self.lista_popup:
            selection = self.lista_popup.curselection()
            if selection:
                item = self.lista_popup.get(selection[0])
                self.valor_seleccionado.set(item)
                self._close_popup()
                if self.on_select:
                    self.on_select(item)
        return "break"
    
    def _on_up_arrow(self, event):
        """Se ejecuta cuando se presiona la flecha arriba."""
        if self.lista_popup:
            cursel = self.lista_popup.curselection()
            if cursel:
                index = cursel[0] - 1
                if index >= 0:
                    self.lista_popup.selection_clear(0, tk.END)
                    self.lista_popup.selection_set(index)
                    self.lista_popup.see(index)
            else:
                # Si no hay selección, seleccionar el último
                size = self.lista_popup.size()
                if size > 0:
                    self.lista_popup.selection_set(size - 1)
                    self.lista_popup.see(size - 1)
        return "break"
    
    def _on_down_arrow(self, event):
        """Se ejecuta cuando se presiona la flecha abajo."""
        if self.lista_popup:
            cursel = self.lista_popup.curselection()
            if cursel:
                index = cursel[0] + 1
                if index < self.lista_popup.size():
                    self.lista_popup.selection_clear(0, tk.END)
                    self.lista_popup.selection_set(index)
                    self.lista_popup.see(index)
            else:
                # Si no hay selección, seleccionar el primero
                if self.lista_popup.size() > 0:
                    self.lista_popup.selection_set(0)
                    self.lista_popup.see(0)
        return "break"
    
    def _on_focus_out(self, event):
        """Se ejecuta cuando se pierde el foco en el entry."""
        # Cerrar el popup cuando el entry pierde el foco
        self.after(50, self._close_popup)
    
    def _on_listbox_focus_out(self, event):
        """Se ejecuta cuando se pierde el foco en el listbox."""
        # Cerrar cuando se hace click fuera del dropdown
        self.after(50, self._close_popup)


class GestorAlmacenesUI:
    def __init__(self, root):
        """Inicializa la interfaz gráfica."""
        self.root = root
        self.root.title("Gestor de Almacenes - Sistema Local")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        
        # Colores verdes personalizados
        self.COLOR_PRIMARIO = "#1b5e20"      # Verde oscuro
        self.COLOR_SECUNDARIO = "#4caf50"    # Verde medio
        self.COLOR_CLARO = "#81c784"         # Verde claro
        self.COLOR_MUY_CLARO = "#c8e6c9"     # Verde muy claro
        self.COLOR_FONDO = "#f1f8e9"         # Verde fondo
        self.COLOR_TEXTO = "#1b5e20"         # Verde oscuro para texto
        self.COLOR_BLANCO = "#ffffff"        # Blanco
        
        # Configurar colores de fondo
        self.root.configure(bg=self.COLOR_FONDO)
        
        # Configurar estilo verde
        self._configurar_estilo_verde()
        
        # Separar rutas de datos (persistentes) y recursos (embebidos en PyInstaller)
        self.ruta_base = self._obtener_ruta_datos_persistente()
        self.ruta_recursos = self._obtener_ruta_recursos()
        self.imagen_logo = None
        
        try:
            # Inicializar base de datos en ruta persistente
            ruta_bd = os.path.join(self.ruta_base, "data", "almacen.xlsx")
            self._preparar_base_datos_inicial(ruta_bd)
            self.db = GestorAlmacen(ruta_bd)
            
            # Limpiar movimientos anteriores a 2026-04-17
            self.db.limpiar_movimientos_antiguos("2026-04-17")
            
            # Crear interfaz
            self._crear_interfaz()
            
            # Cargar datos iniciales
            self._actualizar_lista_productos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al inicializar: {str(e)}")
            self.root.destroy()

    def _obtener_ruta_datos_persistente(self):
        """Retorna la carpeta donde deben guardarse datos entre reinicios."""
        if getattr(sys, "frozen", False):
            # En ejecutable portable, guardar junto al .exe
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def _obtener_ruta_recursos(self):
        """Retorna la carpeta de recursos embebidos (modo PyInstaller) o local."""
        if hasattr(sys, "_MEIPASS"):
            return sys._MEIPASS
        return os.path.dirname(os.path.abspath(__file__))

    def _preparar_base_datos_inicial(self, ruta_bd_destino):
        """Copia la base de datos embebida solo en la primera ejecución, si existe."""
        carpeta_data_destino = os.path.dirname(ruta_bd_destino)
        if carpeta_data_destino and not os.path.exists(carpeta_data_destino):
            os.makedirs(carpeta_data_destino, exist_ok=True)

        if os.path.exists(ruta_bd_destino):
            return

        ruta_bd_origen = os.path.join(self.ruta_recursos, "data", "almacen.xlsx")
        if os.path.exists(ruta_bd_origen):
            try:
                shutil.copy2(ruta_bd_origen, ruta_bd_destino)
            except Exception:
                # Si falla la copia, GestorAlmacen creará un archivo nuevo.
                pass
    
    def _configurar_estilo_verde(self):
        """Configura el esquema de colores verde de la aplicación."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores para widgets
        style.configure('TFrame', background=self.COLOR_FONDO, relief='flat')
        style.configure('TLabel', background=self.COLOR_FONDO, foreground=self.COLOR_TEXTO, font=('Arial', 9))
        style.configure('Title.TLabel', background=self.COLOR_FONDO, foreground=self.COLOR_PRIMARIO, font=('Arial', 12, 'bold'))
        
        # Botones verdes
        style.configure('TButton', background=self.COLOR_SECUNDARIO, foreground=self.COLOR_BLANCO)
        style.map('TButton',
                 background=[('pressed', self.COLOR_PRIMARIO), ('active', self.COLOR_CLARO)],
                 foreground=[('pressed', self.COLOR_BLANCO), ('active', self.COLOR_BLANCO)])
        
        # Entrada verde
        style.configure('TEntry', background=self.COLOR_BLANCO, foreground=self.COLOR_TEXTO, relief='solid', borderwidth=1)
        style.configure('TCombobox', background=self.COLOR_BLANCO, foreground=self.COLOR_TEXTO, fieldbackground=self.COLOR_BLANCO)
        
        # LabelFrame verde
        style.configure('TLabelframe', background=self.COLOR_FONDO, foreground=self.COLOR_PRIMARIO, font=('Arial', 10, 'bold'))
        style.configure('TLabelframe.Label', background=self.COLOR_FONDO, foreground=self.COLOR_PRIMARIO, font=('Arial', 10, 'bold'))
        
        # Notebook (pestañas)
        style.configure('TNotebook', background=self.COLOR_FONDO, borderwidth=2)
        style.configure('TNotebook.Tab', background=self.COLOR_CLARO, foreground=self.COLOR_PRIMARIO, padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', self.COLOR_SECUNDARIO)], foreground=[('selected', self.COLOR_BLANCO)])
        style.configure('TNotebook.Tab', padding=[30, 15])
        
        # Treeview
        style.configure('Treeview', background=self.COLOR_BLANCO, foreground=self.COLOR_TEXTO, fieldbackground=self.COLOR_BLANCO)
        style.configure('Treeview.Heading', background=self.COLOR_PRIMARIO, foreground=self.COLOR_BLANCO, font=('Arial', 10, 'bold'))
        style.map('Treeview', background=[('selected', self.COLOR_CLARO)])
        
        # Scrollbar
        style.configure('Vertical.TScrollbar', background=self.COLOR_MUY_CLARO, troughcolor=self.COLOR_FONDO)
        style.configure('Horizontal.TScrollbar', background=self.COLOR_MUY_CLARO, troughcolor=self.COLOR_FONDO)
    
    def _crear_interfaz(self):
        """Crea la interfaz principal con pestañas."""
        # Frame superior con encabezado verde
        frame_encabezado = tk.Frame(self.root, bg=self.COLOR_PRIMARIO, height=80)
        frame_encabezado.pack(fill=tk.X, padx=0, pady=0)
        frame_encabezado.pack_propagate(False)
        
        # Cargar y mostrar logo si existe
        ruta_logo = os.path.join(self.ruta_recursos, "logo.png")
        if os.path.exists(ruta_logo) and PILLOW_DISPONIBLE:
            try:
                img = Image.open(ruta_logo)
                img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                self.imagen_logo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(frame_encabezado, image=self.imagen_logo, bg=self.COLOR_PRIMARIO)
                logo_label.pack(side=tk.LEFT, padx=15, pady=10)
            except Exception as e:
                print(f"No se pudo cargar el logo: {e}")
        
        # Titulo
        titulo = tk.Label(frame_encabezado, text="GESTOR DE ALMACENES", 
                          font=("Arial", 18, "bold"), bg=self.COLOR_PRIMARIO, 
                          fg=self.COLOR_BLANCO)
        titulo.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Subtitulo
        subtitulo = tk.Label(frame_encabezado, text="Sistema Local de Inventario", 
                             font=("Arial", 10), bg=self.COLOR_PRIMARIO, 
                             fg=self.COLOR_MUY_CLARO)
        subtitulo.pack(side=tk.LEFT, padx=10)
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestañas
        self._crear_pestana_productos()
        self._crear_pestana_movimientos()
        self._crear_pestana_historial()
        self._crear_pestana_reportes()
        self._crear_pestana_importacion()
    
    def _crear_pestana_productos(self):
        """Crea la pestaña de gestión de productos."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Productos")
        
        # Frame de entrada
        frame_entrada = ttk.LabelFrame(frame, text="Agregar Nuevo Producto", padding=10)
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)
        
        # Nombre
        ttk.Label(frame_entrada, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(frame_entrada, width=40)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Descripción
        ttk.Label(frame_entrada, text="Descripción:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_descripcion = ttk.Entry(frame_entrada, width=40)
        self.entry_descripcion.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        # Stock inicial
        ttk.Label(frame_entrada, text="Stock Inicial:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_stock = ttk.Entry(frame_entrada, width=40)
        self.entry_stock.grid(row=2, column=1, sticky=tk.EW, padx=5)
        
        # Unidad de medida (DDL)
        ttk.Label(frame_entrada, text="Unidad Medida:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.combo_unidad = ttk.Combobox(frame_entrada, values=["Unidades", "Kg", "Otro"], width=38, state="readonly")
        self.combo_unidad.grid(row=3, column=1, sticky=tk.EW, padx=5)
        self.combo_unidad.current(0)  # Por defecto "Unidades"
        
        # URL de imagen (opcional)
        ttk.Label(frame_entrada, text="URL Imagen (opcional):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_url_imagen = ttk.Entry(frame_entrada, width=40)
        self.entry_url_imagen.grid(row=4, column=1, sticky=tk.EW, padx=5)
        
        # Botón agregar
        btn_agregar = ttk.Button(frame_entrada, text="✅ Agregar Producto", 
                                command=self._agregar_producto)
        btn_agregar.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10, padx=5)
        
        frame_entrada.columnconfigure(1, weight=1)
        
        # Botón reiniciar periodo
        btn_reiniciar = ttk.Button(frame_entrada,text="🧹 Reiniciar periodo",command=self._reiniciar_periodo_desde_ui)
        
        btn_reiniciar.grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=5, padx=5)

        # Frame de lista de productos
        frame_lista = ttk.LabelFrame(frame, text="Productos Registrados", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear Treeview con scrollbar
        scroll = ttk.Scrollbar(frame_lista)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_productos = ttk.Treeview(frame_lista, 
                                          columns=("ID", "Nombre", "Descripción", "Stock", "Unidad"),
                                          height=15,
                                          yscrollcommand=scroll.set)
        scroll.config(command=self.tree_productos.yview)
        
        # Definir encabezados
        self.tree_productos.column("#0", width=0, stretch=tk.NO)
        self.tree_productos.column("ID", anchor=tk.CENTER, width=40)
        self.tree_productos.column("Nombre", anchor=tk.W, width=150)
        self.tree_productos.column("Descripción", anchor=tk.W, width=200)
        self.tree_productos.column("Stock", anchor=tk.CENTER, width=80)
        self.tree_productos.column("Unidad", anchor=tk.CENTER, width=80)
        
        self.tree_productos.heading("#0", text="", anchor=tk.W)
        self.tree_productos.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree_productos.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tree_productos.heading("Descripción", text="Descripción", anchor=tk.W)
        self.tree_productos.heading("Stock", text="Stock", anchor=tk.CENTER)
        self.tree_productos.heading("Unidad", text="Unidad", anchor=tk.CENTER)
        
        self.tree_productos.pack(fill=tk.BOTH, expand=True)
        
        # Evento para mostrar detalles del producto al hacer doble click
        self.tree_productos.bind("<Double-1>", self._mostrar_detalles_producto)
    
    def _mostrar_detalles_producto(self, event):
        """Muestra una ventana con los detalles completos del producto seleccionado."""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        
        item = self.tree_productos.item(seleccion[0])
        valores = item['values']
        
        if not valores:
            return
        
        id_producto = valores[0]
        
        # Obtener detalles completos del producto
        producto = self.db.obtener_producto_por_id(id_producto)
        if not producto:
            return
        
        # Crear ventana de detalles
        ventana_detalles = tk.Toplevel(self.root)
        ventana_detalles.title(f"Detalles del Producto - {producto['nombre']}")
        ventana_detalles.geometry("500x400")
        ventana_detalles.configure(bg=self.COLOR_FONDO)
        ventana_detalles.resizable(True, True)
        
        # Frame principal
        frame_principal = ttk.Frame(ventana_detalles)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(frame_principal, text=f"📦 {producto['nombre']}", 
                          font=('Arial', 14, 'bold'), foreground=self.COLOR_PRIMARIO)
        titulo.pack(pady=(0, 20))
        
        # Información del producto
        info_frame = ttk.LabelFrame(frame_principal, text="Información del Producto", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Crear labels con la información
        ttk.Label(info_frame, text=f"ID: {producto['id']}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Nombre: {producto['nombre']}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Descripción: {producto['descripcion']}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Stock Actual: {producto['stock']}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Unidad de Medida: {producto['unidad']}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Fecha de Creación: {producto['fecha_creacion']}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        
        # URL de imagen (si existe)
        if producto.get('url_imagen') and producto['url_imagen'].strip():
            ttk.Label(info_frame, text=f"URL Imagen: {producto['url_imagen']}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
            
            # Botón para abrir la imagen
            btn_ver_imagen = ttk.Button(info_frame, text="🔗 Ver Imagen", 
                                       command=lambda: self._abrir_url_imagen(producto['url_imagen']))
            btn_ver_imagen.pack(anchor=tk.W, pady=(5, 0))
        else:
            ttk.Label(info_frame, text="URL Imagen: No especificada", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        
        # Botón cerrar
        btn_cerrar = ttk.Button(frame_principal, text="Cerrar", command=ventana_detalles.destroy)
        btn_cerrar.pack(pady=(10, 0))
    
    def _abrir_url_imagen(self, url):
        """Abre la URL de la imagen en el navegador predeterminado."""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la URL: {str(e)}")
    
    def _crear_pestana_movimientos(self):
        """Crea la pestaña para registrar entradas y salidas."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="↔️ Movimientos")
        
        # Frame de entrada
        frame_entrada = ttk.LabelFrame(frame, text="Registrar Movimiento", padding=10)
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)
        
        # Producto - usando dropdown personalizado con búsqueda
        ttk.Label(frame_entrada, text="Producto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_producto = DropdownConBusqueda(frame_entrada, width=50, max_height=6)
        self.combo_producto.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Variable para almacenar productos disponibles
        self.productos_disponibles = []
        self.lista_productos_completa = []
        
        # Tipo de movimiento
        ttk.Label(frame_entrada, text="Tipo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_tipo = ttk.Combobox(frame_entrada, values=["Entrada", "Salida"], 
                                       width=50, state="readonly")
        self.combo_tipo.grid(row=1, column=1, sticky=tk.EW, padx=5)


        
        # Cantidad
        ttk.Label(frame_entrada, text="Cantidad:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_cantidad = ttk.Entry(frame_entrada, width=50)
        self.entry_cantidad.grid(row=2, column=1, sticky=tk.EW, padx=5)
        
        # Motivo
        ttk.Label(frame_entrada, text="Motivo:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_motivo = ttk.Entry(frame_entrada, width=50)
        self.entry_motivo.grid(row=3, column=1, sticky=tk.EW, padx=5)
        
        # Responsable
        ttk.Label(frame_entrada, text="Responsable:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.combo_responsable = ttk.Combobox(
            frame_entrada,
            values=[
                "Julio",
                "Sara",
                "Yulán",
                "Silvia",
                "Ángel",
                "Practicantes Comunicación",
                "Practicantes Bienestar",
                "Cooperantes"
            ],
            width=48,
            state="readonly"
        )
        self.combo_responsable.grid(row=4, column=1, sticky=tk.EW, padx=5)
        self.combo_responsable.current(0)



        # Botón registrar
        btn_registrar = ttk.Button(frame_entrada, text="✅ Registrar Movimiento", 
                                  command=self._registrar_movimiento)
        btn_registrar.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10, padx=5)
        
        frame_entrada.columnconfigure(1, weight=1)
        
        # Frame de historial rápido
        frame_historial = ttk.LabelFrame(frame, text="Últimos Movimientos", padding=10)
        frame_historial.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scroll = ttk.Scrollbar(frame_historial)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_historial = ttk.Treeview(frame_historial,
                                           columns=("Fecha", "Producto", "Tipo", "Cantidad", "Stock Actual", "Responsable"),
                                           height=10,
                                           yscrollcommand=scroll.set)
        scroll.config(command=self.tree_historial.yview)
        
        self.tree_historial.column("#0", width=0, stretch=tk.NO)
        self.tree_historial.column("Fecha", anchor=tk.CENTER, width=130)
        self.tree_historial.column("Producto", anchor=tk.W, width=200)
        self.tree_historial.column("Tipo", anchor=tk.CENTER, width=80)
        self.tree_historial.column("Cantidad", anchor=tk.CENTER, width=80)
        self.tree_historial.column("Stock Actual", anchor=tk.CENTER, width=100)
        self.tree_historial.column("Responsable", anchor=tk.W, width=150)
        
        self.tree_historial.heading("Fecha", text="Fecha", anchor=tk.CENTER)
        self.tree_historial.heading("Producto", text="Producto", anchor=tk.W)
        self.tree_historial.heading("Tipo", text="Tipo", anchor=tk.CENTER)
        self.tree_historial.heading("Cantidad", text="Cantidad", anchor=tk.CENTER)
        self.tree_historial.heading("Stock Actual", text="Stock Actual", anchor=tk.CENTER)
        self.tree_historial.heading("Responsable", text="Responsable", anchor=tk.W)
        
        self.tree_historial.pack(fill=tk.BOTH, expand=True)
    
    def _crear_pestana_historial(self):
        """Crea la pestaña de historial detallado."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Historial")
        
        # Frame de filtrado por producto
        frame_filtro = ttk.LabelFrame(frame, text="Filtrar Historial", padding=10)
        frame_filtro.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_filtro, text="Seleccionar Producto:").pack(side=tk.LEFT, padx=5)
        self.combo_filtro = ttk.Combobox(frame_filtro, width=40, state="readonly")
        self.combo_filtro.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(frame_filtro, text="🔍 Ver Historial", 
                  command=self._actualizar_historial).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_filtro, text="🔄 Todos", 
                  command=self._mostrar_todo_historial).pack(side=tk.LEFT, padx=5)
        
        # Frame de filtrado por rango de fechas
        frame_fechas = ttk.LabelFrame(frame, text="Buscar por Rango de Fechas (DD/MM/YYYY)", padding=10)
        frame_fechas.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_fechas, text="Desde:").pack(side=tk.LEFT, padx=5)
        self.entry_fecha_inicio = ttk.Entry(frame_fechas, width=15)
        self.entry_fecha_inicio.pack(side=tk.LEFT, padx=5)
        self.entry_fecha_inicio.insert(0, "01/01/2025")
        
        ttk.Label(frame_fechas, text="Hasta:").pack(side=tk.LEFT, padx=5)
        self.entry_fecha_fin = ttk.Entry(frame_fechas, width=15)
        self.entry_fecha_fin.pack(side=tk.LEFT, padx=5)
        self.entry_fecha_fin.insert(0, "31/12/2026")
        
        ttk.Button(frame_fechas, text="🔎 Buscar por Fecha", 
                  command=self._buscar_movimientos_por_fecha).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_fechas, text="🔄 Limpiar Filtros", 
                  command=self._mostrar_todo_historial).pack(side=tk.LEFT, padx=5)
        
        # Frame de tabla
        frame_tabla = ttk.LabelFrame(frame, text="Movimientos Registrados", padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scroll = ttk.Scrollbar(frame_tabla)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_historial_completo = ttk.Treeview(frame_tabla,
                                                     columns=("Fecha", "Mes", "Año", "Tipo", "Producto", "Cantidad", 
                                                             "Stock Antr.", "Stock Nuevo", "Motivo", "Responsable"),
                                                     height=15,
                                                     yscrollcommand=scroll.set)
        scroll.config(command=self.tree_historial_completo.yview)
        
        # Configurar columnas
        self.tree_historial_completo.column("#0", width=0, stretch=tk.NO)
        anchos = {"Fecha": 130, "Mes": 40, "Año": 40, "Tipo": 70, "Producto": 150, "Cantidad": 70,
                 "Stock Antr.": 80, "Stock Nuevo": 80, "Motivo": 120, "Responsable": 100}
        
        for col, ancho in anchos.items():
            self.tree_historial_completo.column(col, anchor=tk.CENTER, width=ancho)
            self.tree_historial_completo.heading(col, text=col, anchor=tk.CENTER)
        
        self.tree_historial_completo.pack(fill=tk.BOTH, expand=True)
    
    def _crear_pestana_reportes(self):
        """Crea la pestaña de reportes."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Reportes")
        
        # Frame de opciones
        frame_opciones = ttk.LabelFrame(frame, text="Generar Reportes", padding=10)
        frame_opciones.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_opciones, text="📈 Generar Reporte Completo", 
                  command=self._generar_reporte).pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(frame_opciones, text="💾 Exportar a Excel", 
                  command=self._exportar_excel).pack(fill=tk.X, padx=5, pady=5)
        
        # Frame de info
        frame_info = ttk.LabelFrame(frame, text="Resumen del Almacén", padding=10)
        frame_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.texto_reporte = scrolledtext.ScrolledText(frame_info, height=20, width=80, 
                                                       state=tk.DISABLED)
        self.texto_reporte.pack(fill=tk.BOTH, expand=True)
    
    def _crear_pestana_importacion(self):
        """Crea la pestaña de importación/exportación."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📥📤 Importar/Exportar")
        
        # Frame de descargar plantilla
        frame_descargar = ttk.LabelFrame(frame, text="Descargar Plantilla", padding=10)
        frame_descargar.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_descargar, 
                 text="Descarga una plantilla Excel para llenarla y luego importarla al sistema.",
                 wraplength=400).pack(pady=5)
        
        ttk.Button(frame_descargar, text="⬇️ Descargar Plantilla", 
                  command=self._descargar_plantilla).pack(fill=tk.X, padx=5, pady=5)
        
        # Frame de importar
        frame_importar = ttk.LabelFrame(frame, text="Importar Productos", padding=10)
        frame_importar.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_importar,
                 text="Selecciona un archivo Excel con productos a cargar.",
                 wraplength=400).pack(pady=5)
        
        ttk.Button(frame_importar, text="📂 Seleccionar Archivo", 
                  command=self._importar_archivo).pack(fill=tk.X, padx=5, pady=5)
        
        # Frame de resultado
        frame_resultado = ttk.LabelFrame(frame, text="Resultado de Importación", padding=10)
        frame_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.texto_importacion = scrolledtext.ScrolledText(frame_resultado, height=15, width=80,
                                                          state=tk.DISABLED)
        self.texto_importacion.pack(fill=tk.BOTH, expand=True)
    
    def _agregar_producto(self):
        """Agrega un nuevo producto."""
        try:
            nombre = self.entry_nombre.get().strip()
            descripcion = self.entry_descripcion.get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre del producto es obligatorio")
                return
            
            # Formatear nombre a titlecase (primera letra mayúscula, resto minúscula)
            nombre = nombre.title()
            
            # Detectar similitud con productos existentes
            producto_similar, similitud = self.db.encontrar_productos_similares(nombre, umbral=0.8)
            
            if producto_similar:
                # Mostrar advertencia sobre similitud con tres opciones
                # Diálogo personalizado de tres opciones
                respuesta = dialogo_tres_opciones(
                    self.root,
                    "Producto Similar Detectado",
                    f"Se encontró un producto muy parecido:\n\n"
                    f"Producto existente: {producto_similar['nombre']}\n"
                    f"Similitud: {similitud*100:.1f}%\n\n"
                    f"¿Qué desea hacer?",
                    opcion1="Modificar su entrada o salida",
                    opcion2="Cancelar proceso",
                    opcion3="Agregar de todas formas"
                )
                if respuesta == "Modificar su entrada o salida":
                    # Redirigir a movimientos con el producto preseleccionado
                    self.notebook.select(1)  # Ir a pestaña de movimientos (índice 1)
                    # Precompletar campos
                    self.combo_producto.set(f"{producto_similar['id']} - {producto_similar['nombre']}")
                    self.combo_tipo.set("Entrada")
                    self.entry_cantidad.focus()
                    messagebox.showinfo("Información", "Por favor completa el movimiento. Los campos de motivo y responsable están vacíos para que los llenes manualmente.")
                    return
                elif respuesta == "Cancelar proceso":
                    # Si dice no, no agrega nada pero mantiene la información
                    messagebox.showinfo("Cancelado", "Se canceló la adición. Los datos se mantienen en el formulario para que puedas revisarlos.")
                    return
                elif respuesta == "Agregar de todas formas":
                    # Opción extra: agregar de todas formas
                    confirm = messagebox.askyesno(
                        "Confirmar duplicado",
                        "¿Está seguro que desea agregar este producto aunque sea similar? Esto puede generar duplicados.")
                    if not confirm:
                        messagebox.showinfo("Cancelado", "No se agregó el producto duplicado.")
                        return
                    # Si confirma, continúa con el flujo normal para agregar el producto duplicado

            
            # Validar stock
            stock_str = self.entry_stock.get().strip()
            try:
                stock = int(stock_str)
                if stock <= 0:
                    messagebox.showerror("Error", "El stock debe ser un número entero mayor o igual a 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "El stock debe ser un número entero válido (sin decimales ni símbolos)")
                return
            
            unidad = self.combo_unidad.get()
            url_imagen = self.entry_url_imagen.get().strip()
            
            id_prod = self.db.agregar_producto(nombre, descripcion, stock, unidad, url_imagen)
            
            # Limpiar campos
            self.entry_nombre.delete(0, tk.END)
            self.entry_descripcion.delete(0, tk.END)
            self.entry_stock.delete(0, tk.END)
            self.combo_unidad.current(0)
            self.entry_url_imagen.delete(0, tk.END)
            
            # Actualizar lista
            self._actualizar_lista_productos()
            
            messagebox.showinfo("Éxito", f"Producto agregado correctamente con ID: {id_prod}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def _actualizar_lista_productos(self):
        """Actualiza la lista de productos en la interfaz."""
        # Limpiar árbol
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Obtener productos
        productos = self.db.obtener_productos()
        
        # Agregar productos al árbol
        for prod in productos:
            self.tree_productos.insert("", "end", 
                                      values=(prod["id"], prod["nombre"], prod["descripcion"],
                                             prod["stock"], prod["unidad"]))
        
        # Actualizar combo de productos en Historial
        opciones = [f"{p['id']} - {p['nombre']}" for p in productos]
        self.combo_filtro.config(values=opciones)
        
        # Actualizar dropdown personalizado de productos en Movimientos
        self.lista_productos_completa = productos
        self.combo_producto.set_items(opciones)
        # Sincronizar productos_disponibles con opciones del dropdown
        self.productos_disponibles = []
        for prod in productos:
            # Solo agregar si está en opciones
            if f"{prod['id']} - {prod['nombre']}" in opciones:
                self.productos_disponibles.append(prod)

    # BACKUP
    def _reiniciar_periodo_desde_ui(self):
        from tkinter import messagebox, filedialog
        from backup_utils import reiniciar_periodo

        confirmar = messagebox.askyesno(
            "Confirmar",
            "⚠️ Esta acción eliminará los datos operativos.\n\n¿Deseas continuar?"
        )

        if not confirmar:
            return

        carpeta = filedialog.askdirectory(title="Selecciona carpeta para respaldo")

        if not carpeta:
            return

        try:
            ruta_excel = "data/almacen.xlsx"

            resultado = reiniciar_periodo(ruta_excel, carpeta)

            if resultado:
                messagebox.showinfo("Éxito", "Periodo reiniciado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo reiniciar el periodo")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    #FIN BACKUP 


    
    def _registrar_movimiento(self):
        """Registra un movimiento de entrada o salida."""
        try:
            seleccion = self.combo_producto.get().strip()
            tipo = self.combo_tipo.get()
            
            # Validar cantidad
            cantidad_str = self.entry_cantidad.get().strip()
            try:
                cantidad = int(cantidad_str)
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero válido (sin decimales ni símbolos)")
                return
            
            motivo = self.entry_motivo.get().strip()
            responsable = self.combo_responsable.get().strip()
            
            if not seleccion or not tipo:
                messagebox.showerror("Error", "Debe seleccionar producto y tipo de movimiento")
                return
            
            # Validar que el producto seleccionado existe realmente
            try:
                id_prod = int(seleccion.split(" - ")[0])
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Debe seleccionar un producto válido de la lista")
                return
            
            prod_en_lista = next((p for p in self.productos_disponibles if p["id"] == id_prod), None)
            if not prod_en_lista:
                messagebox.showerror("Error", "El producto seleccionado no existe o fue eliminado")
                return

            if not motivo:
                messagebox.showerror("Error", "El motivo es obligatorio")
                return
            
            if not responsable:
                messagebox.showerror("Error", "El responsable es obligatorio")
                return
            
            # Registrar movimiento
            resultado = self.db.registrar_movimiento(id_prod, tipo, cantidad, motivo, responsable)
            
            if resultado:
                # Limpiar campos
                self.combo_producto.set("")
                self.combo_tipo.set("")
                self.entry_cantidad.delete(0, tk.END)
                self.entry_motivo.delete(0, tk.END)
                self.combo_responsable.current(0)
                
                # Actualizar información
                self._actualizar_lista_productos()
                self._cargar_historial_rapido()
                
                messagebox.showinfo("Éxito", "Movimiento registrado correctamente")
            else:
                messagebox.showerror("Error", "No hay suficiente stock para esta salida")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")
    
    
    def _cargar_historial_rapido(self):
        """Carga los últimos movimientos en la tabla rápida."""
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)
        
        movimientos = self.db.obtener_movimientos()
        
        # Mostrar últimos 10
        for mov in movimientos[-10:]:
            # Obtener stock actual del producto
            prod = self.db.obtener_producto_por_id(mov["id_producto"])
            stock_actual = prod["stock"] if prod else "-"
            self.tree_historial.insert("", "end",
                                      values=(mov["fecha"], mov["nombre_producto"], 
                                             mov["tipo"], mov["cantidad"], stock_actual, mov["responsable"]))
    
    def _actualizar_historial(self):
        """Actualiza el historial filtrado por producto."""
        seleccion = self.combo_filtro.get()
        
        if not seleccion:
            self._mostrar_todo_historial()
            return
        
        id_prod = int(seleccion.split(" - ")[0])
        
        for item in self.tree_historial_completo.get_children():
            self.tree_historial_completo.delete(item)
        
        movimientos = self.db.obtener_movimientos(id_prod)
        
        for mov in movimientos:
            self.tree_historial_completo.insert("", "end",
                                               values=(mov["fecha"], mov.get("mes", ""), mov.get("año", ""),
                                                      mov["tipo"], mov["nombre_producto"],
                                                      mov["cantidad"], mov["stock_anterior"],
                                                      mov["stock_nuevo"], mov["motivo"], mov["responsable"]))
    
    def _mostrar_todo_historial(self):
        """Muestra todo el historial sin filtro."""
        for item in self.tree_historial_completo.get_children():
            self.tree_historial_completo.delete(item)
        
        movimientos = self.db.obtener_movimientos()
        
        for mov in movimientos:
            self.tree_historial_completo.insert("", "end",
                                               values=(mov["fecha"], mov.get("mes", ""), mov.get("año", ""),
                                                      mov["tipo"], mov["nombre_producto"],
                                                      mov["cantidad"], mov["stock_anterior"],
                                                      mov["stock_nuevo"], mov["motivo"], mov["responsable"]))
    
    def _buscar_movimientos_por_fecha(self):
        """Busca movimientos en un rango de fechas."""
        try:
            fecha_inicio_str = self.entry_fecha_inicio.get().strip()
            fecha_fin_str = self.entry_fecha_fin.get().strip()
            
            # Convertir formato DD/MM/YYYY a YYYY-MM-DD
            from datetime import datetime
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/YYYY")
                return
            
            # Limpiar tabla
            for item in self.tree_historial_completo.get_children():
                self.tree_historial_completo.delete(item)
            
            # Obtener movimientos en el rango
            movimientos = self.db.obtener_movimientos_por_rango_fechas(fecha_inicio, fecha_fin)
            
            if not movimientos:
                messagebox.showinfo("Información", "No hay movimientos en el rango de fechas especificado")
                return
            
            # Mostrar resultados
            for mov in movimientos:
                self.tree_historial_completo.insert("", "end",
                                                   values=(mov["fecha"], mov.get("mes", ""), mov.get("año", ""),
                                                          mov["tipo"], mov["nombre_producto"],
                                                          mov["cantidad"], mov["stock_anterior"],
                                                          mov["stock_nuevo"], mov["motivo"], mov["responsable"]))
            
            messagebox.showinfo("Éxito", f"Se encontraron {len(movimientos)} movimientos en el rango de fechas")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar movimientos: {str(e)}")
    
    def _generar_reporte(self):
        """Genera el reporte completo."""
        try:
            self.db.generar_reporte()
            
            # Obtener información
            productos = self.db.obtener_productos()
            movimientos = self.db.obtener_movimientos()
            
            # Construir texto del reporte
            texto = f"=== REPORTE DE ALMACÉN ===\n"
            texto += f"Fecha de Generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            texto += f"\n{'='*80}\n"
            
            # Resumen general
            total_productos = len(productos)
            total_movimientos = len(movimientos)
            
            texto += f"\n📊 RESUMEN GENERAL:\n"
            texto += f"Total de Productos: {total_productos}\n"
            texto += f"Total de Movimientos: {total_movimientos}\n"
            
            # Detalle por producto
            texto += f"\n{'='*80}\n"
            texto += f"\n📦 DETALLE POR PRODUCTO:\n\n"
            
            for prod in productos:
                texto += f"ID: {prod['id']} | {prod['nombre']}\n"
                texto += f"  Descripción: {prod['descripcion']}\n"
                texto += f"  Stock Actual: {prod['stock']} {prod['unidad']}\n"
                
                # Movimientos del producto
                prod_movs = [m for m in movimientos if m['id_producto'] == prod['id']]
                if prod_movs:
                    entradas = sum(m['cantidad'] for m in prod_movs if m['tipo'].lower() == 'entrada')
                    salidas = sum(m['cantidad'] for m in prod_movs if m['tipo'].lower() == 'salida')
                    texto += f"  Entradas: {entradas} | Salidas: {salidas} | Movimientos: {len(prod_movs)}\n"
                texto += "\n"
            
            # Mostrar en la interfaz
            self.texto_reporte.config(state=tk.NORMAL)
            self.texto_reporte.delete(1.0, tk.END)
            self.texto_reporte.insert(1.0, texto)
            self.texto_reporte.config(state=tk.DISABLED)
            
            messagebox.showinfo("Éxito", "Reporte generado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def _exportar_excel(self):
        """Exporta el contenido a Excel."""
        try:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            if ruta:
                # El archivo Excel ya esta actualizado en la BD
                shutil.copy(self.db.ruta_bd, ruta)
                messagebox.showinfo("Exito", f"Archivo exportado a:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def _descargar_plantilla(self):
        """Descarga la plantilla para cargar productos."""
        try:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile="plantilla_carga.xlsx"
            )
            
            if ruta:
                # Crear plantilla en el directorio de templates
                self.db.exportar_plantilla_carga(ruta)
                messagebox.showinfo("Éxito", f"Plantilla descargada a:\n{ruta}\n\nLlénala y luego importa el archivo")
        except Exception as e:
            messagebox.showerror("Error", f"Error al descargar plantilla: {str(e)}")
    
    def _importar_archivo(self):
        """Importa productos desde un archivo Excel."""
        try:
            ruta = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if ruta:
                cantidad, errores = self.db.cargar_productos_desde_excel(ruta)
                
                # Mostrar resultado
                self.texto_importacion.config(state=tk.NORMAL)
                self.texto_importacion.delete(1.0, tk.END)
                
                resultado = f"RESULTADO DE IMPORTACIÓN\n"
                resultado += f"{'='*60}\n\n"
                resultado += f"✅ Productos importados correctamente: {cantidad}\n\n"
                
                if errores:
                    resultado += f"⚠️ ERRORES ENCONTRADOS ({len(errores)}):\n"
                    for error in errores:
                        resultado += f"  • {error}\n"
                else:
                    resultado += f"✅ No se encontraron errores\n"
                
                self.texto_importacion.insert(1.0, resultado)
                self.texto_importacion.config(state=tk.DISABLED)
                
                # Actualizar lista
                self._actualizar_lista_productos()
                
                messagebox.showinfo("Importación Completada", f"Se importaron {cantidad} productos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar: {str(e)}")


def main():
    """Función principal."""
    root = tk.Tk()
    app = GestorAlmacenesUI(root)
    
    # Cargar datos al iniciar
    app._cargar_historial_rapido()
    app._mostrar_todo_historial()
    
    root.mainloop()


if __name__ == "__main__":
    main()
