"""
Widget modernizado para filtrar por colores
"""
import tkinter as tk
from typing import List, Dict, Callable, Optional, Set

from ...style.color_palette import ColorPalette


class ModernColorFilterWidget(tk.Frame):
    """Widget modernizado para filtrar productos por colores"""

    def __init__(self, parent, colors_data: List[Dict], on_filter_change: Optional[Callable] = None,
                 colors=None, fonts=None):
        super().__init__(parent, bg=ColorPalette.BG)

        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {
            'heading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8)
        }

        self.colors_data = colors_data
        self.on_filter_change = on_filter_change
        self.selected_colors: Set[str] = set()

        # Referencias a widgets
        self.color_chips = {}
        self.canvas = None
        self.inner_frame = None

        self._create_modern_widgets()

    def _create_modern_widgets(self):
        """Crear los widgets del filtro modernos"""
        # Header
        self._create_header()

        # Container principal con scroll horizontal
        self._create_scrollable_container()

        # Botón para limpiar filtros
        self._create_clear_button()

    def _create_header(self):
        """Crear header del widget"""
        header = tk.Frame(self, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 15))

        tk.Label(header, text="🎨 Filtrar por color:",
                 font=self.fonts['heading'],
                 bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)

    def _create_scrollable_container(self):
        """Crear contenedor principal con scroll horizontal"""
        container = tk.Frame(self, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        container.pack(fill=tk.BOTH, expand=True)

        # Canvas con scroll horizontal
        self.canvas = tk.Canvas(container, height=120, bg=self.colors['card'],
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar horizontal
        scrollbar = tk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        scrollbar.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.canvas.configure(xscrollcommand=scrollbar.set)

        # Frame interior para los chips de color
        self.inner_frame = tk.Frame(self.canvas, bg=self.colors['card'])
        self.canvas_window = self.canvas.create_window(0, 0, anchor="nw", window=self.inner_frame)

        # Crear chips de color
        self._create_color_chips()

        # Configurar scroll region
        self._update_scroll_region()

    def _create_color_chips(self):
        """Crear chips de color modernos"""
        for i, color_info in enumerate(self.colors_data):
            chip = ColorChip(
                self.inner_frame,
                color_info,
                on_toggle=self._on_chip_toggle,
                colors=self.colors,
                fonts=self.fonts
            )
            chip.pack(side=tk.LEFT, padx=8, pady=10)
            self.color_chips[color_info['color_hex']] = chip

    def _create_clear_button(self):
        """Crear botón para limpiar filtros"""
        clear_frame = tk.Frame(self, bg=self.colors['bg'])
        clear_frame.pack(fill=tk.X, pady=(10, 0))

        self.clear_btn = tk.Button(clear_frame, text="🗑️ Limpiar filtros",
                                   font=self.fonts['small'],
                                   bg=self.colors['card'], fg=self.colors['text'],
                                   bd=1, relief=tk.FLAT, padx=15, pady=6,
                                   cursor='hand2', command=self.clear_filters)
        self.clear_btn.pack(anchor=tk.W)

        # Efectos hover
        self.clear_btn.bind('<Enter>', lambda e: self.clear_btn.config(bg=self.colors['border']))
        self.clear_btn.bind('<Leave>', lambda e: self.clear_btn.config(bg=self.colors['card']))

    def _update_scroll_region(self):
        """Actualizar región de scroll"""
        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_chip_toggle(self, color_hex: str, selected: bool):
        """Manejar toggle de chip de color"""
        if selected:
            self.selected_colors.add(color_hex)
        else:
            self.selected_colors.discard(color_hex)

        if self.on_filter_change:
            self.on_filter_change(list(self.selected_colors))

    # API pública
    def update_colors_data(self, colors_data: List[Dict]):
        """Actualizar datos de colores"""
        self.colors_data = colors_data

        # Limpiar chips existentes
        for chip in self.color_chips.values():
            chip.destroy()
        self.color_chips.clear()

        # Crear nuevos chips
        self._create_color_chips()
        self._update_scroll_region()

    def clear_filters(self):
        """Limpiar todos los filtros"""
        self.selected_colors.clear()

        # Resetear todos los chips
        for chip in self.color_chips.values():
            chip.set_selected(False)

        if self.on_filter_change:
            self.on_filter_change([])

    def get_selected_colors(self) -> List[str]:
        """Obtener colores seleccionados"""
        return list(self.selected_colors)

    def set_selected_colors(self, colors: List[str]):
        """Establecer colores seleccionados"""
        self.selected_colors = set(colors)

        # Actualizar chips
        for color_hex, chip in self.color_chips.items():
            chip.set_selected(color_hex in self.selected_colors)

    def has_selected_colors(self) -> bool:
        """Verificar si hay colores seleccionados"""
        return len(self.selected_colors) > 0

    def get_filter_summary(self) -> str:
        """Obtener resumen de filtros aplicados"""
        if not self.selected_colors:
            return "Sin filtros aplicados"

        count = len(self.selected_colors)
        return f"{count} color{'es' if count > 1 else ''} seleccionado{'s' if count > 1 else ''}"


class ColorChip(tk.Frame):
    """Chip individual de color para filtro"""

    def __init__(self, parent, color_info: Dict, on_toggle: Callable, colors=None, fonts=None):
        super().__init__(parent, bg=colors['card'] if colors else '#FFFFFF')

        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {'body': ('Segoe UI', 10), 'caption': ('Segoe UI', 8)}

        self.color_info = color_info
        self.on_toggle = on_toggle
        self.is_selected = False

        # Referencias a widgets
        self.chip_button = None
        self.selection_indicator = None

        self._create_chip()

    def _create_chip(self):
        """Crear el chip de color"""
        color_hex = self.color_info['color_hex']
        nombre = self.color_info.get('nombre_color', color_hex)
        cantidad = self.color_info['cantidad']

        # Botón principal del chip
        self.chip_button = tk.Button(
            self, bg=color_hex, bd=0, width=6, height=3,
            cursor='hand2', relief=tk.FLAT,
            command=self._toggle_selection
        )
        self.chip_button.pack()

        # Indicador de selección (inicialmente oculto)
        self.selection_indicator = tk.Frame(self, bg=self.colors['primary'], height=3)
        # No empaquetamos inicialmente

        # Nombre del color (truncado si es muy largo)
        display_name = nombre[:8] + "..." if len(nombre) > 8 else nombre
        name_label = tk.Label(self, text=display_name,
                              font=self.fonts['caption'],
                              bg=self.colors['card'], fg=self.colors['text'])
        name_label.pack(pady=(5, 2))

        # Cantidad
        count_label = tk.Label(self, text=f"({cantidad})",
                               font=('Segoe UI', 7),
                               bg=self.colors['card'], fg=self.colors['text_secondary'])
        count_label.pack()

        # Tooltip con nombre completo
        self._create_tooltip(nombre)

        # Efectos hover
        self._setup_hover_effects()

    def _create_tooltip(self, full_name: str):
        """Crear tooltip con nombre completo del color"""

        def show_tooltip(event):
            if hasattr(self, 'tooltip'):
                return

            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

            label = tk.Label(self.tooltip, text=full_name,
                             background='#FFFFE0', font=self.fonts['caption'],
                             padx=8, pady=4)
            label.pack()

        def hide_tooltip(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                del self.tooltip

        self.chip_button.bind('<Enter>', show_tooltip)
        self.chip_button.bind('<Leave>', hide_tooltip)

    def _setup_hover_effects(self):
        """Configurar efectos hover"""

        def on_enter(event):
            if not self.is_selected:
                self.chip_button.config(relief=tk.RAISED, bd=1)

        def on_leave(event):
            if not self.is_selected:
                self.chip_button.config(relief=tk.FLAT, bd=0)

        self.chip_button.bind('<Enter>', on_enter)
        self.chip_button.bind('<Leave>', on_leave)

    def _toggle_selection(self):
        """Alternar selección del chip"""
        self.set_selected(not self.is_selected)

        if self.on_toggle:
            self.on_toggle(self.color_info['color_hex'], self.is_selected)

    def set_selected(self, selected: bool):
        """Establecer estado de selección"""
        self.is_selected = selected

        if selected:
            self.chip_button.config(relief=tk.SOLID, bd=2)
            self.selection_indicator.pack(fill=tk.X, before=self.chip_button)
        else:
            self.chip_button.config(relief=tk.FLAT, bd=0)
            self.selection_indicator.pack_forget()

    def get_color_hex(self) -> str:
        """Obtener código hex del color"""
        return self.color_info['color_hex']

    def get_color_name(self) -> str:
        """Obtener nombre del color"""
        return self.color_info.get('nombre_color', self.color_info['color_hex'])

    def get_count(self) -> int:
        """Obtener cantidad de productos con este color"""
        return self.color_info['cantidad']


class ColorFilterGroup(tk.Frame):
    """Grupo de filtros de color con categorías"""

    def __init__(self, parent, title: str, colors_data: List[Dict],
                 on_filter_change: Optional[Callable] = None, colors=None, fonts=None):
        super().__init__(parent, bg=ColorPalette.BG)

        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {'heading': ('Segoe UI', 12, 'bold')}

        self.title = title
        self.colors_data = colors_data
        self.on_filter_change = on_filter_change

        self.filter_widget = None
        self.collapsed = False

        self._create_group()

    def _create_group(self):
        """Crear grupo de filtros"""
        # Header con título y botón colapsar
        header = tk.Frame(self, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 10))

        self.toggle_btn = tk.Button(header, text="▼", font=self.fonts['heading'],
                                    bg=self.colors['bg'], fg=self.colors['text'],
                                    bd=0, cursor='hand2', command=self._toggle_collapse)
        self.toggle_btn.pack(side=tk.LEFT)

        tk.Label(header, text=self.title, font=self.fonts['heading'],
                 bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT, padx=(5, 0))

        # Widget de filtro
        self.filter_widget = ModernColorFilterWidget(
            self, self.colors_data, self.on_filter_change, self.colors, self.fonts
        )
        self.filter_widget.pack(fill=tk.BOTH, expand=True)

    def _toggle_collapse(self):
        """Alternar colapso del grupo"""
        self.collapsed = not self.collapsed

        if self.collapsed:
            self.filter_widget.pack_forget()
            self.toggle_btn.config(text="▶")
        else:
            self.filter_widget.pack(fill=tk.BOTH, expand=True)
            self.toggle_btn.config(text="▼")

    def update_colors_data(self, colors_data: List[Dict]):
        """Actualizar datos de colores"""
        self.colors_data = colors_data
        if self.filter_widget:
            self.filter_widget.update_colors_data(colors_data)

    def get_selected_colors(self) -> List[str]:
        """Obtener colores seleccionados"""
        return self.filter_widget.get_selected_colors() if self.filter_widget else []

    def clear_filters(self):
        """Limpiar filtros"""
        if self.filter_widget:
            self.filter_widget.clear_filters()


class AdvancedColorFilter(tk.Frame):
    """Filtro avanzado de colores con múltiples categorías"""

    def __init__(self, parent, on_filter_change: Optional[Callable] = None, colors=None, fonts=None):
        super().__init__(parent, bg=ColorPalette.BG)

        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {'title': ('Segoe UI', 14, 'bold')}

        self.on_filter_change = on_filter_change
        self.filter_groups = {}

        self._create_advanced_filter()

    def _create_advanced_filter(self):
        """Crear filtro avanzado"""
        # Título principal
        title_frame = tk.Frame(self, bg=self.colors['bg'])
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text="🎨 Filtros Avanzados de Color",
                 font=self.fonts['title'],
                 bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)

        # Container principal con scroll
        self._create_scrollable_container()

    def _create_scrollable_container(self):
        """Crear contenedor con scroll para múltiples categorías"""
        canvas = tk.Canvas(self, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.groups_container = scrollable_frame

    def add_filter_group(self, title: str, colors_data: List[Dict]) -> ColorFilterGroup:
        """Agregar grupo de filtros"""
        group = ColorFilterGroup(
            self.groups_container, title, colors_data,
            self._on_group_filter_change, self.colors, self.fonts
        )
        group.pack(fill=tk.X, pady=(0, 15))

        self.filter_groups[title] = group
        return group

    def _on_group_filter_change(self, selected_colors: List[str]):
        """Manejar cambio en filtros de grupo"""
        # Consolidar todos los colores seleccionados de todos los grupos
        all_selected = []
        for group in self.filter_groups.values():
            all_selected.extend(group.get_selected_colors())

        if self.on_filter_change:
            self.on_filter_change(list(set(all_selected)))  # Eliminar duplicados

    def clear_all_filters(self):
        """Limpiar todos los filtros"""
        for group in self.filter_groups.values():
            group.clear_filters()

    def get_all_selected_colors(self) -> List[str]:
        """Obtener todos los colores seleccionados"""
        all_selected = []
        for group in self.filter_groups.values():
            all_selected.extend(group.get_selected_colors())
        return list(set(all_selected))  # Eliminar duplicados