from dataclasses import dataclass
from typing import List
from .enums import OrientacionImpresion,NivelDificultad

@dataclass
class ConfiguracionImpresion:
    orientacion: OrientacionImpresion = OrientacionImpresion.CUALQUIERA
    requiere_soportes: bool = False
    tolerancia_encaje: float = 0.2

    def requiere_atencion(self) -> bool:
        return (
                self.requiere_soportes or
                self.tolerancia_encaje != 0.2 or
                self.orientacion.requiere_atencion
        )

    def consejos(self, nivel: NivelDificultad) -> List[str]:
        tips = []

        if self.requiere_soportes:
            tips.append("Configurar soportes según orientación")

        if self.tolerancia_encaje != 0.2:
            tips.append(f"Tolerancia de encaje: {self.tolerancia_encaje} mm")

        if self.orientacion == OrientacionImpresion.ANGULO_45:
            tips.append("Orientación a 45° - verificar adhesión de capas")

        if self.orientacion == OrientacionImpresion.ANGULO_CUSTOM:
            tips.append("Orientación personalizada - revisar configuración")

        if nivel == NivelDificultad.DIFICIL:
            tips.append("Revisar configuración de velocidad e infill")

        if nivel == NivelDificultad.EXPERTO:
            tips.append("Requiere experiencia avanzada en impresión 3D")

        return tips
