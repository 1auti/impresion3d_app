"""
Controlador para manejar la lógica de productos
"""
from typing import List, Optional
from models.producto import Producto
from utils.file_utils import FileUtils


class ProductController:
    """Controlador para manejar operaciones de productos"""

    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.productos_actuales: List[Producto] = []
        self.producto_seleccionado: Optional[Producto] = None
        self.colores_filtrados: List[str] = []
        self.termino_busqueda: str = ""

        # Callbacks para notificar cambios
        self.on_productos_changed = None
        self.on_selection_changed = None
        self.on_filters_changed = None

    def cargar_productos(self):
        """Cargar todos los productos desde la base de datos"""
        try:
            self.productos_actuales = self.db_manager.obtener_todos_productos()
            self._notificar_cambio_productos()
            return True, f"Se cargaron {len(self.productos_actuales)} productos"
        except Exception as e:
            return False, f"Error al cargar productos: {str(e)}"

    def buscar_productos(self, termino):
        """Buscar productos por término"""
        self.termino_busqueda = termino.strip()

        # Ignorar placeholder
        if self.termino_busqueda == "Nombre, material, color...":
            self.termino_busqueda = ""

        try:
            if self.termino_busqueda:
                self.productos_actuales = self.db_manager.buscar_productos(self.termino_busqueda)
            else:
                self.productos_actuales = self.db_manager.obtener_todos_productos()

            self._notificar_cambio_productos()
            return True, f"Se encontraron {len(self.productos_actuales)} productos"
        except Exception as e:
            return False, f"Error en la búsqueda: {str(e)}"

    def seleccionar_producto(self, producto_id):
        """Seleccionar un producto por ID"""
        if producto_id:
            self.producto_seleccionado = next(
                (p for p in self.productos_actuales if p.id == producto_id), None
            )
        else:
            self.producto_seleccionado = None

        self._notificar_cambio_seleccion()

    def crear_producto(self, datos_producto):
        """Crear un nuevo producto"""
        try:
            # Aquí se podría validar los datos antes de crear
            nuevo_producto = self.db_manager.crear_producto(datos_producto)
            self.cargar_productos()  # Recargar lista
            return True, "Producto creado exitosamente"
        except Exception as e:
            return False, f"Error al crear producto: {str(e)}"

    def actualizar_producto(self, producto, datos_actualizados):
        """Actualizar un producto existente"""
        try:
            success = self.db_manager.actualizar_producto(producto.id, datos_actualizados)
            if success:
                self.cargar_productos()  # Recargar lista
                # Si el producto actualizado era el seleccionado, reseleccionarlo
                if self.producto_seleccionado and self.producto_seleccionado.id == producto.id:
                    self.seleccionar_producto(producto.id)
                return True, "Producto actualizado exitosamente"
            else:
                return False, "No se pudo actualizar el producto"
        except Exception as e:
            return False, f"Error al actualizar producto: {str(e)}"

    def eliminar_producto(self, producto):
        """Eliminar un producto"""
        try:
            # Eliminar imagen si existe
            if producto.imagen_path:
                FileUtils.delete_product_image(producto.imagen_path)

            success = self.db_manager.eliminar_producto(producto.id)
            if success:
                # Limpiar selección si se eliminó el producto seleccionado
                if self.producto_seleccionado and self.producto_seleccionado.id == producto.id:
                    self.producto_seleccionado = None
                    self._notificar_cambio_seleccion()

                self.cargar_productos()  # Recargar lista
                return True, "Producto eliminado exitosamente"
            else:
                return False, "No se pudo eliminar el producto"
        except Exception as e:
            return False, f"Error al eliminar producto: {str(e)}"

    def aplicar_filtro_colores(self, colores_filtrados):
        """Aplicar filtro por colores"""
        self.colores_filtrados = colores_filtrados.copy()
        self._notificar_cambio_filtros()

    def limpiar_filtros(self):
        """Limpiar todos los filtros"""
        self.colores_filtrados = []
        self._notificar_cambio_filtros()

    def obtener_productos_filtrados(self):
        """Obtener productos aplicando filtros actuales"""
        productos = self.productos_actuales

        # Aplicar filtro de colores si existe
        if self.colores_filtrados:
            productos = [
                p for p in productos
                if self._producto_tiene_colores_filtrados(p)
            ]

        return productos

    def _producto_tiene_colores_filtrados(self, producto):
        """Verificar si un producto tiene alguno de los colores filtrados"""
        if hasattr(producto, 'colores_especificaciones') and producto.colores_especificaciones:
            return any(c.color_hex in self.colores_filtrados for c in producto.colores_especificaciones)
        elif hasattr(producto, 'color') and producto.color:
            return producto.color in self.colores_filtrados
        return False

    def obtener_estadisticas(self):
        """Obtener estadísticas de productos"""
        try:
            return self.db_manager.obtener_estadisticas()
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {
                'total_productos': 0,
                'tiempo_promedio_impresion': 0,
                'total_colores': 0,
                'promedio_colores_por_producto': 0,
                'productos_por_material': {}
            }

    def obtener_colores_disponibles(self):
        """Obtener colores disponibles para filtros"""
        try:
            return self.db_manager.obtener_colores_disponibles()
        except Exception as e:
            print(f"Error al obtener colores: {e}")
            return []

    def exportar_productos(self):
        """Obtener productos para exportación"""
        return self.productos_actuales

    # Métodos para configurar callbacks
    def set_on_productos_changed(self, callback):
        """Configurar callback para cuando cambian los productos"""
        self.on_productos_changed = callback

    def set_on_selection_changed(self, callback):
        """Configurar callback para cuando cambia la selección"""
        self.on_selection_changed = callback

    def set_on_filters_changed(self, callback):
        """Configurar callback para cuando cambian los filtros"""
        self.on_filters_changed = callback

    # Métodos privados para notificar cambios
    def _notificar_cambio_productos(self):
        """Notificar que los productos han cambiado"""
        if self.on_productos_changed:
            self.on_productos_changed(self.obtener_productos_filtrados())

    def _notificar_cambio_seleccion(self):
        """Notificar que la selección ha cambiado"""
        if self.on_selection_changed:
            self.on_selection_changed(self.producto_seleccionado)

    def _notificar_cambio_filtros(self):
        """Notificar que los filtros han cambiado"""
        if self.on_filters_changed:
            self.on_filters_changed(self.colores_filtrados)
        # También notificar cambio en productos para actualizar la lista
        self._notificar_cambio_productos()

    # Métodos de utilidad
    def tiene_productos(self):
        """Verificar si hay productos cargados"""
        return len(self.productos_actuales) > 0

    def tiene_producto_seleccionado(self):
        """Verificar si hay un producto seleccionado"""
        return self.producto_seleccionado is not None

    def get_producto_seleccionado(self):
        """Obtener el producto seleccionado"""
        return self.producto_seleccionado

    def get_total_productos(self):
        """Obtener total de productos"""
        return len(self.productos_actuales)

    def get_total_productos_filtrados(self):
        """Obtener total de productos después de aplicar filtros"""
        return len(self.obtener_productos_filtrados())