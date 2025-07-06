"""
Controlador para la ventana de agregar productos
"""
import tkinter as tk
from typing import Dict, Any, Optional, Callable
from models.producto import Producto
from utils.file_utils import FileUtils
from ..validators.product_validator import ProductValidator


class AddProductController:
    """Controlador para manejar la lógica de agregar productos"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.validator = ProductValidator()

        # Variables del formulario
        self.vars = self._create_variables()

        # Referencias a componentes
        self.basic_tab = None
        self.colors_tab = None
        self.config_tab = None

        # Callbacks
        self.on_success = None
        self.on_error = None
        self.on_warning = None
        self.on_validation_error = None

        # Estado
        self.producto_creado = False

    def _create_variables(self) -> Dict[str, tk.Variable]:
        """Crear variables para los campos del formulario"""
        return {
            'nombre': tk.StringVar(),
            'descripcion': tk.StringVar(),
            'peso': tk.DoubleVar(value=0.0),
            'tiempo_impresion': tk.IntVar(value=0),
            'material': tk.StringVar(value="PLA"),
            'temperatura_extrusor': tk.IntVar(value=200),
            'temperatura_cama': tk.IntVar(value=60)
        }

    def set_components(self, basic_tab, colors_tab, config_tab):
        """Configurar referencias a los componentes de pestañas"""
        self.basic_tab = basic_tab
        self.colors_tab = colors_tab
        self.config_tab = config_tab

        # Configurar callbacks de error en las pestañas
        if hasattr(basic_tab, 'on_error'):
            basic_tab.on_error = self._handle_error
        if hasattr(colors_tab, 'on_warning'):
            colors_tab.on_warning = self._handle_warning

    def set_callbacks(self, on_success=None, on_error=None, on_warning=None, on_validation_error=None):
        """Configurar callbacks"""
        self.on_success = on_success
        self.on_error = on_error
        self.on_warning = on_warning
        self.on_validation_error = on_validation_error

    def get_variables(self) -> Dict[str, tk.Variable]:
        """Obtener variables del formulario"""
        return self.vars

    def validate_basic_fields(self) -> bool:
        """Validar campos básicos"""
        vars_dict = {name: var.get() for name, var in self.vars.items()}
        result = self.validator.validate_basic_fields(vars_dict)

        if not result.is_valid:
            self._handle_validation_errors(result.errors, "Campos básicos")
            return False

        if result.warnings:
            self._handle_warnings(result.warnings)

        return True

    def validate_temperature_fields(self) -> bool:
        """Validar campos de temperatura"""
        vars_dict = {name: var.get() for name, var in self.vars.items()}
        result = self.validator.validate_temperature_fields(vars_dict)

        if not result.is_valid:
            self._handle_validation_errors(result.errors, "Configuración de temperatura")
            return False

        if result.warnings:
            self._handle_warnings(result.warnings)

        return True

    def validate_color_specifications(self) -> bool:
        """Validar especificaciones de color"""
        if not self.colors_tab:
            return False

        color_specs = self.colors_tab.get_color_specifications()
        result = self.validator.validate_color_specifications(color_specs)

        if not result.is_valid:
            self._handle_validation_errors(result.errors, "Especificaciones de color")
            return False

        if result.warnings:
            self._handle_warnings(result.warnings)

        return True

    def validate_complete_form(self) -> bool:
        """Validar formulario completo"""
        vars_dict = {name: var.get() for name, var in self.vars.items()}

        # Obtener datos de componentes
        color_specs = self.colors_tab.get_color_specifications() if self.colors_tab else []
        guide_text = self.config_tab.get_guide_text() if self.config_tab else ""
        image_path = self.basic_tab.get_image_path() if self.basic_tab else None

        # Validación completa
        result = self.validator.validate_complete_product(vars_dict, color_specs, guide_text, image_path)

        if not result.is_valid:
            self._handle_validation_errors(result.errors, "Validación completa")
            return False

        if result.warnings:
            self._handle_warnings(result.warnings)

        return True

    def create_product(self) -> bool:
        """Crear el producto"""
        if not self.validate_complete_form():
            return False

        try:
            # Obtener especificaciones de color
            color_specs = self.colors_tab.get_color_specifications()

            # Calcular peso total
            peso_total = sum(spec.peso_color for spec in color_specs)

            # Crear objeto producto
            producto = Producto(
                nombre=self.vars['nombre'].get().strip(),
                descripcion=self.vars['descripcion'].get().strip(),
                peso=peso_total,
                color="",  # Se usa colores_especificaciones en su lugar
                colores_especificaciones=color_specs,
                tiempo_impresion=self.vars['tiempo_impresion'].get(),
                material=self.vars['material'].get(),
                temperatura_extrusor=self.vars['temperatura_extrusor'].get(),
                temperatura_cama=self.vars['temperatura_cama'].get(),
                guia_impresion=self.config_tab.get_guide_text() if self.config_tab else ""
            )

            # Guardar imagen si existe
            image_path = self.basic_tab.get_image_path() if self.basic_tab else None
            if image_path:
                saved_path = self._save_product_image(image_path, producto.nombre)
                if saved_path:
                    producto.imagen_path = saved_path
                else:
                    # Preguntar si continuar sin imagen
                    if not self._confirm_continue_without_image():
                        return False

            # Guardar en base de datos
            producto_id = self.db_manager.crear_producto(producto)

            if producto_id:
                self.producto_creado = True
                self._handle_success("Producto creado exitosamente")
                return True
            else:
                self._handle_error("No se pudo crear el producto en la base de datos")
                return False

        except Exception as e:
            self._handle_error(f"Error al crear producto: {str(e)}")
            return False

    def _save_product_image(self, image_path: str, product_name: str) -> Optional[str]:
        """Guardar imagen del producto"""
        try:
            return FileUtils.save_product_image(image_path, product_name)
        except Exception as e:
            self._handle_error(f"Error al guardar imagen: {str(e)}")
            return None

    def _confirm_continue_without_image(self) -> bool:
        """Confirmar si continuar sin imagen"""
        # Esto debería ser manejado por el componente de UI
        if self.on_warning:
            return self.on_warning("No se pudo guardar la imagen. ¿Desea continuar sin imagen?")
        return True

    def show_preview(self) -> Dict[str, Any]:
        """Obtener datos para vista previa"""
        if not self.validate_basic_fields():
            return None

        vars_dict = {name: var.get() for name, var in self.vars.items()}
        color_specs = self.colors_tab.get_color_specifications() if self.colors_tab else []
        guide_text = self.config_tab.get_guide_text() if self.config_tab else ""
        image_path = self.basic_tab.get_image_path() if self.basic_tab else None

        peso_total = sum(spec.peso_color for spec in color_specs)

        return {
            'nombre': vars_dict['nombre'],
            'descripcion': vars_dict['descripcion'],
            'material': vars_dict['material'],
            'peso_total': peso_total,
            'tiempo_impresion': vars_dict['tiempo_impresion'],
            'temperatura_extrusor': vars_dict['temperatura_extrusor'],
            'temperatura_cama': vars_dict['temperatura_cama'],
            'num_colores': len(color_specs),
            'tiene_imagen': image_path is not None,
            'tiene_guia': len(guide_text.strip()) > 0 if guide_text else False
        }

    def apply_material_preset(self, material: str) -> None:
        """Aplicar preset de material"""
        presets = {
            'PLA': {'extrusor': 200, 'cama': 60},
            'ABS': {'extrusor': 240, 'cama': 80},
            'PETG': {'extrusor': 230, 'cama': 70},
            'TPU': {'extrusor': 220, 'cama': 50},
            'NYLON': {'extrusor': 250, 'cama': 90},
            'RESINA': {'extrusor': 25, 'cama': 25}
        }

        if material.upper() in presets:
            preset = presets[material.upper()]
            self.vars['material'].set(material)
            self.vars['temperatura_extrusor'].set(preset['extrusor'])
            self.vars['temperatura_cama'].set(preset['cama'])

    def reset_form(self) -> None:
        """Resetear formulario"""
        # Resetear variables
        for var in self.vars.values():
            if isinstance(var, tk.StringVar):
                var.set("")
            elif isinstance(var, (tk.IntVar, tk.DoubleVar)):
                var.set(0)

        # Valores por defecto
        self.vars['material'].set("PLA")
        self.vars['temperatura_extrusor'].set(200)
        self.vars['temperatura_cama'].set(60)

        # Resetear componentes
        if self.basic_tab:
            self.basic_tab.quitar_imagen()

        if self.colors_tab:
            # Limpiar especificaciones de color y agregar una nueva
            for widget in self.colors_tab.color_specifications:
                widget.destroy()
            self.colors_tab.color_specifications = []
            self.colors_tab.agregar_especificacion_color()

        if self.config_tab and self.config_tab.guia_text:
            self.config_tab.guia_text.delete('1.0', 'end')

        self.producto_creado = False

    def get_form_progress(self) -> Dict[str, bool]:
        """Obtener progreso del formulario"""
        vars_dict = {name: var.get() for name, var in self.vars.items()}

        basic_complete = bool(vars_dict.get('nombre', '').strip())
        colors_complete = bool(self.colors_tab and self.colors_tab.get_color_specifications())
        config_complete = bool(
            vars_dict.get('temperatura_extrusor', 0) > 0 and
            vars_dict.get('temperatura_cama', 0) >= 0
        )

        return {
            'basic': basic_complete,
            'colors': colors_complete,
            'config': config_complete,
            'overall': basic_complete and colors_complete and config_complete
        }

    # Métodos de manejo de eventos
    def _handle_success(self, message: str):
        """Manejar evento de éxito"""
        if self.on_success:
            self.on_success(message)

    def _handle_error(self, message: str):
        """Manejar evento de error"""
        if self.on_error:
            self.on_error(message)

    def _handle_warning(self, message: str):
        """Manejar evento de advertencia"""
        if self.on_warning:
            self.on_warning(message)

    def _handle_warnings(self, warnings: list):
        """Manejar múltiples advertencias"""
        if warnings and self.on_warning:
            for warning in warnings:
                self.on_warning(warning)

    def _handle_validation_errors(self, errors: list, context: str = ""):
        """Manejar errores de validación"""
        if errors and self.on_validation_error:
            error_message = f"Errores en {context}:\n" + "\n".join(f"• {error}" for error in errors)
            self.on_validation_error(error_message)

    # Métodos de utilidad
    def is_form_dirty(self) -> bool:
        """Verificar si el formulario ha sido modificado"""
        # Verificar si algún campo tiene valores no vacíos
        for name, var in self.vars.items():
            if name in ['temperatura_extrusor', 'temperatura_cama']:
                # Estos tienen valores por defecto
                continue

            if isinstance(var, tk.StringVar) and var.get().strip():
                return True
            elif isinstance(var, (tk.IntVar, tk.DoubleVar)) and var.get() > 0:
                return True

        # Verificar imagen
        if self.basic_tab and self.basic_tab.get_image_path():
            return True

        # Verificar especificaciones de color
        if self.colors_tab:
            specs = self.colors_tab.get_color_specifications()
            if any(spec.peso_color > 0 for spec in specs):
                return True

        # Verificar guía
        if self.config_tab:
            guide = self.config_tab.get_guide_text()
            if guide and guide.strip():
                return True

        return False

    def get_summary(self) -> Dict[str, Any]:
        """Obtener resumen del producto para confirmación"""
        vars_dict = {name: var.get() for name, var in self.vars.items()}
        color_specs = self.colors_tab.get_color_specifications() if self.colors_tab else []

        return {
            'nombre': vars_dict.get('nombre', ''),
            'material': vars_dict.get('material', ''),
            'peso_total': sum(spec.peso_color for spec in color_specs),
            'tiempo': vars_dict.get('tiempo_impresion', 0),
            'num_piezas': len(color_specs),
            'tiene_imagen': bool(self.basic_tab and self.basic_tab.get_image_path()),
            'tiene_guia': bool(self.config_tab and self.config_tab.get_guide_text().strip())
        }