"""
Validador para productos y formularios
"""
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Resultado de validación"""
    is_valid: bool
    errors: List[str]
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class ProductValidator:
    """Validador para productos y formularios"""

    @staticmethod
    def validate_basic_fields(vars_dict: Dict[str, Any]) -> ValidationResult:
        """Validar campos básicos del producto"""
        errors = []
        warnings = []

        # Nombre (requerido)
        nombre = vars_dict.get('nombre', '').strip() if vars_dict.get('nombre') else ''
        if not nombre:
            errors.append("El nombre del producto es requerido")
        elif len(nombre) < 3:
            errors.append("El nombre debe tener al menos 3 caracteres")
        elif len(nombre) > 100:
            errors.append("El nombre no puede exceder 100 caracteres")

        # Material (requerido)
        material = vars_dict.get('material', '').strip() if vars_dict.get('material') else ''
        if not material:
            errors.append("El material es requerido")

        # Peso
        try:
            peso = float(vars_dict.get('peso', 0))
            if peso < 0:
                errors.append("El peso no puede ser negativo")
            elif peso == 0:
                warnings.append("El peso es 0. ¿Está seguro de que es correcto?")
            elif peso > 10000:
                warnings.append("El peso parece muy alto (>10kg). Verifique que sea correcto")
        except (ValueError, TypeError):
            errors.append("El peso debe ser un número válido")

        # Tiempo de impresión
        try:
            tiempo = int(vars_dict.get('tiempo_impresion', 0))
            if tiempo < 0:
                errors.append("El tiempo de impresión no puede ser negativo")
            elif tiempo == 0:
                warnings.append("El tiempo de impresión es 0. ¿Está seguro?")
            elif tiempo > 10080:  # 7 días en minutos
                warnings.append("El tiempo de impresión parece muy largo (>7 días)")
        except (ValueError, TypeError):
            errors.append("El tiempo de impresión debe ser un número entero válido")

        # Descripción (opcional pero con límites)
        descripcion = vars_dict.get('descripcion', '').strip() if vars_dict.get('descripcion') else ''
        if descripcion and len(descripcion) > 500:
            errors.append("La descripción no puede exceder 500 caracteres")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    def validate_temperature_fields(vars_dict: Dict[str, Any]) -> ValidationResult:
        """Validar campos de temperatura"""
        errors = []
        warnings = []

        # Temperatura del extrusor
        try:
            temp_extrusor = int(vars_dict.get('temperatura_extrusor', 0))
            if temp_extrusor < 150:
                errors.append("La temperatura del extrusor debe ser al menos 150°C")
            elif temp_extrusor > 300:
                errors.append("La temperatura del extrusor no debe exceder 300°C")
            elif temp_extrusor < 180:
                warnings.append("Temperatura del extrusor muy baja. Verifique el material")
        except (ValueError, TypeError):
            errors.append("La temperatura del extrusor debe ser un número válido")

        # Temperatura de la cama
        try:
            temp_cama = int(vars_dict.get('temperatura_cama', 0))
            if temp_cama < 0:
                errors.append("La temperatura de la cama no puede ser negativa")
            elif temp_cama > 120:
                errors.append("La temperatura de la cama no debe exceder 120°C")
        except (ValueError, TypeError):
            errors.append("La temperatura de la cama debe ser un número válido")

        # Validación cruzada material-temperatura
        material = vars_dict.get('material', '').upper()
        if material and 'temperatura_extrusor' in vars_dict:
            try:
                temp_extrusor = int(vars_dict['temperatura_extrusor'])
                temp_warnings = ProductValidator._validate_material_temperature(material, temp_extrusor)
                warnings.extend(temp_warnings)
            except:
                pass  # Ya se validó arriba

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    def _validate_material_temperature(material: str, temperatura: int) -> List[str]:
        """Validar temperatura según material"""
        warnings = []

        temp_ranges = {
            'PLA': (190, 220),
            'ABS': (230, 250),
            'PETG': (220, 240),
            'TPU': (210, 230),
            'NYLON': (240, 270),
            'RESINA': (25, 35)  # Para resina UV
        }

        if material in temp_ranges:
            min_temp, max_temp = temp_ranges[material]
            if temperatura < min_temp:
                warnings.append(f"Temperatura baja para {material}. Rango recomendado: {min_temp}-{max_temp}°C")
            elif temperatura > max_temp:
                warnings.append(f"Temperatura alta para {material}. Rango recomendado: {min_temp}-{max_temp}°C")

        return warnings

    @staticmethod
    def validate_color_specifications(color_specs: List) -> ValidationResult:
        """Validar especificaciones de color"""
        errors = []
        warnings = []

        if not color_specs:
            errors.append("Debe agregar al menos una especificación de color")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        total_peso = 0.0
        nombres_utilizados = set()
        colores_utilizados = set()

        for i, spec in enumerate(color_specs):
            # Validar nombre de pieza
            if not spec.nombre_pieza or not spec.nombre_pieza.strip():
                errors.append(f"Especificación {i + 1}: El nombre de la pieza es requerido")
            elif spec.nombre_pieza.strip() in nombres_utilizados:
                warnings.append(f"Especificación {i + 1}: Nombre de pieza duplicado")
            else:
                nombres_utilizados.add(spec.nombre_pieza.strip())

            # Validar peso
            try:
                peso = float(spec.peso_color)
                if peso <= 0:
                    errors.append(f"Especificación {i + 1}: El peso debe ser mayor a 0")
                elif peso > 5000:
                    warnings.append(f"Especificación {i + 1}: Peso muy alto para una pieza individual")
                total_peso += peso
            except (ValueError, TypeError):
                errors.append(f"Especificación {i + 1}: El peso debe ser un número válido")

            # Validar color
            if not spec.color_hex:
                errors.append(f"Especificación {i + 1}: Debe seleccionar un color")
            elif spec.color_hex in colores_utilizados:
                warnings.append(f"Especificación {i + 1}: Color duplicado")
            else:
                colores_utilizados.add(spec.color_hex)

            # Validar formato de color hex
            if spec.color_hex and not ProductValidator._is_valid_hex_color(spec.color_hex):
                errors.append(f"Especificación {i + 1}: Formato de color inválido")

        # Validaciones generales
        if total_peso > 10000:
            warnings.append(f"Peso total muy alto: {total_peso:.1f}g")
        elif total_peso == 0:
            errors.append("El peso total no puede ser 0")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    def _is_valid_hex_color(color: str) -> bool:
        """Validar formato de color hexadecimal"""
        if not color or not color.startswith('#'):
            return False

        if len(color) not in [4, 7]:  # #RGB o #RRGGBB
            return False

        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_guide_text(guide_text: str) -> ValidationResult:
        """Validar texto de guía"""
        errors = []
        warnings = []

        if guide_text and len(guide_text) > 5000:
            errors.append("La guía de impresión no puede exceder 5000 caracteres")

        if not guide_text or len(guide_text.strip()) < 10:
            warnings.append("La guía de impresión está vacía o muy corta")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    def validate_complete_product(vars_dict: Dict[str, Any], color_specs: List, guide_text: str,
                                  image_path: str = None) -> ValidationResult:
        """Validación completa del producto"""
        all_errors = []
        all_warnings = []

        # Validar campos básicos
        basic_result = ProductValidator.validate_basic_fields(vars_dict)
        all_errors.extend(basic_result.errors)
        all_warnings.extend(basic_result.warnings)

        # Validar temperaturas
        temp_result = ProductValidator.validate_temperature_fields(vars_dict)
        all_errors.extend(temp_result.errors)
        all_warnings.extend(temp_result.warnings)

        # Validar especificaciones de color
        color_result = ProductValidator.validate_color_specifications(color_specs)
        all_errors.extend(color_result.errors)
        all_warnings.extend(color_result.warnings)

        # Validar guía
        guide_result = ProductValidator.validate_guide_text(guide_text)
        all_errors.extend(guide_result.errors)
        all_warnings.extend(guide_result.warnings)

        # Validar imagen (opcional)
        if image_path:
            image_result = ProductValidator.validate_image_path(image_path)
            all_errors.extend(image_result.errors)
            all_warnings.extend(image_result.warnings)
        else:
            all_warnings.append("No se ha seleccionado una imagen para el producto")

        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings
        )

    @staticmethod
    def validate_image_path(image_path: str) -> ValidationResult:
        """Validar ruta de imagen"""
        errors = []
        warnings = []

        if not image_path:
            return ValidationResult(is_valid=True, errors=errors, warnings=warnings)

        import os
        from utils.file_utils import FileUtils

        # Verificar que el archivo existe
        if not os.path.exists(image_path):
            errors.append("El archivo de imagen no existe")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # Verificar que es una imagen válida
        if not FileUtils.is_valid_image(image_path):
            errors.append("El archivo no es una imagen válida")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

        # Verificar tamaño del archivo
        file_size = os.path.getsize(image_path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            warnings.append("El archivo de imagen es muy grande (>10MB)")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )


class FormValidator:
    """Validador específico para formularios en tiempo real"""

    def __init__(self):
        self.field_validators = {
            'nombre': self._validate_nombre,
            'peso': self._validate_peso,
            'tiempo_impresion': self._validate_tiempo,
            'temperatura_extrusor': self._validate_temp_extrusor,
            'temperatura_cama': self._validate_temp_cama
        }

    def validate_field(self, field_name: str, value: Any) -> Tuple[bool, str]:
        """Validar campo individual"""
        if field_name in self.field_validators:
            return self.field_validators[field_name](value)
        return True, ""

    def _validate_nombre(self, value: str) -> Tuple[bool, str]:
        """Validar nombre en tiempo real"""
        if not value:
            return False, "Requerido"
        elif len(value) < 3:
            return False, "Mínimo 3 caracteres"
        elif len(value) > 100:
            return False, "Máximo 100 caracteres"
        return True, ""

    def _validate_peso(self, value) -> Tuple[bool, str]:
        """Validar peso en tiempo real"""
        try:
            peso = float(value)
            if peso < 0:
                return False, "No puede ser negativo"
            elif peso > 10000:
                return False, "Peso muy alto"
            return True, ""
        except (ValueError, TypeError):
            return False, "Debe ser un número"

    def _validate_tiempo(self, value) -> Tuple[bool, str]:
        """Validar tiempo en tiempo real"""
        try:
            tiempo = int(value)
            if tiempo < 0:
                return False, "No puede ser negativo"
            elif tiempo > 10080:
                return False, "Tiempo muy largo"
            return True, ""
        except (ValueError, TypeError):
            return False, "Debe ser un número entero"

    def _validate_temp_extrusor(self, value) -> Tuple[bool, str]:
        """Validar temperatura del extrusor"""
        try:
            temp = int(value)
            if temp < 150:
                return False, "Mínimo 150°C"
            elif temp > 300:
                return False, "Máximo 300°C"
            return True, ""
        except (ValueError, TypeError):
            return False, "Debe ser un número"

    def _validate_temp_cama(self, value) -> Tuple[bool, str]:
        """Validar temperatura de la cama"""
        try:
            temp = int(value)
            if temp < 0:
                return False, "No puede ser negativo"
            elif temp > 120:
                return False, "Máximo 120°C"
            return True, ""
        except (ValueError, TypeError):
            return False, "Debe ser un número"