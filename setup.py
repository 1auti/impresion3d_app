#!/usr/bin/env python3
"""
Script de configuración inicial para la aplicación de Impresión 3D
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Verificar versión de Python"""
    print("🔍 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print(f"❌ Python {version.major}.{version.minor} detectado.")
        print("⚠️  Se requiere Python 3.12 o superior.")
        return False
    print(f"✅ Python {version.major}.{version.minor} - OK")
    return True


def create_directories():
    """Crear estructura de directorios"""
    print("\n📁 Creando estructura de directorios...")

    directories = [
        "database",
        "models",
        "ui",
        "utils",
        "data",
        "assets",
        "assets/images"
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")

    print("✅ Estructura de directorios creada")


def create_init_files():
    """Crear archivos __init__.py en los paquetes"""
    print("\n📄 Creando archivos __init__.py...")

    packages = ["database", "models", "ui", "utils"]

    for package in packages:
        init_file = Path(package) / "__init__.py"
        if not init_file.exists():
            init_file.write_text(f'"""\nPaquete {package}\n"""\n')
            print(f"   ✅ {package}/__init__.py")

    print("✅ Archivos __init__.py creados")


def install_dependencies():
    """Instalar dependencias"""
    print("\n📦 Instalando dependencias...")

    try:
        # Actualizar pip
        print("   📥 Actualizando pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        # Instalar desde requirements.txt
        if Path("requirements.txt").exists():
            print("   📥 Instalando paquetes desde requirements.txt...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencias instaladas correctamente")
        else:
            print("⚠️  No se encontró requirements.txt")
            print("   Instalando Pillow manualmente...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

    return True


def verify_imports():
    """Verificar que todos los imports funcionen"""
    print("\n🔍 Verificando imports...")

    try:
        import tkinter
        print("   ✅ tkinter (interfaz gráfica)")
    except ImportError:
        print("   ❌ tkinter no está disponible")
        print("      En Linux, instala: sudo apt-get install python3-tk")
        return False

    try:
        import sqlite3
        print("   ✅ sqlite3 (base de datos)")
    except ImportError:
        print("   ❌ sqlite3 no está disponible")
        return False

    try:
        from PIL import Image
        print("   ✅ Pillow (procesamiento de imágenes)")
    except ImportError:
        print("   ❌ Pillow no está instalado")
        return False

    print("✅ Todos los imports verificados")
    return True


def create_sample_data():
    """Crear datos de ejemplo (opcional)"""
    response = input("\n¿Desea crear productos de ejemplo? (s/n): ").lower()

    if response == 's':
        print("\n📝 Creando productos de ejemplo...")
        try:
            from datebase.db_manager import DatabaseManager
            from models.producto import Producto

            db = DatabaseManager()
            db.init_database()

            # Productos de ejemplo
            productos_ejemplo = [
                Producto(
                    nombre="Soporte para Smartphone",
                    descripcion="Soporte universal ajustable para teléfonos",
                    peso=45.5,
                    color="Negro",
                    tiempo_impresion=180,
                    material="PLA",
                    temperatura_extrusor=210,
                    temperatura_cama=60,
                    guia_impresion="""Configuración recomendada:
- Altura de capa: 0.2mm
- Relleno: 20%
- Velocidad: 50mm/s
- Soportes: No necesarios
- Adhesión: Brim de 5mm

Consejos:
- Imprimir con la base plana hacia abajo
- Verificar primera capa para buena adhesión"""
                ),
                Producto(
                    nombre="Organizador de Escritorio",
                    descripcion="Organizador modular con compartimentos",
                    peso=120.0,
                    color="Azul",
                    tiempo_impresion=420,
                    material="PETG",
                    temperatura_extrusor=240,
                    temperatura_cama=80,
                    guia_impresion="""Configuración:
- Altura de capa: 0.3mm
- Relleno: 15%
- Velocidad: 40mm/s
- Primera capa lenta a 20mm/s"""
                ),
                Producto(
                    nombre="Llavero Personalizado",
                    descripcion="Llavero con diseño personalizable",
                    peso=8.5,
                    color="Rojo",
                    tiempo_impresion=45,
                    material="PLA",
                    temperatura_extrusor=200,
                    temperatura_cama=50,
                    guia_impresion="""Impresión rápida:
- Altura de capa: 0.15mm para mejor detalle
- Relleno: 100% para mayor resistencia
- Sin soportes necesarios"""
                )
            ]

            for producto in productos_ejemplo:
                db.crear_producto(producto)
                print(f"   ✅ Creado: {producto.nombre}")

            print("✅ Productos de ejemplo creados")

        except Exception as e:
            print(f"❌ Error al crear productos de ejemplo: {e}")


def main():
    """Función principal del instalador"""
    print("🖨️  CONFIGURACIÓN DE APLICACIÓN DE IMPRESIÓN 3D")
    print("=" * 50)

    # Verificar Python
    if not check_python_version():
        sys.exit(1)

    # Crear directorios
    create_directories()

    # Crear archivos init
    create_init_files()

    # Instalar dependencias
    if not install_dependencies():
        print("\n⚠️  Hubo problemas al instalar dependencias")
        print("   Intenta instalar manualmente con: pip install -r requirements.txt")

    # Verificar imports
    if not verify_imports():
        print("\n❌ Algunos componentes no están disponibles")
        sys.exit(1)

    # Datos de ejemplo
    create_sample_data()

    print("\n" + "=" * 50)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("\n🚀 Para ejecutar la aplicación:")
    print("   python main.py")
    print("\n📖 Consulta README.md para más información")


if __name__ == "__main__":
    main()