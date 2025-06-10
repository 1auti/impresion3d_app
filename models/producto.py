"""
Modelo de Producto para la aplicación de impresión 3D
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Producto:
    """Clase que representa un producto de impresión 3D"""

    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    peso: float = 0.0  # En gramos
    color: str = ""
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
        if 'fecha_creacion' in data and data['fecha_creacion']:
            data['fecha_creacion'] = datetime.fromisoformat(data['fecha_creacion'])
        if 'fecha_modificacion' in data and data['fecha_modificacion']:
            data['fecha_modificacion'] = datetime.fromisoformat(data['fecha_modificacion'])
        return cls(**data)

    def tiempo_impresion_formato(self):
        """Devolver tiempo de impresión en formato legible"""
        horas = self.tiempo_impresion // 60
        minutos = self.tiempo_impresion % 60
        if horas > 0:
            return f"{horas}h {minutos}min"
        return f"{minutos}min"

    def __str__(self):
        """Representación en string del producto"""
        return f"Producto: {self.nombre} - {self.color} - {self.tiempo_impresion_formato()}"