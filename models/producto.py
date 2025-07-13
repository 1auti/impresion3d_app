"""
Modelo de Producto para la aplicación de impresión 3D
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime

from models.color_specification import ColorEspecificacion
from models.pieza import Pieza


@dataclass
class Producto:
    """Clase que representa un producto de impresión 3D - REFACTORIZADA"""

    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    peso: float = 0.0  # Peso total en gramos (calculado automáticamente)
    color: str = ""  # Color principal (deprecated, mantener por compatibilidad)
    colores_especificaciones: List[ColorEspecificacion] = field(default_factory=list)
    tiempo_impresion: int = 0  # En minutos (tiempo base, calculado automáticamente)
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

    def get_todas_las_piezas(self) -> List[Pieza]:
        """Obtener todas las piezas del producto como objetos Pieza"""
        todas_piezas = []
        for color_spec in self.colores_especificaciones:
            todas_piezas.extend(color_spec.get_piezas_como_objetos())
        return todas_piezas

    def get_estadisticas_avanzadas(self) -> Dict[str, any]:
        """Obtener estadísticas avanzadas del producto"""
        todas_piezas = self.get_todas_las_piezas()

        if not todas_piezas:
            return {
                'total_piezas': 0,
                'peso_calculado': self.peso,
                'tiempo_calculado': self.tiempo_impresion,
                'colores_activos': len(self.colores_especificaciones),
                'piezas_criticas': 0,
                'requieren_soportes': 0,
                'dificultad_general': 'Fácil'
            }

        # Calcular estadísticas
        piezas_criticas = [p for p in todas_piezas if isinstance(p, Pieza) and p.metadata.critica]
        piezas_soportes = [p for p in todas_piezas if isinstance(p, Pieza) and p.configuracion.requiere_soportes]

        # Dificultad general (máxima entre todas las piezas)
        from models.pieza.enums import NivelDificultad
        dificultades = [p.dificultad for p in todas_piezas if isinstance(p, Pieza)]
        dificultad_maxima = NivelDificultad.FACIL
        if dificultades:
            dificultad_maxima = max(dificultades, key=lambda d: d.valor_numerico)

        return {
            'total_piezas': len(todas_piezas),
            'peso_calculado': self.get_peso_total(),
            'tiempo_calculado': self.get_tiempo_total(),
            'colores_activos': len(self.colores_especificaciones),
            'piezas_criticas': len(piezas_criticas),
            'requieren_soportes': len(piezas_soportes),
            'dificultad_general': dificultad_maxima.value
        }

    def actualizar_pesos_automaticamente(self):
        """Actualizar peso total basado en las piezas individuales"""
        self.peso = self.get_peso_total()
        self.fecha_modificacion = datetime.now()

    def actualizar_tiempos_automaticamente(self):
        """Actualizar tiempo total basado en las piezas individuales"""
        tiempo_base = 0
        for color_spec in self.colores_especificaciones:
            tiempo_base += color_spec.get_tiempo_total_piezas()

        if tiempo_base > 0:
            self.tiempo_impresion = tiempo_base

        self.fecha_modificacion = datetime.now()

    def generar_descripcion_automatica(self) -> str:
        """Generar descripción automática basada en piezas y configuración"""
        from services.description_service import DescriptionGeneratorService
        return DescriptionGeneratorService.generate_product_description(self)

    def validar_integridad(self) -> List[str]:
        """Validar integridad del producto y retornar lista de problemas"""
        problemas = []

        if not self.nombre.strip():
            problemas.append("El producto debe tener un nombre")

        if not self.colores_especificaciones:
            problemas.append("El producto debe tener al menos una especificación de color")

        todas_piezas = self.get_todas_las_piezas()
        if not todas_piezas:
            problemas.append("El producto debe tener al menos una pieza")

        # Validar que hay piezas con peso
        piezas_con_peso = [p for p in todas_piezas if isinstance(p, Pieza) and p.peso_g > 0]
        if not piezas_con_peso and self.peso <= 0:
            problemas.append("El producto debe tener peso especificado")

        # Validar temperaturas
        if self.temperatura_extrusor < 150 or self.temperatura_extrusor > 300:
            problemas.append("Temperatura del extrusor fuera del rango válido (150-300°C)")

        if self.temperatura_cama < 0 or self.temperatura_cama > 120:
            problemas.append("Temperatura de la cama fuera del rango válido (0-120°C)")

        return problemas

    # ========== MÉTODOS ORIGINALES MANTENIDOS ==========

    def to_dict(self):
        """Convertir el objeto a diccionario - MEJORADO"""
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
        """Crear objeto desde diccionario - MEJORADO"""
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
        """Calcular peso total sumando todos los colores - MEJORADO"""
        if self.colores_especificaciones:
            # Intentar usar peso calculado de piezas primero
            peso_calculado = sum(c.get_peso_calculado() for c in self.colores_especificaciones)
            return peso_calculado if peso_calculado > 0 else self.peso
        return self.peso

    def get_tiempo_total(self):
        """Calcular tiempo total incluyendo cambios de color - MEJORADO"""
        tiempo_base = self.tiempo_impresion

        # Sumar tiempo de piezas individuales si está disponible
        tiempo_piezas = 0
        for color_spec in self.colores_especificaciones:
            tiempo_piezas += color_spec.get_tiempo_total_piezas()

        if tiempo_piezas > 0:
            tiempo_base = tiempo_piezas

        # Agregar tiempo adicional por cambios de color
        if self.colores_especificaciones:
            tiempo_base += sum(c.tiempo_adicional for c in self.colores_especificaciones)

        return tiempo_base

    def get_colores_hex(self):
        """Obtener lista de colores en formato hexadecimal"""
        return [c.color_hex for c in self.colores_especificaciones]

    def get_color_principal(self):
        """Obtener el color principal (el primero o el de mayor peso)"""
        if self.colores_especificaciones:
            # Retornar el color con mayor peso (usando peso calculado)
            return max(self.colores_especificaciones, key=lambda c: c.get_peso_calculado())
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
        """Representación en string del producto - MEJORADA"""
        colores = len(self.colores_especificaciones)
        total_piezas = len(self.get_todas_las_piezas())
        return f"Producto: {self.nombre} - {total_piezas} pieza(s) - {colores} color(es) - {self.tiempo_impresion_formato()}"

