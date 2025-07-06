# ui/state/form_state.py
"""
Gestión de estado del formulario y detección de cambios
"""

import tkinter as tk
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from models.producto import Producto


@dataclass
class FieldChange:
    """Representa un cambio en un campo"""
    field_name: str
    original_value: Any
    current_value: Any
    field_label: str


class FormStateManager:
    """Gestor de estado del formulario con detección de cambios"""

    def __init__(self, producto: Producto):
        self.producto = producto
        self.variables: Dict[str, tk.Variable] = {}
        self.entries: Dict[str, tk.Widget] = {}
        self.original_values: Dict[str, Any] = {}
        self.change_listeners: List[Callable] = []
        self.field_labels: Dict[str, str] = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'peso': 'Peso',
            'tiempo_impresion': 'Tiempo de impresión',
            'material': 'Material',
            'temperatura_extrusor': 'Temperatura extrusor',
            'temperatura_cama': 'Temperatura cama'
        }
        self._setup_variables()

    def _setup_variables(self):
        """Configurar variables del formulario"""
        self.variables = {
            'nombre': tk.StringVar(value=self.producto.nombre),
            'descripcion': tk.StringVar(value=self.producto.descripcion or ""),
            'peso': tk.DoubleVar(value=self.producto.peso),
            'tiempo_impresion': tk.IntVar(value=self.producto.tiempo_impresion),
            'material': tk.StringVar(value=self.producto.material),
            'temperatura_extrusor': tk.IntVar(value=self.producto.temperatura_extrusor),
            'temperatura_cama': tk.IntVar(value=self.producto.temperatura_cama)
        }

        # Guardar valores originales
        self.original_values = {k: v.get() for k, v in self.variables.items()}

        # Configurar detección de cambios
        for var_name, var in self.variables.items():
            var.trace('w', lambda *args, vn=var_name: self._on_variable_change(vn))

    def add_change_listener(self, listener: Callable):
        """Agregar listener para cambios"""
        self.change_listeners.append(listener)

    def _on_variable_change(self, var_name: str):
        """Manejar cambio en variable"""
        for listener in self.change_listeners:
            listener(var_name)

    def get_variable(self, name: str) -> tk.Variable:
        """Obtener variable por nombre"""
        return self.variables.get(name)

    def get_all_variables(self) -> Dict[str, tk.Variable]:
        """Obtener todas las variables"""
        return self.variables.copy()

    def register_entry(self, name: str, widget: tk.Widget):
        """Registrar widget de entrada"""
        self.entries[name] = widget

    def get_entry(self, name: str) -> tk.Widget:
        """Obtener widget de entrada"""
        return self.entries.get(name)

    def get_changed_fields(self) -> List[FieldChange]:
        """Obtener campos que han cambiado"""
        changes = []
        for var_name, variable in self.variables.items():
            current_value = variable.get()
            original_value = self.original_values[var_name]

            if current_value != original_value:
                changes.append(FieldChange(
                    field_name=var_name,
                    original_value=original_value,
                    current_value=current_value,
                    field_label=self.field_labels.get(var_name, var_name)
                ))

        return changes

    def has_changes(self) -> bool:
        """Verificar si hay cambios"""
        return len(self.get_changed_fields()) > 0

    def reset_to_original(self):
        """Resetear todos los valores a los originales"""
        for var_name, original_value in self.original_values.items():
            self.variables[var_name].set(original_value)

    def apply_changes_to_producto(self) -> Producto:
        """Aplicar cambios al producto"""
        self.producto.nombre = self.variables['nombre'].get().strip()
        self.producto.descripcion = self.variables['descripcion'].get().strip()
        self.producto.peso = self.variables['peso'].get()
        self.producto.tiempo_impresion = self.variables['tiempo_impresion'].get()
        self.producto.material = self.variables['material'].get()
        self.producto.temperatura_extrusor = self.variables['temperatura_extrusor'].get()
        self.producto.temperatura_cama = self.variables['temperatura_cama'].get()

        return self.producto

    def validate(self) -> List[str]:
        """Validar campos del formulario"""
        errors = []

        if not self.variables['nombre'].get().strip():
            errors.append("El nombre del producto es requerido")

        try:
            peso = self.variables['peso'].get()
            if peso < 0:
                errors.append("El peso no puede ser negativo")
        except (ValueError, tk.TclError):
            errors.append("El peso debe ser un número válido")

        try:
            tiempo = self.variables['tiempo_impresion'].get()
            if tiempo < 0:
                errors.append("El tiempo de impresión no puede ser negativo")
        except (ValueError, tk.TclError):
            errors.append("El tiempo de impresión debe ser un número válido")

        return errors


