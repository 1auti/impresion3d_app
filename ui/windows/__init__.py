""" Modulo de ventanas

 Este  modulo centraliza todas las ventanas de la apliccacion para facilitar las importarciones a otras partes del
 proyecto...

"""

# Importaciones
from .modern_detail_product import  ModernProductDetailWindow
from .modern_add_product import ModernAddProductWindow
from .modern_edit_product import ModernEditProductWindowRefactored

# Exportamos para que sea mas facil de implementar
__all__ = [
    "ModernProductDetailWindow",
    "ModernAddProductWindow",
    "ModernEditProductWindowRefactored"
]

# Funcion para verificar que todas las ventanas estan disponibles
def get_availiable_windows():
    """ Retorna lista de ventanas disponibles"""
    return __all__

# Funcion de ayuda para implementar dinamicamente
def get_windows_class(windows_name):
    """ Obtenemos una clase de ventana  por nombre"""
    windows_map = {
        'add' : ModernAddProductWindow,
        'edit' : ModernEditProductWindowRefactored,
        'details' : ModernProductDetailWindow

    }

    return windows_map.get(windows_name)
