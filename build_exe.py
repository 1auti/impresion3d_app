#!/usr/bin/env python3
"""
Script para construir ejecutable de la aplicación usando PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def check_pyinstaller():
    """Verificar si PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("❌ PyInstaller no está instalado")
        response = input("¿Desea instalarlo ahora? (s/n): ").lower()
        if response == 's':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
                print("✅ PyInstaller instalado correctamente")
                return True
            except:
                print("❌ Error al instalar PyInstaller")
                print("   Instálelo manualmente con: pip install pyinstaller")
                return False
        return False


def create_spec_file():
    """Crear archivo .spec personalizado para PyInstaller"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database/*.py', 'database'),
        ('models/*.py', 'models'),
        ('ui/*.py', 'ui'),
        ('utils/*.py', 'utils'),
        ('assets', 'assets'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.colorchooser',
        'sqlite3',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GestionImpresion3D',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # False para no mostrar consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GestionImpresion3D',
)
"""

    with open('impresion3d.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print("✅ Archivo .spec creado")


def create_icon():
    """Crear un icono simple si no existe"""
    icon_path = Path("assets/icon.ico")
    if not icon_path.exists():
        print("⚠️  No se encontró icono. Creando uno temporal...")
        try:
            from PIL import Image, ImageDraw

            # Crear imagen simple con logo 3D
            img = Image.new('RGBA', (256, 256), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            # Dibujar un cubo simple (representando impresión 3D)
            # Cara frontal
            draw.rectangle([60, 100, 160, 200], fill=(0, 120, 212), outline=(0, 80, 160))
            # Cara superior
            draw.polygon([(60, 100), (110, 50), (210, 50), (160, 100)],
                         fill=(0, 150, 255), outline=(0, 80, 160))
            # Cara lateral
            draw.polygon([(160, 100), (210, 50), (210, 150), (160, 200)],
                         fill=(0, 100, 180), outline=(0, 80, 160))

            # Guardar como ICO
            img.save(icon_path, format='ICO')
            print("✅ Icono temporal creado")
        except Exception as e:
            print(f"⚠️  No se pudo crear icono: {e}")


def build_executable():
    """Construir el ejecutable"""
    print("\n🔨 Construyendo ejecutable...")

    # Crear directorios necesarios
    Path("assets").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)

    # Crear icono si no existe
    create_icon()

    # Ejecutar PyInstaller
    try:
        if os.path.exists('impresion3d.spec'):
            # Usar archivo spec
            subprocess.run([sys.executable, "-m", "PyInstaller", "impresion3d.spec", "--clean"])
        else:
            # Comando directo
            subprocess.run([
                sys.executable, "-m", "PyInstaller",
                "--name", "GestionImpresion3D",
                "--windowed",  # Sin consola
                "--onedir",  # Un directorio con todos los archivos
                "--clean",  # Limpiar cache
                "--add-data", f"assets{os.pathsep}assets",
                "--add-data", f"README.md{os.pathsep}.",
                "--hidden-import", "tkinter",
                "--hidden-import", "PIL._tkinter_finder",
                "main.py"
            ])

        print("\n✅ Construcción completada")
        print(f"📁 Ejecutable en: dist/GestionImpresion3D/")

    except Exception as e:
        print(f"❌ Error durante la construcción: {e}")
        return False

    return True


def create_installer_script():
    """Crear script de instalación para el usuario final"""

    # Script para Windows (install.bat)
    windows_script = """@echo off
echo ========================================
echo   Instalador - Gestion Impresion 3D
echo ========================================
echo.

set INSTALL_DIR=%USERPROFILE%\\GestionImpresion3D

echo Instalando en: %INSTALL_DIR%
echo.

REM Crear directorio de instalacion
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar archivos
echo Copiando archivos...
xcopy /E /I /Y "GestionImpresion3D" "%INSTALL_DIR%"

REM Crear acceso directo en escritorio
echo Creando acceso directo...
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%USERPROFILE%\\Desktop\\Gestion Impresion 3D.lnk'); $SC.TargetPath = '%INSTALL_DIR%\\GestionImpresion3D.exe'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.IconLocation = '%INSTALL_DIR%\\GestionImpresion3D.exe'; $SC.Save()"

echo.
echo ✅ Instalacion completada!
echo.
echo Encontrara el acceso directo en su escritorio.
echo.
pause
"""

    # Script para Linux/Mac (install.sh)
    unix_script = """#!/bin/bash

echo "========================================"
echo "   Instalador - Gestión Impresión 3D"
echo "========================================"
echo ""

INSTALL_DIR="$HOME/GestionImpresion3D"

echo "Instalando en: $INSTALL_DIR"
echo ""

# Crear directorio de instalación
mkdir -p "$INSTALL_DIR"

# Copiar archivos
echo "Copiando archivos..."
cp -R GestionImpresion3D/* "$INSTALL_DIR/"

# Hacer ejecutable
chmod +x "$INSTALL_DIR/GestionImpresion3D"

# Crear lanzador de escritorio
DESKTOP_FILE="$HOME/.local/share/applications/gestion-impresion3d.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Gestión Impresión 3D
Comment=Aplicación para gestionar productos de impresión 3D
Exec=$INSTALL_DIR/GestionImpresion3D
Icon=$INSTALL_DIR/icon.png
Terminal=false
Categories=Utility;Graphics;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "✅ Instalación completada!"
echo ""
echo "Puede encontrar la aplicación en el menú de aplicaciones."
echo "O ejecutar directamente: $INSTALL_DIR/GestionImpresion3D"
echo ""
"""

    # Guardar scripts
    with open('dist/install_windows.bat', 'w', encoding='utf-8') as f:
        f.write(windows_script)

    with open('dist/install_unix.sh', 'w', encoding='utf-8') as f:
        f.write(unix_script)

    os.chmod('dist/install_unix.sh', 0o755)

    print("✅ Scripts de instalación creados")


def create_readme():
    """Crear README para la distribución"""
    readme_content = """# 🖨️ Gestión de Impresión 3D - Instrucciones de Instalación

## Windows

1. Ejecute `install_windows.bat`
2. Se creará un acceso directo en el escritorio
3. ¡Listo para usar!

## Linux/Mac

1. Abra una terminal en esta carpeta
2. Ejecute: `./install_unix.sh`
3. La aplicación aparecerá en el menú de aplicaciones

## Uso Directo (sin instalar)

También puede ejecutar directamente desde la carpeta:
- Windows: `GestionImpresion3D/GestionImpresion3D.exe`
- Linux/Mac: `./GestionImpresion3D/GestionImpresion3D`

## Requisitos

- No requiere Python instalado
- No requiere conexión a internet
- Base de datos local incluida

## Soporte

Si encuentra problemas, verifique:
- Que tiene permisos de escritura en la carpeta
- Antivirus no esté bloqueando la aplicación
- En Linux/Mac: que el archivo tenga permisos de ejecución

---
Versión 1.0 - Sistema de gestión de productos para impresión 3D
"""

    with open('dist/LEEME.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("✅ README de distribución creado")


def package_distribution():
    """Empaquetar para distribución"""
    print("\n📦 Empaquetando para distribución...")

    dist_name = "GestionImpresion3D_v1.0"

    # Crear estructura de distribución
    if os.path.exists(f"dist/{dist_name}"):
        shutil.rmtree(f"dist/{dist_name}")

    os.makedirs(f"dist/{dist_name}")

    # Copiar ejecutable
    shutil.copytree("dist/GestionImpresion3D", f"dist/{dist_name}/GestionImpresion3D")

    # Copiar scripts de instalación
    if os.path.exists("dist/install_windows.bat"):
        shutil.copy("dist/install_windows.bat", f"dist/{dist_name}/")
    if os.path.exists("dist/install_unix.sh"):
        shutil.copy("dist/install_unix.sh", f"dist/{dist_name}/")
    if os.path.exists("dist/LEEME.txt"):
        shutil.copy("dist/LEEME.txt", f"dist/{dist_name}/")

    # Crear ZIP
    print("📦 Creando archivo ZIP...")
    shutil.make_archive(f"dist/{dist_name}", 'zip', "dist", dist_name)

    print(f"\n✅ Distribución creada: dist/{dist_name}.zip")
    print(f"   Tamaño: {os.path.getsize(f'dist/{dist_name}.zip') / 1024 / 1024:.1f} MB")


def main():
    """Función principal"""
    print("🖨️  CONSTRUCTOR DE EJECUTABLE - GESTIÓN IMPRESIÓN 3D")
    print("=" * 50)

    # Verificar PyInstaller
    if not check_pyinstaller():
        print("\n❌ No se puede continuar sin PyInstaller")
        return

    # Preguntar opciones
    print("\nOpciones de construcción:")
    print("1. Construcción rápida (un directorio)")
    print("2. Construcción completa con instaladores")
    print("3. Solo crear archivo .spec")

    opcion = input("\nSeleccione opción (1-3): ").strip()

    if opcion == "3":
        create_spec_file()
        print("\n✅ Archivo .spec creado. Puede editarlo y ejecutar:")
        print("   pyinstaller impresion3d.spec")
        return

    # Construir ejecutable
    if build_executable():
        if opcion == "2":
            # Crear instaladores y empaquetar
            create_installer_script()
            create_readme()
            package_distribution()

            print("\n🎉 ¡Construcción completa terminada!")
            print("\nPara distribuir:")
            print(f"1. Comparta el archivo: dist/GestionImpresion3D_v1.0.zip")
            print("2. El usuario debe descomprimir y ejecutar el instalador")
            print("\n💡 Consejo: Puede firmar digitalmente el ejecutable para evitar")
            print("   advertencias de Windows Defender.")
        else:
            print("\n🎉 ¡Construcción rápida terminada!")
            print(f"\nEjecutable en: dist/GestionImpresion3D/")
            print("Puede copiar toda esa carpeta para distribuir.")


if __name__ == "__main__":
    main()