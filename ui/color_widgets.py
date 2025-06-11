"""
Widgets personalizados para manejo de colores centrados en piezas
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from typing import List, Callable, Optional, Dict
import re

from models.producto import ColorEspecificacion


class ColorPicker(ttk.Frame):
    """Widget selector de color hexadecimal compacto"""

    def __init__(self, parent, initial_color="#000000", callback=None, compact=False):
        super().__init__(parent)

        self.color_var = tk.StringVar(value=initial_color)
        self.callback = callback
        self.compact = compact

        if compact:
            # Versión compacta: solo botón de color
            self.color_button = tk.Button(
                self, text="", width=3, height=1,
                bg=initial_color, command=self._choose_color,
                relief=tk.RAISED, bd=2
            )
            self.color_button.pack()
        else:
            # Versión completa: entry + botón
            self.hex_entry = ttk.Entry(self, textvariable=self.color_var, width=10)
            self.hex_entry.pack(side=tk.LEFT, padx=(0, 5))
            self.hex_entry.bind('<FocusOut>', self._validate_hex)
            self.hex_entry.bind('<Return>', self._validate_hex)

            self.color_button = tk.Button(
                self, text="   ", width=3, height=1,
                bg=initial_color, command=self._choose_color
            )
            self.color_button.pack(side=tk.LEFT)

        # Actualizar color inicial
        self._update_color_display()

    def _choose_color(self):
        """Abrir selector de color"""
        color = colorchooser.askcolor(
            initialcolor=self.color_var.get(),
            title="Seleccionar color"
        )

        if color[1]:  # color[1] es el valor hexadecimal
            self.color_var.set(color[1])
            self._update_color_display()
            if self.callback:
                self.callback(color[1])

    def _validate_hex(self, event=None):
        """Validar código hexadecimal"""
        if self.compact:
            return

        hex_color = self.color_var.get().strip()

        # Agregar # si no lo tiene
        if not hex_color.startswith('#'):
            hex_color = '#' + hex_color

        # Validar formato
        if re.match(r'^#[0-9A-Fa-f]{6}$', hex_color):
            self.color_var.set(hex_color.upper())
            self._update_color_display()
            if self.callback:
                self.callback(hex_color.upper())
        else:
            self.color_var.set("#000000")
            self._update_color_display()

    def _update_color_display(self):
        """Actualizar el botón con el color seleccionado"""
        try:
            self.color_button.configure(bg=self.color_var.get())
        except:
            self.color_button.configure(bg="#000000")

    def get_color(self):
        """Obtener el color seleccionado"""
        return self.color_var.get()

    def set_color(self, color):
        """Establecer un color"""
        self.color_var.set(color)
        self._update_color_display()


class PieceColorWidget(ttk.Frame):
    """Widget para una pieza individual con su color"""

    def __init__(self, parent, pieza_nombre="", color_hex="#000000", peso=0.0, on_delete=None):
        super().__init__(parent)

        self.on_delete = on_delete

        # Frame principal con borde
        self.main_frame = ttk.Frame(self, relief=tk.RIDGE, borderwidth=1)
        self.main_frame.pack(fill=tk.X, padx=2, pady=2)

        # Selector de color (compacto)
        self.color_picker = ColorPicker(self.main_frame, initial_color=color_hex, compact=True)
        self.color_picker.pack(side=tk.LEFT, padx=5, pady=5)

        # Nombre de la pieza
        self.nombre_var = tk.StringVar(value=pieza_nombre)
        self.nombre_entry = ttk.Entry(self.main_frame, textvariable=self.nombre_var, width=25)
        self.nombre_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.nombre_entry.insert(0, "Nombre de la pieza...")
        self.nombre_entry.bind('<FocusIn>', self._on_focus_in)
        self.nombre_entry.bind('<FocusOut>', self._on_focus_out)

        # Peso
        ttk.Label(self.main_frame, text="Peso:").pack(side=tk.LEFT, padx=(10, 2))
        self.peso_var = tk.DoubleVar(value=peso)
        self.peso_spin = ttk.Spinbox(self.main_frame, textvariable=self.peso_var,
                                    from_=0, to=1000, increment=0.1, width=8)
        self.peso_spin.pack(side=tk.LEFT, padx=(0, 2))
        ttk.Label(self.main_frame, text="g").pack(side=tk.LEFT)

        # Botón eliminar
        if on_delete:
            ttk.Button(self.main_frame, text="✕", width=3,
                      command=lambda: on_delete(self)).pack(side=tk.RIGHT, padx=5)

    def _on_focus_in(self, event):
        """Limpiar placeholder al enfocar"""
        if self.nombre_var.get() == "Nombre de la pieza...":
            self.nombre_entry.delete(0, tk.END)

    def _on_focus_out(self, event):
        """Restaurar placeholder si está vacío"""
        if not self.nombre_var.get().strip():
            self.nombre_var.set("Nombre de la pieza...")

    def get_data(self):
        """Obtener datos de la pieza"""
        nombre = self.nombre_var.get().strip()
        if nombre == "Nombre de la pieza...":
            nombre = ""

        return {
            'nombre': nombre,
            'color_hex': self.color_picker.get_color(),
            'peso': self.peso_var.get()
        }

    def is_valid(self):
        """Verificar si la pieza tiene datos válidos"""
        nombre = self.nombre_var.get().strip()
        return nombre and nombre != "Nombre de la pieza..." and self.peso_var.get() > 0


class ColorSpecificationWidget(ttk.LabelFrame):
    """Widget simplificado para especificar colores por pieza"""

    def __init__(self, parent, color_spec: Optional[ColorEspecificacion] = None,
                 on_delete=None, index=0):
        super().__init__(parent, text="Especificaciones de Color por Pieza", padding="10")

        self.on_delete = on_delete
        self.index = index
        self.piece_widgets = []

        # Frame de instrucciones
        inst_frame = ttk.Frame(self)
        inst_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(inst_frame, text="💡 Agrega cada pieza con su color y peso:",
                 font=('Arial', 10, 'italic')).pack(side=tk.LEFT)

        # Frame con scroll para las piezas
        self.canvas = tk.Canvas(self, height=200)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Frame para las piezas
        self.pieces_frame = ttk.Frame(self.scrollable_frame)
        self.pieces_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Botones de acción
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="➕ Agregar Pieza",
                  command=self.agregar_pieza).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="🎨 Agregar múltiples piezas del mismo color",
                  command=self.agregar_multiples_piezas).pack(side=tk.LEFT, padx=5)

        # Resumen
        self.resumen_label = ttk.Label(button_frame, text="Total: 0 piezas, 0g",
                                      font=('Arial', 10, 'bold'))
        self.resumen_label.pack(side=tk.RIGHT, padx=5)

        # Cargar datos si existen
        if color_spec and color_spec.piezas:
            self.cargar_desde_especificacion(color_spec)
        else:
            # Agregar una pieza por defecto
            self.agregar_pieza()

        # Actualizar resumen
        self.actualizar_resumen()

    def cargar_desde_especificacion(self, color_spec: ColorEspecificacion):
        """Cargar piezas desde una especificación existente"""
        # Si hay múltiples piezas con el mismo color, crear una entrada para cada una
        peso_por_pieza = color_spec.peso_color / len(color_spec.piezas) if color_spec.piezas else 0

        for pieza in color_spec.piezas:
            widget = PieceColorWidget(
                self.pieces_frame,
                pieza_nombre=pieza,
                color_hex=color_spec.color_hex,
                peso=round(peso_por_pieza, 2),
                on_delete=self.eliminar_pieza
            )
            widget.pack(fill=tk.X, pady=2)
            self.piece_widgets.append(widget)

    def agregar_pieza(self, nombre="", color="#000000", peso=0.0):
        """Agregar una nueva pieza"""
        widget = PieceColorWidget(
            self.pieces_frame,
            pieza_nombre=nombre,
            color_hex=color,
            peso=peso,
            on_delete=self.eliminar_pieza
        )
        widget.pack(fill=tk.X, pady=2)
        self.piece_widgets.append(widget)
        self.actualizar_resumen()

        # Auto-scroll al final
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def agregar_multiples_piezas(self):
        """Diálogo para agregar múltiples piezas del mismo color"""
        dialog = tk.Toplevel(self)
        dialog.title("Agregar múltiples piezas")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Color
        color_frame = ttk.Frame(main_frame)
        color_frame.pack(fill=tk.X, pady=5)
        ttk.Label(color_frame, text="Color para todas las piezas:").pack(side=tk.LEFT, padx=(0, 10))
        color_picker = ColorPicker(color_frame, initial_color="#000000")
        color_picker.pack(side=tk.LEFT)

        # Lista de piezas
        ttk.Label(main_frame, text="Piezas (una por línea):").pack(anchor=tk.W, pady=(10, 5))

        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        piezas_text = tk.Text(text_frame, height=8, width=40)
        piezas_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame, command=piezas_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        piezas_text.config(yscrollcommand=scrollbar.set)

        # Peso por pieza
        peso_frame = ttk.Frame(main_frame)
        peso_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(peso_frame, text="Peso por pieza (g):").pack(side=tk.LEFT, padx=(0, 10))
        peso_var = tk.DoubleVar(value=5.0)
        peso_spin = ttk.Spinbox(peso_frame, textvariable=peso_var,
                               from_=0, to=100, increment=0.5, width=10)
        peso_spin.pack(side=tk.LEFT)

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        def agregar():
            color = color_picker.get_color()
            peso = peso_var.get()
            piezas = piezas_text.get('1.0', 'end-1c').strip().split('\n')

            for pieza in piezas:
                pieza = pieza.strip()
                if pieza:
                    self.agregar_pieza(pieza, color, peso)

            dialog.destroy()

        ttk.Button(btn_frame, text="Agregar", command=agregar).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.RIGHT)

        # Placeholder de ejemplo
        piezas_text.insert('1.0', "Ejemplo:\nBase\nTapa\nBotón frontal\nBotón trasero")

        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

    def eliminar_pieza(self, widget):
        """Eliminar una pieza"""
        if len(self.piece_widgets) > 1:
            widget.destroy()
            self.piece_widgets.remove(widget)
            self.actualizar_resumen()
        else:
            messagebox.showwarning("Advertencia", "Debe mantener al menos una pieza")

    def actualizar_resumen(self):
        """Actualizar el resumen de piezas y peso"""
        total_piezas = len(self.piece_widgets)
        total_peso = sum(w.peso_var.get() for w in self.piece_widgets if hasattr(w, 'peso_var'))
        self.resumen_label.config(text=f"Total: {total_piezas} piezas, {total_peso:.1f}g")

    def get_specification(self) -> ColorEspecificacion:
        """Obtener la especificación de color consolidada"""
        # Agrupar piezas por color
        color_groups = {}

        for widget in self.piece_widgets:
            data = widget.get_data()
            if widget.is_valid():
                color = data['color_hex']
                if color not in color_groups:
                    color_groups[color] = {
                        'piezas': [],
                        'peso_total': 0.0,
                        'nombre_color': ""
                    }
                color_groups[color]['piezas'].append(data['nombre'])
                color_groups[color]['peso_total'] += data['peso']

        # Si no hay grupos válidos, devolver especificación vacía
        if not color_groups:
            return ColorEspecificacion()

        # Por ahora, devolver la primera especificación (la más usada)
        # En el futuro, podrías devolver múltiples especificaciones
        color_hex = max(color_groups.keys(), key=lambda k: len(color_groups[k]['piezas']))
        group = color_groups[color_hex]

        return ColorEspecificacion(
            color_hex=color_hex,
            nombre_color=self._get_color_name(color_hex),
            peso_color=group['peso_total'],
            tiempo_adicional=5 if len(color_groups) > 1 else 0,  # Tiempo si hay cambio de color
            piezas=group['piezas'],
            notas=f"Total de colores diferentes: {len(color_groups)}"
        )

    def get_all_specifications(self) -> List[ColorEspecificacion]:
        """Obtener todas las especificaciones de color (una por cada color único)"""
        # Agrupar piezas por color
        color_groups = {}

        for widget in self.piece_widgets:
            data = widget.get_data()
            if widget.is_valid():
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
                nombre_color=self._get_color_name(color_hex),
                peso_color=group['peso_total'],
                tiempo_adicional=5 if i > 0 else 0,  # Tiempo de cambio después del primer color
                piezas=group['piezas'],
                notas=""
            )
            specifications.append(spec)

        return specifications

    def _get_color_name(self, hex_color):
        """Obtener nombre descriptivo del color"""
        # Mapa básico de colores comunes
        color_names = {
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
            '#A52A2A': 'Marrón'
        }

        return color_names.get(hex_color.upper(), hex_color)


class ColorFilterWidget(ttk.Frame):
    """Widget para filtrar por colores"""

    def __init__(self, parent, colors: List[Dict], on_filter_change=None):
        super().__init__(parent)

        self.colors = colors
        self.on_filter_change = on_filter_change
        self.selected_colors = set()

        self._create_widgets()

    def _create_widgets(self):
        """Crear los widgets del filtro"""
        ttk.Label(self, text="Filtrar por color:").pack(anchor=tk.W)

        # Frame con scroll para los colores
        canvas = tk.Canvas(self, height=100)
        canvas.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        scrollbar.pack(fill=tk.X)

        canvas.configure(xscrollcommand=scrollbar.set)

        # Frame interior para los botones de color
        inner_frame = ttk.Frame(canvas)
        canvas_window = canvas.create_window(0, 0, anchor="nw", window=inner_frame)

        # Crear botones de color
        for i, color_info in enumerate(self.colors):
            color_hex = color_info['color_hex']
            nombre = color_info['nombre_color']
            cantidad = color_info['cantidad']

            # Frame para cada color
            color_frame = ttk.Frame(inner_frame)
            color_frame.pack(side=tk.LEFT, padx=5, pady=5)

            # Checkbox
            var = tk.BooleanVar()
            check = ttk.Checkbutton(
                color_frame,
                variable=var,
                command=lambda c=color_hex, v=var: self._toggle_color(c, v)
            )
            check.pack()

            # Muestra de color
            color_label = tk.Label(
                color_frame,
                text="   ",
                bg=color_hex,
                width=4,
                height=2,
                relief=tk.RAISED
            )
            color_label.pack()

            # Nombre y cantidad
            ttk.Label(color_frame, text=nombre, font=('Arial', 8)).pack()
            ttk.Label(color_frame, text=f"({cantidad})", font=('Arial', 8)).pack()

        # Actualizar región de scroll
        inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Botón para limpiar filtros
        ttk.Button(self, text="Limpiar filtros",
                  command=self.clear_filters).pack(pady=(5, 0))

    def _toggle_color(self, color_hex, var):
        """Alternar selección de color"""
        if var.get():
            self.selected_colors.add(color_hex)
        else:
            self.selected_colors.discard(color_hex)

        if self.on_filter_change:
            self.on_filter_change(list(self.selected_colors))

    def clear_filters(self):
        """Limpiar todos los filtros"""
        self.selected_colors.clear()

        # Desmarcar todos los checkboxes
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):
                # Obtener el frame interior
                for item in widget.winfo_children():
                    if isinstance(item, ttk.Frame):
                        for child in item.winfo_children():
                            if isinstance(child, ttk.Frame):
                                for subchild in child.winfo_children():
                                    if isinstance(subchild, ttk.Checkbutton):
                                        subchild.state(['!selected'])

        if self.on_filter_change:
            self.on_filter_change([])