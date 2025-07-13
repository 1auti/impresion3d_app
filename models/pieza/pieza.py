from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from models.pieza.ensamblaje import Ensamblaje
from models.pieza.metadatos import MetadataPieza
from models.pieza.enums import NivelDificultad,OrientacionImpresion,TipoUnion
from .configuracion import  ConfiguracionImpresion


@dataclass
class Pieza:
    id: Optional[int]
    nombre: str
    descripcion: str
    peso_g: float
    tiempo_impresion_min: int
    dificultad: NivelDificultad

    configuracion: ConfiguracionImpresion = field(default_factory=ConfiguracionImpresion)
    ensamblaje: Ensamblaje = field(default_factory=Ensamblaje)
    metadata: MetadataPieza = field(default_factory=MetadataPieza)

    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if self.peso_g < 0:
            self.peso_g = 0.0
        if self.tiempo_impresion_min < 0:
            self.tiempo_impresion_min = 0

    def duracion_formateada(self) -> str:
        """Obtener duración formateada"""
        if self.tiempo_impresion_min < 60:
            return f"{self.tiempo_impresion_min}min"
        else:
            horas = self.tiempo_impresion_min // 60
            minutos = self.tiempo_impresion_min % 60
            if minutos == 0:
                return f"{horas}h"
            else:
                return f"{horas}h {minutos}min"

    def dificultad_icono(self) -> str:
        """Obtener icono de dificultad"""
        return self.dificultad.icono

    def requiere_atencion(self) -> bool:
        return (
                self.configuracion.requiere_atencion() or
                self.ensamblaje.requiere_atencion() or
                self.metadata.critica
        )

    def get_consejos_impresion(self) -> List[str]:
        """Obtener consejos específicos para la impresión"""
        return self.configuracion.consejos(self.dificultad)

    def get_consejos_ensamblaje(self) -> List[str]:
        """Obtener consejos específicos para el ensamblaje"""
        consejos = []

        if self.ensamblaje.requiere_atencion():
            if self.ensamblaje.tipo_union != TipoUnion.ENCAJE:
                consejos.append(f"Usar {self.ensamblaje.tipo_union.value.lower()} para ensamblaje")

            herramientas = self.ensamblaje.get_herramientas_necesarias()
            if herramientas:
                consejos.append(f"Herramientas necesarias: {', '.join(herramientas)}")

            if self.ensamblaje.notas_postproceso:
                consejos.append(f"Post-procesamiento: {self.ensamblaje.notas_postproceso}")

        if self.metadata.critica:
            consejos.append("⚠️ Pieza crítica - revisar calidad antes de continuar")

        return consejos

    def get_resumen_completo(self) -> str:
        """Obtener resumen completo de la pieza"""
        parts = [f"{self.dificultad_icono()} {self.nombre}"]

        if self.peso_g > 0:
            parts.append(f"({self.peso_g}g)")

        if self.tiempo_impresion_min > 0:
            parts.append(f"- {self.duracion_formateada()}")

        if self.descripcion:
            parts.append(f"- {self.descripcion}")

        etiquetas = self.metadata.get_etiquetas()
        if etiquetas:
            parts.append(f"[{', '.join(etiquetas)}]")

        return " ".join(parts)

    def get_tiempo_total_con_ensamblaje(self) -> int:
        """Obtener tiempo total incluyendo ensamblaje en minutos"""
        return self.tiempo_impresion_min + self.ensamblaje.get_tiempo_estimado_ensamblaje()

    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario para serialización"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'peso_g': self.peso_g,
            'tiempo_impresion_min': self.tiempo_impresion_min,
            'dificultad': self.dificultad.value,
            'configuracion': {
                'orientacion': self.configuracion.orientacion.value,
                'requiere_soportes': self.configuracion.requiere_soportes,
                'tolerancia_encaje': self.configuracion.tolerancia_encaje,
            },
            'ensamblaje': {
                'orden': self.ensamblaje.orden,
                'tipo_union': self.ensamblaje.tipo_union.value,
                'notas_postproceso': self.ensamblaje.notas_postproceso,
            },
            'metadata': {
                'critica': self.metadata.critica,
                'permite_colores_alternativos': self.metadata.permite_colores_alternativos,
                'es_decorativa': self.metadata.es_decorativa,
                'es_funcional': self.metadata.es_funcional,
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pieza':
        """Crear instancia desde diccionario"""
        configuracion = ConfiguracionImpresion(
            orientacion=OrientacionImpresion(data['configuracion']['orientacion']),
            requiere_soportes=data['configuracion']['requiere_soportes'],
            tolerancia_encaje=data['configuracion']['tolerancia_encaje'],
        )

        ensamblaje = Ensamblaje(
            orden=data['ensamblaje']['orden'],
            tipo_union=TipoUnion(data['ensamblaje']['tipo_union']),
            notas_postproceso=data['ensamblaje']['notas_postproceso'],
        )

        metadata = MetadataPieza(
            critica=data['metadata']['critica'],
            permite_colores_alternativos=data['metadata']['permite_colores_alternativos'],
            es_decorativa=data['metadata']['es_decorativa'],
            es_funcional=data['metadata']['es_funcional'],
        )

        return cls(
            id=data['id'],
            nombre=data['nombre'],
            descripcion=data['descripcion'],
            peso_g=data['peso_g'],
            tiempo_impresion_min=data['tiempo_impresion_min'],
            dificultad=NivelDificultad(data['dificultad']),
            configuracion=configuracion,
            ensamblaje=ensamblaje,
            metadata=metadata
        )

    @classmethod
    def from_simple_name(cls, nombre: str) -> 'Pieza':
        """Crear pieza básica desde nombre (para compatibilidad con sistema anterior)"""
        return cls(
            id=None,
            nombre=nombre,
            descripcion="",
            peso_g=0.0,
            tiempo_impresion_min=0,
            dificultad=NivelDificultad.FACIL,
        )

    def __str__(self) -> str:
        """Representación en string"""
        parts = [self.nombre]
        if self.peso_g > 0:
            parts.append(f"({self.peso_g}g)")
        if self.configuracion.requiere_soportes:
            parts.append("🏗️")
        if self.metadata.critica:
            parts.append("⚠️")
        return " ".join(parts)
