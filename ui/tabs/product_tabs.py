# ui/tabs/product_tabs.py
"""
Pestañas del editor de productos como componentes separados
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from typing import List, Callable
import os
from PIL import Image, ImageTk, ImageDraw

from ui.components.base import ModernFrame, ModernField, ModernButton, ScrollableFrame
from config.styles import ModernTheme
from ui.state.form_state import FormStateManager, ImageStateManager, GuideStateManager
from utils.file_utils import FileUtils
from ui.components.color_widgets.color_specification_widget import ModernColorSpecificationWidget


class BaseTab:
    """Clase base para pestañas"""

    def __init__(self, notebook: ttk.Notebook, title: str, icon: str,
                 theme: ModernTheme, form_state: FormStateManager):
        self.notebook = notebook
        self.title = title
        self.icon = icon
        self.theme = theme
        self.form_state = form_state
        self.tab_frame = None
        self.setup_tab()

    def setup_tab(self):
        """Configurar pestaña base"""
        self.tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_frame, text=f"{self.icon} {self.title}")
        self.create_content()

    def create_content(self):
        """Crear contenido de la pestaña (override en subclases)"""
        pass

    def get_frame(self) -> ttk.Frame:
        """Obtener frame de la pestaña"""
        return self.tab_frame


class BasicInfoTab(BaseTab):
    """Pestaña de información básica"""

    def __init__(self, notebook: ttk.Notebook, theme: ModernTheme,
                 form_state: FormStateManager, image_state: ImageStateManager):
        self.image_state = image_state
        self.image_label = None
        self.image_info = None
        super().__init__(notebook, "Información Básica", "📝", theme, form_state)

    def create_content(self):
        """Crear contenido de información básica"""
        # Frame principal con scroll
        scrollable = ScrollableFrame(self.tab_frame, self.theme)
        scrollable.pack(fill=tk.BOTH, expand=True)

        main_content = scrollable.get_frame()
        main_content.configure(padx=30, pady=20)
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        # Crear tarjetas
        self._create_fields_card(main_content)
        self._create_image_card(main_content)

    def _create_fields_card(self, parent):
        """Crear tarjeta de campos básicos"""
        fields_card = ModernFrame(parent, self.theme, card_style=True)
        fields_card.grid(row=0, column=0, sticky='nsew', padx=(0, 15), pady=(0, 20))

        # Header
        header = tk.Frame(fields_card, bg=self.theme.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(
            header,
            text="📋 Datos del Producto",
            font=self.theme.fonts['subheading'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W)

        # Campos
        content = tk.Frame(fields_card, bg=self.theme.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Definir campos
        fields_config = [
            ('nombre', 'Nombre del Producto *', 'entry', None),
            ('descripcion', 'Descripción', 'entry', None),
            ('material', 'Material *', 'combobox',
             {'values': ['PLA', 'ABS', 'PETG', 'TPU', 'Nylon', 'Resina']}),
            ('peso', 'Peso estimado (gramos)', 'spinbox',
             {'from_': 0, 'to': 10000, 'increment': 0.1}),
            ('tiempo_impresion', 'Tiempo base (minutos)', 'spinbox',
             {'from_': 0, 'to': 10000, 'increment': 1})
        ]

        # Crear campos
        for field_name, label_text, widget_type, options in fields_config:
            variable = self.form_state.get_variable(field_name)
            widget = ModernField.create_field(
                content, field_name, label_text, widget_type,
                variable, self.theme, options
            )
            self.form_state.register_entry(field_name, widget)

    def _create_image_card(self, parent):
        """Crear tarjeta de imagen"""
        image_card = ModernFrame(parent, self.theme, card_style=True)
        image_card.grid(row=0, column=1, sticky='nsew', padx=(15, 0), pady=(0, 20))

        # Header
        header = tk.Frame(image_card, bg=self.theme.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(
            header,
            text="🖼️ Imagen del Producto",
            font=self.theme.fonts['subheading'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W)

        # Estado de imagen
        status_text = "Imagen modificada" if self.image_state.has_changes else "Imagen actual"
        status_color = self.theme.colors['warning'] if self.image_state.has_changes else self.theme.colors[
            'text_secondary']

        tk.Label(
            header,
            text=status_text,
            font=self.theme.fonts['caption'],
            bg=self.theme.colors['card'],
            fg=status_color
        ).pack(anchor=tk.W)

        # Área de imagen
        image_area = tk.Frame(
            image_card,
            bg=self.theme.colors['accent'],
            highlightbackground=self.theme.colors['border'],
            highlightthickness=1
        )
        image_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        self.image_label = tk.Label(
            image_area,
            text="📷\nCargando imagen...",
            font=self.theme.fonts['body'],
            bg=self.theme.colors['accent'],
            fg=self.theme.colors['text_secondary'],
            cursor='hand2'
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=40)
        self.image_label.bind('<Button-1>', lambda e: self._select_image())

        # Botones
        btn_frame = tk.Frame(image_card, bg=self.theme.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        btn_select = ModernButton.create(
            btn_frame, "🔄 Cambiar Imagen", self._select_image, 'secondary', self.theme
        )
        btn_select.pack(fill=tk.X, pady=(0, 10))

        btn_remove = ModernButton.create(
            btn_frame, "🗑️ Quitar Imagen", self._remove_image, 'danger', self.theme
        )
        btn_remove.pack(fill=tk.X)

        # Info de imagen
        self.image_info = tk.Label(
            btn_frame,
            text="",
            font=self.theme.fonts['caption'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text_secondary']
        )
        self.image_info.pack(pady=(10, 0))

        # Mostrar imagen inicial
        self._display_image()

    def _select_image(self):
        """Seleccionar nueva imagen"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen del producto",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp *.webp"),
                ("Todos los archivos", "*.*")
            ]
        )

        if file_path and FileUtils.is_valid_image(file_path):
            self.image_state.set_image_path(file_path)
            self._display_image()
        elif file_path:
            # Mostrar error (necesitaría acceso al MessageDialog)
            pass

    def _remove_image(self):
        """Quitar imagen"""
        self.image_state.remove_image()
        self._display_image()

    def _display_image(self):
        """Mostrar imagen actual"""
        image_path = self.image_state.get_current_path()

        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.thumbnail((250, 250), Image.Resampling.LANCZOS)

                # Crear máscara redondeada
                mask = Image.new('L', img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle([(0, 0), img.size], radius=10, fill=255)

                output = Image.new('RGBA', img.size, (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)

                photo = ImageTk.PhotoImage(output)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo

                # Actualizar info
                size = FileUtils.get_file_size_readable(image_path)
                estado = "Nueva imagen" if self.image_state.has_changes else "Imagen actual"
                self.image_info.configure(
                    text=f"📁 {os.path.basename(image_path)}\n📊 {estado} - {size}"
                )

            except Exception as e:
                self._remove_image()
        else:
            self.image_label.configure(image="", text="📷\nSin imagen")
            self.image_label.image = None
            if self.image_state.has_changes:
                self.image_info.configure(text="Imagen eliminada")
            else:
                self.image_info.configure(text="")


class ColorsTab(BaseTab):
    """Pestaña de colores y piezas"""

    def __init__(self, notebook: ttk.Notebook, theme: ModernTheme,
                 form_state: FormStateManager, producto):
        self.producto = producto
        self.color_specifications = []
        super().__init__(notebook, "Colores y Piezas", "🎨", theme, form_state)

    def create_content(self):
        """Crear contenido de colores"""
        main_content = tk.Frame(self.tab_frame, bg=self.theme.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Header con información
        self._create_header_card(main_content)

        # Área de especificaciones
        self._create_specifications_area(main_content)

    def _create_header_card(self, parent):
        """Crear tarjeta de header"""
        header_card = ModernFrame(parent, self.theme, card_style=True)
        header_card.pack(fill=tk.X, pady=(0, 20))

        header_content = tk.Frame(header_card, bg=self.theme.colors['card'])
        header_content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            header_content,
            text="🎨 Especificaciones de Color por Pieza",
            font=self.theme.fonts['subheading'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W)

        # Comparación con original
        original_colors = len(self.producto.colores_especificaciones)
        comparison_text = f"Original: {original_colors} especificación(es) de color"
        tk.Label(
            header_content,
            text=comparison_text,
            font=self.theme.fonts['caption'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text_secondary']
        ).pack(anchor=tk.W, pady=(5, 0))

    def _create_specifications_area(self, parent):
        """Crear área de especificaciones"""
        spec_card = ModernFrame(parent, self.theme, card_style=True)
        spec_card.pack(fill=tk.BOTH, expand=True)

        # Área scrollable para especificaciones
        scrollable = ScrollableFrame(spec_card, self.theme)
        scrollable.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.colors_frame = scrollable.get_frame()

        # Botón para agregar especificación
        btn_frame = tk.Frame(spec_card, bg=self.theme.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        add_btn = ModernButton.create(
            btn_frame,
            "➕ Agregar Especificación de Color",
            self._add_color_specification,
            'primary',
            self.theme
        )
        add_btn.pack(fill=tk.X)

        # Cargar especificaciones existentes
        self._load_existing_specifications()

    def _add_color_specification(self):
        """Agregar nueva especificación de color"""
        index = len(self.color_specifications)

        # Crear widget de especificación (no filtro)
        color_widget = ModernColorSpecificationWidget(
            self.colors_frame,
            color_spec=None,  # Nueva especificación vacía
            index=index,
            on_delete=self._eliminar_especificacion_color,  # ← Corregir nombre del método
            colors=self.theme.colors,  # ← Usar theme.colors
            fonts=self.theme.fonts  # ← Usar theme.fonts
        )

        color_widget.pack(fill=tk.X, pady=10)
        self.color_specifications.append(color_widget)

    def delate_color_specificacion_widget(self,index):
        """Eliminar especificación de color"""
        if len(self.color_specifications) > 1:
            widget = self.color_specifications[index]
            widget.destroy()
            del self.color_specifications[index]

            # Reindexar los widgets restantes
            for i, widget in enumerate(self.color_specifications):
                widget.index = i
        else:
            # Mostrar mensaje de advertencia
            # Aquí podrías usar tu sistema de notificaciones
            print("Debe mantener al menos una especificación de color")

    def _load_existing_specifications(self):
        """Cargar especificaciones existentes"""
        if self.producto.colores_especificaciones:
            for color_spec in self.producto.colores_especificaciones:
                self._add_color_specification_widget(color_spec)
        else:
            # Agregar una especificación vacía por defecto
            self._add_color_specification_widget()

    def _add_color_specification_widget(self, color_spec=None):
        """Agregar widget de especificación de color"""
        index = len(self.color_specifications)

        color_widget = ModernColorSpecificationWidget(
            self.colors_frame,
            color_spec=color_spec,  # Especificación existente o None para nueva
            index=index,
            on_delete=self._eliminar_especificacion_color,
            colors=self.theme.colors,
            fonts=self.theme.fonts
        )

        color_widget.pack(fill=tk.X, pady=10)
        self.color_specifications.append(color_widget)

    def get_color_specifications(self):
        """Obtener todas las especificaciones de color válidas"""
        specs = []
        for widget in self.color_specifications:
            try:
                widget_specs = widget.get_all_specifications()
                for spec in widget_specs:
                    if hasattr(spec, 'peso_color') and spec.peso_color > 0:
                        specs.append(spec)
            except AttributeError:
                # Si el widget no tiene get_all_specifications, continuar
                continue
        return specs


class ConfigTab(BaseTab):
    """Pestaña de configuración"""

    def create_content(self):
        """Crear contenido de configuración"""
        main_content = tk.Frame(self.tab_frame, bg=self.theme.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        main_content.grid_columnconfigure(0, weight=1)
        main_content.grid_columnconfigure(1, weight=1)

        self._create_print_config_card(main_content)
        self._create_guide_card(main_content)

    def _create_print_config_card(self, parent):
        """Crear tarjeta de configuración de impresión"""
        config_card = ModernFrame(parent, self.theme, card_style=True)
        config_card.grid(row=0, column=0, sticky='nsew', padx=(0, 15))

        # Header
        header = tk.Frame(config_card, bg=self.theme.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(
            header,
            text="🌡️ Configuración de Impresión",
            font=self.theme.fonts['subheading'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W)

        # Campos de temperatura
        content = tk.Frame(config_card, bg=self.theme.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        temp_fields = [
            ('temperatura_extrusor', 'Temperatura del Extrusor (°C)',
             {'from_': 150, 'to': 300, 'increment': 5}),
            ('temperatura_cama', 'Temperatura de la Cama (°C)',
             {'from_': 0, 'to': 120, 'increment': 5})
        ]

        for field_name, label_text, options in temp_fields:
            variable = self.form_state.get_variable(field_name)
            widget = ModernField.create_field(
                content, field_name, label_text, 'spinbox',
                variable, self.theme, options
            )
            self.form_state.register_entry(field_name, widget)

    def _create_guide_card(self, parent):
        """Crear tarjeta de guía"""
        guide_card = ModernFrame(parent, self.theme, card_style=True)
        guide_card.grid(row=0, column=1, sticky='nsew', padx=(15, 0))

        # Header
        header = tk.Frame(guide_card, bg=self.theme.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(
            header,
            text="📖 Guía de Impresión",
            font=self.theme.fonts['subheading'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W)

        # Área de texto para la guía
        self.guide_text = scrolledtext.ScrolledText(
            guide_card,
            wrap=tk.WORD,
            height=15,
            font=self.theme.fonts['body'],
            bg='white',
            fg=self.theme.colors['text'],
            relief=tk.FLAT,
            borderwidth=1,
            selectbackground=self.theme.colors['primary'],
            selectforeground='white'
        )
        self.guide_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    def load_guide_content(self, guide_content: str):
        """Cargar contenido de la guía"""
        self.guide_text.delete('1.0', tk.END)
        self.guide_text.insert('1.0', guide_content or "")

    def get_guide_content(self) -> str:
        """Obtener contenido de la guía"""
        return self.guide_text.get('1.0', 'end-1c')


class HistoryTab(BaseTab):
    """Pestaña de historial"""

    def __init__(self, notebook: ttk.Notebook, theme: ModernTheme,
                 form_state: FormStateManager, producto):
        self.producto = producto
        super().__init__(notebook, "Historial", "📊", theme, form_state)

    def create_content(self):
        """Crear contenido del historial"""
        main_content = tk.Frame(self.tab_frame, bg=self.theme.colors['bg'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Timeline de cambios
        timeline_card = ModernFrame(main_content, self.theme, card_style=True)
        timeline_card.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(timeline_card, bg=self.theme.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 15))

        tk.Label(
            header,
            text="📊 Historial del Producto",
            font=self.theme.fonts['subheading'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W)

        # Contenido del historial
        history_content = tk.Frame(timeline_card, bg=self.theme.colors['card'])
        history_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self._create_timeline_items(history_content)
        self._create_statistics_section(history_content)

    def _create_timeline_items(self, parent):
        """Crear items de timeline"""
        # Información de creación
        if self.producto.fecha_creacion:
            self._create_history_item(
                parent,
                "📝 Producto creado",
                self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
                "El producto fue creado en el sistema",
                self.theme.colors['success']
            )

        # Información de modificación
        if self.producto.fecha_modificacion:
            self._create_history_item(
                parent,
                "✏️ Última modificación",
                self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M'),
                "Se realizaron cambios en el producto",
                self.theme.colors['warning']
            )

    def _create_history_item(self, parent, title: str, date: str,
                             description: str, color: str):
        """Crear item de historial"""
        item_frame = tk.Frame(parent, bg=self.theme.colors['card'])
        item_frame.pack(fill=tk.X, pady=(0, 15))

        # Punto de timeline
        timeline_frame = tk.Frame(item_frame, bg=self.theme.colors['card'])
        timeline_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))

        point = tk.Frame(timeline_frame, bg=color, width=12, height=12)
        point.pack(pady=(5, 0))

        # Contenido
        content_frame = ModernFrame(item_frame, self.theme, card_style=False)
        content_frame.configure(bg=self.theme.colors['accent'])
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        content = tk.Frame(content_frame, bg=self.theme.colors['accent'])
        content.pack(fill=tk.X, padx=15, pady=10)

        # Título y fecha
        header_frame = tk.Frame(content, bg=self.theme.colors['accent'])
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text=title,
            font=self.theme.fonts['body'],
            bg=self.theme.colors['accent'],
            fg=self.theme.colors['text']
        ).pack(side=tk.LEFT)

        tk.Label(
            header_frame,
            text=date,
            font=self.theme.fonts['caption'],
            bg=self.theme.colors['accent'],
            fg=self.theme.colors['text_secondary']
        ).pack(side=tk.RIGHT)

        # Descripción
        tk.Label(
            content,
            text=description,
            font=self.theme.fonts['caption'],
            bg=self.theme.colors['accent'],
            fg=self.theme.colors['text_secondary']
        ).pack(anchor=tk.W, pady=(5, 0))

    def _create_statistics_section(self, parent):
        """Crear sección de estadísticas"""
        stats_frame = ModernFrame(parent, self.theme, card_style=False)
        stats_frame.configure(bg=self.theme.colors['accent'])
        stats_frame.pack(fill=tk.X, pady=(20, 0))

        stats_content = tk.Frame(stats_frame, bg=self.theme.colors['accent'])
        stats_content.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            stats_content,
            text="📈 Estadísticas",
            font=self.theme.fonts['body'],
            bg=self.theme.colors['accent'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W, pady=(0, 10))

        stats_grid = tk.Frame(stats_content, bg=self.theme.colors['accent'])
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

            stat_frame = ModernFrame(stats_grid, self.theme, card_style=True)
            stat_frame.grid(row=row, column=col, sticky='ew', padx=5, pady=5)
            stats_grid.grid_columnconfigure(col, weight=1)

            tk.Label(
                stat_frame,
                text=label,
                font=self.theme.fonts['caption'],
                bg=self.theme.colors['card'],
                fg=self.theme.colors['text_secondary']
            ).pack(padx=10, pady=(8, 2))

            tk.Label(
                stat_frame,
                text=value,
                font=self.theme.fonts['body'],
                bg=self.theme.colors['card'],
                fg=self.theme.colors['text']
            ).pack(padx=10, pady=(0, 8))