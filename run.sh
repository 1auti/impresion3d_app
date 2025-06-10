#!/bin/bash
# ===== run.sh - Script de ejecución para Linux/macOS =====

echo "========================================"
echo "   Aplicación de Impresión 3D"
echo "========================================"
echo ""

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 no está instalado${NC}"
    echo "Por favor, instala Python 3.12 o superior"
    exit 1
fi

# Verificar versión de Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.12"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${YELLOW}ADVERTENCIA: Se detectó Python $PYTHON_VERSION${NC}"
    echo "Se recomienda Python $REQUIRED_VERSION o superior"
    echo ""
fi

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo ""
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Verificar dependencias
if ! pip show Pillow &> /dev/null; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
    echo ""
fi

# Verificar tkinter (en Linux puede requerir instalación separada)
if ! python -c "import tkinter" &> /dev/null; then
    echo -e "${YELLOW}ADVERTENCIA: tkinter no está disponible${NC}"
    echo "En Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "En Fedora: sudo dnf install python3-tkinter"
    echo "En macOS: tkinter viene incluido con Python"
    echo ""
    read -p "Presiona Enter para continuar o Ctrl+C para cancelar..."
fi

# Ejecutar aplicación
echo -e "${GREEN}Iniciando aplicación...${NC}"
echo ""
python main.py

# Verificar código de salida
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}ERROR: La aplicación se cerró con errores${NC}"
    read -p "Presiona Enter para salir..."
fi

# Desactivar entorno virtual
deactivate