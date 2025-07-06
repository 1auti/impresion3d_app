"""
Ventana para agregar nuevo producto - Versión Modernizada
"""

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
import os
from PIL import Image, ImageTk, ImageDraw

from database.db_manager import DatabaseManager
from models.producto import Producto
from utils.file_utils import FileUtils


class ModernAddProductWindow:
    """Ventana modernizada para agregar un nuevo producto"""

    def __init__(self, parent, db_manager: DatabaseManager):
        self.parent = parent
        self.db_manager = db_manager
        self.producto_creado = False
        self.imagen_path = None
        self.color_specifications = []

        # Configurar colores y estilos modernos
        self.setup_modern_colors()

        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title("Agregar Nuevo Producto")
        self.window.geometry("1000x800")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(bg=self.colors['bg'])

        # Variables
        self.crear_variables()

        # Configurar estilos
        self.setup_modern_styles()

        # Crear interfaz
        self.create_modern_widgets()

        # Centrar ventana
        self.center_window()

        # Focus en el primer campo
        self.entries['nombre'].focus()

    def setup_modern_colors(self):
        """Configurar paleta de colores moderna"""
        self.colors = {
            'bg': '#F8FAFC',
            'card': '#FFFFFF',
            'primary': '#6366F1',
            'primary_hover': '#5558E3',
            'secondary': '#EC4899',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'text': '#1E293B',
            'text_secondary': '#64748B',
            'border': '#E2E8F0',
            'accent': '#F1F5F9',
            'input_bg': '#FFFFFF'
        }

        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8)
        }

    def setup_modern_styles(self):
        """Configurar estilos modernos"""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook moderno
        style.configure('Modern.TNotebook',
                       background=self.colors['card'],
                       borderwidth=0,
                       relief='flat')

        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       padding=(20, 12),
                       borderwidth=0,
                       font=self.fonts['body'])

        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['primary_hover'])],
                 foreground=[('selected', 'white'),
                           ('active', 'white')])

        # Entry moderno
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['border'],
                       darkcolor=self.colors['border'],
                       insertcolor=self.colors['text'],
                       font=self.fonts['body'])

        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.colors['primary']),
                            ('!focus', self.colors['border'])])

        # Combobox moderno
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'],
                       font=self.fonts['body'])

        # Spinbox moderno
        style.configure('Modern.TSpinbox',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'],
                       font=self.fonts['body'])

        # LabelFrame moderno
        style.configure('Modern.TLabelframe',
                       background=self.colors['card'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'],
                       font=self.fonts['subheading'])

        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       font=self.fonts['subheading'])

    def crear_variables(self):
        """Crear variables para los campos"""
        self.vars = {
            'nombre': tk.StringVar(),
            'descripcion': tk.StringVar(),
            'peso': tk.DoubleVar(value=0.0),
            'tiempo_impresion': tk.IntVar(value=0),
            'material': tk.StringVar(value="PLA"),
            'temperatura_extrusor': tk.IntVar(value=200),
            'temperatura_cama': tk.IntVar(value=60)
        }
        self.entries = {}

    def create_modern_widgets(self):
        """Crear interfaz moderna"""
        # Frame principal
        main_container = tk.Frame(self.window, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header moderno
        self.create_modern_header(main_container)

        # Contenido principal
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Notebook modernizado
        self.notebook = ttk.Notebook(content_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Crear pestañas
        self.create_basic_info_tab()
        self.create_colors_tab()
        self.create_config_tab()

        # Botones de acción
        self.create_action_buttons(main_container)

    def create_modern_header(self, parent):
        """Crear header moderno"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        # Icono y título
        icon_label = tk.Label(header_content, text="➕", font=('Segoe UI', 28),
                             bg=self.colors['primary'], fg='white')
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        title_info = tk.Frame(header_content, bg=self.colors['primary'])
        title_info.pack(side=tk.LEFT)

        title_label = tk.Label(title_info, text="Agregar Nuevo Producto",
                              font=self.fonts['title'],
                              bg=self.colors['primary'], fg='white')
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_info, text="Complete la información del producto de impresión 3D",
                                 font=self.fonts['body'],
                                 bg=self.colors['primary'], fg='white')
        subtitle_label.pack(anchor=tk.W)

        # Indicador de progreso
        progress_frame = tk.Frame(header_content, bg=self.colors['primary'])
        progress_frame.pack(side=tk.RIGHT)

        tk.Label(progress_frame, text="Paso 1 de 3",
                font=self.fonts['small'],
                bg=self.colors['primary'], fg='white').pack()

    def create_basic_info_tab(self):
        """Crear pestaña de información básica"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="📝 Información Básica")

        # Scroll container
        canvas = tk.Canvas(tab_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Contenido principal
        main_content = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Grid de dos columnas
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        # Columna izquierda - Campos básicos
        self.create_basic_fields_card(main_content)

        # Columna derecha - Imagen
        self.create_image_card(main_content)

    def create_basic_fields_card(self, parent):
        """Crear tarjeta de campos básicos"""
        fields_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        fields_card.grid(row=0, column=0, sticky='nsew', padx=(0, 15), pady=(0, 20))

        # Header
        header = tk.Frame(fields_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="📋 Datos del Producto",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Contenido
        content = tk.Frame(fields_card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Campos
        fields = [
            ('nombre', 'Nombre del Producto *', 'entry', None),
            ('descripcion', 'Descripción', 'entry', None),
            ('material', 'Material *', 'combobox', ['PLA', 'ABS', 'PETG', 'TPU', 'Nylon', 'Resina']),
            ('peso', 'Peso estimado (gramos)', 'spinbox', {'from_': 0, 'to': 10000, 'increment': 0.1}),
            ('tiempo_impresion', 'Tiempo base (minutos)', 'spinbox', {'from_': 0, 'to': 10000, 'increment': 1})
        ]

        for field_name, label_text, widget_type, options in fields:
            self.create_modern_field(content, field_name, label_text, widget_type, options)

    def create_modern_field(self, parent, field_name, label_text, widget_type, options):
        """Crear campo moderno"""
        field_frame = tk.Frame(parent, bg=self.colors['card'])
        field_frame.pack(fill=tk.X, pady=(0, 20))

        # Label
        label = tk.Label(field_frame, text=label_text,
                        font=self.fonts['body'],
                        bg=self.colors['card'], fg=self.colors['text'])
        label.pack(anchor=tk.W, pady=(0, 8))

        # Widget según tipo
        if widget_type == 'entry':
            widget = ttk.Entry(field_frame, textvariable=self.vars[field_name],
                              style='Modern.TEntry', font=self.fonts['body'])
            widget.pack(fill=tk.X, ipady=8)

        elif widget_type == 'combobox':
            widget = ttk.Combobox(field_frame, textvariable=self.vars[field_name],
                                 values=options, style='Modern.TCombobox',
                                 font=self.fonts['body'], state='readonly')
            widget.pack(fill=tk.X, ipady=8)

        elif widget_type == 'spinbox':
            widget = ttk.Spinbox(field_frame, textvariable=self.vars[field_name],
                                style='Modern.TSpinbox', font=self.fonts['body'],
                                **options)
            widget.pack(fill=tk.X, ipady=8)

        self.entries[field_name] = widget

        # Agregar placeholder/hint si es necesario
        if field_name == 'nombre':
            hint = tk.Label(field_frame, text="Ejemplo: Base para smartphone, Figura decorativa...",
                           font=self.fonts['caption'],
                           bg=self.colors['card'], fg=self.colors['text_secondary'])
            hint.pack(anchor=tk.W, pady=(5, 0))

    def create_image_card(self, parent):
        """Crear tarjeta de imagen"""
        image_card = tk.Frame(parent, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        image_card.grid(row=0, column=1, sticky='nsew', padx=(15, 0), pady=(0, 20))

        # Header
        header = tk.Frame(image_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="🖼️ Imagen del Producto",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Área de imagen
        image_area = tk.Frame(image_card, bg=self.colors['accent'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        image_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        self.image_label = tk.Label(image_area, text="📷\nSin imagen\n\nHaz clic para seleccionar",
                                   font=self.fonts['body'],
                                   bg=self.colors['accent'], fg=self.colors['text_secondary'],
                                   cursor='hand2')
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=40)
        self.image_label.bind('<Button-1>', lambda e: self.seleccionar_imagen())

        # Botones de imagen
        btn_frame = tk.Frame(image_card, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        btn_select = self.create_modern_button(btn_frame, "📁 Seleccionar Imagen",
                                              self.seleccionar_imagen, 'secondary')
        btn_select.pack(fill=tk.X, pady=(0, 10))

        btn_remove = self.create_modern_button(btn_frame, "🗑️ Quitar Imagen",
                                              self.quitar_imagen, 'danger')
        btn_remove.pack(fill=tk.X)

        # Info de imagen
        self.image_info = tk.Label(btn_frame, text="",
                                  font=self.fonts['caption'],
                                  bg=self.colors['card'], fg=self.colors['text_secondary'])
        self.image_info.pack(pady=(10, 0))

    def create_colors_tab(self):
        """Crear pestaña de especificaciones de color"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="🎨 Colores y Piezas")

        # Contenido principal
        main_content = tk.Frame(tab_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Header con instrucciones
        header_card = tk.Frame(main_content, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        header_card.pack(fill=tk.X, pady=(0, 20))

        header_content = tk.Frame(header_card, bg=self.colors['card'])
        header_content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(header_content, text="🎨 Especificaciones de Color por Pieza",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        instructions = tk.Label(header_content,
                               text="Define cada pieza del producto con su color y peso específico. Esto te ayudará a calcular el material exacto necesario.",
                               font=self.fonts['body'],
                               bg=self.colors['card'], fg=self.colors['text_secondary'],
                               wraplength=600, justify=tk.LEFT)
        instructions.pack(anchor=tk.W, pady=(5, 0))

        # Área de especificaciones con scroll
        spec_card = tk.Frame(main_content, bg=self.colors['card'],
                            highlightbackground=self.colors['border'],
                            highlightthickness=1)
        spec_card.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(spec_card, bg=self.colors['card'], highlightthickness=0)
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

        # Botón para agregar especificación
        btn_frame = tk.Frame(scrollable_frame, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        add_btn = self.create_modern_button(btn_frame, "➕ Agregar Especificación de Color",
                                           self.agregar_especificacion_color, 'primary')
        add_btn.pack(fill=tk.X)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Agregar primera especificación
        self.agregar_especificacion_color()

    def create_config_tab(self):
        """Crear pestaña de configuración"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="⚙️ Configuración")

        # Contenido principal
        main_content = tk.Frame(tab_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Grid de dos columnas
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        # Configuración de impresión
        self.create_print_config_card(main_content)

        # Guía de impresión
        self.create_guide_card(main_content)

    def create_print_config_card(self, parent):
        """Crear tarjeta de configuración de impresión"""
        config_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        config_card.grid(row=0, column=0, sticky='nsew', padx=(0, 15))

        # Header
        header = tk.Frame(config_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="🌡️ Configuración de Impresión",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Contenido
        content = tk.Frame(config_card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Campos de temperatura
        temp_fields = [
            ('temperatura_extrusor', 'Temperatura del Extrusor (°C)', {'from_': 150, 'to': 300, 'increment': 5}),
            ('temperatura_cama', 'Temperatura de la Cama (°C)', {'from_': 0, 'to': 120, 'increment': 5})
        ]

        for field_name, label_text, options in temp_fields:
            field_frame = tk.Frame(content, bg=self.colors['card'])
            field_frame.pack(fill=tk.X, pady=(0, 20))

            label = tk.Label(field_frame, text=label_text,
                            font=self.fonts['body'],
                            bg=self.colors['card'], fg=self.colors['text'])
            label.pack(anchor=tk.W, pady=(0, 8))

            widget = ttk.Spinbox(field_frame, textvariable=self.vars[field_name],
                                style='Modern.TSpinbox', font=self.fonts['body'],
                                **options)
            widget.pack(fill=tk.X, ipady=8)
            self.entries[field_name] = widget

        # Presets por material
        preset_frame = tk.Frame(content, bg=self.colors['accent'])
        preset_frame.pack(fill=tk.X, pady=(20, 0))

        preset_content = tk.Frame(preset_frame, bg=self.colors['accent'])
        preset_content.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(preset_content, text="💡 Presets por Material",
                font=self.fonts['body'],
                bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        presets = {
            'PLA': {'extrusor': 200, 'cama': 60},
            'ABS': {'extrusor': 240, 'cama': 80},
            'PETG': {'extrusor': 230, 'cama': 70},
            'TPU': {'extrusor': 220, 'cama': 50}
        }

        for material, temps in presets.items():
            btn = tk.Button(preset_content, text=f"{material} ({temps['extrusor']}°/{temps['cama']}°)",
                           font=self.fonts['caption'],
                           bg=self.colors['card'], fg=self.colors['text'],
                           bd=1, relief=tk.FLAT, padx=8, pady=4,
                           command=lambda m=material, t=temps: self.aplicar_preset(m, t))
            btn.pack(side=tk.LEFT, padx=5)

    def create_guide_card(self, parent):
        """Crear tarjeta de guía"""
        guide_card = tk.Frame(parent, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        guide_card.grid(row=0, column=1, sticky='nsew', padx=(15, 0))

        # Header
        header = tk.Frame(guide_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="📖 Guía de Impresión",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # ScrolledText moderno
        self.guia_text = scrolledtext.ScrolledText(
            guide_card, wrap=tk.WORD, height=15,
            font=self.fonts['body'],
            bg='white', fg=self.colors['text'],
            relief=tk.FLAT, borderwidth=1,
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        self.guia_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        # Sugerencias
        suggestions_frame = tk.Frame(guide_card, bg=self.colors['accent'])
        suggestions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        suggestions_content = tk.Frame(suggestions_frame, bg=self.colors['accent'])
        suggestions_content.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(suggestions_content, text="💡 Sugerencias para la guía:",
                font=self.fonts['body'],
                bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 5))

        suggestions_text = """• Configuración del slicer (altura de capa, relleno)
• Preparación de la superficie de impresión
• Consejos para la primera capa
• Manejo de soportes si son necesarios
• Post-procesamiento recomendado"""

        tk.Label(suggestions_content, text=suggestions_text,
                font=self.fonts['caption'],
                bg=self.colors['accent'], fg=self.colors['text_secondary'],
                justify=tk.LEFT).pack(anchor=tk.W)

    def create_action_buttons(self, parent):
        """Crear botones de acción"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X)

        # Botón cancelar
        btn_cancel = self.create_modern_button(btn_frame, "❌ Cancelar",
                                              self.window.destroy, 'secondary')
        btn_cancel.pack(side=tk.RIGHT, padx=(10, 0))

        # Botón guardar
        btn_save = self.create_modern_button(btn_frame, "💾 Guardar Producto",
                                            self.guardar_producto, 'primary')
        btn_save.pack(side=tk.RIGHT)

        # Botón vista previa
        btn_preview = self.create_modern_button(btn_frame, "👁️ Vista Previa",
                                               self.mostrar_vista_previa, 'secondary')
        btn_preview.pack(side=tk.LEFT)

    def create_modern_button(self, parent, text, command, style='secondary'):
        """Crear botón moderno"""
        colors = {
            'primary': (self.colors['primary'], 'white', self.colors['primary_hover']),
            'secondary': (self.colors['card'], self.colors['text'], self.colors['accent']),
            'danger': (self.colors['danger'], 'white', '#DC2626')
        }

        bg, fg, hover = colors.get(style, colors['secondary'])

        btn_frame = tk.Frame(parent, bg=bg,
                            highlightbackground=self.colors['border'],
                            highlightthickness=1 if style == 'secondary' else 0)

        btn = tk.Button(btn_frame, text=text, command=command,
                       font=self.fonts['body'], bg=bg, fg=fg,
                       bd=0, padx=20, pady=12, cursor='hand2',
                       activebackground=hover, activeforeground=fg)
        btn.pack(fill=tk.BOTH)

        # Efectos hover
        def on_enter(e):
            btn.config(bg=hover)
            btn_frame.config(bg=hover)

        def on_leave(e):
            btn.config(bg=bg)
            btn_frame.config(bg=bg)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        return btn_frame

    def agregar_especificacion_color(self):
        """Agregar nueva especificación de color"""
        index = len(self.color_specifications)

        color_widget = ColorSpecificationWidget(
            self.colors_frame,
            index=index,
            on_delete=self.eliminar_especificacion_color
        )
        color_widget.pack(fill=tk.X, pady=10)

        self.color_specifications.append(color_widget)

    def eliminar_especificacion_color(self, index):
        """Eliminar especificación de color"""
        if len(self.color_specifications) > 1:
            widget = self.color_specifications[index]
            widget.destroy()
            del self.color_specifications[index]

            # Reindexar
            for i, widget in enumerate(self.color_specifications):
                widget.index = i
                widget.configure(text=f"Color {i + 1}")
        else:
            self.show_modern_message("Advertencia",
                                   "Debe mantener al menos una especificación de color",
                                   'warning')

    def aplicar_preset(self, material, temps):
        """Aplicar preset de temperatura"""
        self.vars['temperatura_extrusor'].set(temps['extrusor'])
        self.vars['temperatura_cama'].set(temps['cama'])
        self.vars['material'].set(material)

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
            self.mostrar_imagen_preview()
        elif file_path:
            self.show_modern_message("Error",
                                   "El archivo seleccionado no es una imagen válida",
                                   'error')

    def mostrar_imagen_preview(self):
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
                self.show_modern_message("Error", f"Error al cargar imagen: {str(e)}", 'error')
                self.quitar_imagen()

    def quitar_imagen(self):
        """Quitar imagen seleccionada"""
        self.imagen_path = None
        self.image_label.configure(image="", text="📷\nSin imagen\n\nHaz clic para seleccionar")
        self.image_label.image = None
        self.image_info.configure(text="")

    def mostrar_vista_previa(self):
        """Mostrar vista previa del producto"""
        if not self.validar_campos_basicos():
            return

        # Crear ventana de vista previa
        preview_window = tk.Toplevel(self.window)
        preview_window.title("Vista Previa del Producto")
        preview_window.geometry("600x500")
        preview_window.transient(self.window)
        preview_window.configure(bg=self.colors['bg'])

        # Contenido de vista previa
        content = tk.Frame(preview_window, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Simular información del producto
        tk.Label(content, text=f"📦 {self.vars['nombre'].get()}",
                font=self.fonts['title'],
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=(20, 10))

        info_text = f"""Material: {self.vars['material'].get()}
Peso estimado: {self.vars['peso'].get():.1f}g
Tiempo base: {self.vars['tiempo_impresion'].get()} min
Temperatura extrusor: {self.vars['temperatura_extrusor'].get()}°C
Temperatura cama: {self.vars['temperatura_cama'].get()}°C

Especificaciones de color: {len(self.color_specifications)} configuraciones"""

        tk.Label(content, text=info_text,
                font=self.fonts['body'],
                bg=self.colors['card'], fg=self.colors['text'],
                justify=tk.LEFT).pack(pady=20)

        # Botón cerrar
        btn_close = self.create_modern_button(content, "Cerrar", preview_window.destroy, 'primary')
        btn_close.pack(pady=20)

    def validar_campos_basicos(self):
        """Validar campos básicos"""
        if not self.vars['nombre'].get().strip():
            self.show_modern_message("Error", "El nombre del producto es requerido", 'error')
            self.notebook.select(0)  # Ir a la primera pestaña
            self.entries['nombre'].focus()
            return False
        return True

    def validar_campos(self):
        """Validar todos los campos"""
        if not self.validar_campos_basicos():
            return False

        try:
            peso = self.vars['peso'].get()
            if peso < 0:
                self.show_modern_message("Error", "El peso no puede ser negativo", 'error')
                return False
        except:
            self.show_modern_message("Error", "El peso debe ser un número válido", 'error')
            return False

        try:
            tiempo = self.vars['tiempo_impresion'].get()
            if tiempo < 0:
                self.show_modern_message("Error", "El tiempo de impresión no puede ser negativo", 'error')
                return False
        except:
            self.show_modern_message("Error", "El tiempo de impresión debe ser un número válido", 'error')
            return False

        return True

    def guardar_producto(self):
        """Guardar el nuevo producto"""
        if not self.validar_campos():
            return

        try:
            # Obtener especificaciones de color
            color_specs = []
            peso_total = 0.0

            for widget in self.color_specifications:
                specs = widget.get_all_specifications()
                for spec in specs:
                    if spec.peso_color > 0:
                        color_specs.append(spec)
                        peso_total += spec.peso_color

            if not color_specs:
                self.show_modern_message("Error",
                                       "Debe agregar al menos una pieza con peso mayor a 0",
                                       'error')
                self.notebook.select(1)  # Ir a pestaña de colores
                return

            # Crear producto
            producto = Producto(
                nombre=self.vars['nombre'].get().strip(),
                descripcion=self.vars['descripcion'].get().strip(),
                peso=peso_total,
                color="",
                colores_especificaciones=color_specs,
                tiempo_impresion=self.vars['tiempo_impresion'].get(),
                material=self.vars['material'].get(),
                temperatura_extrusor=self.vars['temperatura_extrusor'].get(),
                temperatura_cama=self.vars['temperatura_cama'].get(),
                guia_impresion=self.guia_text.get('1.0', 'end-1c')
            )

            # Guardar imagen
            if self.imagen_path:
                saved_path = FileUtils.save_product_image(self.imagen_path, producto.nombre)
                if saved_path:
                    producto.imagen_path = saved_path
                else:
                    if not self.show_confirmation("Advertencia",
                                                "No se pudo guardar la imagen. ¿Desea continuar sin imagen?"):
                        return

            # Guardar en base de datos
            producto_id = self.db_manager.crear_producto(producto)

            if producto_id:
                self.producto_creado = True
                self.show_modern_message("Éxito", "Producto creado exitosamente", 'success')
                self.window.after(2000, self.window.destroy)  # Cerrar después de 2 segundos
            else:
                self.show_modern_message("Error", "No se pudo crear el producto", 'error')

        except Exception as e:
            self.show_modern_message("Error", f"Error al guardar producto: {str(e)}", 'error')

    def show_modern_message(self, title, message, msg_type='info'):
        """Mostrar mensaje moderno"""
        msg_window = tk.Toplevel(self.window)
        msg_window.title(title)
        msg_window.geometry("400x200")
        msg_window.transient(self.window)
        msg_window.grab_set()
        msg_window.configure(bg=self.colors['card'])

        colors = {
            'success': ('#10B981', '✅'),
            'error': ('#EF4444', '❌'),
            'info': ('#6366F1', 'ℹ️'),
            'warning': ('#F59E0B', '⚠️')
        }

        color, icon = colors.get(msg_type, colors['info'])

        content = tk.Frame(msg_window, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        tk.Label(content, text=icon, font=('Segoe UI', 32),
                bg=self.colors['card'], fg=color).pack(pady=(0, 15))

        tk.Label(content, text=title, font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack()

        tk.Label(content, text=message, font=self.fonts['body'],
                bg=self.colors['card'], fg=self.colors['text_secondary'],
                wraplength=340, justify=tk.CENTER).pack(pady=(10, 20))

        btn = self.create_modern_button(content, "Aceptar", msg_window.destroy, 'primary')
        btn.pack()

        # Centrar
        msg_window.update_idletasks()
        x = (msg_window.winfo_screenwidth() // 2) - (msg_window.winfo_width() // 2)
        y = (msg_window.winfo_screenheight() // 2) - (msg_window.winfo_height() // 2)
        msg_window.geometry(f'+{x}+{y}')

        if msg_type == 'success':
            msg_window.after(3000, msg_window.destroy)

    def show_confirmation(self, title, message):
        """Mostrar diálogo de confirmación"""
        dialog = tk.Toplevel(self.window)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.configure(bg=self.colors['card'])

        content = tk.Frame(dialog, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        tk.Label(content, text="⚠️", font=('Segoe UI', 32),
                bg=self.colors['card'], fg=self.colors['warning']).pack(pady=(0, 15))

        tk.Label(content, text=title, font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack()

        tk.Label(content, text=message, font=self.fonts['body'],
                bg=self.colors['card'], fg=self.colors['text_secondary'],
                wraplength=340, justify=tk.CENTER).pack(pady=(10, 20))

        btn_frame = tk.Frame(content, bg=self.colors['card'])
        btn_frame.pack()

        result = {'confirmed': False}

        def confirm():
            result['confirmed'] = True
            dialog.destroy()

        btn_cancel = self.create_modern_button(btn_frame, "Cancelar", dialog.destroy, 'secondary')
        btn_cancel.pack(side=tk.LEFT, padx=5)

        btn_confirm = self.create_modern_button(btn_frame, "Continuar", confirm, 'primary')
        btn_confirm.pack(side=tk.LEFT, padx=5)

        # Centrar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

        dialog.wait_window()
        return result['confirmed']

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')