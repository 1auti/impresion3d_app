# 🖨️ Aplicación de Gestión de Productos para Impresión 3D

Una aplicación de escritorio desarrollada en Python para gestionar información sobre productos de impresión 3D, incluyendo guías de impresión, configuraciones y gestión de imágenes.

## 📋 Características

- **Gestión completa de productos**: Agregar, editar, eliminar y buscar productos
- **Almacenamiento local**: Base de datos SQLite sin necesidad de conexión a internet
- **Gestión de imágenes**: Subir y visualizar imágenes de productos
- **Guías de impresión**: Documentar instrucciones detalladas para cada producto
- **Configuración de impresión**: Temperaturas, tiempos y materiales
- **Interfaz intuitiva**: Diseño amigable con Tkinter
- **Exportación de datos**: Guardar información en formato JSON
- **Vista previa**: Visualización rápida de productos seleccionados

## 🛠️ Requisitos

- Python 3.12 o superior
- Sistema operativo: Windows, macOS o Linux

## 📦 Instalación

1. **Clonar o descargar el proyecto**:
```bash
git clone https://github.com/tuusuario/impresion3d_app.git
cd impresion3d_app
```

2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

1. **Ejecutar la aplicación**:
```bash
python main.py
```

2. **Primer uso**:
   - La aplicación creará automáticamente las carpetas necesarias
   - Se inicializará la base de datos local

## 📱 Funcionalidades Principales

### ➕ Agregar Producto
- Click en "Nuevo Producto"
- Completar información básica (nombre, color, peso, etc.)
- Configurar parámetros de impresión
- Agregar guía detallada de impresión
- Subir imagen del producto (opcional)

### 🔍 Buscar Productos
- Utilizar la barra de búsqueda
- Búsqueda por nombre, descripción, color o material
- Resultados en tiempo real

### ✏️ Editar Producto
- Seleccionar producto de la lista
- Click en "Editar Producto"
- Modificar cualquier campo
- Los cambios se registran con fecha y hora

### 👁️ Ver Detalles
- Doble click en un producto o botón "Ver Detalles"
- Vista completa con imagen ampliada
- Guía de impresión completa
- Opción de copiar guía o imprimir detalles

### 📊 Estadísticas
- Total de productos
- Productos por material
- Tiempo promedio de impresión

## 🗂️ Estructura de Datos

### Campos del Producto:
- **Información Básica**:
  - Nombre
  - Descripción
  - Color
  - Peso (gramos)
  - Material (PLA, ABS, PETG, etc.)
  
- **Configuración de Impresión**:
  - Tiempo de impresión (minutos)
  - Temperatura del extrusor (°C)
  - Temperatura de la cama (°C)
  - Guía detallada de impresión

- **Imagen**:
  - Formato: JPG, PNG, GIF, BMP, WebP
  - Redimensionamiento automático
  - Almacenamiento local optimizado

## 💾 Almacenamiento

- **Base de datos**: SQLite (`data/productos.db`)
- **Imágenes**: Carpeta local (`assets/images/`)
- **Exportación**: Formato JSON

## 🔧 Configuración Avanzada

### Personalizar Materiales
Editar en `ui/add_product_window.py`:
```python
values=['PLA', 'ABS', 'PETG', 'TPU', 'Nylon', 'Resina', 'Tu_Material']
```

### Temperaturas por Defecto
Modificar en `models/producto.py`:
```python
temperatura_extrusor: int = 200  # Tu temperatura
temperatura_cama: int = 60       # Tu temperatura
```

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verificar versión de Python: `python --version`
- Reinstalar dependencias: `pip install -r requirements.txt --force-reinstall`

### Error al cargar imágenes
- Verificar que Pillow esté instalado
- Comprobar formato de imagen compatible
- Verificar permisos de escritura en `assets/images/`

### Base de datos corrupta
- Eliminar `data/productos.db`
- La aplicación creará una nueva al iniciar

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio.

---

Desarrollado con ❤️ para la comunidad de impresión 3D