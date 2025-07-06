"""Configuracion de la gama de colores"""

class ColorPalette:
    """Paleta de colores para la aplicacion"""

    #Colores principales
    BG = '#F8FAFC'
    CARD = '#FFFFFF'
    PRIMARY = '#6366F1'
    PRIMARY_HOVER = '#5558E3'
    SECONDARY = '#EC4899'
    SUCCESS = '#10B981'
    WARNING = '#F59E0B'
    DANGER = '#EF4444'

    # Colores de texto
    TEXT = '#1E293B'
    TEXT_SECONDARY = '#64748B'

    # Bordes y sombras
    BORDER = '#E2E8F0'
    SHADOW = '#94A3B8'

    # Gradientes
    GRADIENT_START = '#6366F1'
    GRADIENT_END = '#EC4899'

    @classmethod
    def get_colors_dict(cls):
        """Retorna diccionario con todos los colores"""
        return {
            'bg': cls.BG,
            'card': cls.CARD,
            'primary': cls.PRIMARY,
            'primary_hover': cls.PRIMARY_HOVER,
            'secondary': cls.SECONDARY,
            'success': cls.SUCCESS,
            'warning': cls.WARNING,
            'danger': cls.DANGER,
            'text': cls.TEXT,
            'text_secondary': cls.TEXT_SECONDARY,
            'border': cls.BORDER,
            'shadow': cls.SHADOW,
            'gradient_start': cls.GRADIENT_START,
            'gradient_end': cls.GRADIENT_END
        }


