"""
Ventana para editar producto existente - Versión Modernizada
"""

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
import os
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime

from database.db_manager import DatabaseManager
from models.producto import Producto
from ui.color_widgets import ModernColorFilterWidget
from utils.file_utils import FileUtils


class ModernEditProductWindow:
    """Ventana modernizada para editar un producto existente"""

    def __init__(self, parent, db_manager: DatabaseManager, producto: Producto):
        self.parent = parent
        self.db_manager = db_manager
        self.producto = producto
        self.producto_actualizado = False
        self.imagen_path = producto.imagen_path
        self.nueva_imagen = False
        self.color_specifications = []
        self.cambios_detectados = []

        # Configurar colores y estilos modernos
        self.setup_modern_colors()

        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title(f"Editar Producto - {producto.nombre}")
        self.window.geometry("1100x900")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(bg=self.colors['bg'])

        # Variables
        self.crear_variables()

        # Configurar estilos
        self.setup_modern_styles()

        # Crear interfaz
        self.create_modern_widgets()

        # Cargar datos
        self.cargar_datos_producto()

        # Centrar ventana
        self.center_window()

        # Configurar detección de cambios
        self.setup_change_detection()

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
            'input_bg': '#FFFFFF',
            'modified': '#FEF3C7'  # Color para campos modificados
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

        # Estilos para notebook
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

        # Estilos para entry
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'],
                       font=self.fonts['body'])

        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.colors['primary'])])

        # Estilo especial para campos modificados
        style.configure('Modified.TEntry',
                       fieldbackground=self.colors['modified'],
                       borderwidth=2,
                       relief='flat',
                       bordercolor=self.colors['warning'],
                       font=self.fonts['body'])

        # Estilos para combobox
        style.configure('Modern.TCombobox',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'],
                       font=self.fonts['body'])

        # Estilos para spinbox
        style.configure('Modern.TSpinbox',
                       fieldbackground=self.colors['input_bg'],
                       borderwidth=1,
                       relief='flat',
                       bordercolor=self.colors['border'],
                       font=self.fonts['body'])

    def crear_variables(self):
        """Crear variables para los campos"""
        self.vars = {
            'nombre': tk.StringVar(value=self.producto.nombre),
            'descripcion': tk.StringVar(value=self.producto.descripcion or ""),
            'peso': tk.DoubleVar(value=self.producto.peso),
            'tiempo_impresion': tk.IntVar(value=self.producto.tiempo_impresion),
            'material': tk.StringVar(value=self.producto.material),
            'temperatura_extrusor': tk.IntVar(value=self.producto.temperatura_extrusor),
            'temperatura_cama': tk.IntVar(value=self.producto.temperatura_cama)
        }
        self.entries = {}
        self.original_values = {k: v.get() for k, v in self.vars.items()}

    def setup_change_detection(self):
        """Configurar detección de cambios"""
        for var_name, var in self.vars.items():
            var.trace('w', lambda *args, vn=var_name: self.on_field_change(vn))

    def on_field_change(self, var_name):
        """Manejar cambio en un campo"""
        current_value = self.vars[var_name].get()
        original_value = self.original_values[var_name]

        if current_value != original_value:
            if var_name not in self.cambios_detectados:
                self.cambios_detectados.append(var_name)
            # Cambiar estilo del campo
            if var_name in self.entries:
                self.entries[var_name].configure(style='Modified.TEntry')
        else:
            if var_name in self.cambios_detectados:
                self.cambios_detectados.remove(var_name)
            # Restaurar estilo normal
            if var_name in self.entries:
                self.entries[var_name].configure(style='Modern.TEntry')

        self.update_status_badge()
        if len(self.cambios_detectados) > 0:
            self.show_changes_panel()
        else:
            self.hide_changes_panel()

    def update_status_badge(self):
        """Actualizar badge de estado"""
        if len(self.cambios_detectados) > 0 or self.nueva_imagen:
            color = self.colors['warning']
            text = f"{len(self.cambios_detectados)} cambio(s)"
            icon = "⚠️"
        else:
            color = self.colors['success']
            text = "Sin cambios"
            icon = "✅"

        self.status_badge.configure(bg=color)
        for child in self.status_badge.winfo_children():
            child.configure(bg=color)
            for subchild in child.winfo_children():
                subchild.configure(bg=color)

        self.status_label.configure(text=text)

    def create_modern_widgets(self):
        """Crear interfaz moderna"""
        # Frame principal
        main_container = tk.Frame(self.window, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header moderno
        self.create_modern_header(main_container)

        # Panel de cambios (si hay cambios)
        self.changes_panel = self.create_changes_panel(main_container)

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
        self.create_history_tab()

        # Botones de acción
        self.create_action_buttons(main_container)

    def create_modern_header(self, parent):
        """Crear header moderno"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Icono y título
        icon_label = tk.Label(header_content, text="✏️", font=('Segoe UI', 32),
                             bg=self.colors['primary'], fg='white')
        icon_label.pack(side=tk.LEFT, padx=(0, 20))

        title_info = tk.Frame(header_content, bg=self.colors['primary'])
        title_info.pack(side=tk.LEFT, fill=tk.Y)

        title_label = tk.Label(title_info, text=f"Editando: {self.producto.nombre}",
                              font=self.fonts['title'],
                              bg=self.colors['primary'], fg='white')
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_info, text=f"ID: {self.producto.id} • Modificar información del producto",
                                 font=self.fonts['body'],
                                 bg=self.colors['primary'], fg='white')
        subtitle_label.pack(anchor=tk.W)

        # Información de fechas
        dates_info = tk.Frame(title_info, bg=self.colors['primary'])
        dates_info.pack(anchor=tk.W, pady=(5, 0))

        if self.producto.fecha_creacion:
            tk.Label(dates_info,
                    text=f"Creado: {self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M')}",
                    font=self.fonts['caption'],
                    bg=self.colors['primary'], fg='white').pack(side=tk.LEFT, padx=(0, 15))

        if self.producto.fecha_modificacion:
            tk.Label(dates_info,
                    text=f"Última modificación: {self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M')}",
                    font=self.fonts['caption'],
                    bg=self.colors['primary'], fg='white').pack(side=tk.LEFT)

        # Badge de estado
        status_frame = tk.Frame(header_content, bg=self.colors['primary'])
        status_frame.pack(side=tk.RIGHT)

        self.create_status_badge(status_frame, "Sin cambios", "💾", self.colors['success'])

    def create_status_badge(self, parent, text, icon, color):
        """Crear badge de estado"""
        self.status_badge = tk.Frame(parent, bg=color, highlightthickness=0)
        self.status_badge.pack()

        content = tk.Frame(self.status_badge, bg=color)
        content.pack(padx=15, pady=8)

        tk.Label(content, text=icon, font=self.fonts['body'],
                bg=color, fg='white').pack(side=tk.LEFT, padx=(0, 8))
        self.status_label = tk.Label(content, text=text, font=self.fonts['small'],
                                    bg=color, fg='white')
        self.status_label.pack(side=tk.LEFT)

    def create_changes_panel(self, parent):
        """Crear panel de cambios"""
        changes_frame = tk.Frame(parent, bg=self.colors['warning'], height=40)
        # Inicialmente oculto
        return changes_frame

    def show_changes_panel(self):
        """Mostrar panel de cambios"""
        if len(self.cambios_detectados) > 0:
            self.changes_panel.pack(fill=tk.X, pady=(20, 0))

            # Limpiar contenido anterior
            for widget in self.changes_panel.winfo_children():
                widget.destroy()

            content = tk.Frame(self.changes_panel, bg=self.colors['warning'])
            content.pack(fill=tk.X, padx=20, pady=10)

            tk.Label(content, text="⚠️", font=self.fonts['body'],
                    bg=self.colors['warning'], fg='white').pack(side=tk.LEFT, padx=(0, 10))

            changes_text = f"Campos modificados: {', '.join(self.cambios_detectados)}"
            tk.Label(content, text=changes_text, font=self.fonts['small'],
                    bg=self.colors['warning'], fg='white').pack(side=tk.LEFT)

            # Botón para deshacer cambios
            tk.Button(content, text="Deshacer", font=self.fonts['caption'],
                     bg='white', fg=self.colors['warning'],
                     bd=0, padx=10, pady=2,
                     command=self.deshacer_cambios).pack(side=tk.RIGHT)

    def hide_changes_panel(self):
        """Ocultar panel de cambios"""
        self.changes_panel.pack_forget()

    def deshacer_cambios(self):
        """Deshacer todos los cambios"""
        for var_name, original_value in self.original_values.items():
            self.vars[var_name].set(original_value)

        self.cambios_detectados.clear()
        self.hide_changes_panel()
        self.update_status_badge()

    def create_basic_info_tab(self):
        """Crear pestaña de información básica"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="📝 Información Básica")

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

        main_content = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        self.create_basic_fields_card(main_content)
        self.create_image_card(main_content)

    def create_basic_fields_card(self, parent):
        """Crear tarjeta de campos básicos"""
        fields_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        fields_card.grid(row=0, column=0, sticky='nsew', padx=(0, 15), pady=(0, 20))

        header = tk.Frame(fields_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="📋 Datos del Producto",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        content = tk.Frame(fields_card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

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

        label = tk.Label(field_frame, text=label_text,
                        font=self.fonts['body'],
                        bg=self.colors['card'], fg=self.colors['text'])
        label.pack(anchor=tk.W, pady=(0, 8))

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

    def create_image_card(self, parent):
        """Crear tarjeta de imagen"""
        image_card = tk.Frame(parent, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        image_card.grid(row=0, column=1, sticky='nsew', padx=(15, 0), pady=(0, 20))

        header = tk.Frame(image_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="🖼️ Imagen del Producto",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Mostrar estado de imagen
        if self.nueva_imagen:
            status_color = self.colors['warning']
            status_text = "Imagen modificada"
        else:
            status_color = self.colors['text_secondary']
            status_text = "Imagen actual"

        tk.Label(header, text=status_text,
                font=self.fonts['caption'],
                bg=self.colors['card'], fg=status_color).pack(anchor=tk.W)

        image_area = tk.Frame(image_card, bg=self.colors['accent'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        image_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        self.image_label = tk.Label(image_area, text="📷\nCargando imagen...",
                                   font=self.fonts['body'],
                                   bg=self.colors['accent'], fg=self.colors['text_secondary'],
                                   cursor='hand2')
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=40)
        self.image_label.bind('<Button-1>', lambda e: self.seleccionar_imagen())

        btn_frame = tk.Frame(image_card, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        btn_select = self.create_modern_button(btn_frame, "🔄 Cambiar Imagen",
                                              self.seleccionar_imagen, 'secondary')
        btn_select.pack(fill=tk.X, pady=(0, 10))

        btn_remove = self.create_modern_button(btn_frame, "🗑️ Quitar Imagen",
                                              self.quitar_imagen, 'danger')
        btn_remove.pack(fill=tk.X)

        self.image_info = tk.Label(btn_frame, text="",
                                  font=self.fonts['caption'],
                                  bg=self.colors['card'], fg=self.colors['text_secondary'])
        self.image_info.pack(pady=(10, 0))

    def create_colors_tab(self):
        """Crear pestaña de colores"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="🎨 Colores y Piezas")

        main_content = tk.Frame(tab_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        header_card = tk.Frame(main_content, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        header_card.pack(fill=tk.X, pady=(0, 20))

        header_content = tk.Frame(header_card, bg=self.colors['card'])
        header_content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(header_content, text="🎨 Especificaciones de Color por Pieza",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Comparación con original
        original_colors = len(self.producto.colores_especificaciones)
        comparison_text = f"Original: {original_colors} especificación(es) de color"
        tk.Label(header_content, text=comparison_text,
                font=self.fonts['caption'],
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor=tk.W, pady=(5, 0))

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

        self.colors_frame = tk.Frame(scrollable_frame, bg=self.colors['card'])
        self.colors_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        btn_frame = tk.Frame(scrollable_frame, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        add_btn = self.create_modern_button(btn_frame, "➕ Agregar Especificación de Color",
                                           self.agregar_especificacion_color, 'primary')
        add_btn.pack(fill=tk.X)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_config_tab(self):
        """Crear pestaña de configuración"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="⚙️ Configuración")

        main_content = tk.Frame(tab_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        self.create_print_config_card(main_content)
        self.create_guide_card(main_content)

    def create_print_config_card(self, parent):
        """Crear tarjeta de configuración de impresión"""
        config_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        config_card.grid(row=0, column=0, sticky='nsew', padx=(0, 15))

        header = tk.Frame(config_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="🌡️ Configuración de Impresión",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        content = tk.Frame(config_card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

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

    def create_guide_card(self, parent):
        """Crear tarjeta de guía"""
        guide_card = tk.Frame(parent, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        guide_card.grid(row=0, column=1, sticky='nsew', padx=(15, 0))

        header = tk.Frame(guide_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="📖 Guía de Impresión",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        self.guia_text = scrolledtext.ScrolledText(
            guide_card, wrap=tk.WORD, height=15,
            font=self.fonts['body'],
            bg='white', fg=self.colors['text'],
            relief=tk.FLAT, borderwidth=1,
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        self.guia_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Detectar cambios en la guía
        self.original_guide = ""
        self.guia_text.bind('<KeyRelease>', self.on_guide_change)

    def create_history_tab(self):
        """Crear pestaña de historial"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="📊 Historial")

        main_content = tk.Frame(tab_frame, bg=self.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Timeline de cambios
        timeline_card = tk.Frame(main_content, bg=self.colors['card'],
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        timeline_card.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(timeline_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(header, text="📊 Historial del Producto",
                font=self.fonts['subheading'],
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W)

        # Contenido del historial
        history_content = tk.Frame(timeline_card, bg=self.colors['card'])
        history_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Información de creación
        if self.producto.fecha_creacion:
            self.create_history_item(
                history_content,
                "📝 Producto creado",
                self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
                "El producto fue creado en el sistema",
                self.colors['success']
            )

        # Información de modificación
        if self.producto.fecha_modificacion:
            self.create_history_item(
                history_content,
                "✏️ Última modificación",
                self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M'),
                "Se realizaron cambios en el producto",
                self.colors['warning']
            )

        # Estadísticas del producto
        stats_frame = tk.Frame(history_content, bg=self.colors['accent'])
        stats_frame.pack(fill=tk.X, pady=(20, 0))

        stats_content = tk.Frame(stats_frame, bg=self.colors['accent'])
        stats_content.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(stats_content, text="📈 Estadísticas",
                font=self.fonts['body'],
                bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        stats_grid = tk.Frame(stats_content, bg=self.colors['accent'])
        stats_grid.pack(fill=tk.X)

        stats_data = [
            ("Especificaciones de color", str(len(self.producto.colores_especificaciones))),
            ("Peso total", f"{self.producto.peso}g"),
            ("Tiempo total estimado", f"{self.producto.tiempo_impresion} min"),
            ("Material", self.producto.material)
        ]

        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = i % 2

            stat_frame = tk.Frame(stats_grid, bg=self.colors['card'])
            stat_frame.grid(row=row, column=col, sticky='ew', padx=5, pady=5)
            stats_grid.grid_columnconfigure(col, weight=1)

            tk.Label(stat_frame, text=label,
                    font=self.fonts['caption'],
                    bg=self.colors['card'], fg=self.colors['text_secondary']).pack(padx=10, pady=(8, 2))

            tk.Label(stat_frame, text=value,
                    font=self.fonts['body'],
                    bg=self.colors['card'], fg=self.colors['text']).pack(padx=10, pady=(0, 8))

    def create_history_item(self, parent, title, date, description, color):
        """Crear item de historial"""
        item_frame = tk.Frame(parent, bg=self.colors['card'])
        item_frame.pack(fill=tk.X, pady=(0, 15))

        # Línea de tiempo
        timeline_frame = tk.Frame(item_frame, bg=self.colors['card'])
        timeline_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        # Punto de la línea de tiempo
        point = tk.Frame(timeline_frame, bg=color, width=12, height=12)
        point.pack(pady=(5, 0))

        # Contenido
        content_frame = tk.Frame(item_frame, bg=self.colors['accent'])
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        content = tk.Frame(content_frame, bg=self.colors['accent'])
        content.pack(fill=tk.X, padx=15, pady=10)

        # Título y fecha
        header_frame = tk.Frame(content, bg=self.colors['accent'])
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text=title,
                font=self.fonts['body'],
                bg=self.colors['accent'], fg=self.colors['text']).pack(side=tk.LEFT)

        tk.Label(header_frame, text=date,
                font=self.fonts['caption'],
                bg=self.colors['accent'], fg=self.colors['text_secondary']).pack(side=tk.RIGHT)

        # Descripción
        tk.Label(content, text=description,
                font=self.fonts['caption'],
                bg=self.colors['accent'], fg=self.colors['text_secondary']).pack(anchor=tk.W, pady=(5, 0))

    def create_action_buttons(self, parent):
        """Crear botones de acción"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X)

        # Botón cancelar
        btn_cancel = self.create_modern_button(btn_frame, "❌ Cancelar",
                                              self.cancelar, 'secondary')
        btn_cancel.pack(side=tk.RIGHT, padx=(10, 0))

        # Botón guardar cambios
        self.btn_save = self.create_modern_button(btn_frame, "💾 Guardar Cambios",
                                                 self.guardar_cambios, 'primary')
        self.btn_save.pack(side=tk.RIGHT, padx=(10, 0))

        # Botón restablecer
        btn_reset = self.create_modern_button(btn_frame, "🔄 Restablecer",
                                             self.cargar_datos_producto, 'secondary')
        btn_reset.pack(side=tk.RIGHT, padx=(10, 0))

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

    def cargar_datos_producto(self):
        """Cargar datos del producto"""
        # Cargar guía
        self.guia_text.delete('1.0', tk.END)
        self.guia_text.insert('1.0', self.producto.guia_impresion or "")
        self.original_guide = self.guia_text.get('1.0', 'end-1c')

        # Cargar imagen
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            self.imagen_path = self.producto.imagen_path
            self.mostrar_imagen_preview()
        else:
            self.imagen_path = None
            self.image_label.configure(image="", text="📷\nSin imagen")
            self.image_label.image = None

        # Cargar especificaciones de color
        self.cargar_especificaciones_color()

        # Resetear cambios
        self.cambios_detectados.clear()
        self.nueva_imagen = False
        self.hide_changes_panel()
        self.update_status_badge()

    def cargar_especificaciones_color(self):
        """Cargar especificaciones de color"""
        for widget in self.color_specifications:
            widget.destroy()
        self.color_specifications.clear()

        if self.producto.colores_especificaciones:
            for i, color_spec in enumerate(self.producto.colores_especificaciones):
                self.agregar_especificacion_color(color_spec)
        else:
            self.agregar_especificacion_color()

    def agregar_especificacion_color(self, color_spec=None):
        """Agregar especificación de color"""
        index = len(self.color_specifications)

        color_widget = ModernColorFilterWidget(
            self.colors_frame,
            color_spec=color_spec,
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

            for i, widget in enumerate(self.color_specifications):
                widget.index = i
                widget.configure(text=f"Color {i + 1}")
        else:
            self.show_modern_message("Advertencia",
                                   "Debe mantener al menos una especificación de color",
                                   'warning')

    def seleccionar_imagen(self):
        """Seleccionar nueva imagen"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen del producto",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("Todos los archivos", "*.*")
            ]
        )

        if file_path and FileUtils.is_valid_image(file_path):
            self.imagen_path = file_path
            self.nueva_imagen = True
            self.mostrar_imagen_preview()
            self.update_status_badge()
            self.show_changes_panel()
        elif file_path:
            self.show_modern_message("Error",
                                   "El archivo seleccionado no es una imagen válida",
                                   'error')

    def mostrar_imagen_preview(self):
        """Mostrar vista previa de imagen"""
        if self.imagen_path and os.path.exists(self.imagen_path):
            try:
                img = Image.open(self.imagen_path)
                img.thumbnail((250, 250), Image.Resampling.LANCZOS)

                mask = Image.new('L', img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle([(0, 0), img.size], radius=10, fill=255)

                output = Image.new('RGBA', img.size, (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)

                photo = ImageTk.PhotoImage(output)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo

                size = FileUtils.get_file_size_readable(self.imagen_path)
                estado = "Nueva imagen" if self.nueva_imagen else "Imagen actual"
                self.image_info.configure(text=f"📁 {os.path.basename(self.imagen_path)}\n📊 {estado} - {size}")

            except Exception as e:
                self.show_modern_message("Error", f"Error al cargar imagen: {str(e)}", 'error')
                self.quitar_imagen()

    def quitar_imagen(self):
        """Quitar imagen"""
        self.imagen_path = None
        self.nueva_imagen = True
        self.image_label.configure(image="", text="📷\nSin imagen")
        self.image_label.image = None
        self.image_info.configure(text="Imagen eliminada")
        self.update_status_badge()

    def on_guide_change(self, event=None):
        """Detectar cambios en la guía"""
        current_guide = self.guia_text.get('1.0', 'end-1c')
        if current_guide != self.original_guide:
            if 'guia' not in self.cambios_detectados:
                self.cambios_detectados.append('guia')
        else:
            if 'guia' in self.cambios_detectados:
                self.cambios_detectados.remove('guia')

        self.update_status_badge()
        if len(self.cambios_detectados) > 0:
            self.show_changes_panel()
        else:
            self.hide_changes_panel()

    def detectar_cambios_completos(self):
        """Detectar todos los cambios realizados"""
        cambios = []

        # Cambios en campos básicos
        for field_name, original_value in self.original_values.items():
            current_value = self.vars[field_name].get()
            if current_value != original_value:
                field_labels = {
                    'nombre': 'Nombre',
                    'descripcion': 'Descripción',
                    'peso': 'Peso',
                    'tiempo_impresion': 'Tiempo de impresión',
                    'material': 'Material',
                    'temperatura_extrusor': 'Temperatura extrusor',
                    'temperatura_cama': 'Temperatura cama'
                }
                cambios.append(field_labels.get(field_name, field_name))

        # Cambios en guía
        current_guide = self.guia_text.get('1.0', 'end-1c')
        if current_guide != self.original_guide:
            cambios.append('Guía de impresión')

        # Cambios en imagen
        if self.nueva_imagen:
            cambios.append('Imagen')

        # Cambios en especificaciones de color (simplificado)
        current_specs = len(self.color_specifications)
        original_specs = len(self.producto.colores_especificaciones)
        if current_specs != original_specs:
            cambios.append('Especificaciones de color')

        return cambios

    def mostrar_vista_previa(self):
        """Mostrar vista previa de cambios"""
        cambios = self.detectar_cambios_completos()

        preview_window = tk.Toplevel(self.window)
        preview_window.title("Vista Previa de Cambios")
        preview_window.geometry("600x500")
        preview_window.transient(self.window)
        preview_window.configure(bg=self.colors['bg'])

        content = tk.Frame(preview_window, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(content, text=f"👁️ Vista Previa: {self.vars['nombre'].get()}",
                font=self.fonts['title'],
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=(20, 15))

        if cambios:
            tk.Label(content, text=f"Cambios detectados ({len(cambios)}):",
                    font=self.fonts['subheading'],
                    bg=self.colors['card'], fg=self.colors['warning']).pack(anchor=tk.W, pady=(0, 10))

            for cambio in cambios:
                tk.Label(content, text=f"• {cambio}",
                        font=self.fonts['body'],
                        bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, padx=(20, 0))
        else:
            tk.Label(content, text="✅ No hay cambios detectados",
                    font=self.fonts['body'],
                    bg=self.colors['card'], fg=self.colors['success']).pack(pady=20)

        # Información actual
        info_frame = tk.Frame(content, bg=self.colors['accent'])
        info_frame.pack(fill=tk.X, pady=(20, 0))

        info_content = tk.Frame(info_frame, bg=self.colors['accent'])
        info_content.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(info_content, text="📋 Información actual:",
                font=self.fonts['body'],
                bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        current_info = f"""Material: {self.vars['material'].get()}
Peso: {self.vars['peso'].get():.1f}g
Tiempo: {self.vars['tiempo_impresion'].get()} min
Temp. Extrusor: {self.vars['temperatura_extrusor'].get()}°C
Temp. Cama: {self.vars['temperatura_cama'].get()}°C
Especificaciones: {len(self.color_specifications)}"""

        tk.Label(info_content, text=current_info,
                font=self.fonts['small'],
                bg=self.colors['accent'], fg=self.colors['text'],
                justify=tk.LEFT).pack(anchor=tk.W)

        btn_close = self.create_modern_button(content, "Cerrar", preview_window.destroy, 'primary')
        btn_close.pack(pady=20)

    def validar_campos(self):
        """Validar campos"""
        if not self.vars['nombre'].get().strip():
            self.show_modern_message("Error", "El nombre del producto es requerido", 'error')
            return False

        try:
            peso = self.vars['peso'].get()
            if peso < 0:
                self.show_modern_message("Error", "El peso no puede ser negativo", 'error')
                return False
        except:
            self.show_modern_message("Error", "El peso debe ser un número válido", 'error')
            return False

        return True

    def guardar_cambios(self):
        """Guardar cambios del producto"""
        if not self.validar_campos():
            return

        cambios = self.detectar_cambios_completos()

        if not cambios:
            self.show_modern_message("Sin cambios", "No se detectaron cambios en el producto", 'info')
            return

        # Confirmar cambios
        if not self.show_confirmation("Confirmar cambios",
                                    f"Se detectaron {len(cambios)} cambio(s):\n\n" +
                                    "\n".join(f"• {c}" for c in cambios[:5]) +
                                    ("\n..." if len(cambios) > 5 else "") +
                                    "\n\n¿Desea guardar los cambios?"):
            return

        try:
            # Actualizar producto
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
                                       "Debe mantener al menos una pieza con peso mayor a 0",
                                       'error')
                return

            # Actualizar datos
            self.producto.nombre = self.vars['nombre'].get().strip()
            self.producto.descripcion = self.vars['descripcion'].get().strip()
            self.producto.peso = peso_total
            self.producto.colores_especificaciones = color_specs
            self.producto.tiempo_impresion = self.vars['tiempo_impresion'].get()
            self.producto.material = self.vars['material'].get()
            self.producto.temperatura_extrusor = self.vars['temperatura_extrusor'].get()
            self.producto.temperatura_cama = self.vars['temperatura_cama'].get()
            self.producto.guia_impresion = self.guia_text.get('1.0', 'end-1c')
            self.producto.fecha_modificacion = datetime.now()

            # Manejar imagen
            if self.nueva_imagen:
                if self.producto.imagen_path:
                    FileUtils.delete_product_image(self.producto.imagen_path)

                if self.imagen_path:
                    saved_path = FileUtils.save_product_image(self.imagen_path, self.producto.nombre)
                    if saved_path:
                        self.producto.imagen_path = saved_path
                    else:
                        if not self.show_confirmation("Advertencia",
                                                    "No se pudo guardar la imagen. ¿Continuar?"):
                            return
                else:
                    self.producto.imagen_path = None

            # Guardar en BD
            if self.db_manager.actualizar_producto(self.producto):
                self.producto_actualizado = True
                self.show_modern_message("Éxito", "Producto actualizado exitosamente", 'success')
                self.window.after(2000, self.window.destroy)
            else:
                self.show_modern_message("Error", "No se pudo actualizar el producto", 'error')

        except Exception as e:
            self.show_modern_message("Error", f"Error al guardar cambios: {str(e)}", 'error')

    def cancelar(self):
        """Cancelar edición"""
        cambios = self.detectar_cambios_completos()
        if cambios:
            if self.show_confirmation("Confirmar",
                                    f"Hay {len(cambios)} cambio(s) sin guardar.\n¿Está seguro de cancelar?"):
                self.window.destroy()
        else:
            self.window.destroy()

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
        dialog.geometry("450x250")
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
                wraplength=380, justify=tk.CENTER).pack(pady=(10, 20))

        btn_frame = tk.Frame(content, bg=self.colors['card'])
        btn_frame.pack()

        result = {'confirmed': False}

        def confirm():
            result['confirmed'] = True
            dialog.destroy()

        btn_cancel = self.create_modern_button(btn_frame, "Cancelar", dialog.destroy, 'secondary')
        btn_cancel.pack(side=tk.LEFT, padx=5)

        btn_confirm = self.create_modern_button(btn_frame, "Confirmar", confirm, 'primary')
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