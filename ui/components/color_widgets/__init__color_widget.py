"""
Paquete de widgets modernos para manejo de colores
"""

# Widgets principales
from .color_picker import ModernColorPicker, ColorNameHelper
from .color_widget import ModernPieceColorWidget, PieceColorFactory
from .color_specification_widget import ModernColorSpecificationWidget, MultiplePiecesDialog, TemplatesDialog
from .color_filter_widget import ModernColorFilterWidget, ColorChip, ColorFilterGroup, AdvancedColorFilter

__all__ = [
    # Color Picker
    'ModernColorPicker',
    'ColorNameHelper',

    # Piece Color Widget
    'ModernPieceColorWidget',
    'PieceColorFactory',

    # Color Specification Widget
    'ModernColorSpecificationWidget',
    'MultiplePiecesDialog',
    'TemplatesDialog',

    # Color Filter Widget
    'ModernColorFilterWidget',
    'ColorChip',
    'ColorFilterGroup',
    'AdvancedColorFilter'
]

# Versión del paquete
__version__ = '1.0.0'

# Metadatos
__author__ = '3D Print Manager Team'
__description__ = 'Widgets modernos para manejo de colores en aplicaciones de impresión 3D'

# Funciones de conveniencia
def create_color_picker(parent, **kwargs):
    """Función de conveniencia para crear un color picker estándar"""
    return ModernColorPicker(parent, **kwargs)

def create_piece_widget(parent, **kwargs):
    """Función de conveniencia para crear un widget de pieza estándar"""
    return ModernPieceColorWidget(parent, **kwargs)

def create_color_specification(parent, **kwargs):
    """Función de conveniencia para crear widget de especificación completa"""
    return ModernColorSpecificationWidget(parent, **kwargs)

def create_color_filter(parent, colors_data, **kwargs):
    """Función de conveniencia para crear filtro de colores"""
    return ModernColorFilterWidget(parent, colors_data, **kwargs)

# Configuraciones predeterminadas
DEFAULT_COLOR_PALETTE = {
    'primary_colors': ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'],
    'neutral_colors': ['#000000', '#FFFFFF', '#808080', '#C0C0C0'],
    'popular_colors': ['#FFA500', '#800080', '#FFC0CB', '#A52A2A', '#008000', '#000080']
}

def get_default_colors():
    """Obtener colores predeterminados para widgets"""
    return DEFAULT_COLOR_PALETTE

# Funciones de utilidad
def hex_to_rgb(hex_color: str) -> tuple:
    """Convertir color hex a RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convertir RGB a hex"""
    return f"#{r:02x}{g:02x}{b:02x}".upper()

def get_contrasting_color(hex_color: str) -> str:
    """Obtener color contrastante (blanco o negro) para un color dado"""
    r, g, b = hex_to_rgb(hex_color)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return '#FFFFFF' if luminance < 0.5 else '#000000'

def validate_hex_color(color: str) -> bool:
    """Validar si una cadena es un color hex válido"""
    import re
    return bool(re.match(r'^#[0-9A-Fa-f]{6}$', color))

# Constantes útiles
COMMON_MATERIAL_COLORS = {
    'PLA': ['#FF0000', '#00FF00', '#0000FF', '#FFFFFF', '#000000'],
    'ABS': ['#808080', '#000000', '#FFFFFF', '#FF0000'],
    'PETG': ['#00FFFF', '#FFA500', '#800080'],
    'TPU': ['#000000', '#FF0000', '#0000FF'],
    'Resina': ['#FFFF00', '#FF00FF', '#00FFFF']
}