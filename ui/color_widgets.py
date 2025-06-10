"""
Widgets personalizados para manejo de colores
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from typing import List, Callable, Optional
import re

from models.producto import ColorEspecificacion


class ColorPicker(ttk.Frame):
    """Widget selector de color hexadecimal"""

    def __init__(self, parent, initial_color="#000000", callback=None):
        super().__init__(parent)

        self.color_var = tk.StringVar(value=initial_color)
        self.callback = callback

        # Entry para código hexadecimal
        self.hex_entry = ttk.Entry(self, textvariable=self.color_var, width=10)
        self.hex_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.hex_entry.bind('<FocusOut>', self._validate_hex)
        self.hex_entry.bind('<Return>', self._validate_hex)

        # Botón de color
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


class ColorSpecificationWidget(ttk.LabelFrame):
    """Widget para especificar detalles de un color"""

    def __init__(self, parent, color_spec: Optional[ColorEspecificacion] = None,
                 on_delete=None, index=0):
        super().__init__(parent, text=f"Color {index + 1}", padding="10")

        self.on_delete = on_delete
        self.index = index
        self.piezas = []

        # Inicializar con especificación existente o crear nueva
        if color_spec:
            self.color_hex = color_spec.color_hex
            self.nombre_color = color_spec.nombre_color
            self.peso_color = color_spec.peso_color
            self.tiempo_adicional = color_spec.tiempo_adicional
            self.notas = color_spec.notas
            self.piezas = color_spec.piezas.copy()
        else:
            self.color_hex = "#000000"
            self.nombre_color = ""
            self.peso_color = 0.0
            self.tiempo_adicional = 0
            self.notas = ""

        self._create_widgets()

    def _create_widgets(self):
        """Crear los widgets del panel"""
        # Primera fila: Color y nombre
        row1 = ttk.Frame(self)
        row1.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(row1, text="Color:").pack(side=tk.LEFT, padx=(0, 5))
        self.color_picker = ColorPicker(row1, initial_color=self.color_hex)
        self.color_picker.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row1, text="Nombre:").pack(side=tk.LEFT, padx=(0, 5))
        self.nombre_var = tk.StringVar(value=self.nombre_color)
        self.nombre_entry = ttk.Entry(row1, textvariable=self.nombre_var, width=20)
        self.nombre_entry.pack(side=tk.LEFT)

        # Botón eliminar
        if self.on_delete:
            ttk.Button(row1, text="🗑️ Eliminar",
                       command=lambda: self.on_delete(self.index)).pack(side=tk.RIGHT)

        # Segunda fila: Peso y tiempo
        row2 = ttk.Frame(self)
        row2.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(row2, text="Peso (g):").pack(side=tk.LEFT, padx=(0, 5))
        self.peso_var = tk.DoubleVar(value=self.peso_color)
        self.peso_spin = ttk.Spinbox(row2, textvariable=self.peso_var,
                                     from_=0, to=1000, increment=0.1, width=10)
        self.peso_spin.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(row2, text="Tiempo cambio color (min):").pack(side=tk.LEFT, padx=(0, 5))
        self.tiempo_var = tk.IntVar(value=self.tiempo_adicional)
        self.tiempo_spin = ttk.Spinbox(row2, textvariable=self.tiempo_var,
                                       from_=0, to=60, increment=1, width=10)
        self.tiempo_spin.pack(side=tk.LEFT)

        # Tercera fila: Piezas
        row3 = ttk.Frame(self)
        row3.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(row3, text="Piezas:").pack(side=tk.LEFT, anchor=tk.N, padx=(0, 5))

        piezas_frame = ttk.Frame(row3)
        piezas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Lista de piezas
        self.piezas_listbox = tk.Listbox(piezas_frame, height=3, width=30)
        self.piezas_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar para lista
        scrollbar = ttk.Scrollbar(piezas_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.piezas_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.piezas_listbox.yview)

        # Cargar piezas existentes
        for pieza in self.piezas:
            self.piezas_listbox.insert(tk.END, pieza)

        # Botones para piezas
        btn_frame = ttk.Frame(row3)
        btn_frame.pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(btn_frame, text="➕", width=3,
                   command=self._agregar_pieza).pack(pady=2)
        ttk.Button(btn_frame, text="➖", width=3,
                   command=self._eliminar_pieza).pack(pady=2)

        # Cuarta fila: Notas
        row4 = ttk.Frame(self)
        row4.pack(fill=tk.X)

        ttk.Label(row4, text="Notas:").pack(side=tk.LEFT, anchor=tk.N, padx=(0, 5))
        self.notas_text = tk.Text(row4, height=2, width=40, wrap=tk.WORD)
        self.notas_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.notas_text.insert('1.0', self.notas)

    def _agregar_pieza(self):
        """Agregar una pieza a la lista"""
        dialog = tk.Toplevel(self)
        dialog.title("Agregar Pieza")
        dialog.geometry("300x100")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Nombre de la pieza:").pack(pady=10)

        pieza_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=pieza_var, width=30)
        entry.pack(pady=5)
        entry.focus()

        def agregar():
            pieza = pieza_var.get().strip()
            if pieza:
                self.piezas_listbox.insert(tk.END, pieza)
                self.piezas.append(pieza)
                dialog.destroy()

        entry.bind('<Return>', lambda e: agregar())

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Agregar", command=agregar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT)

        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

    def _eliminar_pieza(self):
        """Eliminar pieza seleccionada"""
        selection = self.piezas_listbox.curselection()
        if selection:
            index = selection[0]
            self.piezas_listbox.delete(index)
            del self.piezas[index]

    def get_specification(self) -> ColorEspecificacion:
        """Obtener la especificación de color"""
        # Actualizar lista de piezas
        self.piezas = list(self.piezas_listbox.get(0, tk.END))

        return ColorEspecificacion(
            color_hex=self.color_picker.get_color(),
            nombre_color=self.nombre_var.get().strip(),
            peso_color=self.peso_var.get(),
            tiempo_adicional=self.tiempo_var.get(),
            notas=self.notas_text.get('1.0', 'end-1c').strip(),
            piezas=self.piezas
        )


class ColorFilterWidget(ttk.Frame):
    """Widget para filtrar por colores"""

    def __init__(self, parent, colors: List[dict], on_filter_change=None):
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