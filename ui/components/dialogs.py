"""
Diálogos modernos para la aplicación
"""
import tkinter as tk
from tkinter import filedialog
import json
import datetime
from .modern_widgets import ModernWidgets
from ..style.color_palette import ColorPalette


class ModernDialogs:
    """Clase para manejar diálogos modernos"""

    def __init__(self, parent_window):
        self.parent = parent_window
        self.colors = ColorPalette.get_colors_dict()
        self.widgets = ModernWidgets()
        self.fonts = {
            'title': ('Segoe UI', 24, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9)
        }

    def show_confirmation_dialog(self, title, message, icon="⚠️", confirm_text="Confirmar", cancel_text="Cancelar"):
        """Mostrar diálogo de confirmación moderno"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self.parent)
        dialog.grab_set()
        dialog.configure(bg=self.colors['card'])

        # Centrar
        self._center_dialog(dialog)

        # Contenido
        tk.Label(dialog, text=icon, font=('Segoe UI', 32),
                 bg=self.colors['card'], fg=self.colors['warning']).pack(pady=(20, 10))

        tk.Label(dialog, text=message, font=self.fonts['subheading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack()

        # Botones
        btn_frame = tk.Frame(dialog, bg=self.colors['card'])
        btn_frame.pack(pady=20)

        result = {'confirmed': False}

        def confirm():
            result['confirmed'] = True
            dialog.destroy()

        def cancel():
            dialog.destroy()

        # Botón cancelar
        cancel_btn = tk.Button(btn_frame, text=cancel_text, font=self.fonts['body'],
                               bg=self.colors['bg'], fg=self.colors['text'],
                               bd=0, padx=20, pady=8, cursor='hand2',
                               command=cancel)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        # Botón confirmar
        confirm_btn = tk.Button(btn_frame, text=confirm_text, font=self.fonts['body'],
                                bg=self.colors['danger'], fg='white',
                                bd=0, padx=20, pady=8, cursor='hand2',
                                command=confirm)
        confirm_btn.pack(side=tk.LEFT, padx=5)

        dialog.wait_window()
        return result['confirmed']

    def show_delete_confirmation(self, product_name):
        """Mostrar confirmación específica para eliminar producto"""
        return self.show_confirmation_dialog(
            "Confirmar eliminación",
            f"¿Eliminar '{product_name}'?\nEsta acción no se puede deshacer",
            "🗑️",
            "Eliminar",
            "Cancelar"
        )

    def show_exit_confirmation(self):
        """Mostrar confirmación de salida"""
        return self.show_confirmation_dialog(
            "Salir",
            "¿Desea salir de la aplicación?",
            "👋",
            "Salir",
            "Cancelar"
        )

    def show_statistics_dialog(self, stats_data):
        """Mostrar estadísticas con diseño moderno"""
        stats_window = tk.Toplevel(self.parent)
        stats_window.title("Estadísticas")
        stats_window.geometry("600x500")
        stats_window.transient(self.parent)
        stats_window.grab_set()
        stats_window.configure(bg=self.colors['bg'])

        # Centrar
        self._center_dialog(stats_window)

        # Contenido
        content = tk.Frame(stats_window, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self._create_stats_header(content)

        # Grid de estadísticas principales
        self._create_main_stats_grid(content, stats_data)

        # Distribución por materiales
        self._create_materials_section(content, stats_data)

        # Botón cerrar
        close_btn = tk.Button(content, text="Cerrar", font=self.fonts['body'],
                              bg=self.colors['primary'], fg='white',
                              bd=0, padx=30, pady=10, cursor='hand2',
                              command=stats_window.destroy)
        close_btn.pack(pady=(20, 0))

    def _create_stats_header(self, parent):
        """Crear header de estadísticas"""
        header = tk.Frame(parent, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 0))

        tk.Label(header, text="📊", font=('Segoe UI', 32),
                 bg=self.colors['card']).pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(header, text="Estadísticas Generales",
                 font=self.fonts['title'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)

    def _create_main_stats_grid(self, parent, stats_data):
        """Crear grid principal de estadísticas"""
        stats_frame = tk.Frame(parent, bg=self.colors['card'])
        stats_frame.pack(fill=tk.X, padx=20, pady=20)

        # Configurar grid
        for i in range(2):
            stats_frame.grid_columnconfigure(i, weight=1)

        # Crear cards de estadísticas
        self._create_stat_display(stats_frame, "Total de Productos",
                                  str(stats_data.get('total_productos', 0)), "📦", 0, 0)

        tiempo_promedio = stats_data.get('tiempo_promedio_impresion', 0)
        self._create_stat_display(stats_frame, "Tiempo Promedio",
                                  f"{tiempo_promedio:.0f} min", "⏱️", 0, 1)

        self._create_stat_display(stats_frame, "Colores Únicos",
                                  str(stats_data.get('total_colores', 0)), "🎨", 1, 0)

        promedio_colores = stats_data.get('promedio_colores_por_producto', 0)
        self._create_stat_display(stats_frame, "Promedio Colores/Producto",
                                  f"{promedio_colores:.1f}", "📊", 1, 1)

    def _create_stat_display(self, parent, label, value, icon, row, col):
        """Crear display individual de estadística"""
        frame = tk.Frame(parent, bg=self.colors['bg'], highlightthickness=0)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        content = tk.Frame(frame, bg=self.colors['bg'])
        content.pack(expand=True, pady=20)

        tk.Label(content, text=icon, font=('Segoe UI', 24),
                 bg=self.colors['bg']).pack()
        tk.Label(content, text=value, font=('Segoe UI', 20, 'bold'),
                 bg=self.colors['bg'], fg=self.colors['primary']).pack()
        tk.Label(content, text=label, font=self.fonts['body'],
                 bg=self.colors['bg'], fg=self.colors['text_secondary']).pack()

    def _create_materials_section(self, parent, stats_data):
        """Crear sección de distribución por materiales"""
        materials_frame = tk.Frame(parent, bg=self.colors['card'])
        materials_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        tk.Label(materials_frame, text="Distribución por Material",
                 font=self.fonts['heading'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(anchor=tk.W, pady=(0, 10))

        productos_por_material = stats_data.get('productos_por_material', {})
        total_productos = stats_data.get('total_productos', 1)

        for material, cantidad in productos_por_material.items():
            self._create_material_bar(materials_frame, material, cantidad, total_productos)

    def _create_material_bar(self, parent, material, cantidad, total):
        """Crear barra de progreso para material"""
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(fill=tk.X, pady=3)

        # Label con información
        label_frame = tk.Frame(frame, bg=self.colors['card'])
        label_frame.pack(fill=tk.X)

        tk.Label(label_frame, text=material, font=self.fonts['body'],
                 bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)
        tk.Label(label_frame, text=f"{cantidad} productos", font=self.fonts['small'],
                 bg=self.colors['card'], fg=self.colors['text_secondary']).pack(side=tk.RIGHT)

        # Barra de progreso
        progress_bg = tk.Frame(frame, bg=self.colors['bg'], height=8)
        progress_bg.pack(fill=tk.X, pady=(3, 0))

        percentage = (cantidad / total) * 100 if total > 0 else 0
        progress_fill = tk.Frame(progress_bg, bg=self.colors['primary'], height=8)
        progress_fill.place(relwidth=percentage / 100, relheight=1)

    def show_export_dialog(self, productos):
        """Mostrar diálogo de exportación"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Exportar productos"
            )

            if file_path:
                # Preparar datos para exportación
                productos_data = []
                for producto in productos:
                    if hasattr(producto, 'to_dict'):
                        productos_data.append(producto.to_dict())
                    else:
                        # Fallback para productos sin método to_dict
                        productos_data.append({
                            'id': producto.id,
                            'nombre': producto.nombre,
                            'material': producto.material,
                            # Agregar más campos según sea necesario
                        })

                export_data = {
                    'version': '1.0',
                    'fecha_exportacion': datetime.datetime.now().isoformat(),
                    'total_productos': len(productos_data),
                    'productos': productos_data
                }

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)

                return True, "Datos exportados exitosamente"

            return False, "Exportación cancelada"

        except Exception as e:
            return False, f"Error al exportar: {str(e)}"

    def _center_dialog(self, dialog):
        """Centrar diálogo en la pantalla"""
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')


