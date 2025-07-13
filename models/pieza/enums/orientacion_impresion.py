from enum import Enum


class OrientacionImpresion(Enum):
    """Orientaciones recomendadas para impresión"""
    VERTICAL = "Vertical"
    HORIZONTAL = "Horizontal"
    ANGULO_45 = "45°"
    ANGULO_CUSTOM = "Ángulo personalizado"
    CUALQUIERA = "Cualquiera"

    @property
    def requiere_atencion(self) -> bool:
        """Determinar si la orientación requiere atención especial"""
        return self in [self.ANGULO_45, self.ANGULO_CUSTOM]