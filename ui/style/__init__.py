"""
Módulo de estilos y temas de la aplicación

Este módulo centraliza todos los estilos, temas y configuraciones visuales
para mantener consistencia en toda la aplicación.
"""

# Importar estilo principal
from .modern_style import ModernStyle

# Importar otros estilos/temas (si existen)
try:
    from .dark_theme import DarkTheme
except ImportError:
    DarkTheme = None

try:
    from .light_theme import LightTheme
except ImportError:
    LightTheme = None

try:
    from .color_palette import ColorPalette
except ImportError:
    ColorPalette = None

try:
    from .font_manager import FontManager
except ImportError:
    FontManager = None

# Exportar para facilitar importación
__all__ = [
    'ModernStyle',
    'DarkTheme',
    'LightTheme',
    'ColorPalette',
    'FontManager'
]


# Función helper para obtener temas disponibles
def get_available_themes():
    """Retorna diccionario con temas disponibles"""
    available = {}
    for theme_name in __all__:
        theme = globals().get(theme_name)
        available[theme_name] = theme is not None
    return available


# Función para obtener estilo por defecto
def get_default_style():
    """Retorna el estilo por defecto de la aplicación"""
    return ModernStyle()


# Factory para crear temas dinámicamente
def create_theme(theme_type='modern'):
    """
    Factory para crear temas dinámicamente

    Args:
        theme_type (str): Tipo de tema ('modern', 'dark', 'light')

    Returns:
        Instancia del tema solicitado
    """
    themes_map = {
        'modern': ModernStyle,
        'dark': DarkTheme if DarkTheme else ModernStyle,
        'light': LightTheme if LightTheme else ModernStyle
    }

    theme_class = themes_map.get(theme_type, ModernStyle)
    return theme_class()


# Configuración global de colores
DEFAULT_COLORS = {
    'bg': '#F8FAFC',
    'card': '#FFFFFF',
    'primary': '#6366F1',
    'secondary': '#EC4899',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'text': '#1E293B',
    'text_secondary': '#64748B',
    'border': '#E2E8F0',
    'accent': '#F1F5F9'
}

# Configuración global de fuentes
DEFAULT_FONTS = {
    'title': ('Segoe UI', 20, 'bold'),
    'heading': ('Segoe UI', 14, 'bold'),
    'subheading': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9),
    'caption': ('Segoe UI', 8)
}