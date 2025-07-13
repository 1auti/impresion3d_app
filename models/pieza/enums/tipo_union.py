from enum import Enum


class TipoUnion(Enum):
    """Tipos de unión entre piezas"""
    ENCAJE = "Encaje"
    PEGAMENTO = "Pegamento"
    TORNILLO = "Tornillo"
    IMANES = "Imanes"
    SOLDADURA = "Soldadura"
    PRESION = "Presión"

    @property
    def requiere_herramientas(self) -> bool:
        """Determinar si el tipo de unión requiere herramientas especiales"""
        return self in [self.TORNILLO, self.SOLDADURA]

    @property
    def es_permanente(self) -> bool:
        """Determinar si la unión es permanente"""
        return self in [self.PEGAMENTO, self.SOLDADURA]