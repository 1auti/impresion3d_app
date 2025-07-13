from .pieza import Pieza
from .enums import NivelDificultad,OrientacionImpresion,TipoUnion
from .configuracion import ConfiguracionImpresion
from .ensamblaje import Ensamblaje
from .metadatos import MetadataPieza


class PiezaBuilder:
    def __init__(self, nombre: str):
        # valores por defecto mínimos
        self.pieza = Pieza(
            id=None,
            nombre=nombre,
            descripcion="",
            peso_g=0.0,
            tiempo_impresion_min=0,
            dificultad=NivelDificultad.FACIL,
        )

    def descripcion(self, desc: str):
        """Establecer descripción de la pieza"""
        self.pieza.descripcion = desc
        return self

    def peso(self, gramos: float):
        """Establecer peso en gramos"""
        self.pieza.peso_g = gramos
        return self

    def tiempo(self, minutos: int):
        """Establecer tiempo de impresión en minutos"""
        self.pieza.tiempo_impresion_min = minutos
        return self

    def dificultad(self, nivel: NivelDificultad):
        """Establecer nivel de dificultad"""
        self.pieza.dificultad = nivel
        return self

    def configuracion(self, config: ConfiguracionImpresion):
        """Establecer configuración de impresión completa"""
        self.pieza.configuracion = config
        return self

    def orientacion(self, orientacion: OrientacionImpresion):
        """Establecer orientación de impresión"""
        self.pieza.configuracion.orientacion = orientacion
        return self

    def soportes(self, requiere: bool = True):
        """Establecer si requiere soportes"""
        self.pieza.configuracion.requiere_soportes = requiere
        return self

    def tolerancia(self, mm: float):
        """Establecer tolerancia de encaje en mm"""
        self.pieza.configuracion.tolerancia_encaje = mm
        return self

    def ensamblaje(self, ens: Ensamblaje):
        """Establecer configuración de ensamblaje completa"""
        self.pieza.ensamblaje = ens
        return self

    def orden_ensamblaje(self, orden: int):
        """Establecer orden de ensamblaje"""
        self.pieza.ensamblaje.orden = orden
        return self

    def tipo_union(self, tipo: TipoUnion):
        """Establecer tipo de unión"""
        self.pieza.ensamblaje.tipo_union = tipo
        return self

    def notas_postproceso(self, notas: str):
        """Establecer notas de post-procesamiento"""
        self.pieza.ensamblaje.notas_postproceso = notas
        return self

    def metadata(self, m: MetadataPieza):
        """Establecer metadatos completos"""
        self.pieza.metadata = m
        return self

    def critica(self, es_critica: bool = True):
        """Marcar como pieza crítica"""
        self.pieza.metadata.critica = es_critica
        return self

    def decorativa(self, es_decorativa: bool = True):
        """Marcar como pieza decorativa"""
        self.pieza.metadata.es_decorativa = es_decorativa
        if es_decorativa:
            self.pieza.metadata.es_funcional = False
        return self

    def funcional(self, es_funcional: bool = True):
        """Marcar como pieza funcional"""
        self.pieza.metadata.es_funcional = es_funcional
        if es_funcional:
            self.pieza.metadata.es_decorativa = False
        return self

    def colores_alternativos(self, permite: bool = True):
        """Establecer si permite colores alternativos"""
        self.pieza.metadata.permite_colores_alternativos = permite
        return self

    def build(self) -> Pieza:
        """Construir la pieza final"""
        return self.pieza

