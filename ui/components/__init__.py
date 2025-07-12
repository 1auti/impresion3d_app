"""
Módulo de componentes UI de la aplicación

Este módulo centraliza todos los componentes de interfaz de usuario
para facilitar las importaciones y mantener una arquitectura limpia.
"""

# Importar componentes principales
from .modern_widgets import ModernWidgets
from .header import HeaderComponent
from .sidebar import SidebarComponent
from .product_list import ProductListComponent
from .detail_panel import DetailPanelComponent
from .dialogs import ModernDialogs, NotificationSystem

# Importar componentes base (si existen)
try:
    from .base import ModernFrame, ModernButton, StatusBadge, MessageDialog, ScrollableFrame
except ImportError:
    # Si no existen, crear clases placeholder o usar None
    ModernFrame = None
    ModernButton = None
    StatusBadge = None
    MessageDialog = None
    ScrollableFrame = None

# Importar tabs de formularios (si existen)
try:
    from .product_form_tabs import BasicInfoTab, ColorsTab, ConfigTab, HistoryTab
except ImportError:
    # Si no existen, crear clases placeholder
    BasicInfoTab = None
    ColorsTab = None
    ConfigTab = None
    HistoryTab = None

# Exportar para facilitar importación
__all__ = [
    # Componentes principales
    'ModernWidgets',
    'HeaderComponent',
    'SidebarComponent',
    'ProductListComponent',
    'DetailPanelComponent',
    'ModernDialogs',
    'NotificationSystem',

    # Componentes base
    'ModernFrame',
    'ModernButton',
    'StatusBadge',
    'MessageDialog',
    'ScrollableFrame',

    # Tabs de formularios
    'BasicInfoTab',
    'ColorsTab',
    'ConfigTab',
    'HistoryTab'
]


# Función helper para verificar componentes disponibles
def get_available_components():
    """Retorna diccionario con componentes disponibles"""
    available = {}
    for component_name in __all__:
        component = globals().get(component_name)
        available[component_name] = component is not None
    return available


# Función para obtener componentes principales
def get_main_components():
    """Retorna los componentes principales necesarios para la ventana principal"""
    return {
        'widgets': ModernWidgets,
        'header': HeaderComponent,
        'sidebar': SidebarComponent,
        'product_list': ProductListComponent,
        'detail_panel': DetailPanelComponent,
        'dialogs': ModernDialogs,
        'notifications': NotificationSystem
    }