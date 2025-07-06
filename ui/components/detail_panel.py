"""
Componente Panel de Detalles para mostrar información del producto seleccionado
"""
import tkinter as tk
import os
from PIL import Image, ImageTk, ImageDraw
from .modern_widgets import ModernWidgets
from ..style.color_palette import ColorPalette


class DetailPanelComponent:
    """Panel moderno para mostrar detalles del producto seleccionado"""

    def __init__(self, parent):
        self.parent = parent
        self.colors = ColorPalette.get_colors_dict()
        self.widgets = ModernWidgets()
        self.fonts = {
            'heading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9)
        }

        # Referencias a elementos de la interfaz
        self.preview_label = None
        self.info_labels = {}
        self.color_samples_frame = None

        self.create_detail_panel()

    def create_detail_panel(self):
        """Crear panel de detalles moderno"""
        # Frame del panel
        self.detail_container = tk.Frame(self.parent, bg=self.colors['bg'])

        self.detail_panel = tk.Frame(self.detail_container, bg=self.colors['card'],
                                     highlightbackground=self.colors['border'],
                                     highlightthickness=1)
        self.detail_panel.pack(fill=tk.BOTH, expand=True)

        # Contenido
        detail_content = tk.Frame(self.detail_panel, bg=self.colors['card'])
        detail_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        tk.Label(detail_content, text="📋 Vista Previa",
                 font=self.fonts['heading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 20))

        # Imagen preview
        self._create_preview_section(detail_content)

        # Información del producto
        self._create_info_section(detail_content)

    def _create_preview_section(self, parent):
        """Crear sección de vista previa de imagen"""
        self.preview_frame = tk.Frame(parent, bg=self.colors['bg'],
                                      height=200, highlightthickness=1,
                                      highlightbackground=self.colors['border'])
        self.preview_frame.pack(fill=tk.X, pady=(0, 20))
        self.preview_frame.pack_propagate(False)

        self.preview_label = tk.Label(self.preview_frame, text="Sin imagen",
                                      font=self.fonts['body'],
                                      bg=self.colors['bg'], fg=self.colors['text_secondary'])
        self.preview_label.pack(expand=True)

    def _create_info_section(self, parent):
        """Crear sección de información del producto"""
        self.info_frame = tk.Frame(parent, bg=self.colors['card'])
        self.info_frame.pack(fill=tk.BOTH, expand=True)

        # Crear campos de información
        self._create_info_field("📦 Nombre:", "-")
        self._create_info_field("🔧 Material:", "-")
        self._create_info_field("⏱️ Tiempo:", "-")
        self._create_info_field("⚖️ Peso:", "-")
        self._create_info_field("🎨 Colores:", "-")

        # Frame para muestras de color
        self.color_samples_frame = tk.Frame(self.info_frame, bg=self.colors['card'])
        self.color_samples_frame.pack(fill=tk.X, pady=(10, 0))

    def _create_info_field(self, label, value):
        """Crear campo de información"""
        field_frame = tk.Frame(self.info_frame, bg=self.colors['card'])
        field_frame.pack(fill=tk.X, pady=5)

        tk.Label(field_frame, text=label, font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text_secondary']).pack(side=tk.LEFT)

        value_label = tk.Label(field_frame, text=value, font=self.fonts['body'],
                               bg=self.colors['card'], fg=self.colors['text'])
        value_label.pack(side=tk.LEFT, padx=(10, 0))

        self.info_labels[label] = value_label

    def pack(self, **kwargs):
        """Empaquetar el panel"""
        self.detail_container.pack(**kwargs)
        return self.detail_container

    def grid(self, **kwargs):
        """Posicionar el panel con grid"""
        self.detail_container.grid(**kwargs)
        return self.detail_container

    def update_product_details(self, producto):
        """Actualizar detalles del producto"""
        if not producto:
            self.clear_details()
            return

        # Actualizar imagen
        self._update_image(producto)

        # Actualizar información
        self._update_product_info(producto)

        # Actualizar muestras de color
        self._update_color_samples(producto)

    def _update_image(self, producto):
        """Actualizar imagen del producto"""
        if producto.imagen_path and os.path.exists(producto.imagen_path):
            try:
                img = Image.open(producto.imagen_path)
                img.thumbnail((180, 180), Image.Resampling.LANCZOS)

                # Agregar borde redondeado a la imagen
                mask = Image.new('L', img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle([(0, 0), img.size], radius=10, fill=255)

                output = Image.new('RGBA', img.size, (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)

                photo = ImageTk.PhotoImage(output)
                self.preview_label.configure(image=photo, text="")
                self.preview_label.image = photo
            except Exception as e:
                self.preview_label.configure(image="", text="Error al cargar imagen")
                self.preview_label.image = None
        else:
            self.preview_label.configure(image="", text="📷 Sin imagen")
            self.preview_label.image = None

    def _update_product_info(self, producto):
        """Actualizar información del producto"""
        # Truncar nombre si es muy largo
        nombre_truncado = producto.nombre[:25] + "..." if len(producto.nombre) > 25 else producto.nombre

        self.info_labels["📦 Nombre:"].config(text=nombre_truncado)
        self.info_labels["🔧 Material:"].config(text=producto.material)
        self.info_labels["⏱️ Tiempo:"].config(text=producto.tiempo_impresion_formato())
        self.info_labels["⚖️ Peso:"].config(text=f"{producto.get_peso_total()}g")

        num_colores = len(producto.colores_especificaciones) if hasattr(producto, 'colores_especificaciones') else 0
        self.info_labels["🎨 Colores:"].config(text=f"{num_colores} colores")

    def _update_color_samples(self, producto):
        """Actualizar muestras de color"""
        # Limpiar muestras anteriores
        for widget in self.color_samples_frame.winfo_children():
            widget.destroy()

        # Mostrar muestras de color
        if hasattr(producto, 'colores_especificaciones') and producto.colores_especificaciones:
            colors_container = tk.Frame(self.color_samples_frame, bg=self.colors['card'])
            colors_container.pack(anchor=tk.W)

            # Mostrar hasta 6 colores
            for i, color_spec in enumerate(producto.colores_especificaciones[:6]):
                color_name = getattr(color_spec, 'nombre_color', None) or getattr(color_spec, 'color_hex', 'Sin nombre')
                color_hex = getattr(color_spec, 'color_hex', '#CCCCCC')

                self.widgets.create_color_sample(colors_container, color_hex, color_name)

            # Indicador de más colores
            if len(producto.colores_especificaciones) > 6:
                tk.Label(colors_container,
                         text=f"+{len(producto.colores_especificaciones) - 6}",
                         font=self.fonts['small'], bg=self.colors['card'],
                         fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=5)
        elif hasattr(producto, 'color') and producto.color:
            # Mostrar color simple si existe
            colors_container = tk.Frame(self.color_samples_frame, bg=self.colors['card'])
            colors_container.pack(anchor=tk.W)

            # Asumir que es un color hex o nombre
            self.widgets.create_color_sample(colors_container, producto.color, producto.color)

    def clear_details(self):
        """Limpiar detalles del panel"""
        # Limpiar imagen
        self.preview_label.configure(image="", text="📷 Sin imagen")
        self.preview_label.image = None

        # Limpiar información
        for label in self.info_labels.values():
            label.configure(text="-")

        # Limpiar muestras de color
        for widget in self.color_samples_frame.winfo_children():
            widget.destroy()

    def set_placeholder_text(self, text="Selecciona un producto para ver detalles"):
        """Establecer texto de placeholder cuando no hay producto seleccionado"""
        self.preview_label.configure(image="", text="📋 " + text)
        self.preview_label.image = None