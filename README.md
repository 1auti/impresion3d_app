# 🖨️ Aplicación de Gestión de Productos para Impresión 3D

Una aplicación de escritorio desarrollada en Python para gestionar información sobre productos de impresión 3D, incluyendo guías de impresión, configuraciones y gestión avanzada de colores con especificaciones detalladas por pieza.

## 📋 Características

- **Gestión completa de productos**: Agregar, editar, eliminar y buscar productos
- **Especificaciones de color avanzadas**: 
  - Selector de color hexadecimal con vista previa
  - Múltiples colores por producto
  - Peso específico por color
  - Piezas asociadas a cada color
  - Tiempo de cambio de color
  - Notas por especificación
- **Filtrado por colores**: Filtrar productos por colores específicos
- **Almacenamiento local**: Base de datos SQLite sin necesidad de conexión a internet
- **Gestión de imágenes**: Subir y visualizar imágenes de productos
- **Guías de impresión**: Documentar instrucciones detalladas para cada producto
- **Configuración de impresión**: Temperaturas, tiempos y materiales
- **Interfaz intuitiva**: Diseño amigable con Tkinter y vistas previas de colores
- **Exportación de datos**: Guardar información en formato JSON
- **Vista previa mejorada**: Visualización rápida con muestras de colores

## 🎨 Nueva Funcionalidad: Especificaciones de Color

### Características principales:
- **Selector de color hexadecimal**: Elige colores precisos con selector visual o código hex
- **Desglose por piezas**: Especifica qué piezas del modelo usan cada color
- **Gestión de peso**: Calcula automáticamente el peso total sumando todos los colores
- **Tiempo de cambio**: Registra tiempo adicional necesario para cambios de color
- **Filtros visuales**: Filtra productos por colores específicos en la lista principal
- **Vista previa de colores**: Muestra muestras de colores en la lista y vista previa

### Ejemplo de uso:
Un robot articulado puede tener:
- **Gris (#808080)**: Cuerpo, base, articulaciones (40g)
- **Naranja (#FFA500)**: Cabeza, manos (20g)
- **Negro (#000000)**: Ojos, detalles (15g)
- **Amarillo (#FFFF00)**: Botones, luces LED (10g)

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
- Completar información básica (nombre, material, etc.)
- **Especificar colores**:
  - Agregar múltiples especificaciones de color
  - Usar selector visual o código hexadecimal
  - Definir piezas para cada color
  - Establecer peso por color
  - Indicar tiempo de cambio de filamento
- Configurar parámetros de impresión
- Agregar guía detallada de impresión
- Subir imagen del producto (opcional)

### 🔍 Buscar Productos
- Utilizar la barra de búsqueda
- Búsqueda por nombre, descripción o material
- **Filtrar por colores**: Seleccionar colores específicos para filtrar
- Resultados en tiempo real
- Vista de muestras de colores en la lista

### ✏️ Editar Producto
- Seleccionar producto de la lista
- Click en "Editar Producto"
- Modificar cualquier campo incluyendo especificaciones de color
- Agregar o eliminar colores
- Los cambios se registran con fecha y hora

### 👁️ Ver Detalles
- Doble click en un producto o botón "Ver Detalles"
- Vista completa con imagen ampliada
- **Desglose completo de colores**:
  - Visualización de cada color con su información
  - Lista de piezas por color
  - Peso y tiempo por especificación
- Guía de impresión completa
- Opción de copiar guía o imprimir detalles

### 📊 Estadísticas
- Total de productos
- Productos por material
- Tiempo promedio de impresión
- **Total de colores únicos utilizados**
- **Promedio de colores por producto**

## 🗂️ Estructura de Datos

### Campos del Producto:
- **Información Básica**:
  - Nombre
  - Descripción
  - Peso total (calculado automáticamente)
  - Material (PLA, ABS, PETG, etc.)
  
- **Especificaciones de Color**:
  - Color hexadecimal (#RRGGBB)
  - Nombre descriptivo del color
  - Peso específico del color (gramos)
  - Tiempo adicional para cambio de color (minutos)
  - Lista de piezas que usan ese color
  - Notas adicionales
  
- **Configuración de Impresión**:
  - Tiempo de impresión base (minutos)
  - Temperatura del extrusor (°C)
  - Temperatura de la cama (°C)
  - Guía detallada de impresión

- **Imagen**:
  - Formato: JPG, PNG, GIF, BMP, WebP
  - Redimensionamiento automático
  - Almacenamiento local optimizado

### Base de Datos:
La aplicación utiliza SQLite con las siguientes tablas:
- **productos**: Información principal del producto
- **color_especificaciones**: Detalles de cada color usado
- **color_piezas**: Piezas asociadas a cada especificación de color

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

### Migración de Datos Antiguos
Si tienes productos creados antes de la actualización de colores:
- Los productos antiguos mantendrán su campo "color" original
- Al editar un producto antiguo, se creará automáticamente una especificación de color
- Se recomienda actualizar gradualmente los productos para aprovechar las nuevas funciones

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