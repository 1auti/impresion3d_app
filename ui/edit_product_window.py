"""
Ventana para editar producto existente
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import scrolledtext
import os
from PIL import Image, ImageTk
from datetime import datetime

from datebase.db_manager import DatabaseManager
from models.producto import Producto
from utils.file_utils import FileUtils


class EditProductWindow:
    """Ventana para editar un producto existente"""

    def __init__(self, parent, db_manager: DatabaseManager, producto: Producto):
        self.parent = parent
        self.db_manager = db_manager
        self.producto = producto
        self.producto_actualizado = False
        self.imagen_path = producto.imagen_path
        self.nueva_imagen = False

        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title(f"Editar Producto - {producto.nombre}")
        self.window.geometry("800x700")
        self.window.transient(parent)
        self.window.grab_set()

        # Variables
        self.crear_variables()

        # Crear interfaz
        self.create_widgets()

        # Cargar datos del producto
        self.cargar_datos_producto()

        # Centrar ventana
        self.center_window()

    def crear_variables(self):
        """Crear variables para los campos"""
        self.vars = {
            'nombre': tk.StringVar(value=self.producto.nombre),
            'descripcion': tk.StringVar(value=self.producto.descripcion),
            'peso': tk.DoubleVar(value=self.producto.peso),
            'color': tk.StringVar(value=self.producto.color),
            'tiempo_impresion': tk.IntVar(value=self.producto.tiempo_impresion),
            'material': tk.StringVar(value=self.producto.material),
            'temperatura_extrusor': tk.IntVar(value=self.producto.temperatura_extrusor),
            'temperatura_cama': tk.IntVar(value=self.producto.temperatura_cama)
        }

        self.entries = {}

    def create_widgets(self):
        """Crear widgets de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="✏️ Editar Producto",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        # Información del producto
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(info_frame, text=f"ID: {self.producto.id}",
                  font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        ttk.Label(info_frame,
                  text=f"Creado: {self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M') if self.producto.fecha_creacion else 'N/A'}",
                  font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        ttk.Label(info_frame,
                  text=f"Modificado: {self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M') if self.producto.fecha_modificacion else 'N/A'}",
                  font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        # Notebook para organizar campos
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña de información básica
        tab_basic = ttk.Frame(notebook, padding="10")
        notebook.add(tab_basic, text="Información Básica")

        # Campos básicos
        fields_basic = [
            ('nombre', 'Nombre del Producto:', 'entry'),
            ('descripcion', 'Descripción:', 'entry'),
            ('color', 'Color:', 'entry'),
            ('material', 'Material:', 'combobox'),
            ('peso', 'Peso (gramos):', 'spinbox'),
            ('tiempo_impresion', 'Tiempo de Impresión (minutos):', 'spinbox')
        ]

        row = 0
        for field_name, label_text, widget_type in fields_basic:
            ttk.Label(tab_basic, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)

            if widget_type == 'entry':
                widget = ttk.Entry(tab_basic, textvariable=self.vars[field_name], width=40)
            elif widget_type == 'combobox' and field_name == 'material':
                widget = ttk.Combobox(tab_basic, textvariable=self.vars[field_name], width=37,
                                      values=['PLA', 'ABS', 'PETG', 'TPU', 'Nylon', 'Resina'])
            elif widget_type == 'spinbox':
                if field_name == 'peso':
                    widget = ttk.Spinbox(tab_basic, textvariable=self.vars[field_name],
                                         from_=0, to=10000, increment=0.1, width=38)
                else:
                    widget = ttk.Spinbox(tab_basic, textvariable=self.vars[field_name],
                                         from_=0, to=10000, increment=1, width=38)

            widget.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
            self.entries[field_name] = widget
            row += 1

        # Imagen
        image_frame = ttk.LabelFrame(tab_basic, text="Imagen del Producto", padding="10")
        image_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10, padx=5)

        self.image_label = ttk.Label(image_frame, text="Sin imagen", relief=tk.SUNKEN,
                                     anchor='center')
        self.image_label.pack(side=tk.LEFT, padx=(0, 10))
        self.image_label.configure(width=20, padding=40)

        btn_frame = ttk.Frame(image_frame)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Button(btn_frame, text="Cambiar Imagen",
                   command=self.seleccionar_imagen).pack(pady=5)
        ttk.Button(btn_frame, text="Quitar Imagen",
                   command=self.quitar_imagen).pack()

        self.image_info = ttk.Label(btn_frame, text="", font=('Arial', 9))
        self.image_info.pack(pady=(10, 0))

        # Pestaña de configuración de impresión
        tab_config = ttk.Frame(notebook, padding="10")
        notebook.add(tab_config, text="Configuración de Impresión")

        # Campos de configuración
        fields_config = [
            ('temperatura_extrusor', 'Temperatura del Extrusor (°C):', 'spinbox'),
            ('temperatura_cama', 'Temperatura de la Cama (°C):', 'spinbox')
        ]

        row = 0
        for field_name, label_text, widget_type in fields_config:
            ttk.Label(tab_config, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)

            widget = ttk.Spinbox(tab_config, textvariable=self.vars[field_name],
                                 from_=0, to=300, increment=5, width=20)
            widget.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
            self.entries[field_name] = widget
            row += 1

        # Guía de impresión
        ttk.Label(tab_config, text="Guía de Impresión:").grid(row=row, column=0,
                                                              sticky=(tk.W, tk.N), pady=5, padx=5)

        self.guia_text = scrolledtext.ScrolledText(tab_config, width=50, height=15, wrap=tk.WORD)
        self.guia_text.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(button_frame, text="💾 Guardar Cambios",
                   command=self.guardar_cambios).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="❌ Cancelar",
                   command=self.cancelar).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="🔄 Restablecer",
                   command=self.cargar_datos_producto).pack(side=tk.RIGHT, padx=5)

    def cargar_datos_producto(self):
        """Cargar los datos del producto en los campos"""
        # Cargar guía
        self.guia_text.delete('1.0', tk.END)
        self.guia_text.insert('1.0', self.producto.guia_impresion)

        # Cargar imagen
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            self.imagen_path = self.producto.imagen_path
            self.mostrar_imagen_preview()
        else:
            self.imagen_path = None
            self.image_label.configure(image="", text="Sin imagen")

    def seleccionar_imagen(self):
        """Seleccionar nueva imagen para el producto"""
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
        elif file_path:
            messagebox.showerror("Error", "El archivo seleccionado no es una imagen válida")

    def mostrar_imagen_preview(self):
        """Mostrar vista previa de la imagen"""
        if self.imagen_path and os.path.exists(self.imagen_path):
            try:
                # Cargar imagen
                img = Image.open(self.imagen_path)
                img.thumbnail((150, 150), Image.Resampling.LANCZOS)

                # Mostrar en label
                photo = ImageTk.PhotoImage(img)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Mantener referencia

                # Mostrar información
                size = FileUtils.get_file_size_readable(self.imagen_path)
                estado = "Nueva imagen" if self.nueva_imagen else "Imagen actual"
                self.image_info.configure(text=f"{estado}\nTamaño: {size}")

            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar imagen: {str(e)}")
                self.quitar_imagen()

    def quitar_imagen(self):
        """Quitar imagen del producto"""
        self.imagen_path = None
        self.nueva_imagen = True  # Marcar que se cambió la imagen (se quitó)
        self.image_label.configure(image="", text="Sin imagen")
        self.image_label.image = None
        self.image_info.configure(text="Imagen eliminada")

    def validar_campos(self):
        """Validar que los campos requeridos estén completos"""
        # Validar nombre
        if not self.vars['nombre'].get().strip():
            messagebox.showerror("Error", "El nombre del producto es requerido")
            self.entries['nombre'].focus()
            return False

        # Validar valores numéricos
        try:
            peso = self.vars['peso'].get()
            if peso < 0:
                messagebox.showerror("Error", "El peso no puede ser negativo")
                return False
        except:
            messagebox.showerror("Error", "El peso debe ser un número válido")
            return False

        try:
            tiempo = self.vars['tiempo_impresion'].get()
            if tiempo < 0:
                messagebox.showerror("Error", "El tiempo de impresión no puede ser negativo")
                return False
        except:
            messagebox.showerror("Error", "El tiempo de impresión debe ser un número válido")
            return False

        return True

    def detectar_cambios(self):
        """Detectar si hay cambios en el producto"""
        cambios = []

        # Comparar campos básicos
        if self.vars['nombre'].get().strip() != self.producto.nombre:
            cambios.append("Nombre")
        if self.vars['descripcion'].get().strip() != self.producto.descripcion:
            cambios.append("Descripción")
        if self.vars['peso'].get() != self.producto.peso:
            cambios.append("Peso")
        if self.vars['color'].get().strip() != self.producto.color:
            cambios.append("Color")
        if self.vars['tiempo_impresion'].get() != self.producto.tiempo_impresion:
            cambios.append("Tiempo de impresión")
        if self.vars['material'].get() != self.producto.material:
            cambios.append("Material")
        if self.vars['temperatura_extrusor'].get() != self.producto.temperatura_extrusor:
            cambios.append("Temperatura extrusor")
        if self.vars['temperatura_cama'].get() != self.producto.temperatura_cama:
            cambios.append("Temperatura cama")

        # Comparar guía
        guia_actual = self.guia_text.get('1.0', 'end-1c')
        if guia_actual != self.producto.guia_impresion:
            cambios.append("Guía de impresión")

        # Comparar imagen
        if self.nueva_imagen:
            cambios.append("Imagen")

        return cambios

    def guardar_cambios(self):
        """Guardar los cambios del producto"""
        if not self.validar_campos():
            return

        # Detectar cambios
        cambios = self.detectar_cambios()

        if not cambios:
            messagebox.showinfo("Sin cambios", "No se detectaron cambios en el producto")
            return

        # Confirmar cambios
        mensaje = f"Se detectaron cambios en:\n" + "\n".join(f"• {campo}" for campo in cambios[:5])
        if len(cambios) > 5:
            mensaje += f"\n... y {len(cambios) - 5} campos más"
        mensaje += "\n\n¿Desea guardar los cambios?"

        if not messagebox.askyesno("Confirmar cambios", mensaje):
            return

        try:
            # Actualizar objeto producto
            self.producto.nombre = self.vars['nombre'].get().strip()
            self.producto.descripcion = self.vars['descripcion'].get().strip()
            self.producto.peso = self.vars['peso'].get()
            self.producto.color = self.vars['color'].get().strip()
            self.producto.tiempo_impresion = self.vars['tiempo_impresion'].get()
            self.producto.material = self.vars['material'].get()
            self.producto.temperatura_extrusor = self.vars['temperatura_extrusor'].get()
            self.producto.temperatura_cama = self.vars['temperatura_cama'].get()
            self.producto.guia_impresion = self.guia_text.get('1.0', 'end-1c')
            self.producto.fecha_modificacion = datetime.now()

            # Manejar imagen si cambió
            if self.nueva_imagen:
                # Eliminar imagen anterior si existe
                if self.producto.imagen_path:
                    FileUtils.delete_product_image(self.producto.imagen_path)

                # Guardar nueva imagen si existe
                if self.imagen_path:
                    saved_path = FileUtils.save_product_image(self.imagen_path, self.producto.nombre)
                    if saved_path:
                        self.producto.imagen_path = saved_path
                    else:
                        if not messagebox.askyesno("Advertencia",
                                                   "No se pudo guardar la imagen. ¿Desea continuar?"):
                            return
                else:
                    self.producto.imagen_path = None

            # Actualizar en base de datos
            if self.db_manager.actualizar_producto(self.producto):
                self.producto_actualizado = True
                messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
                self.window.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")

    def cancelar(self):
        """Cancelar edición"""
        if self.detectar_cambios():
            if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar? Los cambios no guardados se perderán."):
                self.window.destroy()
        else:
            self.window.destroy()

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')