class ChangeNotificationManager:
    """Gestor de notificaciones de cambios"""

    def __init__(self, theme):
        self.theme = theme
        self.changes_panel = None
        self.status_badge = None
        self.is_panel_visible = False

    def setup_notifications(self, parent_frame):
        """Configurar panel de notificaciones"""
        # Panel de cambios (inicialmente oculto)
        self.changes_panel = tk.Frame(parent_frame, bg=self.theme.colors['warning'], height=40)
        return self.changes_panel

    def update_notifications(self, changed_fields: List[FieldChange],
                             has_image_changes: bool = False):
        """Actualizar notificaciones basadas en cambios"""
        total_changes = len(changed_fields)

        if total_changes > 0 or has_image_changes:
            self._show_changes_panel(changed_fields)
            self._update_status_badge(total_changes, warning=True)
        else:
            self._hide_changes_panel()
            self._update_status_badge(0, warning=False)

    def _show_changes_panel(self, changed_fields: List[FieldChange]):
        """Mostrar panel de cambios"""
        if not self.is_panel_visible:
            self.changes_panel.pack(fill=tk.X, pady=(20, 0))
            self.is_panel_visible = True

        # Limpiar contenido anterior
        for widget in self.changes_panel.winfo_children():
            widget.destroy()

        content = tk.Frame(self.changes_panel, bg=self.theme.colors['warning'])
        content.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            content,
            text="⚠️",
            font=self.theme.fonts['body'],
            bg=self.theme.colors['warning'],
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))

        field_names = [change.field_label for change in changed_fields]
        changes_text = f"Campos modificados: {', '.join(field_names)}"
        tk.Label(
            content,
            text=changes_text,
            font=self.theme.fonts['small'],
            bg=self.theme.colors['warning'],
            fg='white'
        ).pack(side=tk.LEFT)

    def _hide_changes_panel(self):
        """Ocultar panel de cambios"""
        if self.is_panel_visible:
            self.changes_panel.pack_forget()
            self.is_panel_visible = False

    def _update_status_badge(self, change_count: int, warning: bool):
        """Actualizar badge de estado"""
        if self.status_badge:
            if warning:
                color = self.theme.colors['warning']
                text = f"{change_count} cambio(s)"
                icon = "⚠️"
            else:
                color = self.theme.colors['success']
                text = "Sin cambios"
                icon = "✅"

            self.status_badge.update(text, icon, color)

    def set_status_badge(self, status_badge):
        """Configurar badge de estado"""
        self.status_badge = status_badge


class ImageStateManager:
    """Gestor de estado para imágenes"""

    def __init__(self, initial_path: str = None):
        self.original_path = initial_path
        self.current_path = initial_path
        self.has_changes = False
        self.change_listeners: List[Callable] = []

    def add_change_listener(self, listener: Callable):
        """Agregar listener para cambios de imagen"""
        self.change_listeners.append(listener)

    def set_image_path(self, new_path: str):
        """Establecer nueva ruta de imagen"""
        self.current_path = new_path
        self.has_changes = (new_path != self.original_path)

        for listener in self.change_listeners:
            listener()

    def remove_image(self):
        """Eliminar imagen"""
        self.current_path = None
        self.has_changes = True

        for listener in self.change_listeners:
            listener()

    def has_image_changes(self) -> bool:
        """Verificar si hay cambios en la imagen"""
        return self.has_changes

    def get_current_path(self) -> str:
        """Obtener ruta actual"""
        return self.current_path

    def reset_to_original(self):
        """Resetear a imagen original"""
        self.current_path = self.original_path
        self.has_changes = False

        for listener in self.change_listeners:
            listener()


class GuideStateManager:
    """Gestor de estado para la guía de impresión"""

    def __init__(self, initial_guide: str = ""):
        self.original_guide = initial_guide
        self.has_changes = False
        self.change_listeners: List[Callable] = []

    def add_change_listener(self, listener: Callable):
        """Agregar listener para cambios"""
        self.change_listeners.append(listener)

    def on_guide_change(self, current_guide: str):
        """Manejar cambio en guía"""
        self.has_changes = (current_guide != self.original_guide)

        for listener in self.change_listeners:
            listener()

    def has_guide_changes(self) -> bool:
        """Verificar si hay cambios en la guía"""
        return self.has_changes

    def reset_to_original(self):
        """Resetear a guía original"""
        self.has_changes = False

        for listener in self.change_listeners:
            listener()