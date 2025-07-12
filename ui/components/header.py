""" Componente Header para la aplicacion """

import tkinter as tk
from .modern_widgets import  ModernWidgets
from ..style.color_palette import  ColorPalette

class HeaderComponent:
    """ Componente Header para la apliacion """

    def __init__(self, parent, on_stats_click=None, on_export_click=None):
        self.parent = parent
        self.colors = ColorPalette.get_colors_dict()
        self.widgets = ModernWidgets()
        self.on_stats_click = on_stats_click
        self.on_export_click = on_export_click

        self.create_header()

    def create_header(self):
        """Crear header moderno con gradiente"""
        self.header_frame = tk.Frame(self.parent, bg=self.colors['primary'], height=80)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)

        # Contenido del header
        header_content = tk.Frame(self.header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Logo y título
        self._create_logo_section(header_content)

        # Botones del header
        self._create_buttons_section(header_content)

    def _create_logo_section(self, parent):
        """Crear sección del logo y título - SOLUCIÓN SIMPLE"""
        logo_frame = tk.Frame(parent, bg=self.colors['primary'])
        logo_frame.pack(side=tk.LEFT, anchor='center')  # ✅ Centrado vertical

        # Frame horizontal para icono + textos
        horizontal_container = tk.Frame(logo_frame, bg=self.colors['primary'])
        horizontal_container.pack(anchor='center', pady=10)  # ✅ Centrado con padding

        # Icono
        icon_label = tk.Label(horizontal_container, text="🎯",
                              font=('Segoe UI', 24),  # ✅ Tamaño proporcionado
                              bg=self.colors['primary'], fg='white')
        icon_label.pack(side=tk.LEFT, padx=(0, 12))

        # Frame vertical SOLO para los textos
        text_container = tk.Frame(horizontal_container, bg=self.colors['primary'])
        text_container.pack(side=tk.LEFT, anchor='center')  # ✅ Centrado vertical

        # Título principal
        title_label = tk.Label(text_container, text="3D Print Manager",
                               font=('Segoe UI', 18, 'bold'),  # ✅ Tamaño ajustado
                               bg=self.colors['primary'], fg='white')
        title_label.pack(anchor='w')  # ✅ Alineado a la izquierda del contenedor

        # Subtítulo en línea separada
        subtitle_label = tk.Label(text_container,
                                  text="Sistema de Gestión de Impresiones 3D",
                                  font=('Segoe UI', 8),  # ✅ Más pequeño para mejor proporción
                                  bg=self.colors['primary'],
                                  fg='white')  # ✅ Color sólido, no rgba
        subtitle_label.pack(anchor='w', pady=(0, 2))  # ✅ Pequeño padding inferior

    def _create_buttons_section(self, parent):
        """Crear sección de botones del header"""
        header_buttons = tk.Frame(parent, bg=self.colors['primary'])
        header_buttons.pack(side=tk.RIGHT)

        # Botón de estadísticas
        if self.on_stats_click:
            stats_btn = self.widgets.create_header_button(
                header_buttons, "📊 Estadísticas", self.on_stats_click
            )
            stats_btn.pack(side=tk.LEFT, padx=5)

        # Botón de exportar
        if self.on_export_click:
            export_btn = self.widgets.create_header_button(
                header_buttons, "💾 Exportar", self.on_export_click
            )
            export_btn.pack(side=tk.LEFT)

    def update_title(self, title, subtitle=None):
        """Actualizar título del header"""
        # Esta función podría implementarse para cambiar dinámicamente el título
        pass
