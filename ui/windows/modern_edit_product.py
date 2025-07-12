
"""
Ventana de edición de productos - CORREGIDA para eliminar errores de pack()
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from PIL import Image, ImageTk

from database.db_manager import DatabaseManager
from models.producto import Producto


class ModernEditProductWindowRefactored:
    """Ventana de edición de productos corregida sin errores de pack()"""

    def __init__(self, parent, db_manager: DatabaseManager, producto: Producto):
        self.parent = parent
        self.db_manager = db_manager
        self.producto = producto
        self.producto_actualizado = False

        # Variables del formulario
        self._init_variables()

        # Configurar ventana
        self._setup_window()

        # Crear interfaz
        self._create_interface()

        # Cargar datos
        self._load_product_data()

        # Centrar ventana
        self._center_window()

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
        """Configurar ventana principal - SIN errores de pack"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Editar Producto - {self.producto.nombre}")
        self.window.geometry("1200x800")
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.configure(bg='#f8fafc')

        # Protocolo de cierre
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_interface(self):
        """Crear interfaz principal - CORREGIDO sin pack duplicados"""

        # ✅ Container principal - solo un fill
        main_container = tk.Frame(self.window, bg='#ffffff')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ✅ Header
        self._create_header(main_container)

        # ✅ Content area
        content_frame = tk.Frame(main_container, bg='#ffffff')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # ✅ Notebook para pestañas
        self._create_notebook(content_frame)

        # ✅ Buttons frame
        self._create_buttons(main_container)

    def _create_header(self, parent):
        """Crear header sin errores de pack"""
        header_frame = tk.Frame(parent, bg='#3b82f6', height=80)
        header_frame.pack(fill=tk.X)  # ✅ Solo un fill
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg='#3b82f6')
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Icono y título
        icon_label = tk.Label(header_content, text="✏️", font=('Segoe UI', 28),
                              bg='#3b82f6', fg='white')
        icon_label.pack(side=tk.LEFT)

        title_frame = tk.Frame(header_content, bg='#3b82f6')
        title_frame.pack(side=tk.LEFT, padx=(15, 0))

        title_label = tk.Label(title_frame, text="Editar Producto",
                               font=('Segoe UI', 20, 'bold'),
                               bg='#3b82f6', fg='white')
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_frame, text=f"Modificando: {self.producto.nombre}",
                                  font=('Segoe UI', 12),
                                  bg='#3b82f6', fg='#e0e7ff')
        subtitle_label.pack(anchor=tk.W)

    def _create_notebook(self, parent):
        """Crear notebook con pestañas - SIN errores pack"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)  # ✅ Sin duplicados

        # Pestañas
        self._create_basic_tab()
        self._create_config_tab()
        self._create_image_tab()

    def _create_basic_tab(self):
        """Crear pestaña básica"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="📋 Información Básica")

        # Scroll frame
        canvas = tk.Canvas(basic_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # ✅ Pack sin duplicados
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill=tk.Y)

        # Contenido
        content = tk.Frame(scrollable_frame, bg='#ffffff')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Campos del formulario
        self._create_form_fields(content)

    def _create_form_fields(self, parent):
        """Crear campos del formulario"""

        # Nombre
        name_frame = tk.Frame(parent, bg='#ffffff')
        name_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(name_frame, text="Nombre del Producto:",
                 font=('Segoe UI', 12, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        name_entry = tk.Entry(name_frame, textvariable=self.vars['nombre'],
                              font=('Segoe UI', 11), bg='#f9fafb',
                              relief=tk.FLAT, bd=1)
        name_entry.pack(fill=tk.X, pady=(5, 0))

        # Descripción
        desc_frame = tk.Frame(parent, bg='#ffffff')
        desc_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(desc_frame, text="Descripción:",
                 font=('Segoe UI', 12, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        desc_entry = tk.Entry(desc_frame, textvariable=self.vars['descripcion'],
                              font=('Segoe UI', 11), bg='#f9fafb',
                              relief=tk.FLAT, bd=1)
        desc_entry.pack(fill=tk.X, pady=(5, 0))

        # Fila de campos numéricos
        numeric_frame = tk.Frame(parent, bg='#ffffff')
        numeric_frame.pack(fill=tk.X, pady=(0, 20))

        # Peso
        peso_col = tk.Frame(numeric_frame, bg='#ffffff')
        peso_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(peso_col, text="Peso (g):",
                 font=('Segoe UI', 10, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        peso_entry = tk.Entry(peso_col, textvariable=self.vars['peso'],
                              font=('Segoe UI', 10), bg='#f9fafb')
        peso_entry.pack(fill=tk.X, pady=(5, 0))

        # Tiempo
        tiempo_col = tk.Frame(numeric_frame, bg='#ffffff')
        tiempo_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(tiempo_col, text="Tiempo (min):",
                 font=('Segoe UI', 10, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        tiempo_entry = tk.Entry(tiempo_col, textvariable=self.vars['tiempo_impresion'],
                                font=('Segoe UI', 10), bg='#f9fafb')
        tiempo_entry.pack(fill=tk.X, pady=(5, 0))

    def _create_config_tab(self):
        """Crear pestaña de configuración"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")

        content = tk.Frame(config_frame, bg='#ffffff')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Material
        material_frame = tk.Frame(content, bg='#ffffff')
        material_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(material_frame, text="Material:",
                 font=('Segoe UI', 12, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        material_combo = ttk.Combobox(material_frame, textvariable=self.vars['material'],
                                      values=["PLA", "ABS", "PETG", "TPU", "ASA"],
                                      font=('Segoe UI', 11), state="readonly")
        material_combo.pack(fill=tk.X, pady=(5, 0))

        # Temperaturas
        temp_frame = tk.Frame(content, bg='#ffffff')
        temp_frame.pack(fill=tk.X, pady=(0, 20))

        # Extrusor
        extrusor_col = tk.Frame(temp_frame, bg='#ffffff')
        extrusor_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        tk.Label(extrusor_col, text="Temp. Extrusor (°C):",
                 font=('Segoe UI', 10, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        extrusor_entry = tk.Entry(extrusor_col, textvariable=self.vars['temperatura_extrusor'],
                                  font=('Segoe UI', 10), bg='#f9fafb')
        extrusor_entry.pack(fill=tk.X, pady=(5, 0))

        # Cama
        cama_col = tk.Frame(temp_frame, bg='#ffffff')
        cama_col.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        tk.Label(cama_col, text="Temp. Cama (°C):",
                 font=('Segoe UI', 10, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        cama_entry = tk.Entry(cama_col, textvariable=self.vars['temperatura_cama'],
                              font=('Segoe UI', 10), bg='#f9fafb')
        cama_entry.pack(fill=tk.X, pady=(5, 0))

        # Guía de impresión
        guide_frame = tk.Frame(content, bg='#ffffff')
        guide_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        tk.Label(guide_frame, text="Guía de Impresión:",
                 font=('Segoe UI', 12, 'bold'),
                 bg='#ffffff', fg='#1f2937').pack(anchor=tk.W)

        from tkinter import scrolledtext
        self.guia_text = scrolledtext.ScrolledText(
            guide_frame, height=10, font=('Segoe UI', 10),
            bg='#f9fafb', relief=tk.FLAT, bd=1
        )
        self.guia_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    def _create_image_tab(self):
        """Crear pestaña de imagen"""
        image_frame = ttk.Frame(self.notebook)
        self.notebook.add(image_frame, text="🖼️ Imagen")

        content = tk.Frame(image_frame, bg='#ffffff')
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Preview de imagen
        preview_frame = tk.Frame(content, bg='#f3f4f6', height=300,
                                 highlightbackground='#d1d5db', highlightthickness=1)
        preview_frame.pack(fill=tk.X, pady=(0, 20))
        preview_frame.pack_propagate(False)

        self.image_label = tk.Label(preview_frame, text="Sin imagen",
                                    font=('Segoe UI', 12),
                                    bg='#f3f4f6', fg='#6b7280')
        self.image_label.pack(expand=True)

        # Botones de imagen
        btn_frame = tk.Frame(content, bg='#ffffff')
        btn_frame.pack(fill=tk.X)

        select_btn = tk.Button(btn_frame, text="📁 Seleccionar Imagen",
                               command=self._select_image,
                               font=('Segoe UI', 10), bg='#3b82f6', fg='white',
                               relief=tk.FLAT, padx=20, pady=8)
        select_btn.pack(side=tk.LEFT)

        remove_btn = tk.Button(btn_frame, text="🗑️ Quitar Imagen",
                               command=self._remove_image,
                               font=('Segoe UI', 10), bg='#ef4444', fg='white',
                               relief=tk.FLAT, padx=20, pady=8)
        remove_btn.pack(side=tk.LEFT, padx=(10, 0))

    def _create_buttons(self, parent):
        """Crear botones de acción - SIN errores pack"""
        button_frame = tk.Frame(parent, bg='#ffffff')
        button_frame.pack(fill=tk.X, pady=(20, 0))  # ✅ Solo un fill

        # Botón cancelar
        cancel_btn = tk.Button(button_frame, text="❌ Cancelar",
                               command=self._on_close,
                               font=('Segoe UI', 11), bg='#6b7280', fg='white',
                               relief=tk.FLAT, padx=30, pady=12)
        cancel_btn.pack(side=tk.RIGHT)

        # Botón guardar
        save_btn = tk.Button(button_frame, text="💾 Guardar Cambios",
                             command=self._save_changes,
                             font=('Segoe UI', 11, 'bold'), bg='#10b981', fg='white',
                             relief=tk.FLAT, padx=30, pady=12)
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))

    def _load_product_data(self):
        """Cargar datos del producto"""
        # Cargar guía si existe
        if self.guia_text and self.producto.guia_impresion:
            self.guia_text.insert('1.0', self.producto.guia_impresion)

        # Cargar imagen si existe
        self._load_image()

    def _load_image(self):
        """Cargar imagen del producto"""
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            try:
                image = Image.open(self.producto.imagen_path)
                image.thumbnail((280, 280), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo

            except Exception as e:
                self.image_label.configure(text=f"Error: {str(e)}")
        else:
            self.image_label.configure(text="Sin imagen")

    def _select_image(self):
        """Seleccionar nueva imagen"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if file_path:
            self.imagen_path.set(file_path)
            self._load_image()

    def _remove_image(self):
        """Quitar imagen"""
        self.imagen_path.set("")
        self.image_label.configure(image="", text="Sin imagen")
        self.image_label.image = None

    def _save_changes(self):
        """Guardar cambios en el producto"""
        try:
            # Validar campos requeridos
            if not self.vars['nombre'].get().strip():
                messagebox.showerror("Error", "El nombre del producto es requerido")
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
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", f"Error al actualizar: {message}")

        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

    def _on_close(self):
        """Manejar cierre de ventana"""
        if messagebox.askokcancel("Salir", "¿Está seguro de salir? Los cambios no guardados se perderán."):
            self.window.destroy()

    def _center_window(self):
        """Centrar ventana en pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

