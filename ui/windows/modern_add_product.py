"""
Ventana modernizada y simplificada para agregar productos
"""
import tkinter as tk
from tkinter import ttk

from ..style.modern_style import ModernStyle
from ..components.modern_widgets import ModernWidgets
from ..components.product_form_tabs import BasicInfoTab, ColorsTab, ConfigTab
from ..components.dialogs import ModernDialogs, NotificationSystem
from ..controllers.add_product_controller import AddProductController
from config.app_config import config


class ModernAddProductWindow:
    """Ventana modernizada para agregar productos"""

    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.producto_creado = False

        # Inicializar sistemas
        self._initialize_systems()

        # Crear ventana
        self._create_window()

        # Crear controlador
        self._setup_controller()

        # Crear interfaz
        self._create_interface()

        # Configurar eventos
        self._setup_events()

        # Centrar ventana y configurar focus
        self._finalize_setup()

    def _initialize_systems(self):
        """Inicializar sistemas principales"""
        self.styles = ModernStyle()
        self.widgets = ModernWidgets()
        self.dialogs = ModernDialogs(None)  # Se configurará después
        self.notifications = NotificationSystem(None)  # Se configurará después

    def _create_window(self):
        """Crear y configurar ventana principal"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Agregar Nuevo Producto")
        self.window.geometry("1000x800")
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.configure(bg=self.styles.colors['bg'])

        # Configurar estilos
        self.styles.apply_styles(self.window)

        # Configurar sistemas de diálogos con la ventana
        self.dialogs = ModernDialogs(self.window)
        self.notifications = NotificationSystem(self.window)

    def _setup_controller(self):
        """Configurar controlador"""
        self.controller = AddProductController(self.db_manager)

        # Configurar callbacks del controlador
        self.controller.set_callbacks(
            on_success=self._on_success,
            on_error=self._on_error,
            on_warning=self._on_warning,
            on_validation_error=self._on_validation_error
        )

    def _create_interface(self):
        """Crear interfaz principal"""
        # Frame principal
        main_container = tk.Frame(self.window, bg=self.styles.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header moderno
        self._create_header(main_container)

        # Contenido principal
        content_frame = tk.Frame(main_container, bg=self.styles.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Notebook con pestañas
        self._create_notebook(content_frame)

        # Botones de acción
        self._create_action_buttons(main_container)

    def _create_header(self, parent):
        """Crear header moderno"""
        header_frame = tk.Frame(parent, bg=self.styles.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=self.styles.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)

        # Icono y título
        icon_label = tk.Label(header_content, text="➕", font=('Segoe UI', 28),
                              bg=self.styles.colors['primary'], fg='white')
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        title_info = tk.Frame(header_content, bg=self.styles.colors['primary'])
        title_info.pack(side=tk.LEFT)

        title_label = tk.Label(title_info, text="Agregar Nuevo Producto",
                               font=self.styles.fonts['title'],
                               bg=self.styles.colors['primary'], fg='white')
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_info, text="Complete la información del producto de impresión 3D",
                                  font=self.styles.fonts['body'],
                                  bg=self.styles.colors['primary'], fg='white')
        subtitle_label.pack(anchor=tk.W)

        # Indicador de progreso
        self.progress_label = tk.Label(header_content, text="Paso 1 de 3",
                                       font=self.styles.fonts['small'],
                                       bg=self.styles.colors['primary'], fg='white')
        self.progress_label.pack(side=tk.RIGHT)

    def _create_notebook(self, parent):
        """Crear notebook con pestañas"""
        # Configurar estilo del notebook
        style = ttk.Style()
        style.configure('Modern.TNotebook',
                        background=self.styles.colors['card'],
                        borderwidth=0, relief='flat')

        style.configure('Modern.TNotebook.Tab',
                        background=self.styles.colors['accent'],
                        foreground=self.styles.colors['text'],
                        padding=(20, 12), borderwidth=0,
                        font=self.styles.fonts['body'])

        style.map('Modern.TNotebook.Tab',
                  background=[('selected', self.styles.colors['primary']),
                              ('active', self.styles.colors['primary_hover'])],
                  foreground=[('selected', 'white'), ('active', 'white')])

        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Crear pestañas
        self._create_tabs()

        # Bind evento de cambio de pestaña
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    def _create_tabs(self):
        """Crear pestañas del formulario"""
        # Variables del controlador
        vars_dict = self.controller.get_variables()

        # Pestaña de información básica
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="📝 Información Básica")
        self.basic_tab = BasicInfoTab(basic_frame, vars_dict,
                                      colors=self.styles.colors,
                                      fonts=self.styles.fonts)

        # Pestaña de colores
        colors_frame = ttk.Frame(self.notebook)
        self.notebook.add(colors_frame, text="🎨 Colores y Piezas")
        self.colors_tab = ColorsTab(colors_frame, vars_dict,
                                    colors=self.styles.colors,
                                    fonts=self.styles.fonts)

        # Pestaña de configuración
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")
        self.config_tab = ConfigTab(config_frame, vars_dict,
                                    colors=self.styles.colors,
                                    fonts=self.styles.fonts)

        # Configurar componentes en el controlador
        self.controller.set_components(self.basic_tab, self.colors_tab, self.config_tab)

    def _create_action_buttons(self, parent):
        """Crear botones de acción"""
        btn_frame = tk.Frame(parent, bg=self.styles.colors['bg'])
        btn_frame.pack(fill=tk.X)

        # Botón cancelar
        btn_cancel = self.widgets.create_modern_button(
            btn_frame, "❌ Cancelar", self._cancel, 'secondary'
        )
        btn_cancel.pack(side=tk.RIGHT, padx=(10, 0))

        # Botón guardar
        btn_save = self.widgets.create_modern_button(
            btn_frame, "💾 Guardar Producto", self._save_product, 'primary'
        )
        btn_save.pack(side=tk.RIGHT)

        # Botón vista previa
        btn_preview = self.widgets.create_modern_button(
            btn_frame, "👁️ Vista Previa", self._show_preview, 'secondary'
        )
        btn_preview.pack(side=tk.LEFT)

        # Botón resetear (oculto inicialmente)
        self.btn_reset = self.widgets.create_modern_button(
            btn_frame, "🔄 Resetear", self._reset_form, 'secondary'
        )
        # No empaquetamos el botón reset inicialmente

    def _setup_events(self):
        """Configurar eventos"""
        # Evento de cierre de ventana
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Bind teclas de atajo
        self.window.bind('<Control-s>', lambda e: self._save_product())
        self.window.bind('<Escape>', lambda e: self._cancel())
        self.window.bind('<F5>', lambda e: self._show_preview())

    def _finalize_setup(self):
        """Finalizar configuración"""
        # Centrar ventana
        self._center_window()

        # Focus en el primer campo
        if hasattr(self.basic_tab, 'entries') and 'nombre' in self.basic_tab.entries:
            self.basic_tab.entries['nombre'].focus()

        # Actualizar indicador de progreso
        self._update_progress_indicator()

    # Métodos de eventos
    def _on_tab_changed(self, event):
        """Manejar cambio de pestaña"""
        selected_tab = self.notebook.index(self.notebook.select())
        self.progress_label.config(text=f"Paso {selected_tab + 1} de 3")

        # Validar pestaña anterior si no es la primera vez
        if hasattr(self, '_tab_visited'):
            self._validate_current_tab()

        self._tab_visited = True

    def _validate_current_tab(self):
        """Validar pestaña actual"""
        current_tab = self.notebook.index(self.notebook.select())

        if current_tab == 0:  # Información básica
            self.controller.validate_basic_fields()
        elif current_tab == 1:  # Colores
            self.controller.validate_color_specifications()
        elif current_tab == 2:  # Configuración
            self.controller.validate_temperature_fields()

    def _show_preview(self):
        """Mostrar vista previa del producto"""
        preview_data = self.controller.show_preview()
        if not preview_data:
            return

        # Crear ventana de vista previa
        preview_window = tk.Toplevel(self.window)
        preview_window.title("Vista Previa del Producto")
        preview_window.geometry("600x500")
        preview_window.transient(self.window)
        preview_window.configure(bg=self.styles.colors['bg'])

        # Contenido de vista previa
        content = tk.Frame(preview_window, bg=self.styles.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        tk.Label(content, text=f"📦 {preview_data['nombre']}",
                 font=self.styles.fonts['title'],
                 bg=self.styles.colors['card'], fg=self.styles.colors['text']).pack(pady=(20, 10))

        # Información del producto
        info_text = f"""Material: {preview_data['material']}
