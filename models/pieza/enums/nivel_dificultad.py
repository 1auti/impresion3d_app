from enum import Enum


class NivelDificultad(Enum):
    """Niveles de dificultad para impresiones pieza"""
    FACIL = "Fácil"
    MEDIO = "Medio"
    DIFICIL = "Difícil"
    EXPERTO = "Experto"

    @property
    def icono(self) -> str:
        """Obtener icono de dificultad"""
        iconos = {
            self.FACIL: "🟢",
            self.MEDIO: "🟡",
            self.DIFICIL: "🟠",
            self.EXPERTO: "🔴"
        }
        return iconos.get(self, "⚪")

    @property
    def valor_numerico(self) -> int:
        """Obtener valor numérico para comparaciones"""
        valores = {
            self.FACIL: 1,
            self.MEDIO: 2,
            self.DIFICIL: 3,
            self.EXPERTO: 4
        }
        return valores.get(self, 1)