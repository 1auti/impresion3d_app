from dataclasses import dataclass
from typing import List


@dataclass
class MetadataPieza:
    critica: bool = False
    permite_colores_alternativos: bool = True
    es_decorativa: bool = False
    es_funcional: bool = True

    def get_prioridad(self) -> int:
        """Obtener prioridad de la pieza (1=alta, 3=baja)"""
        if self.critica:
            return 1
        elif self.es_funcional and not self.es_decorativa:
            return 2
        else:
            return 3

    def get_etiquetas(self) -> List[str]:
        """Obtener etiquetas descriptivas de la pieza"""
        etiquetas = []

        if self.critica:
            etiquetas.append("⚠️ Crítica")

        if self.es_decorativa:
            etiquetas.append("🎨 Decorativa")

        if self.es_funcional:
            etiquetas.append("⚙️ Funcional")

        if not self.permite_colores_alternativos:
            etiquetas.append("🎯 Color específico")

        return etiquetas