Peso total: {preview_data['peso_total']:.1f}g
Tiempo de impresión: {preview_data['tiempo_impresion']} min
Temperatura extrusor: {preview_data['temperatura_extrusor']}°C
Temperatura cama: {preview_data['temperatura_cama']}°C

Especificaciones de color: {preview_data['num_colores']} configuraciones
Imagen: {'Sí' if preview_data['tiene_imagen'] else 'No'}
Guía de impresión: {'Sí' if preview_data['tiene_guia'] else 'No'}"""

        tk.Label(content, text=info_text, font=self.styles.fonts['body'],
                 bg=self.styles.colors['card'], fg=self.styles.colors['text'],
                 justify=tk.LEFT).pack(pady=20)

        # Botón cerrar
        btn_close = self.widgets.create_modern_button(
            content, "Cerrar", preview_window.destroy, 'primary'
        )
        btn_close.pack(pady=20)

        # Centrar ventana de vista previa
        self._center_window_on_parent(preview_window, self.window)

    def _save_product(self):
        """Guardar producto"""
        if self.controller.create_product():
            # El éxito se maneja en el callback _on_success
            pass

    def _reset_form(self):
        """Resetear formulario"""
        if self.controller.is_form_dirty():
            if self.dialogs.show_confirmation_dialog(
                    "Resetear Formulario",
                    "¿Está seguro de que desea resetear el formulario?\nSe perderán todos los datos ingresados.",
                    "🔄"
            ):
                self.controller.reset_form()
                self.notebook.select(0)  # Volver a la primera pestaña
                self._update_progress_indicator()
                self.notifications.show_notification("Formulario reseteado", 'info')

    def _cancel(self):
        """Cancelar y cerrar ventana"""
        if self.controller.is_form_dirty():
            if self.dialogs.show_confirmation_dialog(
                    "Cancelar",
                    "¿Está seguro de que desea cancelar?\nSe perderán todos los datos ingresados.",
                    "❌"
            ):
                self.window.destroy()
        else:
            self.window.destroy()

    def _on_closing(self):
        """Manejar cierre de ventana"""
        self._cancel()

    # Callbacks del controlador
    def _on_success(self, message):
        """Manejar éxito"""
        self.producto_creado = True
        self.notifications.show_notification(f"✓ {message}", 'success')
        # Cerrar ventana después de mostrar notificación
        self.window.after(2000, self.window.destroy)

    def _on_error(self, message):
        """Manejar error"""
        self.notifications.show_notification(f"✕ {message}", 'error')

    def _on_warning(self, message):
        """Manejar advertencia"""
        return self.dialogs.show_confirmation_dialog(
            "Advertencia", message, "⚠️", "Continuar", "Cancelar"
        )

    def _on_validation_error(self, message):
        """Manejar error de validación"""
        # Mostrar diálogo con errores de validación
        dialog = tk.Toplevel(self.window)
        dialog.title("Errores de Validación")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.configure(bg=self.styles.colors['bg'])

        # Contenido
        content = tk.Frame(dialog, bg=self.styles.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header = tk.Frame(content, bg=self.styles.colors['card'])
        header.pack(fill=tk.X, pady=(0, 20))

        tk.Label(header, text="❌", font=('Segoe UI', 32),
                 bg=self.styles.colors['card'], fg=self.styles.colors['danger']).pack()

        tk.Label(header, text="Errores de Validación", font=self.styles.fonts['heading'],
                 bg=self.styles.colors['card'], fg=self.styles.colors['text']).pack(pady=(10, 0))

        # Mensaje con scroll
        from tkinter import scrolledtext
        text_widget = scrolledtext.ScrolledText(
            content, wrap=tk.WORD, height=15, font=self.styles.fonts['body'],
            bg='white', fg=self.styles.colors['text'], relief=tk.FLAT
        )
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        text_widget.insert('1.0', message)
        text_widget.config(state='disabled')

        # Botón cerrar
        btn_close = self.widgets.create_modern_button(
            content, "Cerrar", dialog.destroy, 'primary'
        )
        btn_close.pack()

        # Centrar diálogo
        self._center_window_on_parent(dialog, self.window)

    def _update_progress_indicator(self):
        """Actualizar indicador de progreso"""
        progress = self.controller.get_form_progress()

        completed = sum(1 for complete in progress.values() if complete)
        total = len(progress) - 1  # Excluir 'overall'

        self.progress_label.config(text=f"Progreso: {completed}/{total}")

        # Mostrar botón reset si hay progreso
        if completed > 0:
            self.btn_reset.pack(side=tk.LEFT, padx=(10, 0))
        else:
            self.btn_reset.pack_forget()

    # Métodos de utilidad
    def _center_window(self):
        """Centrar ventana en pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2) - 40
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def _center_window_on_parent(self, child, parent):
        """Centrar ventana hijo en ventana padre"""
        child.update_idletasks()
        parent.update_idletasks()

        x = parent.winfo_x() + (parent.winfo_width() // 2) - (child.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (child.winfo_height() // 2)

        child.geometry(f'+{x}+{y}')


# Función de conveniencia para mantener compatibilidad
def ModernAddProductWindow_Factory(parent, db_manager):
    """Factory function para crear la ventana de agregar producto"""
    return ModernAddProductWindow(parent, db_manager)