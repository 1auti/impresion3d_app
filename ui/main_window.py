"""
Ventana principal de la aplicación
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
import os
from typing import List, Optional
from PIL import Image, ImageTk

from database.db_manager import DatabaseManager
from models.producto import Producto
from ui.add_product_window import AddProductWindow
from ui.edit_product_window import EditProductWindow
from ui.product_detail_window import ProductDetailWindow
from ui.color_widgets import ColorFilterWidget
from utils.file_utils import FileUtils


class MainWindow:
    """Ventana principal de la aplicación"""

    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Productos - Impresión 3D")
        self.root.geometry("1200x700")

        # Configurar estilo
        self.setup_styles()

        # Base de datos
        self.db_manager = DatabaseManager()

        # Variables
        self.productos_actuales: List[Producto] = []
        self.producto_seleccionado: Optional[Producto] = None
        self.colores_filtrados: List[str] = []  # Colores seleccionados para filtrar

        # Crear interfaz
        self.create_widgets()

        # Cargar productos
        self.cargar_productos()

        # Configurar eventos de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        """Configurar estilos de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')

        # Colores
        self.colors = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'select': '#0078d4',
            'button': '#0078d4',
            'button_hover': '#106ebe',
            'danger': '#d32f2f',
            'success': '#388e3c'
        }

        # Configurar estilos
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))

        # Estilo para botones
        style.configure('Primary.TButton', font=('Arial', 10))
        style.map('Primary.TButton',
                  background=[('active', self.colors['button_hover'])])

        style.configure('Danger.TButton', font=('Arial', 10))
        style.map('Danger.TButton',
                  background=[('active', '#b71c1c')])

    def create_widgets(self):
        """Crear todos los widgets de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(main_frame, text="🖨️ Gestión de Productos para Impresión 3D",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Frame de búsqueda y botones
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))

        # Búsqueda
        ttk.Label(control_frame, text="Buscar:").pack(anchor=tk.W)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.buscar_productos())
        search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=30)
        search_entry.pack(fill=tk.X, pady=(5, 10))

        # Botones de acción
        ttk.Label(control_frame, text="Acciones:", style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))

        ttk.Button(control_frame, text="➕ Nuevo Producto",
                  command=self.nuevo_producto, style='Primary.TButton').pack(fill=tk.X, pady=2)

        self.btn_editar = ttk.Button(control_frame, text="✏️ Editar Producto",
                                     command=self.editar_producto, state='disabled')
        self.btn_editar.pack(fill=tk.X, pady=2)

        self.btn_ver = ttk.Button(control_frame, text="👁️ Ver Detalles",
                                 command=self.ver_detalles, state='disabled')
        self.btn_ver.pack(fill=tk.X, pady=2)

        self.btn_eliminar = ttk.Button(control_frame, text="🗑️ Eliminar",
                                      command=self.eliminar_producto,
                                      state='disabled', style='Danger.TButton')
        self.btn_eliminar.pack(fill=tk.X, pady=2)

        # Separador
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)

        # Filtro de colores
        self.color_filter = None
        self.actualizar_filtro_colores()

        # Separador
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)

        # Botones adicionales
        ttk.Button(control_frame, text="📊 Estadísticas",
                  command=self.mostrar_estadisticas).pack(fill=tk.X, pady=2)

        ttk.Button(control_frame, text="💾 Exportar Datos",
                  command=self.exportar_datos).pack(fill=tk.X, pady=2)

        # Frame de lista de productos
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título de la lista
        ttk.Label(list_frame, text="Lista de Productos", style='Heading.TLabel').pack(anchor=tk.W)

        # Treeview para lista de productos
        columns = ('ID', 'Nombre', 'Colores', 'Material', 'Tiempo', 'Peso')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=20)

        # Configurar columnas
        self.tree.column('#0', width=0, stretch=False)  # Columna oculta
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Nombre', width=250)
        self.tree.column('Colores', width=150)
        self.tree.column('Material', width=80, anchor='center')
        self.tree.column('Tiempo', width=100, anchor='center')
        self.tree.column('Peso', width=80, anchor='center')

        # Encabezados
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre del Producto')
        self.tree.heading('Colores', text='Colores')
        self.tree.heading('Material', text='Material')
        self.tree.heading('Tiempo', text='Tiempo')
        self.tree.heading('Peso', text='Peso (g)')

        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Empaquetar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(5, 0))
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Eventos del treeview
        self.tree.bind('<<TreeviewSelect>>', self.on_select_producto)
        self.tree.bind('<Double-Button-1>', lambda e: self.ver_detalles())

        # Frame de vista previa
        preview_frame = ttk.LabelFrame(main_frame, text="Vista Previa", padding="10")
        preview_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

        # Imagen de vista previa
        self.preview_label = ttk.Label(preview_frame, text="Sin imagen",
                                      relief=tk.SUNKEN, anchor='center')
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # Información de vista previa
        self.info_frame = ttk.Frame(preview_frame)
        self.info_frame.pack(fill=tk.X, pady=(10, 0))

        self.info_labels = {}
        info_fields = ['Nombre:', 'Material:', 'Tiempo:', 'Colores:']
        for field in info_fields:
            frame = ttk.Frame(self.info_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=field, font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
            label = ttk.Label(frame, text="-", font=('Arial', 9))
            label.pack(side=tk.LEFT, padx=(5, 0))
            self.info_labels[field] = label

        # Frame para mostrar muestras de colores
        self.colors_preview_frame = ttk.Frame(self.info_frame)
        self.colors_preview_frame.pack(fill=tk.X, pady=(5, 0))

        # Barra de estado
        self.status_bar = ttk.Label(self.root, text="Listo", relief=tk.SUNKEN)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def cargar_productos(self):
        """Cargar productos desde la base de datos"""
        try:
            self.productos_actuales = self.db_manager.obtener_todos_productos()
            self.actualizar_lista()
            self.actualizar_filtro_colores()  # Actualizar filtro de colores
            self.actualizar_estado(f"Se cargaron {len(self.productos_actuales)} productos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {str(e)}")

    def actualizar_lista(self):
        """Actualizar la lista de productos en el TreeView"""
        # Limpiar lista actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtrar productos si hay colores seleccionados
        productos_mostrar = self.productos_actuales

        if self.colores_filtrados:
            productos_mostrar = [
                p for p in self.productos_actuales
                if any(c.color_hex in self.colores_filtrados for c in p.colores_especificaciones)
            ]

        # Agregar productos
        for producto in productos_mostrar:
            # Obtener representación de colores
            if producto.colores_especificaciones:
                colores_str = ", ".join([
                    f"{c.nombre_color or c.color_hex}"
                    for c in producto.colores_especificaciones[:3]  # Mostrar máximo 3
                ])
                if len(producto.colores_especificaciones) > 3:
                    colores_str += f" (+{len(producto.colores_especificaciones) - 3})"
            else:
                colores_str = producto.color or "Sin color"

            valores = (
                producto.id,
                producto.nombre,
                colores_str,
                producto.material,
                producto.tiempo_impresion_formato(),
                f"{producto.get_peso_total()}g"
            )

            # Insertar con etiquetas para colores (para futura funcionalidad de color en filas)
            item = self.tree.insert('', 'end', values=valores)

            # Agregar tag de color si tiene un color predominante
            if producto.colores_especificaciones:
                color_principal = producto.get_color_principal()
                if color_principal:
                    self.tree.item(item, tags=(color_principal.color_hex,))

        self.actualizar_estado(f"Mostrando {len(productos_mostrar)} productos")

    def buscar_productos(self):
        """Buscar productos según el término de búsqueda"""
        termino = self.search_var.get().strip()

        if termino:
            self.productos_actuales = self.db_manager.buscar_productos(termino)
        else:
            self.productos_actuales = self.db_manager.obtener_todos_productos()

        self.actualizar_lista()
        self.actualizar_estado(f"Mostrando {len(self.productos_actuales)} productos")

    def on_select_producto(self, event):
        """Manejar selección de producto"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            producto_id = item['values'][0]

            # Buscar producto seleccionado
            self.producto_seleccionado = next(
                (p for p in self.productos_actuales if p.id == producto_id), None
            )

            if self.producto_seleccionado:
                self.actualizar_vista_previa()
                self.habilitar_botones(True)
        else:
            self.producto_seleccionado = None
            self.limpiar_vista_previa()
            self.habilitar_botones(False)

    def actualizar_vista_previa(self):
        """Actualizar la vista previa del producto seleccionado"""
        if not self.producto_seleccionado:
            return

        # Actualizar imagen
        if self.producto_seleccionado.imagen_path and os.path.exists(self.producto_seleccionado.imagen_path):
            try:
                img = FileUtils.get_image_thumbnail(self.producto_seleccionado.imagen_path, (200, 200))
                if img:
                    photo = ImageTk.PhotoImage(img)
                    self.preview_label.configure(image=photo, text="")
                    self.preview_label.image = photo  # Mantener referencia
            except Exception as e:
                self.preview_label.configure(image="", text="Error al cargar imagen")
                self.preview_label.image = None
        else:
            self.preview_label.configure(image="", text="Sin imagen")
            self.preview_label.image = None

        # Actualizar información
        self.info_labels['Nombre:'].configure(text=self.producto_seleccionado.nombre[:30])
        self.info_labels['Material:'].configure(text=self.producto_seleccionado.material)
        self.info_labels['Tiempo:'].configure(text=self.producto_seleccionado.tiempo_impresion_formato())

        # Actualizar información de colores
        num_colores = len(self.producto_seleccionado.colores_especificaciones)
        self.info_labels['Colores:'].configure(text=f"{num_colores} color(es)")

        # Limpiar muestras de colores anteriores
        for widget in self.colors_preview_frame.winfo_children():
            widget.destroy()

        # Mostrar muestras de colores (máximo 5)
        if self.producto_seleccionado.colores_especificaciones:
            ttk.Label(self.colors_preview_frame, text="Muestras:",
                     font=('Arial', 8)).pack(side=tk.LEFT, padx=(0, 5))

            for i, color_spec in enumerate(self.producto_seleccionado.colores_especificaciones[:5]):
                color_frame = tk.Frame(self.colors_preview_frame)
                color_frame.pack(side=tk.LEFT, padx=2)

                # Muestra de color
                color_label = tk.Label(color_frame, text="", bg=color_spec.color_hex,
                                     width=2, height=1, relief=tk.RAISED)
                color_label.pack()

                # Tooltip con nombre del color
                self._create_tooltip(color_label,
                                   f"{color_spec.nombre_color or color_spec.color_hex}\n{color_spec.peso_color}g")

            if num_colores > 5:
                ttk.Label(self.colors_preview_frame, text=f"+{num_colores-5}",
                         font=('Arial', 8)).pack(side=tk.LEFT, padx=2)

    def _create_tooltip(self, widget, text):
        """Crear un tooltip simple para un widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0",
                           relief=tk.SOLID, borderwidth=1, font=('Arial', 8))
            label.pack()
            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def limpiar_vista_previa(self):
        """Limpiar la vista previa"""
        self.preview_label.configure(image="", text="Sin imagen")
        self.preview_label.image = None

        for label in self.info_labels.values():
            label.configure(text="-")

        # Limpiar muestras de colores
        for widget in self.colors_preview_frame.winfo_children():
            widget.destroy()

    def habilitar_botones(self, habilitar: bool):
        """Habilitar o deshabilitar botones de acción"""
        estado = 'normal' if habilitar else 'disabled'
        self.btn_editar.configure(state=estado)
        self.btn_ver.configure(state=estado)
        self.btn_eliminar.configure(state=estado)

    def nuevo_producto(self):
        """Abrir ventana para crear nuevo producto"""
        ventana = AddProductWindow(self.root, self.db_manager)
        self.root.wait_window(ventana.window)

        if ventana.producto_creado:
            self.cargar_productos()
            self.actualizar_estado("Producto creado exitosamente")

    def editar_producto(self):
        """Abrir ventana para editar producto seleccionado"""
        if not self.producto_seleccionado:
            return

        ventana = EditProductWindow(self.root, self.db_manager, self.producto_seleccionado)
        self.root.wait_window(ventana.window)

        if ventana.producto_actualizado:
            self.cargar_productos()
            self.actualizar_estado("Producto actualizado exitosamente")

    def ver_detalles(self):
        """Ver detalles del producto seleccionado"""
        if not self.producto_seleccionado:
            return

        ventana = ProductDetailWindow(self.root, self.producto_seleccionado)
        self.root.wait_window(ventana.window)

    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        if not self.producto_seleccionado:
            return

        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el producto '{self.producto_seleccionado.nombre}'?\n"
            f"Esta acción no se puede deshacer."
        )

        if respuesta:
            try:
                # Eliminar imagen si existe
                if self.producto_seleccionado.imagen_path:
                    FileUtils.delete_product_image(self.producto_seleccionado.imagen_path)

                # Eliminar de la base de datos
                if self.db_manager.eliminar_producto(self.producto_seleccionado.id):
                    self.cargar_productos()
                    self.actualizar_estado("Producto eliminado exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el producto")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")

    def mostrar_estadisticas(self):
        """Mostrar ventana de estadísticas"""
        try:
            stats = self.db_manager.obtener_estadisticas()

            # Crear ventana de estadísticas
            stats_window = tk.Toplevel(self.root)
            stats_window.title("Estadísticas")
            stats_window.geometry("450x400")
            stats_window.transient(self.root)
            stats_window.grab_set()

            # Frame principal
            frame = ttk.Frame(stats_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)

            # Título
            ttk.Label(frame, text="📊 Estadísticas de Productos",
                     style='Title.TLabel').pack(pady=(0, 20))

            # Estadísticas generales
            ttk.Label(frame, text=f"Total de productos: {stats['total_productos']}",
                     font=('Arial', 11)).pack(anchor=tk.W, pady=5)

            ttk.Label(frame, text=f"Tiempo promedio de impresión: {stats['tiempo_promedio_impresion']:.0f} minutos",
                     font=('Arial', 11)).pack(anchor=tk.W, pady=5)

            # Estadísticas de colores
            ttk.Label(frame, text=f"Total de colores únicos: {stats['total_colores']}",
                     font=('Arial', 11)).pack(anchor=tk.W, pady=5)

            ttk.Label(frame, text=f"Promedio de colores por producto: {stats['promedio_colores_por_producto']}",
                     font=('Arial', 11)).pack(anchor=tk.W, pady=5)

            # Productos por material
            ttk.Label(frame, text="Productos por material:",
                     font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(15, 5))

            for material, cantidad in stats['productos_por_material'].items():
                ttk.Label(frame, text=f"  • {material}: {cantidad} productos",
                         font=('Arial', 10)).pack(anchor=tk.W, pady=2)

            # Botón cerrar
            ttk.Button(frame, text="Cerrar",
                      command=stats_window.destroy).pack(pady=(20, 0))

            # Centrar ventana
            stats_window.update_idletasks()
            x = (stats_window.winfo_screenwidth() // 2) - (stats_window.winfo_width() // 2)
            y = (stats_window.winfo_screenheight() // 2) - (stats_window.winfo_height() // 2)
            stats_window.geometry(f'+{x}+{y}')

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener estadísticas: {str(e)}")

    def exportar_datos(self):
        """Exportar datos de productos"""
        try:
            # Solicitar archivo de destino
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Exportar productos"
            )

            if file_path:
                # Preparar datos para exportar
                productos_data = []
                for producto in self.db_manager.obtener_todos_productos():
                    productos_data.append(producto.to_dict())

                # Exportar
                export_data = {
                    'version': '1.0',
                    'total_productos': len(productos_data),
                    'productos': productos_data
                }

                if FileUtils.export_product_data(export_data, file_path):
                    messagebox.showinfo("Éxito", f"Datos exportados exitosamente a:\n{file_path}")
                else:
                    messagebox.showerror("Error", "Error al exportar datos")

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def actualizar_estado(self, mensaje: str):
        """Actualizar barra de estado"""
        self.status_bar.configure(text=mensaje)

    def actualizar_filtro_colores(self):
        """Actualizar el widget de filtro de colores"""
        # Obtener colores disponibles
        colores = self.db_manager.obtener_colores_disponibles()

        if colores:
            # Eliminar filtro anterior si existe
            if hasattr(self, 'color_filter') and self.color_filter:
                self.color_filter.destroy()

            # Buscar el control_frame correcto
            # El control_frame es donde están los botones y la búsqueda
            # Necesitamos encontrar el segundo separador y poner el filtro después
            control_frame = None
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Frame):
                            # Verificar si este frame tiene el search_var
                            for subchild in child.winfo_children():
                                if isinstance(subchild, ttk.Entry) and hasattr(self, 'search_var'):
                                    if subchild.cget('textvariable') == str(self.search_var):
                                        control_frame = child
                                        break

            if control_frame:
                # Crear el filtro de colores
                self.color_filter = ColorFilterWidget(
                    control_frame,
                    colores,
                    on_filter_change=self.aplicar_filtro_color
                )

                # Encontrar la posición correcta (después del primer separador)
                separators = [w for w in control_frame.winfo_children() if isinstance(w, ttk.Separator)]
                if separators:
                    # Colocar después del primer separador
                    self.color_filter.pack(after=separators[0], fill=tk.X, pady=10)

    def aplicar_filtro_color(self, colores_seleccionados):
        """Aplicar filtro de colores a la lista"""
        self.colores_filtrados = colores_seleccionados
        self.actualizar_lista()

    def on_closing(self):
        """Manejar cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.root.destroy()