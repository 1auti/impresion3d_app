"""
Widget moderno para una pieza individual con su color
"""
import tkinter as tk
from typing import Callable, Optional, Dict, Any

from .color_picker import ModernColorPicker
from ...style.color_palette import ColorPalette


class ModernPieceColorWidget(tk.Frame):
    """Widget moderno para configurar una pieza individual con color y peso"""

    def __init__(self, parent, pieza_nombre="", color_hex="#000000", peso=0.0,
                 on_delete: Optional[Callable] = None, colors=None, fonts=None):
        super().__init__(parent, bg=ColorPalette.BG)

        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8)
        }

        self.on_delete = on_delete

        # Variables
        self.nombre_var = tk.StringVar(value=pieza_nombre)
        self.peso_var = tk.DoubleVar(value=peso)

        # Referencias a widgets
        self.color_picker = None
        self.nombre_entry = None
        self.peso_spin = None

        self.create_widgets(color_hex)
        self._setup_placeholder_behavior()

    def create_widgets(self, color_hex: str):
        """Crear widgets de la pieza"""
        # Frame principal con diseño moderno
        self.main_frame = tk.Frame(self, bg=self.colors['card'],
                                   highlightbackground=self.colors['border'],
                                   highlightthickness=1)
        self.main_frame.pack(fill=tk.X, padx=5, pady=3)

        # Contenido interno
        content = tk.Frame(self.main_frame, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=15, pady=12)

        # Selector de color (compacto)
        self._create_color_section(content, color_hex)

        # Campo de nombre
        self._create_name_section(content)

        # Campo de peso
        self._create_weight_section(content)

        # Botón eliminar
        self._create_delete_button(content)

    def _create_color_section(self, parent, color_hex: str):
        """Crear sección de selector de color"""
        self.color_picker = ModernColorPicker(parent, initial_color=color_hex,
                                              compact=True, colors=self.colors,
                                              fonts=self.fonts)
        self.color_picker.pack(side=tk.LEFT, padx=(0, 15))

    def _create_name_section(self, parent):
        """Crear sección de nombre de pieza"""
        name_frame = tk.Frame(parent, bg=self.colors['card'])
        name_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        name_label = tk.Label(name_frame, text="Nombre de la pieza:",
                              font=self.fonts['small'],
                              bg=self.colors['card'], fg=self.colors['text_secondary'])
        name_label.pack(anchor=tk.W)

        # Entry con estilo moderno
        entry_frame = tk.Frame(name_frame, bg=self.colors['card'],
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        entry_frame.pack(fill=tk.X, pady=(3, 0))

        self.nombre_entry = tk.Entry(entry_frame, textvariable=self.nombre_var,
                                     font=self.fonts['body'], bd=0,
                                     bg=self.colors['card'], fg=self.colors['text'])
        self.nombre_entry.pack(fill=tk.X, padx=8, pady=4)

        # Eventos de focus para bordes
        self.nombre_entry.bind('<FocusIn>', lambda e: entry_frame.config(
            highlightbackground=self.colors['primary']))
        self.nombre_entry.bind('<FocusOut>', lambda e: entry_frame.config(
            highlightbackground=self.colors['border']))

    def _create_weight_section(self, parent):
        """Crear sección de peso"""
        peso_frame = tk.Frame(parent, bg=self.colors['card'])
        peso_frame.pack(side=tk.LEFT, padx=(0, 15))

        peso_label = tk.Label(peso_frame, text="Peso (g):",
                              font=self.fonts['small'],
                              bg=self.colors['card'], fg=self.colors['text_secondary'])
        peso_label.pack(anchor=tk.W)

        # Spinbox con estilo moderno
        peso_spinbox_frame = tk.Frame(peso_frame, bg=self.colors['card'],
                                      highlightbackground=self.colors['border'],
                                      highlightthickness=1)
        peso_spinbox_frame.pack(pady=(3, 0))

        self.peso_spin = tk.Spinbox(peso_spinbox_frame, textvariable=self.peso_var,
                                    from_=0, to=1000, increment=0.1,
                                    font=self.fonts['body'], bd=0, width=8,
                                    bg=self.colors['card'], fg=self.colors['text'],
                                    buttonbackground=self.colors['accent'],
                                    justify=tk.CENTER)
        self.peso_spin.pack(padx=4, pady=2)

        # Eventos de focus
        self.peso_spin.bind('<FocusIn>', lambda e: peso_spinbox_frame.config(
            highlightbackground=self.colors['primary']))
        self.peso_spin.bind('<FocusOut>', lambda e: peso_spinbox_frame.config(
            highlightbackground=self.colors['border']))

    def _create_delete_button(self, parent):
        """Crear botón de eliminar"""
        if self.on_delete:
            delete_btn = tk.Button(parent, text="🗑️", font=('Segoe UI', 12),
                                   bg=self.colors['danger'], fg='white',
                                   bd=0, width=3, height=1,
                                   cursor='hand2',
                                   command=lambda: self.on_delete(self))
            delete_btn.pack(side=tk.RIGHT)

            # Efectos hover
            delete_btn.bind('<Enter>', lambda e: delete_btn.config(bg='#DC2626'))
            delete_btn.bind('<Leave>', lambda e: delete_btn.config(bg=self.colors['danger']))

    def _setup_placeholder_behavior(self):
        """Configurar comportamiento de placeholder"""
        placeholder_text = "Ej: Base, Tapa, Soporte..."

        # Si no hay nombre inicial, mostrar placeholder
        if not self.nombre_var.get():
            self.nombre_entry.insert(0, placeholder_text)
            self.nombre_entry.config(fg=self.colors['text_secondary'])

        def on_focus_in(event):
            current_text = self.nombre_var.get()
            if current_text in [placeholder_text, ""]:
                self.nombre_entry.delete(0, tk.END)
                self.nombre_entry.config(fg=self.colors['text'])

        def on_focus_out(event):
            current_text = self.nombre_var.get().strip()
            if not current_text:
                self.nombre_var.set(placeholder_text)
                self.nombre_entry.config(fg=self.colors['text_secondary'])

        self.nombre_entry.bind('<FocusIn>', on_focus_in)
        self.nombre_entry.bind('<FocusOut>', on_focus_out)

    # API pública
    def get_data(self) -> Dict[str, Any]:
        """Obtener datos de la pieza"""
        nombre = self.nombre_var.get().strip()
        placeholder_text = "Ej: Base, Tapa, Soporte..."

        if nombre in [placeholder_text, ""]:
            nombre = ""

        return {
            'nombre': nombre,
            'color_hex': self.color_picker.get_color(),
            'peso': self.peso_var.get()
        }

    def set_data(self, data: Dict[str, Any]):
        """Establecer datos de la pieza"""
        if 'nombre' in data:
            self.nombre_var.set(data['nombre'])
        if 'color_hex' in data:
            self.color_picker.set_color(data['color_hex'])
        if 'peso' in data:
            self.peso_var.set(data['peso'])

    def is_valid(self) -> bool:
        """Verificar si la pieza tiene datos válidos"""
        data = self.get_data()
        return (data['nombre'] and
                data['nombre'] != "Ej: Base, Tapa, Soporte..." and
                data['peso'] > 0 and
                self.color_picker.is_valid_color())

    def get_validation_errors(self) -> list:
        """Obtener lista de errores de validación"""
        errors = []
        data = self.get_data()

        if not data['nombre'] or data['nombre'] == "Ej: Base, Tapa, Soporte...":
            errors.append("El nombre de la pieza es requerido")

        if data['peso'] <= 0:
            errors.append("El peso debe ser mayor a 0")

        if not self.color_picker.is_valid_color():
            errors.append("El color seleccionado no es válido")

        return errors

    def set_enabled(self, enabled: bool):
        """Habilitar/deshabilitar el widget"""
        state = 'normal' if enabled else 'disabled'

        self.nombre_entry.config(state=state)
        self.peso_spin.config(state=state)

        # El color picker no tiene estado disabled, pero podemos deshabilitar eventos
        if not enabled:
            self.color_picker.color_button.config(command=lambda: None)
        else:
            self.color_picker.color_button.config(command=self.color_picker._choose_color)

    def highlight_error(self, highlight: bool = True):
        """Resaltar el widget en caso de error"""
        color = self.colors['danger'] if highlight else self.colors['border']
        self.main_frame.config(highlightbackground=color)

    def get_summary(self) -> str:
        """Obtener resumen de la pieza"""
        data = self.get_data()
        if self.is_valid():
            return f"{data['nombre']}: {data['peso']}g ({data['color_hex']})"
        else:
            return "Pieza incompleta"

    def focus_first_field(self):
        """Enfocar el primer campo editable"""
        self.nombre_entry.focus()

    def clear(self):
        """Limpiar todos los campos"""
        self.nombre_var.set("")
        self.peso_var.set(0.0)
        self.color_picker.set_color("#000000")
        self._setup_placeholder_behavior()


class PieceColorFactory:
    """Factory para crear widgets de pieza con configuraciones predefinidas"""

    @staticmethod
    def create_standard_piece(parent, **kwargs):
        """Crear pieza estándar"""
        defaults = {
            'peso': 5.0,
            'color_hex': '#808080'  # Gris por defecto
        }
        defaults.update(kwargs)
        return ModernPieceColorWidget(parent, **defaults)

    @staticmethod
    def create_from_template(parent, template_name: str, **kwargs):
        """Crear pieza desde template predefinido"""
        templates = {
            'base': {'pieza_nombre': 'Base', 'peso': 15.0, 'color_hex': '#000000'},
            'tapa': {'pieza_nombre': 'Tapa', 'peso': 8.0, 'color_hex': '#FFFFFF'},
            'soporte': {'pieza_nombre': 'Soporte', 'peso': 3.0, 'color_hex': '#808080'},
            'botón': {'pieza_nombre': 'Botón', 'peso': 1.0, 'color_hex': '#FF0000'},
            'bisagra': {'pieza_nombre': 'Bisagra', 'peso': 2.5, 'color_hex': '#000000'}
        }

        template = templates.get(template_name, {})
        template.update(kwargs)
        return ModernPieceColorWidget(parent, **template)

    @staticmethod
    def create_batch(parent, pieces_data: list, on_delete=None):
        """Crear múltiples piezas desde lista de datos"""
        widgets = []
        for piece_data in pieces_data:
            piece_data['on_delete'] = on_delete
            widget = ModernPieceColorWidget(parent, **piece_data)
            widgets.append(widget)
        return widgets