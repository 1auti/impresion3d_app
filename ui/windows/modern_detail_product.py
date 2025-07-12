"""
Ventana para ver detalles completos del producto - Versión Modernizada
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import os
from PIL import Image, ImageTk, ImageDraw
import webbrowser
from pathlib import Path

from models.producto import Producto


class ModernProductDetailWindow:
    """Ventana modernizada para ver detalles completos de un producto"""

    def __init__(self, parent, producto: Producto):
        self.parent = parent
        self.producto = producto

        # Configurar paleta de colores moderna
        self.setup_modern_colors()

        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title(f"Detalles - {producto.nombre}")
        self.window.geometry("1100x800")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(bg=self.colors['bg'])

        # Configurar estilos
        self.setup_modern_styles()

        # Crear interfaz
        self.create_modern_widgets()

        # Cargar datos
        self.cargar_datos()

        # Centrar ventana
        self.center_window()

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
            'shadow': '#94A3B8',
            'accent': '#F1F5F9'
        }

        # Configurar fuentes
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

        # Estilo para frames
        style.configure('Modern.TFrame',
                        background=self.colors['card'],
                        relief='flat',
                        borderwidth=1)

        style.configure('Card.TFrame',
                        background=self.colors['card'],
                        relief='flat',
                        borderwidth=0)

        # Estilo para labels
        style.configure('Title.TLabel',
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        font=self.fonts['title'])

        style.configure('Heading.TLabel',
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        font=self.fonts['heading'])

        style.configure('Body.TLabel',
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        font=self.fonts['body'])

        style.configure('Caption.TLabel',
                        background=self.colors['card'],
                        foreground=self.colors['text_secondary'],
                        font=self.fonts['caption'])

        # Estilo para botones
        style.configure('Primary.TButton',
                        font=self.fonts['body'],
                        borderwidth=0,
                        relief='flat',
                        background=self.colors['primary'],
                        foreground='white',
                        padding=(15, 10))

        style.map('Primary.TButton',
                  background=[('active', self.colors['primary_hover'])])

        style.configure('Secondary.TButton',
                        font=self.fonts['body'],
                        borderwidth=1,
                        relief='flat',
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        padding=(15, 10))

        style.map('Secondary.TButton',
                  background=[('active', self.colors['accent'])])

    def create_modern_widgets(self):
        """Crear interfaz moderna"""
        # Frame principal
        main_container = tk.Frame(self.window, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header moderno
        self.create_modern_header(main_container)

        # Contenedor principal con grid
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Configurar grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # Panel izquierdo - Imagen e información básica
        self.create_left_panel(content_frame)

        # Panel derecho - Especificaciones y configuración
        self.create_right_panel(content_frame)

        # Panel inferior - Guía y acciones
        self.create_bottom_panel(main_container)

    def create_modern_header(self, parent):
        """Crear header moderno"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Contenido del header
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        # Icono y título
        icon_label = tk.Label(header_content, text="📋", font=('Segoe UI', 28),
                              bg=self.colors['primary'], fg='white')
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        title_info = tk.Frame(header_content, bg=self.colors['primary'])
        title_info.pack(side=tk.LEFT, fill=tk.Y)

        title_label = tk.Label(title_info, text=self.producto.nombre,
                               font=self.fonts['title'],
                               bg=self.colors['primary'], fg='white')
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_info, text=f"ID: {self.producto.id} • {self.producto.material}",
                                  font=self.fonts['body'],
                                  bg=self.colors['primary'], fg='white')
        subtitle_label.pack(anchor=tk.W)

        # Estado/badges
        badges_frame = tk.Frame(header_content, bg=self.colors['primary'])
        badges_frame.pack(side=tk.RIGHT)

        self.create_badge(badges_frame, f"{self.producto.get_peso_total()}g", "⚖️")
        self.create_badge(badges_frame, self.producto.tiempo_impresion_formato(), "⏱️")

    def create_badge(self, parent, text, icon):
        """Crear badge moderno"""
        badge = tk.Frame(parent, bg='white', highlightthickness=0)
        badge.pack(side=tk.LEFT, padx=5)

        content = tk.Frame(badge, bg='white')
        content.pack(padx=10, pady=5)

        tk.Label(content, text=icon, font=self.fonts['body'],
                 bg='white', fg=self.colors['primary']).pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(content, text=text, font=self.fonts['small'],
                 bg='white', fg=self.colors['text']).pack(side=tk.LEFT)

    def create_left_panel(self, parent):
        """Crear panel izquierdo"""
        left_container = tk.Frame(parent, bg=self.colors['bg'])
        left_container.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # Imagen del producto
        self.create_image_card(left_container)

        # Información básica
        self.create_basic_info_card(left_container)

        # Fechas
        self.create_dates_card(left_container)

    def create_image_card(self, parent):
        """Crear tarjeta de imagen"""
        image_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        image_card.pack(fill=tk.X, pady=(0, 20))

        # Header de la tarjeta
        header = tk.Frame(image_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(header, text="🖼️ Imagen del Producto",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        # Contenedor de imagen
        image_container = tk.Frame(image_card, bg=self.colors['accent'])
        image_container.pack(fill=tk.X, padx=20, pady=(0, 15))

        self.image_label = tk.Label(image_container, text="📷 Sin imagen disponible",
                                    font=self.fonts['body'],
                                    bg=self.colors['accent'], fg=self.colors['text_secondary'],
                                    height=12)
        self.image_label.pack(fill=tk.BOTH, padx=20, pady=20)

        # Botón para ver imagen completa
        btn_frame = tk.Frame(image_card, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        self.btn_open_image = self.create_modern_button(
            btn_frame, "👁️ Ver imagen completa", self.abrir_imagen_completa, 'secondary'
        )
        self.btn_open_image.pack(fill=tk.X)

    def create_basic_info_card(self, parent):
        """Crear tarjeta de información básica"""
        info_card = tk.Frame(parent, bg=self.colors['card'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        info_card.pack(fill=tk.X, pady=(0, 20))

        # Header
        header = tk.Frame(info_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(header, text="ℹ️ Información Básica",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        # Contenido
        content = tk.Frame(info_card, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.info_labels = {}
        info_data = [
            ('📝 Descripción:', self.producto.descripcion or "Sin descripción"),
            ('🔧 Material:', self.producto.material),
            ('⚖️ Peso Total:', f"{self.producto.get_peso_total()} gramos"),
            ('⏱️ Tiempo Base:', f"{self.producto.tiempo_impresion} min"),
            ('🎨 Colores:',
             f"{len(self.producto.colores_especificaciones)} colores" if self.producto.colores_especificaciones else "Sin especificar"),
            ('🌡️ Temp. Extrusor:', f"{self.producto.temperatura_extrusor}°C"),
            ('🌡️ Temp. Cama:', f"{self.producto.temperatura_cama}°C"),
        ]

        for i, (label_text, value) in enumerate(info_data):
            self.create_info_row(content, label_text, value, i)

    def create_info_row(self, parent, label_text, value, row):
        """Crear fila de información"""
        row_frame = tk.Frame(parent, bg=self.colors['card'])
        row_frame.pack(fill=tk.X, pady=3)

        # Label
        label = tk.Label(row_frame, text=label_text,
                         font=self.fonts['body'],
                         bg=self.colors['card'], fg=self.colors['text_secondary'],
                         width=15, anchor='w')
        label.pack(side=tk.LEFT)

        # Valor
        value_label = tk.Label(row_frame, text=value,
                               font=self.fonts['body'],
                               bg=self.colors['card'], fg=self.colors['text'],
                               anchor='w')
        value_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

        self.info_labels[label_text] = value_label

    def create_dates_card(self, parent):
        """Crear tarjeta de fechas"""
        dates_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        dates_card.pack(fill=tk.X)

        content = tk.Frame(dates_card, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(content, text="📅 Fechas",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        if self.producto.fecha_creacion:
            tk.Label(content,
                     text=f"Creado: {self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M')}",
                     font=self.fonts['small'],
                     bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor=tk.W)

        if self.producto.fecha_modificacion:
            tk.Label(content,
                     text=f"Modificado: {self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M')}",
                     font=self.fonts['small'],
                     bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor=tk.W)

    def create_right_panel(self, parent):
        """Crear panel derecho"""
        right_container = tk.Frame(parent, bg=self.colors['bg'])
        right_container.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

        # Especificaciones de color
        self.create_color_specifications_card(right_container)

        # Recomendaciones
        self.create_recommendations_card(right_container)

    def create_color_specifications_card(self, parent):
        """Crear tarjeta de especificaciones de color"""
        color_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        color_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Header
        header = tk.Frame(color_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(header, text="🎨 Especificaciones de Color",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        # Contenido con scroll
        if self.producto.colores_especificaciones:
            canvas = tk.Canvas(color_card, bg=self.colors['card'], height=400,
                               highlightthickness=0)
            scrollbar = ttk.Scrollbar(color_card, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Crear especificaciones
            self.create_color_groups(scrollable_frame)

            canvas.pack(side="left", fill="both", expand=True, padx=20)
            scrollbar.pack(side="right", fill="y", padx=(0, 20))

        else:
            no_colors = tk.Frame(color_card, bg=self.colors['card'])
            no_colors.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            tk.Label(no_colors, text="🎨",
                     font=('Segoe UI', 32),
                     bg=self.colors['card'], fg=self.colors['text_secondary']).pack(pady=(20, 10))
            tk.Label(no_colors, text="No hay especificaciones de color definidas",
                     font=self.fonts['body'],
                     bg=self.colors['card'], fg=self.colors['text_secondary']).pack()

    def create_color_groups(self, parent):
        """Crear grupos de color"""
        # Agrupar piezas por color
        color_groups = {}
        for color_spec in self.producto.colores_especificaciones:
            if color_spec.color_hex not in color_groups:
                color_groups[color_spec.color_hex] = {
                    'nombre': color_spec.nombre_color,
                    'piezas': [],
                    'peso_total': 0,
                    'tiempo_adicional': color_spec.tiempo_adicional
                }
            color_groups[color_spec.color_hex]['piezas'].extend(color_spec.piezas)
            color_groups[color_spec.color_hex]['peso_total'] += color_spec.peso_color

        # Mostrar cada grupo
        for i, (color_hex, group) in enumerate(color_groups.items()):
            self.create_color_group_widget(parent, color_hex, group, i)

        # Resumen
        self.create_color_summary(parent, color_groups)

    def create_color_group_widget(self, parent, color_hex, group, index):
        """Crear widget de grupo de color"""
        group_frame = tk.Frame(parent, bg=self.colors['accent'],
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        group_frame.pack(fill=tk.X, padx=5, pady=10)

        # Header del grupo
        header = tk.Frame(group_frame, bg=self.colors['accent'])
        header.pack(fill=tk.X, padx=15, pady=10)

        # Muestra de color
        color_sample = tk.Frame(header, bg=color_hex, width=40, height=40,
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        color_sample.pack(side=tk.LEFT, padx=(0, 15))
        color_sample.pack_propagate(False)

        # Información del color
        info_frame = tk.Frame(header, bg=self.colors['accent'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(info_frame, text=f"{group['nombre'] or 'Sin nombre'}",
                 font=self.fonts['subheading'],
                 bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W)

        tk.Label(info_frame, text=f"{color_hex} • {group['peso_total']:.1f}g",
                 font=self.fonts['small'],
                 bg=self.colors['accent'], fg=self.colors['text_secondary']).pack(anchor=tk.W)

        if group['tiempo_adicional'] > 0:
            tk.Label(info_frame, text=f"⏱️ +{group['tiempo_adicional']} min (cambio de color)",
                     font=self.fonts['caption'],
                     bg=self.colors['accent'], fg=self.colors['warning']).pack(anchor=tk.W)

        # Lista de piezas
        piezas_frame = tk.Frame(group_frame, bg=self.colors['accent'])
        piezas_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        tk.Label(piezas_frame, text="Piezas:",
                 font=self.fonts['body'],
                 bg=self.colors['accent'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 5))

        # Mostrar piezas en formato de chips
        chips_frame = tk.Frame(piezas_frame, bg=self.colors['accent'])
        chips_frame.pack(fill=tk.X)

        for pieza in group['piezas'][:8]:  # Mostrar máximo 8 piezas
            chip = tk.Label(chips_frame, text=pieza,
                            font=self.fonts['caption'],
                            bg=self.colors['card'], fg=self.colors['text'],
                            padx=8, pady=2,
                            relief=tk.FLAT,
                            highlightbackground=self.colors['border'],
                            highlightthickness=1)
            chip.pack(side=tk.LEFT, padx=3, pady=2)

        if len(group['piezas']) > 8:
            tk.Label(chips_frame, text=f"+{len(group['piezas']) - 8} más",
                     font=self.fonts['caption'],
                     bg=self.colors['text_secondary'], fg='white',
                     padx=8, pady=2).pack(side=tk.LEFT, padx=3, pady=2)

    def create_color_summary(self, parent, color_groups):
        """Crear resumen de colores"""
        summary_frame = tk.Frame(parent, bg=self.colors['card'])
        summary_frame.pack(fill=tk.X, pady=(20, 10))

        tk.Label(summary_frame, text="📊 Resumen Total",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(pady=(0, 10))

        total_colores = len(color_groups)
        total_piezas = sum(len(g['piezas']) for g in color_groups.values())
        tiempo_cambios = sum(g['tiempo_adicional'] for g in color_groups.values())

        summary_text = f"• {total_colores} colores diferentes\n"
        summary_text += f"• {total_piezas} piezas en total\n"
        if tiempo_cambios > 0:
            summary_text += f"• +{tiempo_cambios} min por cambios de color"

        tk.Label(summary_frame, text=summary_text,
                 font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text'],
                 justify=tk.LEFT).pack(anchor=tk.W)

    def create_recommendations_card(self, parent):
        """Crear tarjeta de recomendaciones"""
        rec_card = tk.Frame(parent, bg=self.colors['card'],
                            highlightbackground=self.colors['border'],
                            highlightthickness=1)
        rec_card.pack(fill=tk.X)

        # Header
        header = tk.Frame(rec_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(header, text="💡 Recomendaciones",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        # Contenido
        content = tk.Frame(rec_card, bg=self.colors['card'])
        content.pack(fill=tk.X, padx=20, pady=(0, 20))

        recomendaciones = self.generar_recomendaciones()
        for i, rec in enumerate(recomendaciones):
            rec_frame = tk.Frame(content, bg=self.colors['accent'])
            rec_frame.pack(fill=tk.X, pady=3)

            tk.Label(rec_frame, text="•",
                     font=self.fonts['body'],
                     bg=self.colors['accent'], fg=self.colors['primary']).pack(side=tk.LEFT, padx=(10, 5), pady=8)

            tk.Label(rec_frame, text=rec,
                     font=self.fonts['small'],
                     bg=self.colors['accent'], fg=self.colors['text'],
                     wraplength=280, justify=tk.LEFT).pack(side=tk.LEFT, padx=(0, 10), pady=5)

    def create_bottom_panel(self, parent):
        """Crear panel inferior"""
        bottom_container = tk.Frame(parent, bg=self.colors['bg'])
        bottom_container.pack(fill=tk.X, pady=(20, 0))

        # Configurar grid
        bottom_container.grid_columnconfigure(0, weight=1)
        bottom_container.grid_columnconfigure(1, weight=0)

        # Guía de impresión
        self.create_guide_card(bottom_container)

        # Panel de acciones
        self.create_actions_panel(bottom_container)

    def create_guide_card(self, parent):
        """Crear tarjeta de guía"""
        guide_card = tk.Frame(parent, bg=self.colors['card'],
                              highlightbackground=self.colors['border'],
                              highlightthickness=1)
        guide_card.grid(row=0, column=0, sticky='nsew', padx=(0, 20))

        # Header
        header = tk.Frame(guide_card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(header, text="📖 Guía de Impresión",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

        # ScrolledText moderno
        self.guide_text = scrolledtext.ScrolledText(
            guide_card, wrap=tk.WORD, height=12,
            font=self.fonts['body'],
            bg='white', fg=self.colors['text'],
            relief=tk.FLAT, borderwidth=0,
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        self.guide_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.guide_text.configure(state='disabled')

    def create_actions_panel(self, parent):
        """Crear panel de acciones"""
        actions_card = tk.Frame(parent, bg=self.colors['card'],
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        actions_card.grid(row=0, column=1, sticky='nsew')

        content = tk.Frame(actions_card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(content, text="⚡ Acciones Rápidas",
                 font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(pady=(0, 20))

        # Botones de acción
        btn_copy = self.create_modern_button(content, "📑 Copiar Guía", self.copiar_guia, 'secondary')
        btn_copy.pack(fill=tk.X, pady=5)

        btn_print = self.create_modern_button(content, "🖨️ Imprimir Detalles", self.imprimir_detalles, 'secondary')
        btn_print.pack(fill=tk.X, pady=5)

        # Separador
        separator = tk.Frame(content, height=2, bg=self.colors['border'])
        separator.pack(fill=tk.X, pady=15)

        btn_close = self.create_modern_button(content, "✖️ Cerrar", self.window.destroy, 'primary')
        btn_close.pack(fill=tk.X)

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

    def cargar_datos(self):
        """Cargar datos del producto"""
        # Cargar imagen
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            try:
                img = Image.open(self.producto.imagen_path)
                img.thumbnail((320, 320), Image.Resampling.LANCZOS)

                # Crear imagen con bordes redondeados
                mask = Image.new('L', img.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle([(0, 0), img.size], radius=15, fill=255)

                output = Image.new('RGBA', img.size, (0, 0, 0, 0))
                output.paste(img, (0, 0))
                output.putalpha(mask)

                photo = ImageTk.PhotoImage(output)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo

            except Exception as e:
                print(f"Error al cargar imagen: {e}")
                self.image_label.configure(text="❌ Error al cargar imagen")
        else:
            self.image_label.configure(text="📷 Sin imagen disponible")

        # Cargar guía
        self.guide_text.configure(state='normal')
        self.guide_text.delete('1.0', tk.END)

        if self.producto.guia_impresion:
            self.guide_text.insert('1.0', self.producto.guia_impresion)
        else:
            placeholder_text = """📝 No hay guía de impresión disponible para este producto.

💡 Una guía típica incluiría:
• Configuración del slicer recomendada
• Preparación de la superficie de impresión
• Consejos para la primera capa
• Manejo de soportes si son necesarios
• Post-procesamiento recomendado
• Solución de problemas comunes"""
            self.guide_text.insert('1.0', placeholder_text)

        self.guide_text.configure(state='disabled')

    def generar_recomendaciones(self):
        """Generar recomendaciones basadas en el material y configuración"""
        recomendaciones = []

        # Recomendaciones por material
        if self.producto.material == "PLA":
            recomendaciones.extend([
                "Ideal para principiantes - Fácil de imprimir",
                "Buena adhesión en cama fría (50-60°C)",
                "Velocidad recomendada: 40-60 mm/s",
                "Retracción: 1-2mm a 40-50 mm/s"
            ])
        elif self.producto.material == "ABS":
            recomendaciones.extend([
                "Requiere cama caliente (80-100°C) y ambiente cerrado",
                "Buena resistencia mecánica y térmica",
                "Cuidado con el warping - usar brim o raft",
                "Ventilación recomendada por vapores"
            ])
        elif self.producto.material == "PETG":
            recomendaciones.extend([
                "Combina facilidad del PLA con resistencia del ABS",
                "Temperatura cama: 70-80°C",
                "Excelente para piezas funcionales",
                "Resistente a químicos y rayos UV"
            ])
        elif self.producto.material == "TPU":
            recomendaciones.extend([
                "Material flexible - Imprimir lentamente (15-30 mm/s)",
                "Reducir retracción al mínimo (0.5-1mm)",
                "Direct drive preferible sobre bowden",
                "Cama a 40-50°C para mejor adhesión"
            ])
        else:
            recomendaciones.append(f"Material {self.producto.material} - Consultar configuraciones específicas")

        # Recomendaciones por tiempo de impresión
        tiempo_total = self.producto.get_tiempo_total()
        if tiempo_total > 480:  # Más de 8 horas
            recomendaciones.append("⏰ Impresión larga: Verificar filamento suficiente")
            recomendaciones.append("🔄 Considerar pausas para mantenimiento")

        # Recomendaciones por peso
        if self.producto.get_peso_total() > 100:
            recomendaciones.append("⚖️ Pieza pesada: Asegurar excelente adhesión a la cama")

        # Recomendaciones por múltiples colores
        if len(self.producto.colores_especificaciones) > 1:
            recomendaciones.append("🎨 Múltiples colores: Planificar cambios de filamento")
            recomendaciones.append("⏱️ Tiempo adicional por cambios incluido")

        return recomendaciones[:6]  # Limitar a 6 recomendaciones

    def abrir_imagen_completa(self):
        """Abrir la imagen en el visor predeterminado del sistema"""
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            try:
                if os.name == 'nt':
                    os.startfile(self.producto.imagen_path)
                elif os.name == 'posix' and os.uname().sysname == 'Darwin':
                    os.system(f'open "{self.producto.imagen_path}"')
                else:
                    os.system(f'xdg-open "{self.producto.imagen_path}"')
            except Exception as e:
                self.show_modern_message("Error", f"No se pudo abrir la imagen: {str(e)}", 'error')

    def copiar_guia(self):
        """Copiar la guía de impresión al portapapeles"""
        try:
            guia = self.guide_text.get('1.0', 'end-1c')
            self.window.clipboard_clear()
            self.window.clipboard_append(guia)
            self.show_modern_message("Éxito", "La guía de impresión se copió al portapapeles", 'success')
        except Exception as e:
            self.show_modern_message("Error", f"Error al copiar: {str(e)}", 'error')

    def imprimir_detalles(self):
        """Generar un archivo HTML moderno con los detalles para imprimir"""
        try:
            # Crear HTML moderno
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Detalles - {self.producto.nombre}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #1E293B;
            background: #F8FAFC;
            padding: 20px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #6366F1, #EC4899);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .content {{
            padding: 30px;
        }}

        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: #F8FAFC;
            border-radius: 8px;
            border-left: 4px solid #6366F1;
        }}

        .section h2 {{
            color: #6366F1;
            font-size: 1.4em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .info-item {{
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #E2E8F0;
        }}

        .info-label {{
            font-weight: 600;
            color: #64748B;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}

        .info-value {{
            font-size: 1.1em;
            color: #1E293B;
            font-weight: 500;
        }}

        .color-spec {{
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }}

        .color-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }}

        .color-sample {{
            width: 30px;
            height: 30px;
            border-radius: 6px;
            border: 2px solid #E2E8F0;
        }}

        .color-info h3 {{
            font-size: 1.1em;
            margin-bottom: 5px;
        }}

        .color-meta {{
            color: #64748B;
            font-size: 0.9em;
        }}

        .pieces {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }}

        .piece {{
            background: #F1F5F9;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            color: #475569;
        }}

        .guide {{
            white-space: pre-wrap;
            background: #F8FAFC;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            line-height: 1.5;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            color: #64748B;
            border-top: 1px solid #E2E8F0;
            font-size: 0.9em;
        }}

        .badges {{
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }}

        .badge {{
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; }}
            .header {{ background: #6366F1 !important; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖨️ {self.producto.nombre}</h1>
            <p class="subtitle">Especificaciones Técnicas de Impresión 3D</p>
            <div class="badges">
                <span class="badge">📦 ID: {self.producto.id}</span>
                <span class="badge">🔧 {self.producto.material}</span>
                <span class="badge">⚖️ {self.producto.get_peso_total()}g</span>
                <span class="badge">⏱️ {self.producto.tiempo_impresion_formato()}</span>
            </div>
        </div>

        <div class="content">
            <div class="section">
                <h2>ℹ️ Información Básica</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Descripción</div>
                        <div class="info-value">{self.producto.descripcion or 'Sin descripción'}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Material</div>
                        <div class="info-value">{self.producto.material}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Peso Total</div>
                        <div class="info-value">{self.producto.get_peso_total()} gramos</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Tiempo Base</div>
                        <div class="info-value">{self.producto.tiempo_impresion} minutos</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>⚙️ Configuración de Impresión</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Temperatura Extrusor</div>
                        <div class="info-value">{self.producto.temperatura_extrusor}°C</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Temperatura Cama</div>
                        <div class="info-value">{self.producto.temperatura_cama}°C</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Tiempo Total Estimado</div>
                        <div class="info-value">{self.producto.get_tiempo_total()} minutos</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Colores Diferentes</div>
                        <div class="info-value">{len(self.producto.colores_especificaciones)}</div>
                    </div>
                </div>
            </div>"""

            # Agregar especificaciones de color si existen
            if self.producto.colores_especificaciones:
                # Agrupar por color
                color_groups = {}
                for spec in self.producto.colores_especificaciones:
                    if spec.color_hex not in color_groups:
                        color_groups[spec.color_hex] = {
                            'nombre': spec.nombre_color,
                            'piezas': [],
                            'peso_total': 0,
                            'tiempo_adicional': spec.tiempo_adicional
                        }
                    color_groups[spec.color_hex]['piezas'].extend(spec.piezas)
                    color_groups[spec.color_hex]['peso_total'] += spec.peso_color

                html_content += '''
            <div class="section">
                <h2>🎨 Especificaciones de Color</h2>'''

                for color_hex, group in color_groups.items():
                    html_content += f'''
                <div class="color-spec">
                    <div class="color-header">
                        <div class="color-sample" style="background-color: {color_hex};"></div>
                        <div class="color-info">
                            <h3>{group['nombre'] or 'Sin nombre'}</h3>
                            <div class="color-meta">{color_hex} • {group['peso_total']:.1f}g'''

                    if group['tiempo_adicional'] > 0:
                        html_content += f''' • +{group['tiempo_adicional']} min'''

                    html_content += '''</div>
                        </div>
                    </div>
                    <div class="pieces">'''

                    for pieza in group['piezas']:
                        html_content += f'<span class="piece">{pieza}</span>'

                    html_content += '''
                    </div>
                </div>'''

                html_content += '''
            </div>'''

            # Continuar con guía y footer
            html_content += f'''
            <div class="section">
                <h2>📖 Guía de Impresión</h2>
                <div class="guide">{self.producto.guia_impresion or 'No hay guía disponible'}</div>
            </div>
        </div>

        <div class="footer">
            <p>Generado el {self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M') if self.producto.fecha_creacion else 'N/A'}</p>
            <p>Última modificación: {self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M') if self.producto.fecha_modificacion else 'N/A'}</p>
        </div>
    </div>
</body>
</html>'''

            # Guardar y abrir
            temp_path = Path("temp_print_modern.html")
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            webbrowser.open(str(temp_path.absolute()))
            self.show_modern_message("Éxito",
                                     "Documento generado y abierto en el navegador.\nUsa Ctrl+P (o Cmd+P en Mac) para imprimir.",
                                     'success')

        except Exception as e:
            self.show_modern_message("Error", f"Error al generar documento: {str(e)}", 'error')

    def show_modern_message(self, title, message, msg_type='info'):
        """Mostrar mensaje moderno"""
        # Crear ventana de mensaje moderna
        msg_window = tk.Toplevel(self.window)
        msg_window.title(title)
        msg_window.geometry("400x200")
        msg_window.transient(self.window)
        msg_window.grab_set()
        msg_window.configure(bg=self.colors['card'])

        # Configurar colores según tipo
        colors = {
            'success': ('#10B981', '✅'),
            'error': ('#EF4444', '❌'),
            'info': ('#6366F1', 'ℹ️'),
            'warning': ('#F59E0B', '⚠️')
        }

        color, icon = colors.get(msg_type, colors['info'])

        # Contenido
        content = tk.Frame(msg_window, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Icono
        tk.Label(content, text=icon, font=('Segoe UI', 32),
                 bg=self.colors['card'], fg=color).pack(pady=(0, 15))

        # Título
        tk.Label(content, text=title, font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack()

        # Mensaje
        tk.Label(content, text=message, font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text_secondary'],
                 wraplength=340, justify=tk.CENTER).pack(pady=(10, 20))

        # Botón
        btn = self.create_modern_button(content, "Aceptar", msg_window.destroy, 'primary')
        btn.pack()

        # Centrar
        msg_window.update_idletasks()
        x = (msg_window.winfo_screenwidth() // 2) - (msg_window.winfo_width() // 2)
        y = (msg_window.winfo_screenheight() // 2) - (msg_window.winfo_height() // 2)
        msg_window.geometry(f'+{x}+{y}')

        # Auto-cerrar después de 5 segundos para mensajes de éxito
        if msg_type == 'success':
            msg_window.after(5000, msg_window.destroy)

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')