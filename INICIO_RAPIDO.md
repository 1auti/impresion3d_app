# 🚀 Guía de Inicio Rápido - Gestión de Impresión 3D

## 📥 Instalación en 3 Pasos

### Windows
1. **Descargar** el archivo `GestionImpresion3D_v1.0.zip`
2. **Descomprimir** en cualquier carpeta
3. **Ejecutar** `install_windows.bat`

### Mac/Linux
1. **Descargar** el archivo `GestionImpresion3D_v1.0.zip`
2. **Descomprimir** y abrir terminal en la carpeta
3. **Ejecutar** `./install_unix.sh`

## 🎯 Primer Uso - Tutorial Rápido

### 1️⃣ Agregar tu Primer Producto

1. Click en **"➕ Nuevo Producto"**
2. Completar información básica:
   - **Nombre**: "Mi primera pieza"
   - **Material**: PLA
   - **Tiempo base**: 120 minutos

### 2️⃣ Especificar Colores y Piezas (NUEVO!)

1. Ir a la pestaña **"Especificaciones de Color"**
2. Para cada pieza de tu modelo:
   - Click en el **cuadro de color** para elegir
   - Escribir el **nombre de la pieza**
   - Indicar el **peso en gramos**

**Ejemplo Rápido:**
```
🔴 Base principal → 25g
🔵 Tapa superior → 15g  
⚫ Botones (x4) → 5g
```

💡 **TIP**: Usa "➕ Agregar múltiples piezas del mismo color" para agregar varias piezas rápidamente

### 3️⃣ Guardar y Listo!

Click en **"💾 Guardar"** y tu producto estará registrado con todas sus piezas y colores.

## 🎨 Funciones Clave

### Agregar Piezas Rápidamente

1. Click en **"🎨 Agregar múltiples piezas del mismo color"**
2. Elegir un color
3. Escribir todas las piezas (una por línea):
   ```
   Rueda delantera izquierda
   Rueda delantera derecha
   Rueda trasera izquierda
   Rueda trasera derecha
   ```
4. Establecer peso por pieza
5. Click en "Agregar"

### Filtrar por Color

En la ventana principal:
- Los filtros de color aparecen automáticamente
- Click en los colores para filtrar productos
- Puedes seleccionar múltiples colores

### Ver Desglose de Piezas

Doble click en cualquier producto para ver:
- Todas las piezas organizadas por color
- Peso total y por color
- Tiempo estimado incluyendo cambios de color

## 📸 Capturas de Pantalla

### Vista Principal
```
┌─────────────────────────────────────┐
│ 🖨️ Gestión de Productos 3D         │
├─────────────────────────────────────┤
│ [Buscar: ___________]               │
│                                     │
│ [➕ Nuevo Producto]                 │
│ [✏️ Editar]                        │
│ [👁️ Ver Detalles]                  │
│                                     │
│ Filtrar por color:                 │
│ [🔴] [🔵] [🟢] [⚫] [🟡]          │
│                                     │
│ Lista de Productos:                 │
│ ┌─────────────────────────────┐    │
│ │ Robot Articulado           │    │
│ │ 🔴🔵⚫ 3 colores, 85g      │    │
│ └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### Especificación de Piezas
```
┌─────────────────────────────────────┐
│ Especificaciones de Color por Pieza │
├─────────────────────────────────────┤
│ [🔴] Cabeza del robot      → 20g   │
│ [🔴] Torso principal       → 35g   │
│ [🔵] Brazo izquierdo       → 15g   │
│ [🔵] Brazo derecho         → 15g   │
│ [⚫] Base de soporte       → 10g   │
│                                     │
│ [➕ Agregar Pieza]                  │
│ Total: 5 piezas, 95g                │
└─────────────────────────────────────┘
```

## ❓ Preguntas Frecuentes

### ¿Cómo agregar un producto con muchas piezas pequeñas?

Usa la función "Agregar múltiples piezas del mismo color":
1. Agrupa las piezas por color
2. Usa la herramienta múltiple para cada grupo
3. Ajusta los pesos al final

### ¿Puedo cambiar los colores después?

Sí, selecciona el producto y click en "✏️ Editar". Puedes:
- Cambiar colores de piezas existentes
- Agregar nuevas piezas
- Reorganizar por colores

### ¿Cómo calcula el peso total?

El peso total se calcula automáticamente sumando todos los pesos individuales de las piezas.

### ¿Qué significa "Tiempo de cambio de color"?

Es el tiempo adicional necesario para:
- Pausar la impresión
- Cambiar el filamento
- Purgar el extrusor
- Continuar imprimiendo

Por defecto son 5 minutos por cambio.

## 🆘 Solución de Problemas

### La aplicación no inicia
- **Windows**: Click derecho → "Ejecutar como administrador"
- **Antivirus**: Agregar excepción para GestionImpresion3D.exe

### No puedo ver los colores en los filtros
- Asegúrate de tener al menos un producto con colores especificados
- Los filtros aparecen automáticamente cuando hay colores en la base de datos

### Error al guardar producto
- Verifica que cada pieza tenga:
  - Un nombre (no puede estar vacío)
  - Un peso mayor a 0
  - Un color seleccionado

## 💡 Tips Pro

1. **Organiza por secciones**: Agrupa piezas similares con el mismo color
2. **Usa nombres descriptivos**: "Engranaje principal A" en lugar de "Pieza 1"
3. **Estima pesos**: Si no tienes balanza, usa el peso estimado del slicer
4. **Plantillas**: Crea un producto "plantilla" y duplícalo editando

## 📞 Soporte

- **Manual completo**: Ver README.md
- **Reportar problemas**: [correo/formulario]
- **Actualizaciones**: [sitio web]

---

¡Disfruta gestionando tus impresiones 3D! 🎉