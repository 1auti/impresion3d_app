"""
Módulo de controladores de la aplicación

Este módulo centraliza todos los controladores que manejan la lógica de negocio
y la comunicación entre la interfaz de usuario y la base de datos.
"""

# Importar controladores principales
from .product_controller import ProductController

# Importar controladores específicos (si existen)
try:
    from .add_product_controller import AddProductController
except ImportError:
    AddProductController = None

try:
    from .edit_product_controller import EditProductController
except ImportError:
    EditProductController = None

try:
    from .search_controller import SearchController
except ImportError:
    SearchController = None

try:
    from .export_controller import ExportController
except ImportError:
    ExportController = None

# Exportar para facilitar importación
__all__ = [
    'ProductController',
    'AddProductController',
    'EditProductController',
    'SearchController',
    'ExportController'
]


# Función helper para obtener controladores disponibles
def get_available_controllers():
    """Retorna diccionario con controladores disponibles"""
    available = {}
    for controller_name in __all__:
        controller = globals().get(controller_name)
        available[controller_name] = controller is not None
    return available


# Función para obtener controlador principal
def get_main_controller(db_manager):
    """Retorna el controlador principal de productos"""
    return ProductController(db_manager)


# Factory para crear controladores específicos
def create_controller(controller_type, *args, **kwargs):
    """
    Factory para crear controladores dinámicamente

    Args:
        controller_type (str): Tipo de controlador ('product', 'add', 'edit', etc.)
        *args, **kwargs: Argumentos para el constructor del controlador

    Returns:
        Instancia del controlador solicitado o None si no existe
    """
    controllers_map = {
        'product': ProductController,
        'add_product': AddProductController,
        'edit_product': EditProductController,
        'search': SearchController,
        'export': ExportController
    }

    controller_class = controllers_map.get(controller_type)
    if controller_class:
        return controller_class(*args, **kwargs)
    return None