
"""
Módulo UI principal de la aplicación 3D Print Manager

Este módulo centraliza toda la interfaz de usuario de la aplicación,
proporcionando un punto de entrada limpio y organizado.
"""

#  IMPORTAR SOLO LO ESENCIAL - Ventana principal
from .main_window import ModernMainWindow

#  REFERENCIAR submódulos (sin importar todo)
from . import components
from . import controllers
from . import style
from . import windows

#  Exportar elementos principales que se usan desde fuera
__all__ = [
    'ModernMainWindow',
    'components',
    'controllers',
    'style',
    'windows'
]

# Información del módulo
__version__ = '1.0.0'
__author__ = 'Tu Nombre'
__description__ = 'Interfaz de usuario moderna para gestión de impresión 3D'


#  Función de conveniencia para crear la aplicación principal
def create_application():
    """
    Función de conveniencia para crear la aplicación principal

    Returns:
        tuple: (root, app) - Ventana root de tkinter y instancia de ModernMainWindow
    """
    import tkinter as tk
    root = tk.Tk()
    app = ModernMainWindow(root)
    return root, app


#  Función para verificar dependencias UI
def check_ui_dependencies():
    """
    Verifica que todas las dependencias UI estén disponibles

    Returns:
        dict: Diccionario con el estado de cada dependencia
    """
    dependencies = {
        'tkinter': True,  # Siempre disponible en Python estándar
        'PIL': False,
        'datetime': True,
        'pathlib': True
    }

    # Verificar PIL/Pillow
    try:
        import PIL
        dependencies['PIL'] = True
    except ImportError:
        pass

    return dependencies


#  Función para obtener información del sistema UI
def get_ui_info():
    """
    Obtiene información sobre el sistema UI

    Returns:
        dict: Información del sistema UI
    """
    import tkinter as tk

    # Crear root temporal para obtener info
    root = tk.Tk()
    root.withdraw()

    try:
        info = {
            'tkinter_version': tk.TkVersion,
            'tcl_version': tk.TclVersion,
            'screen_width': root.winfo_screenwidth(),
            'screen_height': root.winfo_screenheight(),
            'dependencies': check_ui_dependencies()
        }
    finally:
        root.destroy()

    return info


# Función helper para importación lazy de componentes pesados
def get_component(component_name):
    """
    Importación lazy de componentes específicos

    Args:
        component_name (str): Nombre del componente

    Returns:
        class: Clase del componente solicitado
    """
    component_map = {
        'main_window': lambda: ModernMainWindow,
        'header': lambda: components.HeaderComponent,
        'sidebar': lambda: components.SidebarComponent,
        'product_list': lambda: components.ProductListComponent,
        'detail_panel': lambda: components.DetailPanelComponent,
    }

    if component_name in component_map:
        return component_map[component_name]()

    raise ImportError(f"Componente '{component_name}' no encontrado")


# Configuración de logging para UI
def setup_ui_logging(level='INFO'):
    """Configurar logging para el módulo UI"""
    import logging

    logger = logging.getLogger('ui')
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger