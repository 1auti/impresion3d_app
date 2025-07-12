"""
Componente Sidebar para la aplicación - CORREGIDO
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

        # Referencias para estadísticas dinámicas
        self.stats_labels = {}
        self.color_filter_frame = None

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

        # Header con contador de filtros activos
        header_frame = tk.Frame(filter_frame, bg=self.colors['card'])
        header_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(header_frame, text="🎨 Filtrar por color",
                font=('Segoe UI', 12),
                bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        self.filter_count_label = tk.Label(header_frame, text="",
                                          font=('Segoe UI', 9),
                                          bg=self.colors['card'], fg=self.colors['primary'])
        self.filter_count_label.pack(side=tk.RIGHT)

        # Frame que se actualizará dinámicamente con los colores
        self.color_filter_frame = tk.Frame(filter_frame, bg=self.colors['card'])
        self.color_filter_frame.pack(fill=tk.X)

    def _create_stats_section(self, parent):
        """Crear sección de estadísticas dinámicas"""
        stats_frame = tk.Frame(parent, bg=self.colors['card'])
        stats_frame.pack(fill=tk.X)

        tk.Label(stats_frame, text="📊 Resumen",
                font=('Segoe UI', 12),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        # Grid de estadísticas
        stats_grid = tk.Frame(stats_frame, bg=self.colors['card'])
        stats_grid.pack(fill=tk.X)

        # Configurar grid para 2 columnas
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)

        # Crear stat cards dinámicos
        self._create_dynamic_stat_card(stats_grid, "productos", "Productos", self.colors['primary'], 0, 0)
        self._create_dynamic_stat_card(stats_grid, "tiempo", "Tiempo Total", self.colors['success'], 0, 1)
        self._create_dynamic_stat_card(stats_grid, "material", "Material", self.colors['warning'], 1, 0)
        self._create_dynamic_stat_card(stats_grid, "colores", "Colores", self.colors['secondary'], 1, 1)

    def _create_dynamic_stat_card(self, parent, stat_key, label, color, row, col):
        """Crear tarjeta de estadística dinámica"""
        card = tk.Frame(parent, bg=color, highlightthickness=0)
        card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

        # Contenido
        content = tk.Frame(card, bg=color)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Valor (inicialmente 0)
        value_label = tk.Label(content, text="0", font=('Segoe UI', 20, 'bold'),
                              bg=color, fg='white')
        value_label.pack()

        # Label
        label_widget = tk.Label(content, text=label, font=('Segoe UI', 8),
                               bg=color, fg='white')
        label_widget.pack()

        # Guardar referencias
        self.stats_labels[stat_key] = value_label

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
        """Actualizar filtros de color - CORREGIDO"""
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

        # Actualizar contador de filtros
        self._update_filter_count()

    def _create_color_chip(self, color_info):
        """Crear chip de color para filtro - CORREGIDO"""
        chip_frame = tk.Frame(self.color_filter_frame, bg=self.colors['card'])
        chip_frame.pack(side=tk.LEFT, padx=3, pady=3)

        # Estado activo/inactivo
        is_active = color_info['color_hex'] in self.colores_filtrados
        border_color = self.colors['primary'] if is_active else self.colors['border']

        # Color chip
        color_btn = tk.Button(chip_frame, text="", bg=color_info['color_hex'],
                            width=4, height=2, bd=2, relief='solid',
                            highlightbackground=border_color,
                            highlightcolor=border_color,
                            highlightthickness=2 if is_active else 1,
                            cursor='hand2',
                            command=lambda c=color_info['color_hex']: self._toggle_color_filter(c))
        color_btn.pack()

        # Badge con cantidad
        badge = tk.Label(chip_frame, text=str(color_info['cantidad']),
                       font=('Segoe UI', 8), bg=self.colors['text'], fg='white',
                       padx=4, pady=0)
        badge.place(relx=1, rely=0, anchor='ne')

        # Tooltip
        self.widgets.create_tooltip(color_btn, color_info.get('nombre_color', color_info['color_hex']))

    def update_stats(self, stats_data):
        """Actualizar estadísticas dinámicamente"""
        try:
            # Actualizar productos
            if 'productos' in self.stats_labels:
                total = stats_data.get('total_productos', 0)
                self.stats_labels['productos'].config(text=str(total))

            # Actualizar tiempo total
            if 'tiempo' in self.stats_labels:
                tiempo_promedio = stats_data.get('tiempo_promedio_impresion', 0)
                tiempo_str = f"{int(tiempo_promedio)}min" if tiempo_promedio else "0min"
                self.stats_labels['tiempo'].config(text=tiempo_str)

            # Actualizar material más usado
            if 'material' in self.stats_labels:
                materiales = stats_data.get('productos_por_material', {})
                if materiales:
                    material_principal = max(materiales.items(), key=lambda x: x[1])
                    self.stats_labels['material'].config(text=material_principal[0])
                else:
                    self.stats_labels['material'].config(text="N/A")

            # Actualizar colores únicos
            if 'colores' in self.stats_labels:
                total_colores = stats_data.get('total_colores', 0)
                self.stats_labels['colores'].config(text=str(total_colores))

        except Exception as e:
            print(f"Error actualizando estadísticas: {e}")

    def _update_filter_count(self):
        """Actualizar contador de filtros activos"""
        count = len(self.colores_filtrados)
        if count > 0:
            self.filter_count_label.config(text=f"({count} activos)")
        else:
            self.filter_count_label.config(text="")

    # Métodos de eventos (callbacks)
    def _on_search_change(self):
        """Manejar cambio en la búsqueda"""
        if 'on_search' in self.callbacks:
            search_term = self.search_var.get()
            # No buscar el placeholder
            if search_term != "Nombre, material, color...":
                self.callbacks['on_search'](search_term)

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
        """Alternar filtro de color - CORREGIDO"""
        if color_hex in self.colores_filtrados:
            self.colores_filtrados.remove(color_hex)
        else:
            self.colores_filtrados.append(color_hex)

        # Actualizar visual de los chips
        self._refresh_color_chips()

        # Notificar cambio
        if 'on_color_filter_change' in self.callbacks:
            self.callbacks['on_color_filter_change'](self.colores_filtrados)

        # Actualizar contador
        self._update_filter_count()

    def _refresh_color_chips(self):
        """Refrescar visual de los chips de color"""
        for widget in self.color_filter_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button) and child.cget('bg').startswith('#'):
                        color_hex = child.cget('bg')
                        is_active = color_hex in self.colores_filtrados
                        border_color = self.colors['primary'] if is_active else self.colors['border']
                        child.config(
                            highlightbackground=border_color,
                            highlightthickness=2 if is_active else 1
                        )

    def _clear_filters(self):
        """Limpiar todos los filtros de color"""
        self.colores_filtrados = []
        self._refresh_color_chips()
        self._update_filter_count()

        if 'on_color_filter_change' in self.callbacks:
            self.callbacks['on_color_filter_change'](self.colores_filtrados)