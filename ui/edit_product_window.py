# ui/edit_product_window_refactored.py
"""
Ventana de edición de productos refactorizada - Versión modular y mantenible
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List

from database.db_manager import DatabaseManager
from models.producto import Producto
from config.styles import ModernTheme
from ui.components.base import (
    ModernFrame, ModernButton, StatusBadge, MessageDialog, ScrollableFrame
)
from ui.state.form_state import (
    FormStateManager, ChangeNotificationManager,
    ImageStateManager, GuideStateManager
)
from ui.tabs.product_tabs import BasicInfoTab, ColorsTab, ConfigTab, HistoryTab
from utils.file_utils import FileUtils


class ModernEditProductWindowRefactored:
    """
    Ventana de edición de productos refactorizada

    Características de la refactorización:
    - Separación de responsabilidades en múltiples clases
    - Gestión de estado centralizada
    - Componentes reutilizables
    - Configuración de estilos centralizada
    - Arquitectura modular y extensible
    """

    def __init__(self, parent, db_manager: DatabaseManager, producto: Producto):
        self.parent = parent
        self.db_manager = db_manager
        self.producto = producto
        self.producto_actualizado = False

        # Configuración del tema
        self.theme = ModernTheme()

        # Gestores de estado
        self.form_state = FormStateManager(producto)
        self.image_state = ImageStateManager(producto.imagen_path)
        self.guide_state = GuideStateManager(producto.guia_impresion or "")
        self.notification_manager = ChangeNotificationManager(self.theme)

        # Referencias a componentes
        self.status_badge = None
        self.tabs = {}

        # Configurar ventana
        self._setup_window()

        # Configurar listeners
        self._setup_listeners()

        # Crear interfaz
        self._create_interface()

        # Cargar datos iniciales
        self._load_initial_data()

    def _setup_window(self):
        """Configurar ventana principal"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Editar Producto - {self.producto.nombre}")
        self.window.geometry("1100x900")
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.configure(bg=self.theme.colors['bg'])

        # Configurar estilos TTK
        self.theme.setup_ttk_styles()

        # Centrar ventana
        self._center_window()

    def _setup_listeners(self):
        """Configurar listeners de eventos"""
        # Listener para cambios en formulario
        self.form_state.add_change_listener(self._on_form_change)

        # Listener para cambios en imagen
        self.image_state.add_change_listener(self._on_image_change)

        # Listener para cambios en guía
        self.guide_state.add_change_listener(self._on_guide_change)

    def _create_interface(self):
        """Crear interfaz principal"""
        # Container principal
        main_container = ModernFrame(self.window, self.theme, card_style=False)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self._create_header(main_container)

        # Panel de notificaciones
        changes_panel = self.notification_manager.setup_notifications(main_container)

        # Contenido principal
        content_frame = ModernFrame(main_container, self.theme, card_style=False)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        # Notebook con pestañas
        self._create_notebook(content_frame)

        # Botones de acción
        self._create_action_buttons(main_container)

    def _create_header(self, parent):
        """Crear header moderno"""
        header_frame = tk.Frame(parent, bg=self.theme.colors['primary'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=self.theme.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Icono y título
        self._create_header_title(header_content)

        # Badge de estado
        self._create_header_status(header_content)

    def _create_header_title(self, parent):
        """Crear título del header"""
        # Icono
        icon_label = tk.Label(
            parent,
            text="✏️",
            font=('Segoe UI', 32),
            bg=self.theme.colors['primary'],
            fg='white'
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 20))

        # Información del producto
        title_info = tk.Frame(parent, bg=self.theme.colors['primary'])
        title_info.pack(side=tk.LEFT, fill=tk.Y)

        # Título principal
        title_label = tk.Label(
            title_info,
            text=f"Editando: {self.producto.nombre}",
            font=self.theme.fonts['title'],
            bg=self.theme.colors['primary'],
            fg='white'
        )
        title_label.pack(anchor=tk.W)

        # Subtítulo
        subtitle_label = tk.Label(
            title_info,
            text=f"ID: {self.producto.id} • Modificar información del producto",
            font=self.theme.fonts['body'],
            bg=self.theme.colors['primary'],
            fg='white'
        )
        subtitle_label.pack(anchor=tk.W)

        # Fechas
        self._create_date_info(title_info)

    def _create_date_info(self, parent):
        """Crear información de fechas"""
        dates_info = tk.Frame(parent, bg=self.theme.colors['primary'])
        dates_info.pack(anchor=tk.W, pady=(5, 0))

        if self.producto.fecha_creacion:
            creation_label = tk.Label(
                dates_info,
                text=f"Creado: {self.producto.fecha_creacion.strftime('%d/%m/%Y %H:%M')}",
                font=self.theme.fonts['caption'],
                bg=self.theme.colors['primary'],
                fg='white'
            )
            creation_label.pack(side=tk.LEFT, padx=(0, 15))

        if self.producto.fecha_modificacion:
            modification_label = tk.Label(
                dates_info,
                text=f"Última modificación: {self.producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M')}",
                font=self.theme.fonts['caption'],
                bg=self.theme.colors['primary'],
                fg='white'
            )
            modification_label.pack(side=tk.LEFT)

    def _create_header_status(self, parent):
        """Crear status badge en header"""
        status_frame = tk.Frame(parent, bg=self.theme.colors['primary'])
        status_frame.pack(side=tk.RIGHT)

        self.status_badge = StatusBadge(status_frame, self.theme)
        badge_frame = self.status_badge.create("Sin cambios", "💾", self.theme.colors['success'])
        badge_frame.pack()

        # Configurar en notification manager
        self.notification_manager.set_status_badge(self.status_badge)

    def _create_notebook(self, parent):
        """Crear notebook con pestañas"""
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Crear pestañas
        self.tabs['basic'] = BasicInfoTab(
            self.notebook, self.theme, self.form_state, self.image_state
        )

        self.tabs['colors'] = ColorsTab(
            self.notebook, self.theme, self.form_state, self.producto
        )

        self.tabs['config'] = ConfigTab(
            self.notebook, self.theme, self.form_state
        )

        self.tabs['history'] = HistoryTab(
            self.notebook, self.theme, self.form_state, self.producto
        )

    def _create_action_buttons(self, parent):
        """Crear botones de acción"""
        btn_frame = ModernFrame(parent, self.theme, card_style=False)
        btn_frame.pack(fill=tk.X)

        # Botones de la derecha
        self._create_main_action_buttons(btn_frame)

        # Botones de la izquierda
        self._create_secondary_action_buttons(btn_frame)

    def _create_main_action_buttons(self, parent):
        """Crear botones principales de acción"""
        # Cancelar
        btn_cancel = ModernButton.create(
            parent, "❌ Cancelar", self._cancel_edit, 'secondary', self.theme
        )
        btn_cancel.pack(side=tk.RIGHT, padx=(10, 0))

        # Guardar
        btn_save = ModernButton.create(
            parent, "💾 Guardar Cambios", self._save_changes, 'primary', self.theme
        )
        btn_save.pack(side=tk.RIGHT, padx=(10, 0))

        # Restablecer
        btn_reset = ModernButton.create(
            parent, "🔄 Restablecer", self._reset_form, 'secondary', self.theme
        )
        btn_reset.pack(side=tk.RIGHT, padx=(10, 0))

    def _create_secondary_action_buttons(self, parent):
        """Crear botones secundarios de acción"""
        # Vista previa
        btn_preview = ModernButton.create(
            parent, "👁️ Vista Previa", self._show_preview, 'secondary', self.theme
        )
        btn_preview.pack(side=tk.LEFT)

    def _load_initial_data(self):
        """Cargar datos iniciales"""
        # Cargar contenido de guía en la pestaña de configuración
        if 'config' in self.tabs:
            self.tabs['config'].load_guide_content(self.producto.guia_impresion)

    def _on_form_change(self, field_name: str):
        """Manejar cambio en formulario"""
        self._update_field_style(field_name)
        self._update_notifications()

    def _on_image_change(self):
        """Manejar cambio en imagen"""
        self._update_notifications()

    def _on_guide_change(self):
        """Manejar cambio en guía"""
        self._update_notifications()

    def _update_field_style(self, field_name: str):
        """Actualizar estilo del campo según cambios"""
        entry = self.form_state.get_entry(field_name)
        if entry:
            changed_fields = self.form_state.get_changed_fields()
            field_changed = any(change.field_name == field_name for change in changed_fields)

            if field_changed:
                entry.configure(style='Modified.TEntry')
            else:
                entry.configure(style='Modern.TEntry')

    def _update_notifications(self):
        """Actualizar notificaciones de cambios"""
        changed_fields = self.form_state.get_changed_fields()
        has_image_changes = self.image_state.has_image_changes()
        has_guide_changes = self.guide_state.has_guide_changes()

        # Actualizar gestión de cambios en guía si existe la pestaña config
        if 'config' in self.tabs:
            current_guide = self.tabs['config'].get_guide_content()
            self.guide_state.on_guide_change(current_guide)

        self.notification_manager.update_notifications(
            changed_fields,
            has_image_changes or has_guide_changes
        )

    def _show_preview(self):
        """Mostrar vista previa de cambios"""
        changed_fields = self.form_state.get_changed_fields()
        changes_list = [change.field_label for change in changed_fields]

        if self.image_state.has_image_changes():
            changes_list.append('Imagen')

        if self.guide_state.has_guide_changes():
            changes_list.append('Guía de impresión')

        self._create_preview_window(changes_list)

    def _create_preview_window(self, changes: List[str]):
        """Crear ventana de vista previa"""
        preview_window = tk.Toplevel(self.window)
        preview_window.title("Vista Previa de Cambios")
        preview_window.geometry("600x500")
        preview_window.transient(self.window)
        preview_window.configure(bg=self.theme.colors['bg'])

        content = ModernFrame(preview_window, self.theme, card_style=True)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        tk.Label(
            content,
            text=f"👁️ Vista Previa: {self.form_state.get_variable('nombre').get()}",
            font=self.theme.fonts['title'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['text']
        ).pack(pady=(20, 15))

        # Lista de cambios
        if changes:
            self._create_changes_list(content, changes)
        else:
            tk.Label(
                content,
                text="✅ No hay cambios detectados",
                font=self.theme.fonts['body'],
                bg=self.theme.colors['card'],
                fg=self.theme.colors['success']
            ).pack(pady=20)

        # Información actual
        self._create_current_info_section(content)

        # Botón cerrar
        btn_close = ModernButton.create(content, "Cerrar", preview_window.destroy, 'primary', self.theme)
        btn_close.pack(pady=20)

    def _create_changes_list(self, parent, changes: List[str]):
        """Crear lista de cambios en vista previa"""
        tk.Label(
            parent,
            text=f"Cambios detectados ({len(changes)}):",
            font=self.theme.fonts['subheading'],
            bg=self.theme.colors['card'],
            fg=self.theme.colors['warning']
        ).pack(anchor=tk.W, pady=(0, 10))

        for change in changes:
            tk.Label(
                parent,
                text=f"• {change}",
                font=self.theme.fonts['body'],
                bg=self.theme.colors['card'],
                fg=self.theme.colors['text']
            ).pack(anchor=tk.W, padx=(20, 0))

    def _create_current_info_section(self, parent):
        """Crear sección de información actual"""
        info_frame = ModernFrame(parent, self.theme, card_style=False)
        info_frame.configure(bg=self.theme.colors['accent'])
        info_frame.pack(fill=tk.X, pady=(20, 0))

        info_content = tk.Frame(info_frame, bg=self.theme.colors['accent'])
        info_content.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            info_content,
            text="📋 Información actual:",
            font=self.theme.fonts['body'],
            bg=self.theme.colors['accent'],
            fg=self.theme.colors['text']
        ).pack(anchor=tk.W, pady=(0, 10))

        current_info = f"""Material: {self.form_state.get_variable('material').get()}
Peso: {self.form_state.get_variable('peso').get():.1f}g
Tiempo: {self.form_state.get_variable('tiempo_impresion').get()} min
Temp. Extrusor: {self.form_state.get_variable('temperatura_extrusor').get()}°C
Temp. Cama: {self.form_state.get_variable('temperatura_cama').get()}°C"""

        tk.Label(
            info_content,
            text=current_info,
            font=self.theme.fonts['small'],
            bg=self.theme.colors['accent'],
            fg=self.theme.colors['text'],
            justify=tk.LEFT
        ).pack(anchor=tk.W)

    def _save_changes(self):
        """Guardar cambios"""
        # Validar campos
        validation_errors = self.form_state.validate()
        if validation_errors:
            MessageDialog.show_message(
                self.window,
                "Error de validación",
                "\n".join(validation_errors),
                'error',
                self.theme
            )
            return

        # Verificar si hay cambios
        has_changes = (
            self.form_state.has_changes() or
            self.image_state.has_image_changes() or
            self.guide_state.has_guide_changes()
        )

        if not has_changes:
            MessageDialog.show_message(
                self.window,
                "Sin cambios",
                "No se detectaron cambios en el producto",
                'info',
                self.theme
            )
            return

        # Confirmar guardar
        if not self._confirm_save():
            return

        try:
            self._perform_save()
            MessageDialog.show_message(
                self.window,
                "Éxito",
                "Producto actualizado exitosamente",
                'success',
                self.theme
            )
            self.producto_actualizado = True
            self.window.after(2000, self.window.destroy)

        except Exception as e:
            MessageDialog.show_message(
                self.window,
                "Error",
                f"Error al guardar cambios: {str(e)}",
                'error',
                self.theme
            )

    def _confirm_save(self) -> bool:
        """Confirmar guardado de cambios"""
        changed_fields = self.form_state.get_changed_fields()
        changes_count = len(changed_fields)

        if self.image_state.has_image_changes():
            changes_count += 1

        if self.guide_state.has_guide_changes():
            changes_count += 1

        field_names = [change.field_label for change in changed_fields[:5]]
        if len(changed_fields) > 5:
            field_names.append("...")

        message = f"Se detectaron {changes_count} cambio(s)"
        if field_names:
            message += f":\n\n" + "\n".join(f"• {name}" for name in field_names)
        message += "\n\n¿Desea guardar los cambios?"

        return MessageDialog.show_confirmation(
            self.window,
            "Confirmar cambios",
            message,
            self.theme
        )

    def _perform_save(self):
        """Realizar guardado efectivo"""
        # Aplicar cambios del formulario
        self.form_state.apply_changes_to_producto()

        # Aplicar cambios de guía
        if 'config' in self.tabs:
            current_guide = self.tabs['config'].get_guide_content()
            self.producto.guia_impresion = current_guide

        # Manejar imagen
        if self.image_state.has_image_changes():
            self._handle_image_save()

        # Actualizar fecha de modificación
        self.producto.fecha_modificacion = datetime.now()

        # Guardar en base de datos
        success = self.db_manager.actualizar_producto(self.producto)
        if not success:
            raise Exception("No se pudo actualizar el producto en la base de datos")

    def _handle_image_save(self):
        """Manejar guardado de imagen"""
        # Eliminar imagen anterior si existe
        if self.producto.imagen_path:
            FileUtils.delete_product_image(self.producto.imagen_path)

        # Guardar nueva imagen
        current_path = self.image_state.get_current_path()
        if current_path:
            saved_path = FileUtils.save_product_image(current_path, self.producto.nombre)
            if saved_path:
                self.producto.imagen_path = saved_path
            else:
                # Si no se puede guardar la imagen, preguntar si continuar
                continue_save = MessageDialog.show_confirmation(
                    self.window,
                    "Advertencia",
                    "No se pudo guardar la imagen. ¿Continuar sin imagen?",
                    self.theme
                )
                if not continue_save:
                    raise Exception("Operación cancelada por el usuario")
                self.producto.imagen_path = None
        else:
            self.producto.imagen_path = None

    def _reset_form(self):
        """Restablecer formulario"""
        self.form_state.reset_to_original()
        self.image_state.reset_to_original()
        self.guide_state.reset_to_original()

        # Recargar datos en pestañas
        self._load_initial_data()

        # Actualizar notificaciones
        self._update_notifications()

    def _cancel_edit(self):
        """Cancelar edición"""
        has_changes = (
            self.form_state.has_changes() or
            self.image_state.has_image_changes() or
            self.guide_state.has_guide_changes()
        )

        if has_changes:
            changes_count = len(self.form_state.get_changed_fields())
            if self.image_state.has_image_changes():
                changes_count += 1
            if self.guide_state.has_guide_changes():
                changes_count += 1

            confirmed = MessageDialog.show_confirmation(
                self.window,
                "Confirmar",
                f"Hay {changes_count} cambio(s) sin guardar.\n¿Está seguro de cancelar?",
                self.theme
            )
            if confirmed:
                self.window.destroy()
        else:
            self.window.destroy()

    def _center_window(self):
        """Centrar ventana en pantalla"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')


# Función de utilidad para crear la ventana refactorizada
def create_edit_product_window(parent, db_manager: DatabaseManager, producto: Producto):
    return ModernEditProductWindowRefactored(parent, db_manager, producto)