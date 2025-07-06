"""
Componente Lista de Productos para mostrar y manejar la lista principal
"""
import tkinter as tk
from tkinter import ttk
from .modern_widgets import ModernTreeview
from ..style.color_palette import ColorPalette


class ProductListComponent:
    """Componente moderno para la lista de productos"""

    def __init__(self, parent, on_selection_change=None, on_double_click=None):
        self.parent = parent
        self.colors = ColorPalette.get_colors_dict()
        self.fonts = {
            'heading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 10),
        }

        # Callbacks
        self.on_selection_change = on_selection_change
        self.on_double_click = on_double_click

        # Referencias
        self.product_count_label = None
        self.tree_wrapper = None

        self.create_product_list()

    def create_product_list(self):
        """Crear lista de productos moderna"""
        # Frame principal
        self.main_frame = tk.Frame(self.parent, bg=self.colors['card'],
                                   highlightbackground=self.colors['border'],
                                   highlightthickness=1)

        # Contenido
        main_content = tk.Frame(self.main_frame, bg=self.colors['card'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header de la lista
        self._create_list_header(main_content)

        # Contenedor del Treeview
        self._create_treeview_container(main_content)

    def _create_list_header(self, parent):
        """Crear header de la lista"""
        list_header = tk.Frame(parent, bg=self.colors['card'])
        list_header.pack(fill=tk.X, pady=(0, 20))

        tk.Label(list_header, text="📦 Lista de Productos",
                 font=self.fonts['heading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        # Contador de productos
        self.product_count_label = tk.Label(list_header, text="0 productos",
                                            font=self.fonts['body'],
                                            bg=self.colors['card'],
                                            fg=self.colors['text_secondary'])
        self.product_count_label.pack(side=tk.RIGHT)

    def _create_treeview_container(self, parent):
        """Crear contenedor del Treeview"""
        tree_container = tk.Frame(parent, bg=self.colors['border'],
                                  highlightthickness=1,
                                  highlightbackground=self.colors['border'])
        tree_container.pack(fill=tk.BOTH, expand=True)

        # Configurar columnas
        columns = ('ID', 'Nombre', 'Colores', 'Material', 'Tiempo', 'Peso')

        # Crear Treeview moderno
        self.tree_wrapper = ModernTreeview(tree_container, columns, self.colors, self.fonts)

        # Configurar columnas
        column_config = {
            '#0': {'width': 0, 'stretch': False},
            'ID': {'width': 60, 'anchor': 'center', 'heading': 'ID'},
            'Nombre': {'width': 300, 'heading': 'Nombre del Producto'},
            'Colores': {'width': 200, 'heading': 'Colores'},
            'Material': {'width': 100, 'anchor': 'center', 'heading': 'Material'},
            'Tiempo': {'width': 120, 'anchor': 'center', 'heading': 'Tiempo'},
            'Peso': {'width': 100, 'anchor': 'center', 'heading': 'Peso'}
        }

        self.tree_wrapper.configure_columns(column_config)
        self.tree_wrapper.pack_with_scrollbar()

        # Configurar eventos
        self.tree_wrapper.tree.bind('<<TreeviewSelect>>', self._on_selection_change)
        self.tree_wrapper.tree.bind('<Double-Button-1>', self._on_double_click)

    def pack(self, **kwargs):
        """Empaquetar el componente"""
        self.main_frame.pack(**kwargs)
        return self.main_frame

    def grid(self, **kwargs):
        """Posicionar el componente con grid"""
        self.main_frame.grid(**kwargs)
        return self.main_frame

    def update_product_list(self, productos, colores_filtrados=None):
        """Actualizar lista de productos"""
        # Filtrar productos si hay filtros de color activos
        productos_mostrar = productos

        if colores_filtrados:
            productos_mostrar = [
                p for p in productos
                if self._product_has_filtered_colors(p, colores_filtrados)
            ]

        # Preparar datos para el treeview
        productos_data = []
        for producto in productos_mostrar:
            # Formatear colores
            colores_str = self._format_product_colors(producto)

            valores = (
                producto.id,
                producto.nombre,
                colores_str,
                producto.material,
                producto.tiempo_impresion_formato(),
                f"{producto.get_peso_total()}g"
            )
            productos_data.append(valores)

        # Actualizar treeview
        self.tree_wrapper.clear_and_populate(productos_data)

        # Actualizar contador
        self.product_count_label.config(text=f"{len(productos_mostrar)} productos")

    def _product_has_filtered_colors(self, producto, colores_filtrados):
        """Verificar si el producto tiene alguno de los colores filtrados"""
        if hasattr(producto, 'colores_especificaciones') and producto.colores_especificaciones:
            return any(c.color_hex in colores_filtrados for c in producto.colores_especificaciones)
        elif hasattr(producto, 'color') and producto.color:
            return producto.color in colores_filtrados
        return False

    def _format_product_colors(self, producto):
        """Formatear colores del producto para mostrar"""
        if hasattr(producto, 'colores_especificaciones') and producto.colores_especificaciones:
            colores_str = ", ".join([
                c.nombre_color or c.color_hex
                for c in producto.colores_especificaciones[:3]
            ])
            if len(producto.colores_especificaciones) > 3:
                colores_str += f" (+{len(producto.colores_especificaciones) - 3})"
            return colores_str
        elif hasattr(producto, 'color') and producto.color:
            return producto.color
        else:
            return "Sin color"

    def get_selected_product_id(self):
        """Obtener ID del producto seleccionado"""
        valores = self.tree_wrapper.get_selected_values()
        if valores:
            return valores[0]  # El ID está en la primera columna
        return None

    def clear_selection(self):
        """Limpiar selección actual"""
        for item in self.tree_wrapper.tree.selection():
            self.tree_wrapper.tree.selection_remove(item)

    def _on_selection_change(self, event):
        """Manejar cambio de selección"""
        if self.on_selection_change:
            producto_id = self.get_selected_product_id()
            self.on_selection_change(producto_id)

    def _on_double_click(self, event):
        """Manejar doble clic"""
        if self.on_double_click:
            producto_id = self.get_selected_product_id()
            if producto_id:
                self.on_double_click(producto_id)