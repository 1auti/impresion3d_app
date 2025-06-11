# 📦 Guía de Distribución - Gestión de Impresión 3D

Esta guía explica cómo preparar y distribuir la aplicación de forma profesional y fácil de usar.

## 🎯 Objetivo

Crear un paquete que los usuarios puedan instalar **sin necesitar Python** ni conocimientos técnicos.

## 📋 Preparación

### 1. Instalar Dependencias de Desarrollo

```bash
# En tu entorno de desarrollo
pip install pyinstaller
pip install pillow
```

### 2. Verificar que Todo Funcione

```bash
# Probar la aplicación
python main.py

# Verificar que no haya errores
```

## 🔨 Crear el Ejecutable

### Opción A: Construcción Automática (Recomendado)

```bash
python build_exe.py
```

Selecciona la opción 2 para construcción completa con instaladores.

### Opción B: Construcción Manual

```bash
# Construcción básica
pyinstaller --name GestionImpresion3D --windowed --onedir main.py

# Construcción con todas las opciones
pyinstaller --name GestionImpresion3D \
            --windowed \
            --onedir \
            --add-data "assets:assets" \
            --add-data "README.md:." \
            --hidden-import tkinter \
            --hidden-import PIL._tkinter_finder \
            --icon assets/icon.ico \
            main.py
```

## 📁 Estructura del Paquete Final

```
GestionImpresion3D_v1.0/
├── GestionImpresion3D/          # Carpeta con el ejecutable
│   ├── GestionImpresion3D.exe   # Ejecutable principal
│   ├── _internal/               # Librerías y dependencias
│   ├── assets/                  # Recursos
│   └── data/                    # Base de datos
├── install_windows.bat          # Instalador Windows
├── install_unix.sh              # Instalador Linux/Mac
└── LEEME.txt                    # Instrucciones
```

## 🚀 Métodos de Distribución

### 1. ZIP Simple (Más Fácil)

**Ventajas:**
- No requiere instalación
- Portable
- Fácil de compartir

**Pasos:**
1. Comprimir la carpeta `dist/GestionImpresion3D_v1.0/`
2. Compartir el archivo ZIP
3. El usuario descomprime y ejecuta

### 2. Google Drive / Dropbox

**Ventajas:**
- Fácil actualización
- Control de versiones
- Enlaces compartibles

**Pasos:**
1. Subir el ZIP a Google Drive
2. Crear enlace de descarga directa
3. Compartir el enlace

**Enlace directo en Google Drive:**
```
https://drive.google.com/uc?export=download&id=FILE_ID
```

### 3. GitHub Releases (Profesional)

**Ventajas:**
- Versionado automático
- Changelogs
- Estadísticas de descarga

**Pasos:**
1. Crear repositorio en GitHub
2. Ir a "Releases" → "Create new release"
3. Subir el archivo ZIP
4. Publicar release

### 4. Instalador NSIS (Windows)

Para crear un instalador profesional tipo `.exe`:

**installer.nsi:**
```nsis
!define APPNAME "Gestión Impresión 3D"
!define COMPANYNAME "Tu Empresa"
!define DESCRIPTION "Sistema de gestión para impresión 3D"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0

RequestExecutionLevel admin

InstallDir "$PROGRAMFILES\${APPNAME}"

Name "${APPNAME}"
Icon "assets\icon.ico"
OutFile "Setup_GestionImpresion3D_v1.0.exe"

!include "MUI2.nsh"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "Spanish"

Section "install"
    SetOutPath "$INSTDIR"
    
    # Copiar archivos
    File /r "dist\GestionImpresion3D\*.*"
    
    # Crear acceso directo
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\GestionImpresion3D.exe"
    CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\GestionImpresion3D.exe"
    
    # Desinstalador
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\*.*"
    RMDir /r "$INSTDIR"
    Delete "$SMPROGRAMS\${APPNAME}\*.*"
    RMDir "$SMPROGRAMS\${APPNAME}"
    Delete "$DESKTOP\${APPNAME}.lnk"
SectionEnd
```

### 5. Crear Paquete Portable

