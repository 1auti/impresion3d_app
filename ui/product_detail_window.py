"""
Ventana para ver detalles completos del producto
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import os
from PIL import Image, ImageTk
import webbrowser
from pathlib import Path

from models.producto import Producto
from utils.file_utils import FileUtils


class ProductDetailWindow:
    """Ventana para ver detalles completos de un producto"""

    def __init__(self, parent, producto: Producto):
        self.parent = parent
        self.producto = producto

        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title(f"Detalles - {producto.nombre}")
        self.window.geometry("900x700")
        self.window.transient(parent)
        self.window.grab_set()

        # Crear interfaz
        self.create_widgets()

        # Cargar datos
        self.cargar_datos()

        # Centrar ventana
        self.center_window()

    def create_widgets(self):
        """Crear widgets de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título con icono
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(header_frame, text="📋", font=('Arial', 24)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(header_frame, text=self.producto.nombre,
                 font=('Arial', 18, 'bold')).pack(side=tk.LEFT)

        # Frame principal con dos columnas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Columna izquierda - Imagen y datos básicos
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 20))

        # Imagen del producto
        image_frame = ttk.LabelFrame(left_frame, text="Imagen del Producto", padding="10")
        image_frame.pack(fill=tk.X)

        self.image_label = ttk.Label(image_frame, text="Sin imagen", relief=tk.SUNKEN,
                                    anchor='center')
        self.image_label.pack()
        self.image_label.configure(padding=50)

        # Botón para abrir imagen en tamaño completo
        self.btn_open_image = ttk.Button(image_frame, text="Ver imagen completa",
                                        command=self.abrir_imagen_completa, state='disabled')
        self.btn_open_image.pack(pady=(10, 0))

        # Información básica
        basic_frame = ttk.LabelFrame(left_frame, text="Información Básica", padding="10")
        basic_frame.pack(fill=tk.X, pady=(20, 0))

        self.info_labels = {}
        info_data = [
            ('ID:', str(self.producto.id)),
            ('Descripción:', self.producto.descripcion or "Sin descripción"),
            ('Peso Total:', f"{self.producto.get_peso_total()} gramos"),
            ('Material:', self.producto.material),
            ('Tiempo Total:', self.producto.get_tiempo_total() // 60 if self.producto.get_tiempo_total() >= 60
                            else f"{self.producto.get_tiempo_total()} min")
        ]

        # Formatear tiempo total correctamente
        tiempo_total = self.producto.get_tiempo_total()
        if tiempo_total >= 60:
            horas = tiempo_total // 60
            minutos = tiempo_total % 60
            info_data[4] = ('Tiempo Total:', f"{horas}h {minutos}min" if minutos > 0 else f"{horas}h")

        for label_text, value in info_data:
            frame = ttk.Frame(basic_frame)
            frame.pack(fill=tk.X, pady=3)

            ttk.Label(frame, text=label_text, font=('Arial', 10, 'bold'),
                     width=12).pack(side=tk.LEFT, anchor=tk.W)
            label = ttk.Label(frame, text=value, font=('Arial', 10))
            label.pack(side=tk.LEFT, padx=(5, 0), anchor=tk.W)
            self.info_labels[label_text] = label

        # Columna derecha - Configuración y guía
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Especificaciones de color
        color_frame = ttk.LabelFrame(right_frame, text="🎨 Especificaciones de Color - Desglose por Piezas", padding="10")
        color_frame.pack(fill=tk.X)

        if self.producto.colores_especificaciones:
            # Crear un canvas con scroll para las especificaciones
            canvas = tk.Canvas(color_frame, height=200)
            scrollbar = ttk.Scrollbar(color_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Agrupar piezas por color para mejor visualización
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

            # Mostrar cada grupo de color
            for i, (color_hex, group) in enumerate(color_groups.items()):
                # Frame para el grupo de color
                group_frame = ttk.Frame(scrollable_frame, relief=tk.RIDGE, borderwidth=1)
                group_frame.pack(fill=tk.X, padx=5, pady=5)

                # Cabecera con color
                header_frame = ttk.Frame(group_frame)
                header_frame.pack(fill=tk.X, padx=10, pady=5)

                # Muestra de color grande
                color_label = tk.Label(header_frame, text="", bg=color_hex,
                                     width=6, height=2, relief=tk.SUNKEN)
                color_label.pack(side=tk.LEFT, padx=(0, 10))

                # Información del color
                info_frame = ttk.Frame(header_frame)
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                ttk.Label(info_frame, text=f"{group['nombre'] or 'Sin nombre'} ({color_hex})",
                         font=('Arial', 11, 'bold')).pack(anchor=tk.W)
                ttk.Label(info_frame, text=f"Peso total: {group['peso_total']:.1f}g",
                         font=('Arial', 10)).pack(anchor=tk.W)
                if group['tiempo_adicional'] > 0:
                    ttk.Label(info_frame, text=f"Tiempo cambio: +{group['tiempo_adicional']} min",
                             font=('Arial', 9), foreground='#666666').pack(anchor=tk.W)

                # Lista de piezas
                piezas_frame = ttk.Frame(group_frame)
                piezas_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

                ttk.Label(piezas_frame, text="Piezas:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)

                # Mostrar piezas en columnas si son muchas
                piezas_list_frame = ttk.Frame(piezas_frame)
                piezas_list_frame.pack(fill=tk.X, padx=(20, 0))

                piezas = group['piezas']
                if len(piezas) > 6:  # Si hay muchas piezas, usar columnas
                    col1 = ttk.Frame(piezas_list_frame)
                    col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    col2 = ttk.Frame(piezas_list_frame)
                    col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                    mid = len(piezas) // 2
                    for j, pieza in enumerate(piezas[:mid]):
                        ttk.Label(col1, text=f"• {pieza}", font=('Arial', 9)).pack(anchor=tk.W)
                    for j, pieza in enumerate(piezas[mid:]):
                        ttk.Label(col2, text=f"• {pieza}", font=('Arial', 9)).pack(anchor=tk.W)
                else:
                    for pieza in piezas:
                        ttk.Label(piezas_list_frame, text=f"• {pieza}", font=('Arial', 9)).pack(anchor=tk.W)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Resumen total
            resumen_frame = ttk.Frame(color_frame)
            resumen_frame.pack(fill=tk.X, pady=(10, 0))

            ttk.Separator(resumen_frame, orient='horizontal').pack(fill=tk.X, pady=5)

            total_colores = len(color_groups)
            total_piezas = sum(len(g['piezas']) for g in color_groups.values())

            ttk.Label(resumen_frame,
                     text=f"Total: {total_colores} colores diferentes, {total_piezas} piezas",
                     font=('Arial', 10, 'bold')).pack()

        else:
            ttk.Label(color_frame, text="No hay especificaciones de color definidas",
                     font=('Arial', 10), foreground='#666666').pack(pady=20)

        # Configuración de impresión
        config_frame = ttk.LabelFrame(right_frame, text="⚙️ Configuración de Impresión", padding="10")
        config_frame.pack(fill=tk.X, pady=(20, 0))

        # Crear un frame tipo tabla para la configuración
        config_data = [
            ('Tiempo estimado:', self.producto.tiempo_impresion_formato()),
            ('Temperatura Extrusor:', f"{self.producto.temperatura_extrusor}°C"),
            ('Temperatura Cama:', f"{self.producto.temperatura_cama}°C"),
        ]

        for i, (label, value) in enumerate(config_data):
            ttk.Label(config_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=3, padx=(0, 20))
            ttk.Label(config_frame, text=value, font=('Arial', 10)).grid(
                row=i, column=1, sticky=tk.W, pady=3)

        # Recomendaciones adicionales
        recom_frame = ttk.Frame(config_frame)
        recom_frame.grid(row=len(config_data), column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Label(recom_frame, text="💡 Recomendaciones:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)

        recomendaciones = self.generar_recomendaciones()
        for rec in recomendaciones:
            ttk.Label(recom_frame, text=f"• {rec}", font=('Arial', 9),
                     foreground='#666666').pack(anchor=tk.W, padx=(20, 0), pady=1)

        # Guía de impresión
        guide_frame = ttk.LabelFrame(right_frame, text="📖 Guía de Impresión", padding="10")
        guide_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # ScrolledText para mostrar la guía
        self.guide_text = scrolledtext.ScrolledText(guide_frame, wrap=tk.WORD,
                                                   height=12, font=('Arial', 10))
        self.guide_text.pack(fill=tk.BOTH, expand=True)

        # Hacer el texto de solo lectura
        self.guide_text.configure(state='disabled')

        # Frame de fechas
        dates_frame = ttk.Frame(main_frame)
        dates_frame.pack(fill=tk.X, pady=(20, 0))

        if self.producto.fecha_creacion:
            ttk.Label(dates_frame, text=f"Creado: {self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M')}",
                     font=('Arial', 9), foreground='#666666').pack(side=tk.LEFT, padx=5)

        if self.producto.fecha_modificacion:
            ttk.Label(dates_frame, text=f"Modificado: {self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M')}",
                     font=('Arial', 9), foreground='#666666').pack(side=tk.LEFT, padx=5)

        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(button_frame, text="📑 Copiar Guía",
                  command=self.copiar_guia).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="🖨️ Imprimir Detalles",
                  command=self.imprimir_detalles).pack(side=tk.LEFT)

        ttk.Button(button_frame, text="Cerrar",
                  command=self.window.destroy).pack(side=tk.RIGHT)

    def cargar_datos(self):
        """Cargar datos del producto en la ventana"""
        # Cargar imagen
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            try:
                img = Image.open(self.producto.imagen_path)
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Mantener referencia

                # Habilitar botón de ver imagen completa
                self.btn_open_image.configure(state='normal')

            except Exception as e:
                print(f"Error al cargar imagen: {e}")
                self.image_label.configure(text="Error al cargar imagen")

        # Cargar guía
        self.guide_text.configure(state='normal')
        self.guide_text.delete('1.0', tk.END)

        if self.producto.guia_impresion:
            self.guide_text.insert('1.0', self.producto.guia_impresion)
        else:
            self.guide_text.insert('1.0', "No hay guía de impresión disponible para este producto.")

        self.guide_text.configure(state='disabled')

    def generar_recomendaciones(self):
        """Generar recomendaciones basadas en el material y configuración"""
        recomendaciones = []

        # Recomendaciones por material
        if self.producto.material == "PLA":
            recomendaciones.append("Buena adhesión en cama fría o con temperatura baja")
            recomendaciones.append("Ideal para principiantes, fácil de imprimir")
        elif self.producto.material == "ABS":
            recomendaciones.append("Requiere cama caliente y ambiente cerrado")
            recomendaciones.append("Buena resistencia mecánica y térmica")
        elif self.producto.material == "PETG":
            recomendaciones.append("Combina facilidad del PLA con resistencia del ABS")
            recomendaciones.append("Resistente a químicos y rayos UV")
        elif self.producto.material == "TPU":
            recomendaciones.append("Material flexible, imprimir lentamente")
            recomendaciones.append("Evitar retracción excesiva")

        # Recomendaciones por tiempo de impresión
        if self.producto.tiempo_impresion > 480:  # Más de 8 horas
            recomendaciones.append("Impresión larga: verificar filamento suficiente")
            recomendaciones.append("Considerar pausas para mantenimiento")

        # Recomendaciones por peso
        if self.producto.peso > 100:
            recomendaciones.append("Pieza pesada: asegurar buena adhesión a la cama")

        return recomendaciones[:4]  # Limitar a 4 recomendaciones

    def abrir_imagen_completa(self):
        """Abrir la imagen en el visor predeterminado del sistema"""
        if self.producto.imagen_path and os.path.exists(self.producto.imagen_path):
            try:
                # En Windows
                if os.name == 'nt':
                    os.startfile(self.producto.imagen_path)
                # En macOS
                elif os.name == 'posix' and os.uname().sysname == 'Darwin':
                    os.system(f'open "{self.producto.imagen_path}"')
                # En Linux
                else:
                    os.system(f'xdg-open "{self.producto.imagen_path}"')
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la imagen: {str(e)}")

    def copiar_guia(self):
        """Copiar la guía de impresión al portapapeles"""
        try:
            guia = self.guide_text.get('1.0', 'end-1c')
            self.window.clipboard_clear()
            self.window.clipboard_append(guia)
            messagebox.showinfo("Copiado", "La guía de impresión se copió al portapapeles")
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar: {str(e)}")

    def imprimir_detalles(self):
        """Generar un archivo HTML con los detalles para imprimir"""
        try:
            # Crear HTML con los detalles
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Detalles - {self.producto.nombre}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #0078d4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #0078d4;
            margin-top: 20px;
        }}
        .info-section {{
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
        .info-row {{
            margin: 5px 0;
        }}
        .label {{
            font-weight: bold;
            display: inline-block;
            width: 150px;
        }}
        .guide {{
            white-space: pre-wrap;
            background-color: #f9f9f9;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        @media print {{
            body {{
                margin: 10px;
            }}
        }}
    </style>
</head>
<body>
    <h1>🖨️ {self.producto.nombre}</h1>
    
    <div class="info-section">
        <h2>Información Básica</h2>
        <div class="info-row"><span class="label">ID:</span> {self.producto.id}</div>
        <div class="info-row"><span class="label">Descripción:</span> {self.producto.descripcion or 'Sin descripción'}</div>
        <div class="info-row"><span class="label">Color:</span> {self.producto.color or 'No especificado'}</div>
        <div class="info-row"><span class="label">Peso:</span> {self.producto.peso} gramos</div>
        <div class="info-row"><span class="label">Material:</span> {self.producto.material}</div>
    </div>
    
    <div class="info-section">
        <h2>Configuración de Impresión</h2>
        <div class="info-row"><span class="label">Tiempo estimado:</span> {self.producto.tiempo_impresion_formato()}</div>
        <div class="info-row"><span class="label">Temperatura Extrusor:</span> {self.producto.temperatura_extrusor}°C</div>
        <div class="info-row"><span class="label">Temperatura Cama:</span> {self.producto.temperatura_cama}°C</div>
    </div>
    
    <div class="info-section">
        <h2>Guía de Impresión</h2>
        <div class="guide">{self.producto.guia_impresion or 'No hay guía disponible'}</div>
    </div>
    
    <div class="info-section">
        <p><small>
            Creado: {self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M') if self.producto.fecha_creacion else 'N/A'}<br>
            Modificado: {self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M') if self.producto.fecha_modificacion else 'N/A'}
        </small></p>
    </div>
</body>
</html>
"""

            # Guardar archivo temporal
            temp_path = Path("temp_print.html")
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Abrir en navegador para imprimir
            webbrowser.open(str(temp_path.absolute()))

            messagebox.showinfo("Imprimir",
                              "Se abrió el documento en su navegador.\n"
                              "Use Ctrl+P (o Cmd+P en Mac) para imprimir.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar documento: {str(e)}")

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')