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
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        # Logo y título
        self._create_logo_section(header_content)

        # Botones del header
        self._create_buttons_section(header_content)

    def _create_logo_section(self, parent):
        """Crear sección del logo y título"""
        logo_frame = tk.Frame(parent, bg=self.colors['primary'])
        logo_frame.pack(side=tk.LEFT)

        # Icono con emoji
        icon_label = tk.Label(logo_frame, text="🎯", font=('Segoe UI', 32),
                              bg=self.colors['primary'], fg='white')
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        # Título
        title_label = tk.Label(logo_frame, text="3D Print Manager",
                               font=('Segoe UI', 24, 'bold'),
                               bg=self.colors['primary'], fg='white')
        title_label.pack(side=tk.LEFT)

        # Subtítulo
        subtitle_label = tk.Label(logo_frame, text="Sistema de Gestión de Impresiones 3D",
                                  font=('Segoe UI', 10),
                                  bg=self.colors['primary'], fg='white')
        subtitle_label.place(x=60, y=35)

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