class NotificationSystem:
    """Sistema de notificaciones modernas"""

    def __init__(self, parent_window):
        self.parent = parent_window
        self.colors = ColorPalette.get_colors_dict()
        self.fonts = {'body': ('Segoe UI', 10)}

    def show_notification(self, mensaje, tipo='info', duration=3000):
        """Mostrar notificación moderna"""
        notif = tk.Toplevel(self.parent)
        notif.wm_overrideredirect(True)

        # Color según tipo
        colors = {
            'success': self.colors['success'],
            'error': self.colors['danger'],
            'warning': self.colors['warning'],
            'info': self.colors['primary']
        }
        bg_color = colors.get(tipo, self.colors['primary'])

        # Frame de notificación
        frame = tk.Frame(notif, bg=bg_color, padx=20, pady=10)
        frame.pack()

        tk.Label(frame, text=mensaje, font=self.fonts['body'],
                 bg=bg_color, fg='white').pack()

        # Posicionar arriba a la derecha
        notif.update_idletasks()
        x = self.parent.winfo_x() + self.parent.winfo_width() - notif.winfo_width() - 20
        y = self.parent.winfo_y() + 100
        notif.geometry(f'+{x}+{y}')

        # Auto-cerrar después del tiempo especificado
        notif.after(duration, notif.destroy)

        return notif