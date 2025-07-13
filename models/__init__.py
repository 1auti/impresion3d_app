
# Importar clases principales
from .producto import Producto, ColorEspecificacion

# Importar todas las clases de piezas
from .pieza import (
    Pieza,
    PiezaBuilder,
    NivelDificultad,
    OrientacionImpresion,
    TipoUnion,
    ConfiguracionImpresion,
    Ensamblaje,
    MetadataPieza
)

# Lista de todas las exportaciones
__all__ = [
    # Clases principales
    'Producto',
    'ColorEspecificacion',
    
    # Clases de piezas
    'Pieza',
    'PiezaBuilder',
    
    # Enums
    'NivelDificultad',
    'OrientacionImpresion', 
    'TipoUnion',
    
    # Clases de configuración
    'ConfiguracionImpresion',
    'Ensamblaje',
    'MetadataPieza',
]











