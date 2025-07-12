"""
Componentes de pestañas para el formulario de productos - CORREGIDO
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import os
from PIL import Image, ImageTk, ImageDraw

from .modern_widgets import ModernWidgets
from ..style.color_palette import ColorPalette
from utils.file_utils import FileUtils
from models.producto import ColorEspecificacion


class BaseFormTab:
    """Clase base para pestañas del formulario"""

    def __init__(self, parent, vars_dict, colors=None, fonts=None):
        self.parent = parent
        self.vars = vars_dict
        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {
            'title': ('Segoe UI', 20, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8)
        }
        self.widgets = ModernWidgets(self.colors, self.fonts)
        self.entries = {}

    def create_scrollable_frame(self, parent):
        """Crear frame con scroll"""
        canvas = tk.Canvas(parent, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def create_card(self, parent, title, row=0, column=0, columnspan=1, padx=(0, 0)):
        """Crear tarjeta con título"""
        card = tk.Frame(parent, bg=self.colors['card'],
                        highlightbackground=self.colors['border'],
                        highlightthickness=1)
        card.grid(row=row, column=column, columnspan=columnspan,
                  sticky='nsew', padx=padx, pady=(0, 20))

        # Header
        header = tk.Frame(card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text=title, font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Content frame
        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        return card, content


class BasicInfoTab(BaseFormTab):
    """Pestaña de información básica"""

    def __init__(self, parent, vars_dict, **kwargs):
        super().__init__(parent, vars_dict, **kwargs)
        self.imagen_path = None
        self.image_label = None
        self.image_info = None
        self.create_tab()

    def create_tab(self):
        """Crear contenido de la pestaña"""
        # Frame principal con scroll
        scrollable_frame = self.create_scrollable_frame(self.parent)

        # Contenido principal
        main_content = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Grid de dos columnas
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        # Crear tarjetas
        self._create_basic_fields_card(main_content)
        self._create_image_card(main_content)

    def _create_basic_fields_card(self, parent):
        """Crear tarjeta de campos básicos"""
        card, content = self.create_card(parent, "📋 Datos del Producto",
                                         row=0, column=0, padx=(0, 15))

        # Campos del formulario
        fields = [
            ('nombre', 'Nombre del Producto *', 'entry', None, 'Ejemplo: Base para smartphone, Figura decorativa...'),
            ('descripcion', 'Descripción', 'entry', None, None),
            ('material', 'Material *', 'combobox', ['PLA', 'ABS', 'PETG', 'TPU', 'Nylon', 'Resina'], None),
            ('peso', 'Peso estimado (gramos)', 'spinbox', {'from_': 0, 'to': 10000, 'increment': 0.1}, None),
            ('tiempo_impresion', 'Tiempo base (minutos)', 'spinbox', {'from_': 0, 'to': 10000, 'increment': 1}, None)
        ]

        for field_name, label_text, widget_type, options, hint in fields:
            self._create_form_field(content, field_name, label_text, widget_type, options, hint)

    def _create_form_field(self, parent, field_name, label_text, widget_type, options, hint):
        """Crear campo del formulario"""
        field_frame = tk.Frame(parent, bg=self.colors['card'])
        field_frame.pack(fill=tk.X, pady=(0, 20))

        # Label
        label = tk.Label(field_frame, text=label_text, font=self.fonts['body'],
                         bg=self.colors['card'], fg=self.colors['text'])
        label.pack(anchor=tk.W, pady=(0, 8))

        # Widget según tipo
        if widget_type == 'entry':
            widget = ttk.Entry(field_frame, textvariable=self.vars[field_name],
                               font=self.fonts['body'])
            widget.pack(fill=tk.X, ipady=8)

        elif widget_type == 'combobox':
            widget = ttk.Combobox(field_frame, textvariable=self.vars[field_name],
                                  values=options, font=self.fonts['body'], state='readonly')
            widget.pack(fill=tk.X, ipady=8)

        elif widget_type == 'spinbox':
            widget = ttk.Spinbox(field_frame, textvariable=self.vars[field_name],
                                 font=self.fonts['body'], **options)
            widget.pack(fill=tk.X, ipady=8)

        self.entries[field_name] = widget

        # Hint/placeholder si existe
        if hint:
            hint_label = tk.Label(field_frame, text=hint, font=self.fonts['caption'],
                                  bg=self.colors['card'], fg=self.colors['text_secondary'])
            hint_label.pack(anchor=tk.W, pady=(5, 0))

    def _create_image_card(self, parent):
        """Crear tarjeta de imagen"""
        card, content = self.create_card(parent, "🖼️ Imagen del Producto",
                                         row=0, column=1, padx=(15, 0))

        # Área de imagen
        image_area = tk.Frame(content, bg=self.colors['accent'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        image_area.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.image_label = tk.Label(image_area, text="📷\nSin imagen\n\nHaz clic para seleccionar",
                                    font=self.fonts['body'], bg=self.colors['accent'],
                                    fg=self.colors['text_secondary'], cursor='hand2')
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=40)
        self.image_label.bind('<Button-1>', lambda e: self.seleccionar_imagen())

        # Botones de imagen
        btn_frame = tk.Frame(content, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X)

        btn_select = self.widgets.create_modern_button(btn_frame, "📁 Seleccionar Imagen",
                                                       self.seleccionar_imagen, 'secondary')
        btn_select.pack(fill=tk.X, pady=(0, 10))

        btn_remove = self.widgets.create_modern_button(btn_frame, "🗑️ Quitar Imagen",
                                                       self.quitar_imagen, 'danger')
        btn_remove.pack(fill=tk.X)

        # Info de imagen
        self.image_info = tk.Label(btn_frame, text="", font=self.fonts['caption'],
                                   bg=self.colors['card'], fg=self.colors['text_secondary'])
        self.image_info.pack(pady=(10, 0))

    def seleccionar_imagen(self):
        """Seleccionar imagen para el producto"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen del producto",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("Todos los archivos", "*.*")
            ]
        )

        if file_path and FileUtils.is_valid_image(file_path):
            self.imagen_path = file_path
            self._mostrar_imagen_preview()
        elif file_path:
            # Mostrar mensaje de error (callback)
            if hasattr(self, 'on_error'):
                self.on_error("El archivo seleccionado no es una imagen válida")

    def _mostrar_imagen_preview(self):
        """Mostrar vista previa de la imagen"""
        if self.imagen_path:
            try:
                img = Image.open(self.imagen_path)
                img.thumbnail((250, 250), Image.Resampling.LANCZOS)

                # Crear imagen con bordes redondeados
                mask = Image.new('L', img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle([(0, 0), img.size], radius=10, fill=255)

                output = Image.new('RGBA', img.size, (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)

                photo = ImageTk.PhotoImage(output)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo

                # Mostrar información
                size = FileUtils.get_file_size_readable(self.imagen_path)
                self.image_info.configure(text=f"📁 {os.path.basename(self.imagen_path)}\n📊 Tamaño: {size}")

            except Exception as e:
                if hasattr(self, 'on_error'):
                    self.on_error(f"Error al cargar imagen: {str(e)}")
                self.quitar_imagen()

    def quitar_imagen(self):
        """Quitar imagen seleccionada"""
        self.imagen_path = None
        self.image_label.configure(image="", text="📷\nSin imagen\n\nHaz clic para seleccionar")
        self.image_label.image = None
        self.image_info.configure(text="")

    def get_image_path(self):
        """Obtener ruta de la imagen"""
        return self.imagen_path


class ColorsTab(BaseFormTab):
    """Pestaña de especificaciones de color - CORREGIDA"""

    def __init__(self, parent, vars_dict, **kwargs):
        super().__init__(parent, vars_dict, **kwargs)
        self.color_specifications = []
        self.colors_frame = None
        self.create_tab()

    def create_tab(self):
        """Crear contenido de la pestaña - CORREGIDO"""
        # Contenido principal
        main_content = tk.Frame(self.parent, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Header con instrucciones
        self._create_instructions_card(main_content)

        # CORRECCIÓN: Llamar al método correcto para crear el área de especificaciones
        self._create_specifications_area(main_content)

    def _create_instructions_card(self, parent):
        """Crear tarjeta de instrucciones"""
        instructions_frame = tk.Frame(parent, bg=self.colors['accent'],
                                      highlightbackground=self.colors['border'],
                                      highlightthickness=1)
        instructions_frame.pack(fill=tk.X, pady=(0, 20))

        content = tk.Frame(instructions_frame, bg=self.colors['accent'])
        content.pack(fill=tk.X, padx=20, pady=15)

        # Título
        tk.Label(content, text="🎨 Especificaciones de Color por Pieza",
                 font=self.fonts['subheading'],
                 bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        # Instrucciones
        instructions = tk.Label(content,
                                text="Define cada pieza del producto con su color y peso específico. Esto te ayudará a calcular el material exacto necesario.",
                                font=self.fonts['body'], bg=self.colors['accent'],
                                fg=self.colors['text_secondary'], wraplength=600, justify=tk.LEFT)
        instructions.pack(anchor=tk.W)

    def _create_specifications_area(self, parent):
        """Crear área de especificaciones - CORREGIDO"""
        spec_card = tk.Frame(parent, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        spec_card.pack(fill=tk.BOTH, expand=True)

        # Header del área
        header = tk.Frame(spec_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(header, text="📝 Piezas y Colores",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Scroll container
        canvas = tk.Canvas(spec_card, bg=self.colors['card'], height=300,
                           highlightthickness=0)
        scrollbar = ttk.Scrollbar(spec_card, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame para las especificaciones
        self.colors_frame = tk.Frame(scrollable_frame, bg=self.colors['card'])
        self.colors_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20))

        # Botón para agregar especificación
        btn_frame = tk.Frame(spec_card, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        add_btn = self.widgets.create_modern_button(btn_frame, "➕ Agregar Especificación de Color",
                                                    self.agregar_especificacion_color, 'primary')
        add_btn.pack(fill=tk.X)

        # Agregar primera especificación automáticamente
        self.agregar_especificacion_color()

    def agregar_especificacion_color(self):
        """Agregar nueva especificación de color"""
        index = len(self.color_specifications)

        color_widget = ColorSpecificationWidget(
            self.colors_frame,
            index=index,
            on_delete=self.eliminar_especificacion_color,
            colors=self.colors,
            fonts=self.fonts
        )
        color_widget.pack(fill=tk.X, pady=10)

        self.color_specifications.append(color_widget)

    def eliminar_especificacion_color(self, index):
        """Eliminar especificación de color - CORREGIDO"""
        if len(self.color_specifications) > 1:
            widget = self.color_specifications[index]
            widget.destroy()
            del self.color_specifications[index]

            # Reindexar widgets restantes
            for i, widget in enumerate(self.color_specifications):
                widget.index = i
                widget.update_title(f"Color {i + 1}")
        else:
            if hasattr(self, 'on_warning'):
                self.on_warning("Debe mantener al menos una especificación de color")

    def get_color_specifications(self):
        """Obtener todas las especificaciones de color"""
        specs = []
        for widget in self.color_specifications:
            widget_specs = widget.get_all_specifications()
            for spec in widget_specs:
                if spec.peso_color > 0:
                    specs.append(spec)
        return specs


class ConfigTab(BaseFormTab):
    """Pestaña de configuración"""

    def __init__(self, parent, vars_dict, **kwargs):
        super().__init__(parent, vars_dict, **kwargs)
        self.guia_text = None
        self.create_tab()

    def create_tab(self):
        """Crear contenido de la pestaña"""
        # Contenido principal
        main_content = tk.Frame(self.parent, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Grid de dos columnas
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        # Crear tarjetas
        self._create_print_config_card(main_content)
        self._create_guide_card(main_content)

    def _create_print_config_card(self, parent):
        """Crear tarjeta de configuración de impresión"""
        card, content = self.create_card(parent, "🌡️ Configuración de Impresión",
                                         row=0, column=0, padx=(0, 15))

        # Campos de temperatura
        temp_fields = [
            ('temperatura_extrusor', 'Temperatura del Extrusor (°C)', {'from_': 150, 'to': 300, 'increment': 5}),
            ('temperatura_cama', 'Temperatura de la Cama (°C)', {'from_': 0, 'to': 120, 'increment': 5})
        ]

        for field_name, label_text, options in temp_fields:
            self._create_temperature_field(content, field_name, label_text, options)

        # Presets por material
        self._create_presets_section(content)

    def _create_temperature_field(self, parent, field_name, label_text, options):
        """Crear campo de temperatura"""
        field_frame = tk.Frame(parent, bg=self.colors['card'])
        field_frame.pack(fill=tk.X, pady=(0, 20))

        label = tk.Label(field_frame, text=label_text, font=self.fonts['body'],
                         bg=self.colors['card'], fg=self.colors['text'])
        label.pack(anchor=tk.W, pady=(0, 8))

        widget = ttk.Spinbox(field_frame, textvariable=self.vars[field_name],
                             font=self.fonts['body'], **options)
        widget.pack(fill=tk.X, ipady=8)
        self.entries[field_name] = widget

    def _create_presets_section(self, parent):
        """Crear sección de presets"""
        preset_frame = tk.Frame(parent, bg=self.colors['accent'])
        preset_frame.pack(fill=tk.X, pady=(20, 0))

        preset_content = tk.Frame(preset_frame, bg=self.colors['accent'])
        preset_content.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(preset_content, text="💡 Presets por Material", font=self.fonts['body'],
                 bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        presets = {
            'PLA': {'extrusor': 200, 'cama': 60},
            'ABS': {'extrusor': 240, 'cama': 80},
            'PETG': {'extrusor': 230, 'cama': 70},
            'TPU': {'extrusor': 220, 'cama': 50}
        }

        for material, temps in presets.items():
            btn = tk.Button(preset_content, text=f"{material} ({temps['extrusor']}°/{temps['cama']}°)",
                            font=self.fonts['caption'], bg=self.colors['card'], fg=self.colors['text'],
                            bd=1, relief=tk.FLAT, padx=8, pady=4,
                            command=lambda m=material, t=temps: self.aplicar_preset(m, t))
            btn.pack(side=tk.LEFT, padx=5)

    def _create_guide_card(self, parent):
        """Crear tarjeta de guía"""
        card, content = self.create_card(parent, "📖 Guía de Impresión",
                                         row=0, column=1, padx=(15, 0))

        # ScrolledText moderno
        self.guia_text = scrolledtext.ScrolledText(
            content, wrap=tk.WORD, height=15, font=self.fonts['body'],
            bg='white', fg=self.colors['text'], relief=tk.FLAT, borderwidth=1,
            selectbackground=self.colors['primary'], selectforeground='white'
        )
        self.guia_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Sugerencias
        self._create_suggestions_section(content)

    def _create_suggestions_section(self, parent):
        """Crear sección de sugerencias"""
        suggestions_frame = tk.Frame(parent, bg=self.colors['accent'])
        suggestions_frame.pack(fill=tk.X)

        suggestions_content = tk.Frame(suggestions_frame, bg=self.colors['accent'])
        suggestions_content.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(suggestions_content, text="💡 Sugerencias para la guía:", font=self.fonts['body'],
                 bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 5))

        suggestions_text = """• Configuración del slicer (altura de capa, relleno)
• Preparación de la superficie de impresión
• Consejos para la primera capa
• Manejo de soportes si son necesarios
• Post-procesamiento recomendado"""

        tk.Label(suggestions_content, text=suggestions_text, font=self.fonts['caption'],
                 bg=self.colors['accent'], fg=self.colors['text_secondary'],
                 justify=tk.LEFT).pack(anchor=tk.W)

    def aplicar_preset(self, material, temps):
        """Aplicar preset de temperatura"""
        self.vars['temperatura_extrusor'].set(temps['extrusor'])
        self.vars['temperatura_cama'].set(temps['cama'])
        self.vars['material'].set(material)

    def get_guide_text(self):
        """Obtener texto de la guía"""
        return self.guia_text.get('1.0', 'end-1c')


class ColorSpecificationWidget(tk.Frame):
    """Widget para especificación individual de color - CORREGIDO"""

    def __init__(self, parent, index, on_delete=None, colors=None, fonts=None):
        super().__init__(parent, bg=colors['card'] if colors else '#FFFFFF')

        self.index = index
        self.on_delete = on_delete
        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {'body': ('Segoe UI', 10), 'caption': ('Segoe UI', 8)}

        # Variables
        self.vars = {
            'nombre_pieza': tk.StringVar(value=f"Pieza {index + 1}"),
            'color_hex': tk.StringVar(value="#FF0000"),
            'nombre_color': tk.StringVar(),
            'peso_color': tk.DoubleVar(value=0.0)
        }

        self.create_widget()

    def create_widget(self):
        """Crear el widget de especificación"""
        # Frame principal con borde
        main_frame = tk.Frame(self, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        main_frame.pack(fill=tk.X, padx=5, pady=5)

        # Header con título y botón eliminar
        header = tk.Frame(main_frame, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=15, pady=(15, 10))

        self.title_label = tk.Label(header, text=f"🎨 Color {self.index + 1}",
                                    font=self.fonts['body'], bg=self.colors['card'],
                                    fg=self.colors['text'])
        self.title_label.pack(side=tk.LEFT)

        if self.on_delete:
            btn_delete = tk.Button(header, text="🗑️", font=self.fonts['caption'],
                                   bg=self.colors['danger'], fg='white', bd=0,
                                   padx=8, pady=4, cursor='hand2',
                                   command=lambda: self.on_delete(self.index))
            btn_delete.pack(side=tk.RIGHT)

        # Contenido
        content = tk.Frame(main_frame, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=15, pady=(0, 15))

        # Grid para campos
        content.grid_columnconfigure(1, weight=1)

        # Campos
        fields = [
            ('nombre_pieza', 'Nombre de la pieza:', 0),
            ('nombre_color', 'Nombre del color:', 1),
            ('peso_color', 'Peso (gramos):', 2)
        ]

        for var_name, label_text, row in fields:
            tk.Label(content, text=label_text, font=self.fonts['body'],
                     bg=self.colors['card'], fg=self.colors['text']).grid(
                row=row, column=0, sticky='w', pady=5, padx=(0, 10))

            if var_name == 'peso_color':
                entry = ttk.Spinbox(content, textvariable=self.vars[var_name],
                                    from_=0, to=10000, increment=0.1, font=self.fonts['body'])
            else:
                entry = ttk.Entry(content, textvariable=self.vars[var_name],
                                  font=self.fonts['body'])

            entry.grid(row=row, column=1, sticky='ew', pady=5, ipady=4)

        # Selector de color
        color_frame = tk.Frame(content, bg=self.colors['card'])
        color_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=10)

        tk.Label(color_frame, text="Color:", font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        self.color_preview = tk.Button(color_frame, text="", width=10, height=2,
                                       bg=self.vars['color_hex'].get(), cursor='hand2',
                                       command=self.seleccionar_color)
        self.color_preview.pack(side=tk.LEFT, padx=10)

        self.color_label = tk.Label(color_frame, text=self.vars['color_hex'].get(),
                                    font=self.fonts['caption'], bg=self.colors['card'],
                                    fg=self.colors['text_secondary'])
        self.color_label.pack(side=tk.LEFT, padx=10)

    def seleccionar_color(self):
        """Seleccionar color"""
        from tkinter import colorchooser

        color = colorchooser.askcolor(initialcolor=self.vars['color_hex'].get())
        if color[1]:  # Si se seleccionó un color
            self.vars['color_hex'].set(color[1])
            self.color_preview.config(bg=color[1])
            self.color_label.config(text=color[1])

    def update_title(self, title):
        """Actualizar título del widget"""
        self.title_label.config(text=title)

    def get_all_specifications(self):
        """Obtener todas las especificaciones como objetos"""
        return [ColorEspecificacion(
            color_hex=self.vars['color_hex'].get(),
            nombre_color=self.vars['nombre_color'].get(),
            piezas=[self.vars['nombre_pieza'].get()],  # Lista de piezas
            peso_color=self.vars['peso_color'].get(),
            tiempo_adicional=0,  # Parámetro requerido
            notas=""  # Parámetro requerido
        )]