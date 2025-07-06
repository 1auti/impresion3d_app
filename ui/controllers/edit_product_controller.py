"""
Controlador para la edición de productos - Refactorizado
"""
from typing import Dict, List, Optional, Callable
from datetime import datetime
from models.producto import Producto
from utils.file_utils import FileUtils


class EditProductController:
    """Controlador para manejar la lógica de edición de productos"""

    def __init__(self, db_manager, producto: Producto):
        self.db_manager = db_manager
        self.producto = producto
        self.original_producto = self._create_producto_copy(producto)

        # Estado del controlador
        self.cambios_detectados = []
        self.nueva_imagen = False
        self.imagen_temporal = None

        # Callbacks
        self.on_change_detected = None
        self.on_save_success = None
        self.on_save_error = None
        self.on_validation_error = None

    def _create_producto_copy(self, producto: Producto) -> Producto:
        """Crear copia del producto para comparar cambios"""
        return Producto(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            peso=producto.peso,
            color=producto.color,
            colores_especificaciones=producto.colores_especificaciones.copy(),
            tiempo_impresion=producto.tiempo_impresion,
            material=producto.material,
            temperatura_extrusor=producto.temperatura_extrusor,
            temperatura_cama=producto.temperatura_cama,
            imagen_path=producto.imagen_path,
            guia_impresion=producto.guia_impresion,
            fecha_creacion=producto.fecha_creacion,
            fecha_modificacion=producto.fecha_modificacion
        )

    def set_callbacks(self, on_change_detected=None, on_save_success=None,
                      on_save_error=None, on_validation_error=None):
        """Configurar callbacks del controlador"""
        self.on_change_detected = on_change_detected
        self.on_save_success = on_save_success
        self.on_save_error = on_save_error
        self.on_validation_error = on_validation_error

    def update_field(self, field_name: str, new_value):
        """Actualizar un campo del producto y detectar cambios"""
        old_value = getattr(self.original_producto, field_name, None)
        setattr(self.producto, field_name, new_value)

        if new_value != old_value:
            if field_name not in self.cambios_detectados:
                self.cambios_detectados.append(field_name)
        else:
            if field_name in self.cambios_detectados:
                self.cambios_detectados.remove(field_name)

        self._notify_change_detected()

    def update_color_specifications(self, color_specs: List):
        """Actualizar especificaciones de color"""
        self.producto.colores_especificaciones = color_specs

        # Calcular peso total
        peso_total = sum(spec.peso_color for spec in color_specs)
        self.producto.peso = peso_total

        # Verificar si hay cambios
        original_specs_count = len(self.original_producto.colores_especificaciones)
        current_specs_count = len(color_specs)

        if current_specs_count != original_specs_count:
            if 'colores_especificaciones' not in self.cambios_detectados:
                self.cambios_detectados.append('colores_especificaciones')
        else:
            if 'colores_especificaciones' in self.cambios_detectados:
                self.cambios_detectados.remove('colores_especificaciones')

        self._notify_change_detected()

    def update_guide(self, guide_text: str):
        """Actualizar guía de impresión"""
        if guide_text != self.original_producto.guia_impresion:
            if 'guia_impresion' not in self.cambios_detectados:
                self.cambios_detectados.append('guia_impresion')
        else:
            if 'guia_impresion' in self.cambios_detectados:
                self.cambios_detectados.remove('guia_impresion')

        self.producto.guia_impresion = guide_text
        self._notify_change_detected()

    def set_new_image(self, image_path: Optional[str]):
        """Establecer nueva imagen"""
        self.imagen_temporal = image_path
        self.nueva_imagen = True

        if 'imagen' not in self.cambios_detectados:
            self.cambios_detectados.append('imagen')

        self._notify_change_detected()

    def remove_image(self):
        """Quitar imagen"""
        self.imagen_temporal = None
        self.nueva_imagen = True

        if 'imagen' not in self.cambios_detectados:
            self.cambios_detectados.append('imagen')

        self._notify_change_detected()

    def has_changes(self) -> bool:
        """Verificar si hay cambios pendientes"""
        return len(self.cambios_detectados) > 0 or self.nueva_imagen

    def get_changes_summary(self) -> List[str]:
        """Obtener resumen de cambios"""
        field_labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'peso': 'Peso',
            'tiempo_impresion': 'Tiempo de impresión',
            'material': 'Material',
            'temperatura_extrusor': 'Temperatura extrusor',
            'temperatura_cama': 'Temperatura cama',
            'guia_impresion': 'Guía de impresión',
            'colores_especificaciones': 'Especificaciones de color',
            'imagen': 'Imagen'
        }

        return [field_labels.get(field, field) for field in self.cambios_detectados]

    def validate_product(self) -> tuple[bool, List[str]]:
        """Validar el producto actual"""
        errors = []

        # Validar nombre
        if not self.producto.nombre.strip():
            errors.append("El nombre del producto es requerido")

        # Validar peso
        if self.producto.peso < 0:
            errors.append("El peso no puede ser negativo")

        # Validar especificaciones de color
        if not self.producto.colores_especificaciones:
            errors.append("Debe tener al menos una especificación de color")
        else:
            valid_specs = [spec for spec in self.producto.colores_especificaciones
                           if spec.peso_color > 0]
            if not valid_specs:
                errors.append("Debe tener al menos una pieza con peso mayor a 0")

        # Validar temperaturas
        if self.producto.temperatura_extrusor < 150 or self.producto.temperatura_extrusor > 300:
            errors.append("Temperatura del extrusor debe estar entre 150-300°C")

        if self.producto.temperatura_cama < 0 or self.producto.temperatura_cama > 120:
            errors.append("Temperatura de la cama debe estar entre 0-120°C")

        return len(errors) == 0, errors

    def save_changes(self) -> bool:
        """Guardar cambios del producto"""
        if not self.has_changes():
            if self.on_save_error:
                self.on_save_error("No hay cambios para guardar")
            return False

        # Validar producto
        is_valid, errors = self.validate_product()
        if not is_valid:
            if self.on_validation_error:
                self.on_validation_error(errors)
            return False

        try:
            # Manejar imagen si cambió
            if self.nueva_imagen:
                self._handle_image_update()

            # Actualizar fecha de modificación
            self.producto.fecha_modificacion = datetime.now()

            # Guardar en base de datos
            success = self.db_manager.actualizar_producto(self.producto)

            if success:
                # Actualizar estado original
                self.original_producto = self._create_producto_copy(self.producto)
                self.cambios_detectados.clear()
                self.nueva_imagen = False

                if self.on_save_success:
                    self.on_save_success("Producto actualizado exitosamente")
                return True
            else:
                if self.on_save_error:
                    self.on_save_error("No se pudo actualizar el producto en la base de datos")
                return False

        except Exception as e:
            if self.on_save_error:
                self.on_save_error(f"Error al guardar cambios: {str(e)}")
            return False

    def _handle_image_update(self):
        """Manejar actualización de imagen"""
        # Eliminar imagen anterior si existe
        if self.original_producto.imagen_path:
            FileUtils.delete_product_image(self.original_producto.imagen_path)

        # Guardar nueva imagen si existe
        if self.imagen_temporal:
            saved_path = FileUtils.save_product_image(self.imagen_temporal, self.producto.nombre)
            if saved_path:
                self.producto.imagen_path = saved_path
            else:
                raise Exception("No se pudo guardar la nueva imagen")
        else:
            self.producto.imagen_path = None

    def reset_changes(self):
        """Resetear todos los cambios"""
        self.producto = self._create_producto_copy(self.original_producto)
        self.cambios_detectados.clear()
        self.nueva_imagen = False
        self.imagen_temporal = None
        self._notify_change_detected()

    def _notify_change_detected(self):
        """Notificar que se detectaron cambios"""
        if self.on_change_detected:
            self.on_change_detected(self.cambios_detectados, self.nueva_imagen)

    def get_product_copy(self) -> Producto:
        """Obtener copia del producto actual"""
        return self._create_producto_copy(self.producto)