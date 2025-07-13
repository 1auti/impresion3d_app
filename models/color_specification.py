"""
Modelo de Producto para la aplicación de impresión 3D
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class ColorEspecificacion:
    """Especificación de un color para el producto"""
    color_hex: str = "#000000"  # Color en formato hexadecimal
    nombre_color: str = ""  # Nombre descriptivo del color
    piezas: List[str] = field(default_factory=list)  # Lista de piezas con este color
    peso_color: float = 0.0  # Peso en gramos para este color
    tiempo_adicional: int = 0  # Tiempo adicional si hay cambio de color
    notas: str = ""  # Notas específicas para este color

    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'color_hex': self.color_hex,
            'nombre_color': self.nombre_color,
            'piezas': self.piezas,
            'peso_color': self.peso_color,
            'tiempo_adicional': self.tiempo_adicional,
            'notas': self.notas
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crear desde diccionario"""
        return cls(**data)


@dataclass
class Producto:
    """Clase que representa un producto de impresión 3D"""

    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    peso: float = 0.0  # Peso total en gramos
    color: str = ""  # Color principal (deprecated, mantener por compatibilidad)
    colores_especificaciones: List[ColorEspecificacion] = field(default_factory=list)
    tiempo_impresion: int = 0  # En minutos
    material: str = "PLA"  # PLA, ABS, PETG, etc.
    temperatura_extrusor: int = 200  # En grados Celsius
    temperatura_cama: int = 60  # En grados Celsius
    imagen_path: Optional[str] = None
    guia_impresion: str = ""
    fecha_creacion: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not self.fecha_creacion:
            self.fecha_creacion = datetime.now()
        if not self.fecha_modificacion:
            self.fecha_modificacion = datetime.now()

    def to_dict(self):
        """Convertir el objeto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'peso': self.peso,
            'color': self.color,
            'colores_especificaciones': [c.to_dict() for c in self.colores_especificaciones],
            'tiempo_impresion': self.tiempo_impresion,
            'material': self.material,
            'temperatura_extrusor': self.temperatura_extrusor,
            'temperatura_cama': self.temperatura_cama,
            'imagen_path': self.imagen_path,
            'guia_impresion': self.guia_impresion,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crear objeto desde diccionario"""
        data = data.copy()  # Evitar modificar el original

        if 'fecha_creacion' in data and data['fecha_creacion']:
            data['fecha_creacion'] = datetime.fromisoformat(data['fecha_creacion'])
        if 'fecha_modificacion' in data and data['fecha_modificacion']:
            data['fecha_modificacion'] = datetime.fromisoformat(data['fecha_modificacion'])

        # Convertir especificaciones de color
        if 'colores_especificaciones' in data:
            color_specs = data.pop('colores_especificaciones')
            if isinstance(color_specs, list):
                data['colores_especificaciones'] = [
                    ColorEspecificacion.from_dict(cs) if isinstance(cs, dict) else cs
                    for cs in color_specs
                ]

        return cls(**data)

    def tiempo_impresion_formato(self):
        """Devolver tiempo de impresión en formato legible"""
        horas = self.tiempo_impresion // 60
        minutos = self.tiempo_impresion % 60
        if horas > 0:
            return f"{horas}h {minutos}min"
        return f"{minutos}min"

    def get_peso_total(self):
        """Calcular peso total sumando todos los colores"""
        if self.colores_especificaciones:
            return sum(c.peso_color for c in self.colores_especificaciones)
        return self.peso

    def get_tiempo_total(self):
        """Calcular tiempo total incluyendo cambios de color"""
        tiempo = self.tiempo_impresion
        if self.colores_especificaciones:
            tiempo += sum(c.tiempo_adicional for c in self.colores_especificaciones)
        return tiempo

    def get_colores_hex(self):
        """Obtener lista de colores en formato hexadecimal"""
        return [c.color_hex for c in self.colores_especificaciones]

    def get_color_principal(self):
        """Obtener el color principal (el primero o el de mayor peso)"""
        if self.colores_especificaciones:
            # Retornar el color con mayor peso
            return max(self.colores_especificaciones, key=lambda c: c.peso_color)
        return None

    def agregar_color(self, color_spec: ColorEspecificacion):
        """Agregar una especificación de color"""
        self.colores_especificaciones.append(color_spec)
        self.fecha_modificacion = datetime.now()

    def eliminar_color(self, color_hex: str):
        """Eliminar una especificación de color por su código hex"""
        self.colores_especificaciones = [
            c for c in self.colores_especificaciones if c.color_hex != color_hex
        ]
        self.fecha_modificacion = datetime.now()

    def __str__(self):
        """Representación en string del producto"""
        colores = len(self.colores_especificaciones)
        return f"Producto: {self.nombre} - {colores} color(es) - {self.tiempo_impresion_formato()}"