"""
Widget selector de color hexadecimal moderno
"""
import tkinter as tk
from tkinter import colorchooser
import re
from typing import Callable, Optional

from ...style.color_palette import ColorPalette


class ModernColorPicker(tk.Frame):
    """Widget selector de color hexadecimal moderno y reutilizable"""

    def __init__(self, parent, initial_color="#000000", callback: Optional[Callable] = None,
                 compact=False, colors=None, fonts=None):
        super().__init__(parent, bg=ColorPalette.BG)

        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {'body': ('Segoe UI', 10)}

        self.color_var = tk.StringVar(value=initial_color)
        self.callback = callback
        self.compact = compact

        # Referencias a widgets
        self.color_button = None
        self.hex_entry = None

        self.create_widgets()
        self._update_color_display()

    def create_widgets(self):
        """Crear widgets del selector"""
        if self.compact:
            self._create_compact_widget()
        else:
            self._create_full_widget()

    def _create_compact_widget(self):
        """Crear versión compacta - solo botón de color"""
        self.color_button = tk.Button(
            self, text="", width=4, height=2,
            bg=self.color_var.get(),
            command=self._choose_color,
            relief=tk.FLAT, bd=0,
            cursor='hand2',
            highlightthickness=2,
            highlightbackground=self.colors['border'],
            highlightcolor=self.colors['primary']
        )
        self.color_button.pack(padx=5, pady=5)

        # Efectos hover
        self._setup_hover_effects()

    def _create_full_widget(self):
        """Crear versión completa - entry + botón"""
        container = tk.Frame(self, bg=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True)

        # Entry con estilo moderno
        self._create_hex_entry(container)

        # Botón de color
        self._create_color_button(container)

    def _create_hex_entry(self, parent):
        """Crear campo de entrada hexadecimal"""
        entry_frame = tk.Frame(parent, bg=self.colors['card'],
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        entry_frame.pack(side=tk.LEFT, padx=(0, 8))

        self.hex_entry = tk.Entry(entry_frame, textvariable=self.color_var,
                                  font=self.fonts['body'], bd=0,
                                  bg=self.colors['card'], fg=self.colors['text'],
                                  width=8, justify=tk.CENTER)
        self.hex_entry.pack(padx=8, pady=6)

        # Eventos de validación
        self.hex_entry.bind('<FocusOut>', self._validate_hex)
        self.hex_entry.bind('<Return>', self._validate_hex)

        # Eventos de focus
        self.hex_entry.bind('<FocusIn>', lambda e: entry_frame.config(
            highlightbackground=self.colors['primary']))
        self.hex_entry.bind('<FocusOut>', lambda e: entry_frame.config(
            highlightbackground=self.colors['border']))

    def _create_color_button(self, parent):
        """Crear botón de color"""
        self.color_button = tk.Button(
            parent, text="", width=4, height=2,
            bg=self.color_var.get(),
            command=self._choose_color,
            relief=tk.FLAT, bd=0,
            cursor='hand2',
            highlightthickness=2,
            highlightbackground=self.colors['border']
        )
        self.color_button.pack(side=tk.LEFT)

        self._setup_hover_effects()

    def _setup_hover_effects(self):
        """Configurar efectos hover"""

        def on_hover_enter(event):
            self.color_button.config(highlightbackground=self.colors['primary'])

        def on_hover_leave(event):
            self.color_button.config(highlightbackground=self.colors['border'])

        self.color_button.bind('<Enter>', on_hover_enter)
        self.color_button.bind('<Leave>', on_hover_leave)

    def _choose_color(self):
        """Abrir selector de color"""
        color = colorchooser.askcolor(
            initialcolor=self.color_var.get(),
            title="🎨 Seleccionar color"
        )

        if color[1]:
            self.set_color(color[1])
            if self.callback:
                self.callback(color[1])

    def _validate_hex(self, event=None):
        """Validar código hexadecimal"""
        if self.compact:
            return

        hex_color = self.color_var.get().strip()

        if not hex_color.startswith('#'):
            hex_color = '#' + hex_color

        if self._is_valid_hex(hex_color):
            self.color_var.set(hex_color.upper())
            self._update_color_display()
            if self.callback:
                self.callback(hex_color.upper())
        else:
            self.color_var.set("#000000")
            self._update_color_display()

    def _is_valid_hex(self, color: str) -> bool:
        """Verificar si es un color hex válido"""
        return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color))

    def _update_color_display(self):
        """Actualizar display del color"""
        try:
            color = self.color_var.get()
            self.color_button.configure(bg=color)

            # Determinar color del texto para contraste
            if not self.compact and len(color) == 7:
                r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                text_color = 'white' if luminance < 0.5 else 'black'
                self.color_button.configure(fg=text_color)

        except Exception:
            self.color_button.configure(bg="#000000")

    # API pública
    def get_color(self) -> str:
        """Obtener el color seleccionado"""
        return self.color_var.get()

    def set_color(self, color: str):
        """Establecer un color"""
        if self._is_valid_hex(color):
            self.color_var.set(color.upper())
            self._update_color_display()

    def set_callback(self, callback: Callable):
        """Establecer callback para cambios de color"""
        self.callback = callback

    def is_valid_color(self) -> bool:
        """Verificar si el color actual es válido"""
        return self._is_valid_hex(self.color_var.get())


class ColorNameHelper:
    """Helper para obtener nombres descriptivos de colores"""

    COLOR_NAMES = {
        '#000000': 'Negro',
        '#FFFFFF': 'Blanco',
        '#FF0000': 'Rojo',
        '#00FF00': 'Verde',
        '#0000FF': 'Azul',
        '#FFFF00': 'Amarillo',
        '#FF00FF': 'Magenta',
        '#00FFFF': 'Cyan',
        '#FFA500': 'Naranja',
        '#800080': 'Morado',
        '#FFC0CB': 'Rosa',
        '#808080': 'Gris',
        '#A52A2A': 'Marrón',
        '#008000': 'Verde Oscuro',
        '#000080': 'Azul Marino',
        '#800000': 'Rojo Oscuro',
        '#808000': 'Oliva',
        '#C0C0C0': 'Plata'
    }

    @classmethod
    def get_color_name(cls, hex_color: str) -> str:
        """Obtener nombre descriptivo del color"""
        return cls.COLOR_NAMES.get(hex_color.upper(), hex_color)

    @classmethod
    def get_closest_color_name(cls, hex_color: str) -> str:
        """Obtener nombre del color más cercano"""
        if hex_color.upper() in cls.COLOR_NAMES:
            return cls.COLOR_NAMES[hex_color.upper()]

        # Lógica básica para encontrar color más cercano
        # Se puede expandir con algoritmos más sofisticados
        try:
            r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)

            # Determinar color base
            if r > 200 and g > 200 and b > 200:
                return "Blanco"
            elif r < 50 and g < 50 and b < 50:
                return "Negro"
            elif r > g and r > b:
                return "Rojo"
            elif g > r and g > b:
                return "Verde"
            elif b > r and b > g:
                return "Azul"
            else:
                return hex_color

        except Exception:
            return hex_color