"""
Configuración central de la aplicación 3D Print Manager
"""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass
class WindowConfig:
    """Configuración de ventana"""
    title: str = "3D Print Manager • Gestión Moderna de Impresiones"
    width: int = 1650
    height: int = 800
    min_width: int = 1200
    min_height: int = 600
    icon_path: str = "assets/icon.ico"


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    db_path: str = "data/products.db"
    backup_enabled: bool = True
    backup_interval_hours: int = 24


@dataclass
class UIConfig:
    """Configuración de interfaz"""
    theme: str = "modern"
    animation_enabled: bool = True
    notification_duration: int = 3000
    auto_save_interval: int = 300  # segundos


@dataclass
class FileConfig:
    """Configuración de archivos"""
    # ✅ Cambiar para coincidir con setup_application_directories()
    images_folder: str = "assets/images"  # Era "assets/product_images"
    export_folder: str = "data/exports"   # Era "exports"
    temp_folder: str = "temp"
    backup_folder: str = "data/backups"   # ✅ Agregar esta línea
    logs_folder: str = "logs"             # ✅ Agregar esta línea
    max_image_size: Tuple[int, int] = (800, 600)
    allowed_image_formats: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')


class AppConfig:
    """Configuración central de la aplicación"""

    def __init__(self):
        self.window = WindowConfig()
        self.database = DatabaseConfig()
        self.ui = UIConfig()
        self.files = FileConfig()

        # Crear directorios si no existen
        self._create_directories()

    def _create_directories(self):
        """Crear directorios necesarios"""
        directories = [
            os.path.dirname(self.database.db_path), #/data
            self.files.images_folder, # /assets/images/
            self.files.export_folder, #data/exports/
            self.files.temp_folder, # temp/
            self.files.backup_folder, # data/backups
            self.files.logs_folder #logs/

        ]

        for directory in directories:
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except OSError as e:
                    print(f"No se pudo crear el directorio {directory}: {e}")

    def get_full_window_geometry(self):
        """Obtener geometría completa de ventana"""
        return f"{self.window.width}x{self.window.height}"

    def get_image_path(self, filename):
        """Obtener ruta completa para imagen"""
        return os.path.join(self.files.images_folder, filename)

    def get_export_path(self, filename):
        """Obtener ruta completa para exportación"""
        return os.path.join(self.files.export_folder, filename)

    def is_valid_image_format(self, filename):
        """Verificar si el formato de imagen es válido"""
        _, ext = os.path.splitext(filename.lower())
        return ext in self.files.allowed_image_formats

    def get_backup_path(self, filename):
        """Obtener ruta completa para backup"""
        return os.path.join(self.files.backup_folder, filename)

    def get_logs_path(self, filename):
        """Obtener ruta completa para logs"""
        return os.path.join(self.files.logs_folder, filename)


# Instancia global de configuración
config = AppConfig()


# Funciones de utilidad para configuración
def get_window_config():
    """Obtener configuración de ventana"""
    return config.window


def get_database_config():
    """Obtener configuración de base de datos"""
    return config.database


def get_ui_config():
    """Obtener configuración de UI"""
    return config.ui


def get_file_config():
    """Obtener configuración de archivos"""
    return config.files


def update_config(**kwargs):
    """Actualizar configuración dinámicamente"""
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            print(f"Configuración '{key}' no encontrada")


# Configuraciones específicas por entorno
class DevelopmentConfig(AppConfig):
    """Configuración para desarrollo"""

    def __init__(self):
        super().__init__()
        self.database.db_path = "data/dev_products.db"
        self.ui.animation_enabled = True


class ProductionConfig(AppConfig):
    """Configuración para producción"""

    def __init__(self):
        super().__init__()
        self.database.backup_enabled = True
        self.ui.animation_enabled = False  # Mejor rendimiento


class TestingConfig(AppConfig):
    """Configuración para testing"""

    def __init__(self):
        super().__init__()
        self.database.db_path = ":memory:"  # Base de datos en memoria
        self.files.images_folder = "test_images"


def get_config_for_environment(env="production"):
    """Obtener configuración según el entorno"""
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_class = configs.get(env, ProductionConfig)
    return config_class()


def setup_application_directories():
    """
    Crear directorios básicos necesarios para la aplicación

    Returns:
        bool: True si todo fue exitoso
    """
    # Directorio base del proyecto
    base_dir = Path(__file__).parent.parent

    # Directorios necesarios
    directories = [
        'data',  # Base de datos
        'assets',  # Recursos
        'assets/images',  # Imágenes de productos
        'logs',  # Archivos de log
        'temp',  # Archivos temporales
        'data/backups',  # Respaldos
        'data/exports'  # Exportaciones
    ]

    print("📁 Creando directorios necesarios...")

    success = True
    for directory in directories:
        dir_path = base_dir / directory
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {directory}")
        except Exception as e:
            print(f"   ❌ {directory}: {e}")
            success = False

    # Crear archivo de configuración básico si no existe
    config_file = base_dir / 'config' / 'app_settings.json'
    if not config_file.exists():
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            import json
            default_config = {
                "version": "1.0.0",
                "first_run": True,
                "theme": "modern"
            }
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            print(f"   ✅ Configuración inicial creada")
        except Exception as e:
            print(f"   ⚠️  Error creando configuración: {e}")

    if success:
        print("✅ Directorios configurados exitosamente")
    else:
        print("⚠️  Algunos directorios no se pudieron crear")

    return success