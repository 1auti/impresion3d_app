"""
Ventana principal modernizada y simplificada de la aplicación - CORREGIDA
"""
import tkinter as tk
from tkinter import messagebox

from .style import ModernStyle

from .components import (
    HeaderComponent,
    SidebarComponent,
    ProductListComponent,
    DetailPanelComponent,
    ModernDialogs,
    NotificationSystem,
    ModernWidgets
)
from .controllers import ProductController

from .windows import (
    ModernAddProductWindow,
    ModernEditProductWindow,
    ModernProductDetailWindow
)

# Importar otros módulos necesarios
from database.db_manager import DatabaseManager


class ModernMainWindow:
    """Ventana principal modernizada y simplificada"""

    def __init__(self, root):
        self.root = root
        self.root.title("3D Print Manager • Gestión Moderna de Impresiones")
        self.root.geometry("1650x800")

        # Configurar el ícono si existe
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass

        # Inicializar sistemas
        self._initialize_systems()

        # Crear interfaz
        self._create_interface()

        # Configurar eventos
        self._setup_events()

        # Cargar datos iniciales
        self._load_initial_data()

        # Centrar ventana
        self._center_window()

    def _initialize_systems(self):
        """Inicializar sistemas principales"""
        self.styles = ModernStyle()
        self.styles.apply_styles(self.root)

        # Base de datos
        self.db_manager = DatabaseManager()
        self.db_manager.init_database()  # Asegurar que la BD esté inicializada

        self.product_controller = ProductController(self.db_manager)

        self.dialogs = ModernDialogs(self.root)
        self.notifications = NotificationSystem(self.root)

        self.widgets = ModernWidgets(self.styles.colors, self.styles.fonts)

    def _create_interface(self):
        """Crear interfaz principal"""
        # Contenedor principal
        self.main_container = tk.Frame(self.root, bg=self.styles.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        self.header = HeaderComponent(
            self.main_container,
            on_stats_click=self._show_statistics,
            on_export_click=self._export_data
        )

        # Contenedor principal con grid
        content_frame = tk.Frame(self.main_container, bg=self.styles.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=5)

        # Configurar grid
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarComponent(content_frame, self._get_sidebar_callbacks())
        self.sidebar.grid(row=0, column=0, sticky='nsew', padx=(0, 20))

        self.product_list = ProductListComponent(
            content_frame,
            on_selection_change=self._on_product_selection_change,
            on_double_click=self._on_product_double_click
        )
        self.product_list.grid(row=0, column=1, sticky='nsew')

        self.detail_panel = DetailPanelComponent(content_frame)
        self.detail_panel.grid(row=0, column=2, sticky='nsew', padx=(20, 0))

        # Floating Action Button
        self.fab = self.widgets.create_floating_action_button(self.root, self._new_product)
        self.fab.place(relx=0.95, rely=0.9, anchor='center')

        # Barra de estado
        self._create_status_bar()

    def _create_status_bar(self):
        """Crear barra de estado"""
        self.status_bar = tk.Frame(self.root, bg=self.styles.colors['text'], height=30)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(self.status_bar, text="✓ Listo",
                                   font=self.styles.fonts['small'],
                                   bg=self.styles.colors['text'], fg='white')
        self.status_label.pack(side=tk.LEFT, padx=20)

        self.status_info = tk.Label(self.status_bar, text="",
                                  font=self.styles.fonts['small'],
                                  bg=self.styles.colors['text'], fg='white')
        self.status_info.pack(side=tk.RIGHT, padx=20)

    def _get_sidebar_callbacks(self):
        """Obtener callbacks para el sidebar"""
        return {
            'on_search': self._on_search,
            'on_new_product': self._new_product,
            'on_edit_product': self._edit_product,
            'on_view_details': self._view_details,
            'on_delete_product': self._delete_product,
            'on_color_filter_change': self._on_color_filter_change
        }

    def _setup_events(self):
        """Configurar eventos y callbacks"""
        # Configurar callbacks del controlador
        self.product_controller.set_on_productos_changed(self._on_products_changed)
        self.product_controller.set_on_selection_changed(self._on_selection_changed)
        self.product_controller.set_on_filters_changed(self._on_filters_changed)

        # Evento de cierre
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _load_initial_data(self):
        """Cargar datos iniciales"""
        try:
            success, message = self.product_controller.cargar_productos()
            if success:
                self._update_status(message)
                self._update_color_filters()
                self._update_sidebar_stats()
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    # Métodos de eventos del controlador
    def _on_products_changed(self, productos_filtrados):
        """Manejar cambio en productos"""
        try:
            self.product_list.update_product_list(productos_filtrados, self.sidebar.colores_filtrados)
            self._update_status(f"✓ Mostrando {len(productos_filtrados)} productos")
            self._update_sidebar_stats()
        except Exception as e:
            print(f"Error actualizando lista de productos: {e}")

    def _on_selection_changed(self, producto_seleccionado):
        """Manejar cambio en selección"""
        try:
            self.detail_panel.update_product_details(producto_seleccionado)
            self.sidebar.enable_buttons(producto_seleccionado is not None)
        except Exception as e:
            print(f"Error actualizando selección: {e}")

    def _on_filters_changed(self, colores_filtrados):
        """Manejar cambio en filtros"""
        try:
            self._update_color_filters()
            self._update_sidebar_stats()
        except Exception as e:
            print(f"Error actualizando filtros: {e}")

    # Métodos de eventos de la interfaz
    def _on_search(self, termino):
        """Manejar búsqueda"""
        try:
            success, message = self.product_controller.buscar_productos(termino)
            if not success:
                self.notifications.show_notification(message, 'error')
        except Exception as e:
            self.notifications.show_notification(f"Error en búsqueda: {str(e)}", 'error')

    def _on_product_selection_change(self, producto_id):
        """Manejar cambio de selección en la lista"""
        try:
            self.product_controller.seleccionar_producto(producto_id)
        except Exception as e:
            print(f"Error seleccionando producto: {e}")

    def _on_product_double_click(self, producto_id):
        """Manejar doble clic en producto"""
        self._view_details()

    def _on_color_filter_change(self, colores_filtrados):
        """Manejar cambio en filtros de color"""
        try:
            self.product_controller.aplicar_filtro_colores(colores_filtrados)
        except Exception as e:
            print(f"Error aplicando filtros: {e}")

    # Métodos de acciones
    def _new_product(self):
        """Crear nuevo producto"""
        try:
            ventana = ModernAddProductWindow(self.root, self.db_manager)
            self.root.wait_window(ventana.window)

            if ventana.producto_creado:
                self.product_controller.cargar_productos()
                self.notifications.show_notification("✓ Producto creado exitosamente", 'success')
        except Exception as e:
            self.notifications.show_notification(f"Error creando producto: {str(e)}", 'error')

    def _edit_product(self):
        """Editar producto seleccionado"""
        try:
            producto = self.product_controller.get_producto_seleccionado()
            if not producto:
                self.notifications.show_notification("Seleccione un producto para editar", 'warning')
                return

            ventana = ModernEditProductWindow(self.root, self.db_manager, producto)
            self.root.wait_window(ventana.window)

            if ventana.producto_actualizado:
                self.product_controller.cargar_productos()
                self.notifications.show_notification("✓ Producto actualizado", 'success')
        except Exception as e:
            self.notifications.show_notification(f"Error editando producto: {str(e)}", 'error')

    def _view_details(self):
        """Ver detalles del producto"""
        try:
            producto = self.product_controller.get_producto_seleccionado()
            if not producto:
                self.notifications.show_notification("Seleccione un producto para ver detalles", 'warning')
                return

            ventana = ModernProductDetailWindow(self.root, producto)
            self.root.wait_window(ventana.window)
        except Exception as e:
            self.notifications.show_notification(f"Error mostrando detalles: {str(e)}", 'error')

    def _delete_product(self):
        """Eliminar producto"""
        try:
            producto = self.product_controller.get_producto_seleccionado()
            if not producto:
                self.notifications.show_notification("Seleccione un producto para eliminar", 'warning')
                return

            if self.dialogs.show_delete_confirmation(producto.nombre):
                success, message = self.product_controller.eliminar_producto(producto)
                if success:
                    self.notifications.show_notification("✓ Producto eliminado", 'success')
                else:
                    self.notifications.show_notification(f"✕ {message}", 'error')
        except Exception as e:
            self.notifications.show_notification(f"Error eliminando producto: {str(e)}", 'error')

    def _show_statistics(self):
        """Mostrar estadísticas"""
        try:
            stats = self.product_controller.obtener_estadisticas()
            self.dialogs.show_statistics_dialog(stats)
        except Exception as e:
            self.notifications.show_notification(f"Error mostrando estadísticas: {str(e)}", 'error')

    def _export_data(self):
        """Exportar datos"""
        try:
            productos = self.product_controller.exportar_productos()
            success, message = self.dialogs.show_export_dialog(productos)

            if success:
                self.notifications.show_notification("✓ " + message, 'success')
            elif message != "Exportación cancelada":
                self.notifications.show_notification("✕ " + message, 'error')
        except Exception as e:
            self.notifications.show_notification(f"Error exportando: {str(e)}", 'error')

    # Métodos de utilidad
    def _update_color_filters(self):
        """Actualizar filtros de color"""
        try:
            colores_disponibles = self.product_controller.obtener_colores_disponibles()
            self.sidebar.update_color_filters(colores_disponibles)
        except Exception as e:
            print(f"Error actualizando filtros de color: {e}")

    def _update_sidebar_stats(self):
        """Actualizar estadísticas del sidebar"""
        try:
            stats = self.product_controller.obtener_estadisticas()
            self.sidebar.update_stats(stats)
        except Exception as e:
            print(f"Error actualizando estadísticas del sidebar: {e}")

    def _update_status(self, mensaje):
        """Actualizar barra de estado"""
        try:
            self.status_label.config(text=mensaje)

            # Mostrar fecha y hora
            from datetime import datetime
            self.status_info.config(text=datetime.now().strftime("%d/%m/%Y %H:%M"))
        except Exception as e:
            print(f"Error actualizando status: {e}")

    def _center_window(self):
        """Centrar ventana en pantalla"""
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2) - 40
            self.root.geometry(f'{width}x{height}+{x}+{y}')
        except Exception as e:
            print(f"Error centrando ventana: {e}")

    def _on_closing(self):
        """Manejar cierre de aplicación"""
        try:
            if self.dialogs.show_exit_confirmation():
                self.root.destroy()
        except Exception as e:
            print(f"Error cerrando aplicación: {e}")
            self.root.destroy()


# Para usar la ventana modernizada
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMainWindow(root)
    root.mainloop()