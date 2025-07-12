"""
Ventana de edición de productos - VERSIÓN COMPLETA MODERNIZADA
Código completo sin errores y con todos los estilos aplicados
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
import os
from PIL import Image, ImageTk

from database.db_manager import DatabaseManager
from models.producto import Producto


class ModernEditProductWindow:
    """Ventana de edición de productos con diseño moderno y mejorado"""

    def __init__(self, parent, db_manager: DatabaseManager, producto: Producto):
        self.parent = parent
        self.db_manager = db_manager
        self.producto = producto
        self.producto_actualizado = False

        # Sistema de estilos moderno
        self._setup_theme()

        # Variables del formulario
        self._init_variables()

        # Configurar ventana
        self._setup_window()

        # Crear interfaz
        self._create_interface()

        # Cargar datos
        self._load_product_data()

        # Aplicar estilos TTK
        self._setup_ttk_styles()

        # Centrar ventana
        self._center_window()

    def _setup_theme(self):
        """Configurar tema y colores"""
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
            'modified': '#FEF3C7'
        }

        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8)
        }

    def _init_variables(self):
        """Inicializar variables del formulario"""
        self.vars = {
            'nombre': tk.StringVar(value=self.producto.nombre),
            'descripcion': tk.StringVar(value=self.producto.descripcion or ""),
            'peso': tk.DoubleVar(value=self.producto.peso or 0.0),
            'tiempo_impresion': tk.IntVar(value=self.producto.tiempo_impresion or 0),
            'material': tk.StringVar(value=self.producto.material or "PLA"),
            'temperatura_extrusor': tk.IntVar(value=self.producto.temperatura_extrusor or 200),
            'temperatura_cama': tk.IntVar(value=self.producto.temperatura_cama or 60)
        }

        # Variables adicionales
        self.imagen_path = tk.StringVar(value=self.producto.imagen_path or "")
        self.guia_text = None
        self.image_label = None

    def _setup_window(self):
        """Configurar ventana principal con estilo moderno"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Editar Producto - {self.producto.nombre}")
        self.window.geometry("1200x850")
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.configure(bg=self.colors['bg'])

        # Configurar resizing con límites mínimos
        self.window.minsize(900, 700)
        self.window.resizable(True, True)

        # Protocolo de cierre
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_interface(self):
        """Crear interfaz principal modernizada"""
        # Container principal con diseño moderno
        main_container = tk.Frame(self.window, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Header modernizado
        self._create_modern_header(main_container)

        # Content area con mejoras visuales
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(25, 0))

        # Notebook moderno para pestañas
        self._create_modern_notebook(content_frame)

        # Buttons frame modernizado
        self._create_modern_buttons(main_container)

    def _create_modern_header(self, parent):
        """Crear header moderno con gradiente visual"""
        # Header card con elevación
        header_card = tk.Frame(parent, bg=self.colors['primary'], height=100)
        header_card.pack(fill=tk.X)
        header_card.pack_propagate(False)

        # Contenido del header con padding
        header_content = tk.Frame(header_card, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=35, pady=25)

        # Icon y título mejorados
        info_frame = tk.Frame(header_content, bg=self.colors['primary'])
        info_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Icono más grande y llamativo
        icon_label = tk.Label(info_frame, text="✏️", font=('Segoe UI', 32),
                              bg=self.colors['primary'], fg='white')
        icon_label.pack(side=tk.LEFT, padx=(0, 20))

        # Títulos con jerarquía visual
        title_container = tk.Frame(info_frame, bg=self.colors['primary'])
        title_container.pack(side=tk.LEFT)

        title_label = tk.Label(title_container, text="Editar Producto",
                               font=self.fonts['title'],
                               bg=self.colors['primary'], fg='white')
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_container,
                                  text=f"Modificando: {self.producto.nombre}",
                                  font=self.fonts['subheading'],
                                  bg=self.colors['primary'], fg='#E0E7FF')
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))

        # Badge de estado
        status_frame = tk.Frame(header_content, bg=self.colors['primary'])
        status_frame.pack(side=tk.RIGHT, padx=(0, 20))

        status_badge = tk.Label(status_frame, text="● Editando",
                                font=self.fonts['small'],
                                bg=self.colors['success'], fg='white',
                                padx=12, pady=6)
        status_badge.pack()

    def _create_modern_notebook(self, parent):
        """Crear notebook con estilos modernos"""
        # Container para el notebook con shadow effect
        notebook_container = tk.Frame(parent, bg=self.colors['bg'])
        notebook_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Shadow frame para efecto de elevación
        shadow_frame = tk.Frame(notebook_container, bg=self.colors['border'], height=2)
        shadow_frame.pack(fill=tk.X, pady=(2, 0))

        # Notebook principal
        self.notebook = ttk.Notebook(notebook_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestañas con iconos mejorados
        self._create_enhanced_basic_tab()
        self._create_enhanced_config_tab()
        self._create_enhanced_image_tab()

    def _create_enhanced_basic_tab(self):
        """Crear pestaña básica mejorada"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="📋 Información Básica")

        # Scroll container modernizado
        canvas = tk.Canvas(basic_frame, bg=self.colors['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)

        # Contenido con spacing mejorado
        content = tk.Frame(scrollable_frame, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Campos del formulario modernizados
        self._create_enhanced_form_fields(content)

    def _create_enhanced_form_fields(self, parent):
        """Crear campos del formulario con estilo moderno"""

        # Sección: Información Principal
        self._create_section_header(parent, "📝 Información Principal")

        # Nombre - Campo destacado
        name_card = self._create_field_card(parent)
        self._create_modern_field(name_card, "Nombre del Producto",
                                  self.vars['nombre'], required=True)

        # Descripción
        desc_card = self._create_field_card(parent)
        self._create_modern_field(desc_card, "Descripción",
                                  self.vars['descripcion'])

        # Sección: Especificaciones
        self._create_section_header(parent, "📊 Especificaciones")

        # Grid de campos numéricos modernizado
        specs_grid = tk.Frame(parent, bg=self.colors['card'])
        specs_grid.pack(fill=tk.X, pady=(0, 30))

        # Peso
        peso_card = tk.Frame(specs_grid, bg=self.colors['card'])
        peso_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        self._create_modern_field(peso_card, "Peso (gramos)",
                                  self.vars['peso'], field_type="number")

        # Tiempo
        tiempo_card = tk.Frame(specs_grid, bg=self.colors['card'])
        tiempo_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))
        self._create_modern_field(tiempo_card, "Tiempo de Impresión (min)",
                                  self.vars['tiempo_impresion'], field_type="number")

    def _create_section_header(self, parent, title):
        """Crear header de sección moderno"""
        section_frame = tk.Frame(parent, bg=self.colors['card'])
        section_frame.pack(fill=tk.X, pady=(25, 15))

        # Línea decorativa
        line_frame = tk.Frame(section_frame, bg=self.colors['border'], height=1)
        line_frame.pack(fill=tk.X, pady=(0, 10))

        # Título de sección
        title_label = tk.Label(section_frame, text=title,
                               font=self.fonts['heading'],
                               bg=self.colors['card'],
                               fg=self.colors['primary'])
        title_label.pack(anchor=tk.W)

    def _create_field_card(self, parent):
        """Crear card contenedor para campo"""
        card = tk.Frame(parent, bg=self.colors['input_bg'],
                        highlightbackground=self.colors['border'],
                        highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 20))
        return card

    def _create_modern_field(self, parent, label_text, variable, required=False, field_type="text"):
        """Crear campo moderno con label y entrada"""
        container = tk.Frame(parent, bg=self.colors['input_bg'])
        container.pack(fill=tk.X, padx=20, pady=15)

        # Label con indicador requerido
        label_frame = tk.Frame(container, bg=self.colors['input_bg'])
        label_frame.pack(fill=tk.X, pady=(0, 8))

        label_text_final = f"{label_text} *" if required else label_text
        color = self.colors['danger'] if required else self.colors['text']

        label = tk.Label(label_frame, text=label_text_final,
                         font=self.fonts['body'],
                         bg=self.colors['input_bg'], fg=color)
        label.pack(anchor=tk.W)

        # Campo de entrada modernizado
        if field_type == "number":
            entry = tk.Spinbox(container, textvariable=variable,
                               font=self.fonts['body'],
                               bg=self.colors['card'], fg=self.colors['text'],
                               relief=tk.FLAT, bd=0, from_=0, to=99999,
                               highlightthickness=2,
                               highlightcolor=self.colors['primary'],
                               highlightbackground=self.colors['border'])
        else:
            entry = tk.Entry(container, textvariable=variable,
                             font=self.fonts['body'],
                             bg=self.colors['card'], fg=self.colors['text'],
                             relief=tk.FLAT, bd=0,
                             highlightthickness=2,
                             highlightcolor=self.colors['primary'],
                             highlightbackground=self.colors['border'])

        entry.pack(fill=tk.X, ipady=8)

    def _create_enhanced_config_tab(self):
        """Crear pestaña de configuración mejorada"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")

        content = tk.Frame(config_frame, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Sección: Material
        self._create_section_header(content, "🧱 Material y Configuración")

        # Material selector modernizado
        material_card = self._create_field_card(content)
        material_container = tk.Frame(material_card, bg=self.colors['input_bg'])
        material_container.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(material_container, text="Tipo de Material",
                 font=self.fonts['body'],
                 bg=self.colors['input_bg'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 8))

        material_combo = ttk.Combobox(material_container, textvariable=self.vars['material'],
                                      values=["PLA", "ABS", "PETG", "TPU", "ASA", "WOOD", "CARBON"],
                                      font=self.fonts['body'], state="readonly")
        material_combo.pack(fill=tk.X, ipady=8)

        # Sección: Temperaturas
        self._create_section_header(content, "🌡️ Configuración de Temperatura")

        # Grid de temperaturas
        temp_grid = tk.Frame(content, bg=self.colors['card'])
        temp_grid.pack(fill=tk.X, pady=(0, 30))

        # Temperatura extrusor
        extrusor_card = tk.Frame(temp_grid, bg=self.colors['card'])
        extrusor_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        self._create_modern_field(extrusor_card, "Temperatura Extrusor (°C)",
                                  self.vars['temperatura_extrusor'], field_type="number")

        # Temperatura cama
        cama_card = tk.Frame(temp_grid, bg=self.colors['card'])
        cama_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0))
        self._create_modern_field(cama_card, "Temperatura Cama (°C)",
                                  self.vars['temperatura_cama'], field_type="number")

        # Guía de impresión modernizada
        self._create_guide_section(content)

    def _create_guide_section(self, parent):
        """Crear sección de guía modernizada"""
        self._create_section_header(parent, "📖 Guía de Impresión")

        guide_card = tk.Frame(parent, bg=self.colors['input_bg'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        guide_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        guide_container = tk.Frame(guide_card, bg=self.colors['input_bg'])
        guide_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(guide_container, text="Instrucciones y notas de impresión",
                 font=self.fonts['body'],
                 bg=self.colors['input_bg'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 8))

        self.guia_text = scrolledtext.ScrolledText(
            guide_container, height=8, font=self.fonts['body'],
            bg=self.colors['card'], fg=self.colors['text'],
            relief=tk.FLAT, bd=0,
            highlightthickness=2,
            highlightcolor=self.colors['primary'],
            highlightbackground=self.colors['border']
        )
        self.guia_text.pack(fill=tk.BOTH, expand=True)

    def _create_enhanced_image_tab(self):
        """Crear pestaña de imagen mejorada"""
        image_frame = ttk.Frame(self.notebook)
        self.notebook.add(image_frame, text="🖼️ Imagen del Producto")

        content = tk.Frame(image_frame, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Sección: Vista Previa
        self._create_section_header(content, "👀 Vista Previa")

        # Preview container modernizado
        preview_card = tk.Frame(content, bg=self.colors['input_bg'],
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        preview_card.pack(fill=tk.X, pady=(0, 30))

        preview_container = tk.Frame(preview_card, bg=self.colors['accent'], height=350)
        preview_container.pack(fill=tk.X, padx=20, pady=20)
        preview_container.pack_propagate(False)

        self.image_label = tk.Label(preview_container, text="📷\nArrastre una imagen aquí\no use el botón para seleccionar",
                                    font=self.fonts['body'],
                                    bg=self.colors['accent'], fg=self.colors['text_secondary'],
                                    justify=tk.CENTER)
        self.image_label.pack(expand=True)

        # Botones de imagen modernizados
        self._create_image_buttons(content)

    def _create_image_buttons(self, parent):
        """Crear botones de imagen modernizados"""
        self._create_section_header(parent, "🔧 Acciones")

        btn_container = tk.Frame(parent, bg=self.colors['card'])
        btn_container.pack(fill=tk.X)

        # Botón seleccionar
        select_btn = self._create_modern_button(
            btn_container, "📁 Seleccionar Imagen",
            self._select_image, 'primary'
        )
        select_btn.pack(side=tk.LEFT, padx=(0, 15))

        # Botón quitar
        remove_btn = self._create_modern_button(
            btn_container, "🗑️ Quitar Imagen",
            self._remove_image, 'danger'
        )
        remove_btn.pack(side=tk.LEFT)

    def _create_modern_button(self, parent, text, command, style='secondary'):
        """Crear botón moderno con efectos"""
        colors = {
            'primary': (self.colors['primary'], 'white', self.colors['primary_hover']),
            'secondary': (self.colors['card'], self.colors['text'], self.colors['accent']),
            'danger': (self.colors['danger'], 'white', '#DC2626')
        }

        bg, fg, hover = colors.get(style, colors['secondary'])

        btn_frame = tk.Frame(parent, bg=bg, highlightbackground=self.colors['border'],
                             highlightthickness=1 if style == 'secondary' else 0)

        btn = tk.Button(btn_frame, text=text, command=command,
                        font=self.fonts['body'], bg=bg, fg=fg,
                        bd=0, padx=20, pady=12, cursor='hand2',
                        activebackground=hover, activeforeground=fg)
        btn.pack(fill=tk.BOTH)

        # Efectos hover
        def on_enter(e):
            if btn['state'] != 'disabled':
                btn.config(bg=hover)
                btn_frame.config(bg=hover)

        def on_leave(e):
            if btn['state'] != 'disabled':
                btn.config(bg=bg)
                btn_frame.config(bg=bg)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        return btn_frame

    def _create_modern_buttons(self, parent):
        """Crear botones de acción modernizados"""
        # Shadow superior
        shadow = tk.Frame(parent, bg=self.colors['border'], height=1)
        shadow.pack(fill=tk.X, pady=(20, 0))

        button_container = tk.Frame(parent, bg=self.colors['card'],
                                    highlightbackground=self.colors['border'],
                                    highlightthickness=1)
        button_container.pack(fill=tk.X, pady=(0, 0))

        button_content = tk.Frame(button_container, bg=self.colors['card'])
        button_content.pack(fill=tk.X, padx=40, pady=20)

        # Botón cancelar
        cancel_btn = self._create_modern_button(
            button_content, "❌ Cancelar",
            self._on_close, 'secondary'
        )
        cancel_btn.pack(side=tk.RIGHT)

        # Botón guardar
        save_btn = self._create_modern_button(
            button_content, "💾 Guardar Cambios",
            self._save_changes, 'primary'
        )
        save_btn.pack(side=tk.RIGHT, padx=(0, 15))

    def _setup_ttk_styles(self):
        """Configurar estilos TTK"""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook styles
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

        # Entry styles
        style.configure('Modern.TEntry',
                        fieldbackground=self.colors['input_bg'],
                        borderwidth=1,
                        relief='flat',
                        bordercolor=self.colors['border'],
                        font=self.fonts['body'])

        style.map('Modern.TEntry',
                  bordercolor=[('focus', self.colors['primary'])])

    def _load_product_data(self):
        """Cargar datos del producto"""
        # Cargar guía si existe
        if self.guia_text and self.producto.guia_impresion:
            self.guia_text.insert('1.0', self.producto.guia_impresion)

        # Cargar imagen si existe
        self._load_image()

    def _load_image(self):
        """Cargar imagen del producto con preview mejorado"""
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            try:
                image = Image.open(self.producto.imagen_path)
                image.thumbnail((320, 320), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.image_label.configure(image=photo, text="",
                                           bg=self.colors['card'])
                self.image_label.image = photo

            except Exception as e:
                self.image_label.configure(text=f"❌ Error al cargar imagen:\n{str(e)}",
                                           bg=self.colors['accent'])
        else:
            self.image_label.configure(text="📷\nArrastre una imagen aquí\no use el botón para seleccionar",
                                       bg=self.colors['accent'])

    def _select_image(self):
        """Seleccionar nueva imagen"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen del producto",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )

        if file_path:
            self.imagen_path.set(file_path)
            self._load_image()

    def _remove_image(self):
        """Quitar imagen"""
        self.imagen_path.set("")
        self.image_label.configure(image="", text="📷\nArrastre una imagen aquí\no use el botón para seleccionar",
                                   bg=self.colors['accent'])
        self.image_label.image = None

    def _save_changes(self):
        """Guardar cambios en el producto"""
        try:
            # Validar campos requeridos
            if not self.vars['nombre'].get().strip():
                messagebox.showerror("Error de Validación",
                                     "El nombre del producto es requerido")
                return

            # Actualizar producto
            self.producto.nombre = self.vars['nombre'].get().strip()
            self.producto.descripcion = self.vars['descripcion'].get().strip()
            self.producto.peso = self.vars['peso'].get()
            self.producto.tiempo_impresion = self.vars['tiempo_impresion'].get()
            self.producto.material = self.vars['material'].get()
            self.producto.temperatura_extrusor = self.vars['temperatura_extrusor'].get()
            self.producto.temperatura_cama = self.vars['temperatura_cama'].get()
            self.producto.imagen_path = self.imagen_path.get() if self.imagen_path.get() else None

            # Guardar guía si existe
            if self.guia_text:
                self.producto.guia_impresion = self.guia_text.get('1.0', 'end-1c').strip()

            # Actualizar en base de datos
            success, message = self.db_manager.actualizar_producto(self.producto)

            if success:
                self.producto_actualizado = True
                messagebox.showinfo("✅ Éxito",
                                    "Producto actualizado correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("❌ Error",
                                     f"Error al actualizar: {message}")

        except Exception as e:
            messagebox.showerror("❌ Error",
                                 f"Error inesperado: {str(e)}")

    def _on_close(self):
        """Manejar cierre de ventana"""
        if messagebox.askokcancel("Confirmar Salida",
                                  "¿Está seguro de salir?\nLos cambios no guardados se perderán."):
            self.window.destroy()

    def _center_window(self):
        """Centrar ventana en pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')


# === EJEMPLO DE USO ===
if __name__ == "__main__":
    # Ejemplo de cómo usar la ventana
    import tkinter as tk

    # Crear ventana principal de prueba
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    # Crear producto de ejemplo
    class ProductoEjemplo:
        def __init__(self):
            self.nombre = "Producto de Ejemplo"
            self.descripcion = "Descripción del producto"
            self.peso = 50.0
            self.tiempo_impresion = 120
            self.material = "PLA"
            self.temperatura_extrusor = 200
            self.temperatura_cama = 60
            self.imagen_path = None
            self.guia_impresion = "Guía de ejemplo"

    # Crear manager de base de datos de ejemplo
    class DBManagerEjemplo:
        def actualizar_producto(self, producto):
            return True, "Producto actualizado correctamente"

    producto = ProductoEjemplo()
    db_manager = DBManagerEjemplo()

    # Crear y mostrar ventana
    ventana = ModernEditProductWindow(root, db_manager, producto)

    root.mainloop()