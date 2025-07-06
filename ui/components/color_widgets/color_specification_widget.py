"""
Widget modernizado para especificar colores por pieza
"""
import tkinter as tk
from tkinter import scrolledtext
from typing import List, Optional, Callable, Dict, Any

from ..color_widgets.color_widget import ModernPieceColorWidget, PieceColorFactory
from .color_picker import ModernColorPicker, ColorNameHelper
from ...style.color_palette import ColorPalette
from ...components.dialogs import NotificationSystem
from models.producto import ColorEspecificacion


class ModernColorSpecificationWidget(tk.Frame):
    """Widget modernizado para especificar colores y piezas de un producto"""

    def __init__(self, parent, color_spec: Optional[ColorEspecificacion] = None,
                 on_delete: Optional[Callable] = None, index=0, colors=None, fonts=None):
        super().__init__(parent, bg=ColorPalette.BG)

        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {
            'title': ('Segoe UI', 14, 'bold'),
            'heading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8)
        }

        self.on_delete = on_delete
        self.index = index
        self.piece_widgets: List[ModernPieceColorWidget] = []

        # Referencias a widgets principales
        self.canvas = None
        self.scrollable_frame = None
        self.pieces_frame = None
        self.header_summary = None
        self.resumen_label = None

        # Sistema de notificaciones
        self.notifications = NotificationSystem(parent)

        self.create_modern_widgets()

        # Cargar datos si existen
        if color_spec and hasattr(color_spec, 'piezas') and color_spec.piezas:
            self.cargar_desde_especificacion(color_spec)
        else:
            self.agregar_pieza()

        self.actualizar_resumen()

    def create_modern_widgets(self):
        """Crear widgets modernos"""
        # Frame principal con diseño moderno
        main_card = tk.Frame(self, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        main_card.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        # Header moderno
        self._create_header(main_card)

        # Instrucciones
        self._create_instructions(main_card)

        # Área de piezas con scroll
        self._create_pieces_area(main_card)

        # Botones de acción
        self._create_action_buttons(main_card)

        # Resumen detallado
        self._create_summary_section(main_card)

    def _create_header(self, parent):
        """Crear header moderno"""
        header = tk.Frame(parent, bg=self.colors['primary'], height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=12)

        # Título con ícono
        title_frame = tk.Frame(header_content, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT)

        tk.Label(title_frame, text="🎨", font=('Segoe UI', 16),
                 bg=self.colors['primary'], fg='white').pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(title_frame, text=f"Especificación de Color #{self.index + 1}",
                 font=self.fonts['heading'],
                 bg=self.colors['primary'], fg='white').pack(side=tk.LEFT)

        # Resumen en el header
        self.header_summary = tk.Label(header_content, text="0 piezas, 0.0g",
                                       font=self.fonts['body'],
                                       bg=self.colors['primary'], fg='white')
        self.header_summary.pack(side=tk.RIGHT)

    def _create_instructions(self, parent):
        """Crear sección de instrucciones"""
        inst_frame = tk.Frame(parent, bg=self.colors['accent'])
        inst_frame.pack(fill=tk.X)

        inst_content = tk.Frame(inst_frame, bg=self.colors['accent'])
        inst_content.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(inst_content, text="💡 Tip:",
                 font=(self.fonts['small'][0], self.fonts['small'][1], 'bold'),
                 bg=self.colors['accent'], fg=self.colors['primary']).pack(side=tk.LEFT, padx=(0, 8))

        tk.Label(inst_content,
                 text="Agrega cada pieza del producto especificando su color y peso individual",
                 font=self.fonts['small'],
                 bg=self.colors['accent'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)

    def _create_pieces_area(self, parent):
        """Crear área de piezas con scroll"""
        pieces_container = tk.Frame(parent, bg=self.colors['card'])
        pieces_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(15, 0))

        # Canvas con scroll
        self.canvas = tk.Canvas(pieces_container, height=200, bg=self.colors['card'],
                                highlightthickness=0, bd=0)

        # Scrollbar moderno
        scrollbar_frame = tk.Frame(pieces_container, bg=self.colors['border'], width=8)
        scrollbar = tk.Scrollbar(scrollbar_frame, orient="vertical", command=self.canvas.yview,
                                 bg=self.colors['accent'], troughcolor=self.colors['border'],
                                 bd=0, highlightthickness=0)
        scrollbar.pack(fill=tk.Y, expand=True)

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['card'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar_frame.pack(side="right", fill="y")

        # Frame para las piezas
        self.pieces_frame = tk.Frame(self.scrollable_frame, bg=self.colors['card'])
        self.pieces_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_action_buttons(self, parent):
        """Crear botones de acción"""
        actions_frame = tk.Frame(parent, bg=self.colors['card'])
        actions_frame.pack(fill=tk.X, padx=20, pady=15)

        # Botón agregar pieza simple
        add_piece_btn = self._create_action_button(
            actions_frame, "➕ Agregar Pieza", self.agregar_pieza,
            self.colors['primary'], '#5558E3'
        )
        add_piece_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Botón agregar múltiples
        add_multiple_btn = self._create_action_button(
            actions_frame, "🎨 Múltiples Piezas", self.agregar_multiples_piezas,
            self.colors['secondary'], '#BE185D'
        )
        add_multiple_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Botón de templates
        template_btn = self._create_action_button(
            actions_frame, "📋 Templates", self.mostrar_templates,
            self.colors['success'], '#059669'
        )
        template_btn.pack(side=tk.LEFT)

    def _create_action_button(self, parent, text, command, bg_color, hover_color):
        """Crear botón de acción con efectos hover"""
        btn = tk.Button(parent, text=text, font=self.fonts['body'],
                        bg=bg_color, fg='white', bd=0,
                        padx=15, pady=8, cursor='hand2', command=command)

        # Efectos hover
        btn.bind('<Enter>', lambda e: btn.config(bg=hover_color))
        btn.bind('<Leave>', lambda e: btn.config(bg=bg_color))

        return btn

    def _create_summary_section(self, parent):
        """Crear sección de resumen"""
        self.resumen_frame = tk.Frame(parent, bg=self.colors['accent'])
        self.resumen_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        resumen_content = tk.Frame(self.resumen_frame, bg=self.colors['accent'])
        resumen_content.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(resumen_content, text="📊 Resumen:",
                 font=(self.fonts['body'][0], self.fonts['body'][1], 'bold'),
                 bg=self.colors['accent'], fg=self.colors['text']).pack(side=tk.LEFT)

        self.resumen_label = tk.Label(resumen_content, text="Total: 0 piezas, 0.0g",
                                      font=self.fonts['body'],
                                      bg=self.colors['accent'], fg=self.colors['text'])
        self.resumen_label.pack(side=tk.LEFT, padx=(10, 0))

    # Métodos de gestión de piezas
    def cargar_desde_especificacion(self, color_spec: ColorEspecificacion):
        """Cargar piezas desde una especificación existente"""
        if not hasattr(color_spec, 'piezas') or not color_spec.piezas:
            return

        peso_por_pieza = color_spec.peso_color / len(color_spec.piezas) if color_spec.piezas else 0

        for pieza in color_spec.piezas:
            self.agregar_pieza(
                nombre=pieza,
                color=color_spec.color_hex,
                peso=round(peso_por_pieza, 2)
            )

    def agregar_pieza(self, nombre="", color="#000000", peso=0.0):
        """Agregar una nueva pieza"""
        widget = ModernPieceColorWidget(
            self.pieces_frame,
            pieza_nombre=nombre,
            color_hex=color,
            peso=peso,
            on_delete=self.eliminar_pieza,
            colors=self.colors,
            fonts=self.fonts
        )
        widget.pack(fill=tk.X, pady=5)
        self.piece_widgets.append(widget)
        self.actualizar_resumen()

        # Auto-scroll al final
        self._auto_scroll_to_bottom()

    def eliminar_pieza(self, widget: ModernPieceColorWidget):
        """Eliminar una pieza"""
        if len(self.piece_widgets) > 1:
            widget.destroy()
            self.piece_widgets.remove(widget)
            self.actualizar_resumen()
        else:
            self.notifications.show_notification(
                "Debe mantener al menos una pieza", 'warning'
            )

    def agregar_multiples_piezas(self):
        """Mostrar diálogo para agregar múltiples piezas"""
        dialog = MultiplePiecesDialog(self, self.colors, self.fonts)
        result = dialog.show()

        if result:
            color = result['color']
            peso = result['peso']
            piezas = result['piezas']

            count = 0
            for pieza in piezas:
                if pieza.strip():
                    self.agregar_pieza(pieza.strip(), color, peso)
                    count += 1

            if count > 0:
                self.notifications.show_notification(
                    f"Se agregaron {count} piezas exitosamente", 'success'
                )

    def mostrar_templates(self):
        """Mostrar diálogo de templates predefinidos"""
        dialog = TemplatesDialog(self, self.colors, self.fonts)
        result = dialog.show()

        if result:
            templates = result['templates']
            for template_name in templates:
                widget = PieceColorFactory.create_from_template(
                    self.pieces_frame, template_name, on_delete=self.eliminar_pieza
                )
                widget.pack(fill=tk.X, pady=5)
                self.piece_widgets.append(widget)

            self.actualizar_resumen()
            self.notifications.show_notification(
                f"Se agregaron {len(templates)} templates", 'success'
            )

    def actualizar_resumen(self):
        """Actualizar el resumen de piezas y peso"""
        total_piezas = len(self.piece_widgets)
        total_peso = sum(w.peso_var.get() for w in self.piece_widgets if hasattr(w, 'peso_var'))

        # Actualizar resumen en el header
        self.header_summary.config(text=f"{total_piezas} piezas, {total_peso:.1f}g")

        # Actualizar resumen detallado
        self.resumen_label.config(text=f"Total: {total_piezas} piezas, {total_peso:.1f}g")

    def _auto_scroll_to_bottom(self):
        """Auto-scroll al final del área de piezas"""
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    # API pública
    def get_specification(self) -> ColorEspecificacion:
        """Obtener la especificación de color principal"""
        specifications = self.get_all_specifications()
        return specifications[0] if specifications else ColorEspecificacion()

    def get_all_specifications(self) -> List[ColorEspecificacion]:
        """Obtener todas las especificaciones de color (una por cada color único)"""
        # Agrupar piezas por color
        color_groups = {}

        for widget in self.piece_widgets:
            if widget.is_valid():
                data = widget.get_data()
                color = data['color_hex']

                if color not in color_groups:
                    color_groups[color] = {
                        'piezas': [],
                        'peso_total': 0.0
                    }
                color_groups[color]['piezas'].append(data['nombre'])
                color_groups[color]['peso_total'] += data['peso']

        # Crear una especificación por cada color
        specifications = []
        for i, (color_hex, group) in enumerate(color_groups.items()):
            spec = ColorEspecificacion(
                color_hex=color_hex,
                nombre_color=ColorNameHelper.get_color_name(color_hex),
                peso_color=group['peso_total'],
                tiempo_adicional=5 if i > 0 else 0,
                piezas=group['piezas'],
                notas=""
            )
            specifications.append(spec)

        return specifications

    def is_valid(self) -> bool:
        """Verificar si la especificación es válida"""
        return len(self.piece_widgets) > 0 and any(w.is_valid() for w in self.piece_widgets)

    def get_validation_errors(self) -> List[str]:
        """Obtener errores de validación"""
        errors = []

        if not self.piece_widgets:
            errors.append("Debe agregar al menos una pieza")
            return errors

        valid_pieces = [w for w in self.piece_widgets if w.is_valid()]
        if not valid_pieces:
            errors.append("Debe tener al menos una pieza válida")

        for i, widget in enumerate(self.piece_widgets):
            if not widget.is_valid():
                piece_errors = widget.get_validation_errors()
                for error in piece_errors:
                    errors.append(f"Pieza {i + 1}: {error}")

        return errors

    def clear_all_pieces(self):
        """Limpiar todas las piezas"""
        for widget in self.piece_widgets:
            widget.destroy()
        self.piece_widgets.clear()
        self.agregar_pieza()  # Agregar una pieza vacía
        self.actualizar_resumen()

    def get_summary_text(self) -> str:
        """Obtener texto de resumen para mostrar"""
        valid_pieces = [w for w in self.piece_widgets if w.is_valid()]
        if not valid_pieces:
            return "Sin piezas válidas"

        total_peso = sum(w.peso_var.get() for w in valid_pieces)
        colors_used = len(set(w.get_data()['color_hex'] for w in valid_pieces))

        return f"{len(valid_pieces)} piezas, {total_peso:.1f}g, {colors_used} colores"


class MultiplePiecesDialog:
    """Diálogo para agregar múltiples piezas del mismo color"""

    def __init__(self, parent, colors, fonts):
        self.parent = parent
        self.colors = colors
        self.fonts = fonts
        self.result = None

    def show(self):
        """Mostrar diálogo y retornar resultado"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Agregar Múltiples Piezas")
        dialog.geometry("500x400")
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg'])

        self._create_dialog_content(dialog)
        self._center_dialog(dialog)

        dialog.wait_window()
        return self.result

    def _create_dialog_content(self, dialog):
        """Crear contenido del diálogo"""
        # Header
        header = tk.Frame(dialog, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        tk.Label(header_content, text="🎨 Agregar Múltiples Piezas",
                 font=self.fonts['title'],
                 bg=self.colors['primary'], fg='white').pack(side=tk.LEFT)

        # Contenido principal
        main_content = tk.Frame(dialog, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Selector de color
        color_picker = self._create_color_section(main_content)

        # Lista de piezas
        piezas_text = self._create_pieces_section(main_content)

        # Peso por pieza
        peso_var = self._create_weight_section(main_content)

        # Botones
        self._create_buttons_section(main_content, dialog, color_picker, piezas_text, peso_var)

    def _create_color_section(self, parent):
        """Crear sección de selector de color"""
        color_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        color_card.pack(fill=tk.X, pady=(0, 20))

        color_content = tk.Frame(color_card, bg=self.colors['card'])
        color_content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(color_content, text="Color para todas las piezas:",
                 font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        color_picker = ModernColorPicker(color_content, initial_color="#000000")
        color_picker.pack(anchor=tk.W)

        return color_picker

    def _create_pieces_section(self, parent):
        """Crear sección de lista de piezas"""
        pieces_card = tk.Frame(parent, bg=self.colors['card'],
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        pieces_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        pieces_content = tk.Frame(pieces_card, bg=self.colors['card'])
        pieces_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(pieces_content, text="Lista de piezas (una por línea):",
                 font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        # Text area con scroll
        text_frame = tk.Frame(pieces_content, bg=self.colors['card'])
        text_frame.pack(fill=tk.BOTH, expand=True)

        piezas_text = tk.Text(text_frame, height=8, width=40,
                              font=self.fonts['body'], bd=0,
                              bg=self.colors['card'], fg=self.colors['text'],
                              highlightthickness=1,
                              highlightbackground=self.colors['border'],
                              selectbackground=self.colors['primary'],
                              selectforeground='white')
        piezas_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=piezas_text.yview,
                                 bg=self.colors['accent'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        piezas_text.config(yscrollcommand=scrollbar.set)

        # Placeholder
        placeholder = """Base principal
Tapa superior
Botón frontal
Botón lateral
Soporte trasero"""
        piezas_text.insert('1.0', placeholder)

        return piezas_text

    def _create_weight_section(self, parent):
        """Crear sección de peso"""
        peso_card = tk.Frame(parent, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        peso_card.pack(fill=tk.X, pady=(0, 20))

        peso_content = tk.Frame(peso_card, bg=self.colors['card'])
        peso_content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(peso_content, text="Peso por pieza (gramos):",
                 font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        peso_var = tk.DoubleVar(value=5.0)
        peso_frame = tk.Frame(peso_content, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        peso_frame.pack(anchor=tk.W)

        peso_spin = tk.Spinbox(peso_frame, textvariable=peso_var,
                               from_=0, to=100, increment=0.5,
                               font=self.fonts['body'], bd=0, width=10,
                               bg=self.colors['card'], fg=self.colors['text'],
                               justify=tk.CENTER)
        peso_spin.pack(padx=8, pady=6)

        return peso_var

    def _create_buttons_section(self, parent, dialog, color_picker, piezas_text, peso_var):
        """Crear sección de botones"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X)

        def agregar():
            color = color_picker.get_color()
            peso = peso_var.get()
            piezas_txt = piezas_text.get('1.0', 'end-1c').strip()
            piezas = [p.strip() for p in piezas_txt.split('\n') if p.strip()]

            self.result = {
                'color': color,
                'peso': peso,
                'piezas': piezas
            }
            dialog.destroy()

        btn_cancel = tk.Button(btn_frame, text="Cancelar",
                               font=self.fonts['body'], bg=self.colors['card'],
                               fg=self.colors['text'], bd=1, padx=20, pady=8,
                               cursor='hand2', command=dialog.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=(10, 0))

        btn_add = tk.Button(btn_frame, text="✅ Agregar Piezas",
                            font=self.fonts['body'], bg=self.colors['success'],
                            fg='white', bd=0, padx=20, pady=8,
                            cursor='hand2', command=agregar)
        btn_add.pack(side=tk.RIGHT)

    def _center_dialog(self, dialog):
        """Centrar diálogo"""
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')


class TemplatesDialog:
    """Diálogo para seleccionar templates predefinidos"""

    def __init__(self, parent, colors, fonts):
        self.parent = parent
        self.colors = colors
        self.fonts = fonts
        self.result = None
        self.template_vars = {}

    def show(self):
        """Mostrar diálogo y retornar resultado"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Templates de Piezas")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.configure(bg=self.colors['bg'])

        self._create_dialog_content(dialog)
        self._center_dialog(dialog)

        dialog.wait_window()
        return self.result

    def _create_dialog_content(self, dialog):
        """Crear contenido del diálogo"""
        # Header
        header = tk.Frame(dialog, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        tk.Label(header_content, text="📋 Templates de Piezas",
                 font=self.fonts['title'],
                 bg=self.colors['primary'], fg='white').pack(side=tk.LEFT)

        # Lista de templates
        main_content = tk.Frame(dialog, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        templates = ['base', 'tapa', 'soporte', 'botón', 'bisagra']

        for template in templates:
            var = tk.BooleanVar()
            self.template_vars[template] = var

            cb = tk.Checkbutton(main_content, text=template.title(),
                                variable=var, font=self.fonts['body'],
                                bg=self.colors['bg'], fg=self.colors['text'])
            cb.pack(anchor=tk.W, pady=5)

        # Botones
        btn_frame = tk.Frame(main_content, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        def agregar():
            selected = [name for name, var in self.template_vars.items() if var.get()]
            self.result = {'templates': selected}
            dialog.destroy()

        btn_cancel = tk.Button(btn_frame, text="Cancelar",
                               font=self.fonts['body'], bg=self.colors['card'],
                               fg=self.colors['text'], bd=1, padx=20, pady=8,
                               cursor='hand2', command=dialog.destroy)
        btn_cancel.pack(side=tk.RIGHT, padx=(10, 0))

        btn_add = tk.Button(btn_frame, text="✅ Agregar Seleccionados",
                            font=self.fonts['body'], bg=self.colors['success'],
                            fg='white', bd=0, padx=20, pady=8,
                            cursor='hand2', command=agregar)
        btn_add.pack(side=tk.RIGHT)

    def _center_dialog(self, dialog):
        """Centrar diálogo"""
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')