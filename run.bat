REM ===== run.bat - Script de ejecución para Windows =====
@echo off
echo ========================================
echo   Aplicacion de Impresion 3D
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.12 o superior desde python.org
    pause
    exit /b 1
)

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
    echo.
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar dependencias
pip show Pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    echo.
)

REM Ejecutar aplicación
echo Iniciando aplicacion...
echo.
python main.py

REM Pausar al finalizar para ver errores
if %errorlevel% neq 0 (
    echo.
    echo ERROR: La aplicacion se cerro con errores
    pause
)

deactivate