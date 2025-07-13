from dataclasses import dataclass
from typing import List

from .enums import TipoUnion


@dataclass
class Ensamblaje:
    orden: int = 0
    tipo_union: TipoUnion = TipoUnion.ENCAJE
    notas_postproceso: str = ""

    def requiere_atencion(self) -> bool:
        return (
                self.tipo_union != TipoUnion.ENCAJE or
                bool(self.notas_postproceso.strip()) or
                self.tipo_union.requiere_herramientas
        )

    def get_herramientas_necesarias(self) -> List[str]:
        """Obtener lista de herramientas necesarias para el ensamblaje"""
        herramientas = {
            TipoUnion.TORNILLO: ["destornillador", "tornillos"],
            TipoUnion.PEGAMENTO: ["pegamento", "prensa o peso"],
            TipoUnion.SOLDADURA: ["soldador", "estaño"],
            TipoUnion.IMANES: ["imanes neodimio"],
        }
        return herramientas.get(self.tipo_union, [])

    def get_tiempo_estimado_ensamblaje(self) -> int:
        """Obtener tiempo estimado de ensamblaje en minutos"""
        tiempos = {
            TipoUnion.ENCAJE: 1,
            TipoUnion.PRESION: 2,
            TipoUnion.TORNILLO: 5,
            TipoUnion.IMANES: 3,
            TipoUnion.PEGAMENTO: 10,  # Incluye tiempo de secado
            TipoUnion.SOLDADURA: 15
        }
        return tiempos.get(self.tipo_union, 5)
