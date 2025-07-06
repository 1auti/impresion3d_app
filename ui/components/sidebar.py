"""
Componente Sidebar para la aplicación
"""
import tkinter as tk
from .modern_widgets import ModernWidgets
from ..style.color_palette import ColorPalette


class SidebarComponent:
    """Componente moderno para el sidebar de la aplicación"""

    def __init__(self, parent, callbacks=None):
        self.parent = parent
        self.colors = ColorPalette.get_colors_dict()
        self.widgets = ModernWidgets()
        self.callbacks = callbacks or {}

        # Variables
        self.search_var = tk.StringVar()
        self.colores_filtrados = []

        # Referencias a botones para habilitar/deshabilitar
        self.btn_editar = None
        self.btn_ver = None
        self.btn_eliminar = None

        self.create_sidebar()

        # Configurar eventos
        self.search_var.trace('w', lambda *args: self._on_search_change())

    def create_sidebar(self):
        """Crear sidebar moderno"""
        # Frame del sidebar con sombra
        self.sidebar_container = tk.Frame(self.parent, bg=self.colors['bg'])

        self.sidebar = tk.Frame(self.sidebar_container, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        self.sidebar.pack(fill=tk.BOTH, expand=True)

        # Padding interno
        sidebar_content = tk.Frame(self.sidebar, bg=self.colors['card'])
        sidebar_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Secciones del sidebar
        self._create_search_section(sidebar_content)
        self._create_actions_section(sidebar_content)
        self._create_separator(sidebar_content)
        self._create_filters_section(sidebar_content)
        self._create_stats_section(sidebar_content)

    def _create_search_section(self, parent):
        """Crear sección de búsqueda"""
        search_frame = tk.Frame(parent, bg=self.colors['card'])
        search_frame.pack(fill=tk.X, pady=(0, 20))

        search_label = tk.Label(search_frame, text="🔍 Buscar productos",
                               font=('Segoe UI', 12),
                               bg=self.colors['card'], fg=self.colors['text'])
        search_label.pack(anchor=tk.W, pady=(0, 10))

        search_entry = self.widgets.create_modern_entry(
            search_frame, self.search_var, "Nombre, material, color..."
        )
        search_entry.pack(fill=tk.X)

    def _create_actions_section(self, parent):
        """Crear sección de acciones"""
        tk.Label(parent, text="Acciones", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(20, 10))

        # Botón nuevo producto
        new_btn = self.widgets.create_modern_button(
            parent, "➕ Nuevo Producto", self._on_new_product, 'primary'
        )
        new_btn.pack(fill=tk.X, pady=5)

        # Botones de edición
        self.btn_editar = self.widgets.create_modern_button(
            parent, "✏️ Editar Producto", self._on_edit_product, 'secondary'
        )
        self.btn_editar.pack(fill=tk.X, pady=5)
        self.btn_editar.inner_button.config(state='disabled')

        self.btn_ver = self.widgets.create_modern_button(
            parent, "👁️ Ver Detalles", self._on_view_details, 'secondary'
        )
        self.btn_ver.pack(fill=tk.X, pady=5)
        self.btn_ver.inner_button.config(state='disabled')

        self.btn_eliminar = self.widgets.create_modern_button(
            parent, "🗑️ Eliminar", self._on_delete_product, 'danger'
        )
        self.btn_eliminar.pack(fill=tk.X, pady=5)
        self.btn_eliminar.inner_button.config(state='disabled')

    def _create_separator(self, parent):
        """Crear separador visual"""
        separator = tk.Frame(parent, height=2, bg=self.colors['border'])
        separator.pack(fill=tk.X, pady=20)

    def _create_filters_section(self, parent):
        """Crear sección de filtros de color"""
        filter_frame = tk.Frame(parent, bg=self.colors['card'])
        filter_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(filter_frame, text="🎨 Filtrar por color",
                font=('Segoe UI', 12),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        # Frame que se actualizará dinámicamente con los colores
        self.color_filter_frame = tk.Frame(filter_frame, bg=self.colors['card'])
        self.color_filter_frame.pack(fill=tk.X)

    def _create_stats_section(self, parent):
        """Crear sección de estadísticas rápidas"""
        stats_frame = tk.Frame(parent, bg=self.colors['card'])
        stats_frame.pack(fill=tk.X)

        tk.Label(stats_frame, text="📊 Resumen",
                font=('Segoe UI', 12),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        # Grid de estadísticas
        stats_grid = tk.Frame(stats_frame, bg=self.colors['card'])
        stats_grid.pack(fill=tk.X)

        # Stat cards
        self.widgets.create_stat_card(stats_grid, "42", "Productos", self.colors['primary'], 0, 0)
        self.widgets.create_stat_card(stats_grid, "156h", "Tiempo Total", self.colors['success'], 0, 1)
        self.widgets.create_stat_card(stats_grid, "2.5kg", "Material", self.colors['warning'], 1, 0)
        self.widgets.create_stat_card(stats_grid, "6", "Colores", self.colors['secondary'], 1, 1)

    def pack(self, **kwargs):
        """Empaquetar el sidebar"""
        self.sidebar_container.pack(**kwargs)
        return self.sidebar_container

    def grid(self, **kwargs):
        """Posicionar el sidebar con grid"""
        self.sidebar_container.grid(**kwargs)
        return self.sidebar_container

    def enable_buttons(self, enable=True):
        """Habilitar/deshabilitar botones de acción"""
        estado = 'normal' if enable else 'disabled'

        buttons = [self.btn_editar, self.btn_ver, self.btn_eliminar]
        button_styles = ['secondary', 'secondary', 'danger']

        for btn, style in zip(buttons, button_styles):
            if btn and hasattr(btn, 'inner_button'):
                btn.inner_button.config(state=estado)

                if estado == 'disabled':
                    btn.inner_button.config(bg='#E0E0E0', fg='#A0A0A0')
                    btn.config(bg='#E0E0E0')
                else:
                    # Restaurar colores según el estilo
                    if style == 'danger':
                        btn.inner_button.config(bg=self.colors['danger'], fg='white')
                        btn.config(bg=self.colors['danger'])
                    else:
                        btn.inner_button.config(bg=self.colors['card'], fg=self.colors['text'])
                        btn.config(bg=self.colors['card'])

    def update_color_filters(self, colores_disponibles):
        """Actualizar filtros de color"""
        # Limpiar filtros anteriores
        for widget in self.color_filter_frame.winfo_children():
            widget.destroy()

        if colores_disponibles:
            # Crear chips de color
            for color_info in colores_disponibles[:8]:  # Mostrar máximo 8 colores
                self._create_color_chip(color_info)

            # Botón para limpiar filtros
            if self.colores_filtrados:
                clear_btn = tk.Button(self.color_filter_frame, text="✕ Limpiar",
                                    font=('Segoe UI', 9),
                                    bg=self.colors['card'], fg=self.colors['danger'],
                                    bd=0, padx=10, pady=5,
                                    cursor='hand2',
                                    command=self._clear_filters)
                clear_btn.pack(side=tk.LEFT, padx=5)

    def _create_color_chip(self, color_info):
        """Crear chip de color para filtro"""
        chip_frame = tk.Frame(self.color_filter_frame, bg=self.colors['card'])
        chip_frame.pack(side=tk.LEFT, padx=3, pady=3)

        # Color chip
        color_btn = tk.Button(chip_frame, text="", bg=color_info['color_hex'],
                            width=4, height=2, bd=0, cursor='hand2',
                            command=lambda c=color_info['color_hex']: self._toggle_color_filter(c))
        color_btn.pack()

        # Badge con cantidad
        badge = tk.Label(chip_frame, text=str(color_info['cantidad']),
                       font=('Segoe UI', 8), bg=self.colors['text'], fg='white',
                       padx=4, pady=0)
        badge.place(relx=1, rely=0, anchor='ne')

        # Marcar si está activo
        if color_info['color_hex'] in self.colores_filtrados:
            chip_frame.config(highlightthickness=2, highlightbackground=self.colors['primary'])

        # Tooltip
        self.widgets.create_tooltip(color_btn, color_info.get('nombre_color', color_info['color_hex']))

    # Métodos de eventos (callbacks)
    def _on_search_change(self):
        """Manejar cambio en la búsqueda"""
        if 'on_search' in self.callbacks:
            self.callbacks['on_search'](self.search_var.get())

    def _on_new_product(self):
        """Manejar nuevo producto"""
        if 'on_new_product' in self.callbacks:
            self.callbacks['on_new_product']()

    def _on_edit_product(self):
        """Manejar edición de producto"""
        if 'on_edit_product' in self.callbacks:
            self.callbacks['on_edit_product']()

    def _on_view_details(self):
        """Manejar ver detalles"""
        if 'on_view_details' in self.callbacks:
            self.callbacks['on_view_details']()

    def _on_delete_product(self):
        """Manejar eliminación de producto"""
        if 'on_delete_product' in self.callbacks:
            self.callbacks['on_delete_product']()

    def _toggle_color_filter(self, color_hex):
        """Alternar filtro de color"""
        if color_hex in self.colores_filtrados:
            self.colores_filtrados.remove(color_hex)
        else:
            self.colores_filtrados.append(color_hex)

        if 'on_color_filter_change' in self.callbacks:
            self.callbacks['on_color_filter_change'](self.colores_filtrados)

    def _clear_filters(self):
        """Limpiar todos los filtros de color"""
        self.colores_filtrados = []
        if 'on_color_filter_change' in self.callbacks:
            self.callbacks['on_color_filter_change'](self.colores_filtrados)