**portable_launcher.bat:**
```batch
@echo off
cd /d "%~dp0"
start "" "GestionImpresion3D\GestionImpresion3D.exe"
```

## 🛡️ Consideraciones de Seguridad

### Firma Digital (Windows)

Para evitar advertencias de Windows Defender:

1. **Certificado de Código:**
   - Comprar certificado de firma de código (~$70-500/año)
   - O usar certificado autofirmado (advertencias menores)

2. **Firmar con signtool:**
   ```cmd
   signtool sign /tr http://timestamp.sectigo.com /td sha256 /fd sha256 /a GestionImpresion3D.exe
   ```

### Permisos en macOS

```bash
# Dar permisos de ejecución
chmod +x GestionImpresion3D

# Eliminar cuarentena
xattr -d com.apple.quarantine GestionImpresion3D
```

## 📝 Documentación para Usuarios

### README_USUARIO.txt
```
GESTIÓN DE IMPRESIÓN 3D v1.0
============================

INSTALACIÓN RÁPIDA:
1. Descomprima el archivo ZIP
2. Windows: Ejecute install_windows.bat
   Linux/Mac: Ejecute ./install_unix.sh
3. Use el acceso directo creado

USO DIRECTO (sin instalar):
- Entre a la carpeta GestionImpresion3D
- Ejecute GestionImpresion3D.exe (Windows)
- O ./GestionImpresion3D (Linux/Mac)

REQUISITOS MÍNIMOS:
- Windows 7/10/11, macOS 10.12+, o Linux
- 100 MB de espacio libre
- No requiere internet
- No requiere Python

SOLUCIÓN DE PROBLEMAS:
- Si Windows bloquea: Click derecho → Propiedades → Desbloquear
- Si no inicia: Ejecute como administrador
- Para soporte: [tu email]
```

## 🔄 Actualización de Versiones

### Script de Actualización Automática

**updater.py:**
```python
import urllib.request
import json
import os
import zipfile
import shutil

VERSION_URL = "https://tu-servidor.com/version.json"
CURRENT_VERSION = "1.0"

def check_updates():
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            data = json.loads(response.read())
            
        if data['version'] > CURRENT_VERSION:
            return data
        return None
    except:
        return None

def download_update(url, filename):
    urllib.request.urlretrieve(url, filename)
    
def apply_update(zip_file):
    # Extraer actualización
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('update_temp')
    
    # Reemplazar archivos
    # ... código de actualización ...
```

## 📊 Métricas y Feedback

### Agregar Analytics Básico

```python
# En main.py, agregar (opcional):
def send_analytics(event):
    """Enviar evento anónimo de uso"""
    try:
        # Solo si el usuario acepta
        if get_user_consent():
            data = {
                'event': event,
                'version': VERSION,
                'os': platform.system()
            }
            # Enviar a tu servidor
    except:
        pass  # Fallar silenciosamente
```

## 🎁 Empaquetado Profesional

### Estructura Completa de Distribución

```
GestionImpresion3D_Installer/
├── Setup.exe                    # Instalador NSIS
├── GestionImpresion3D_Portable.zip  # Versión portable
├── README.pdf                   # Manual de usuario
├── CHANGELOG.txt               # Historial de cambios
├── LICENSE.txt                 # Licencia
└── samples/                    # Productos de ejemplo
    ├── robot.g3d
    ├── soporte.g3d
    └── organizador.g3d
```

## 💡 Tips Finales

1. **Versión Trial:**
   - Limitar a 10 productos
   - Marca de agua en exportaciones
   - Solicitar licencia después de 30 días

2. **Versión Pro:**
   - Sin límites
   - Exportación a STL
   - Sincronización en la nube
   - Soporte prioritario

3. **Marketing:**
   - Video tutorial en YouTube
   - Post en foros de impresión 3D
   - Página web simple con capturas

4. **Soporte:**
   - FAQ en el README
   - Email de soporte
   - Foro de usuarios

## 🚀 Comando Rápido Todo-en-Uno

```bash
# Construir, empaquetar y preparar para distribución
python build_exe.py && echo "✅ Listo para distribuir!"
```

¡Tu aplicación está lista para llegar a miles de usuarios! 🎉