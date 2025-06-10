"""
Gestor de base de datos SQLite para la aplicación
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from models.producto import Producto


class DatabaseManager:
    """Clase para gestionar las operaciones de base de datos"""

    def __init__(self, db_path: str = "data/productos.db"):
        """Inicializar el gestor de base de datos"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)

    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return sqlite3.connect(str(self.db_path))

    def init_database(self):
        """Inicializar la base de datos y crear tablas si no existen"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Crear tabla de productos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    peso REAL DEFAULT 0.0,
                    color TEXT,
                    tiempo_impresion INTEGER DEFAULT 0,
                    material TEXT DEFAULT 'PLA',
                    temperatura_extrusor INTEGER DEFAULT 200,
                    temperatura_cama INTEGER DEFAULT 60,
                    imagen_path TEXT,
                    guia_impresion TEXT,
                    fecha_creacion TEXT,
                    fecha_modificacion TEXT
                )
            ''')

            # Crear índices para búsquedas más rápidas
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_nombre 
                ON productos(nombre)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_material 
                ON productos(material)
            ''')

            conn.commit()

    def crear_producto(self, producto: Producto) -> int:
        """Crear un nuevo producto en la base de datos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO productos (
                    nombre, descripcion, peso, color, tiempo_impresion,
                    material, temperatura_extrusor, temperatura_cama,
                    imagen_path, guia_impresion, fecha_creacion, fecha_modificacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto.nombre,
                producto.descripcion,
                producto.peso,
                producto.color,
                producto.tiempo_impresion,
                producto.material,
                producto.temperatura_extrusor,
                producto.temperatura_cama,
                producto.imagen_path,
                producto.guia_impresion,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))

            conn.commit()
            return cursor.lastrowid

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtener un producto por su ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_producto(row)
            return None

    def obtener_todos_productos(self) -> List[Producto]:
        """Obtener todos los productos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM productos ORDER BY nombre')
            rows = cursor.fetchall()

            return [self._row_to_producto(row) for row in rows]

    def buscar_productos(self, termino: str) -> List[Producto]:
        """Buscar productos por nombre o descripción"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            termino_busqueda = f"%{termino}%"

            cursor.execute('''
                SELECT * FROM productos 
                WHERE nombre LIKE ? OR descripcion LIKE ? OR color LIKE ? OR material LIKE ?
                ORDER BY nombre
            ''', (termino_busqueda, termino_busqueda, termino_busqueda, termino_busqueda))

            rows = cursor.fetchall()
            return [self._row_to_producto(row) for row in rows]

    def actualizar_producto(self, producto: Producto) -> bool:
        """Actualizar un producto existente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE productos SET
                    nombre = ?,
                    descripcion = ?,
                    peso = ?,
                    color = ?,
                    tiempo_impresion = ?,
                    material = ?,
                    temperatura_extrusor = ?,
                    temperatura_cama = ?,
                    imagen_path = ?,
                    guia_impresion = ?,
                    fecha_modificacion = ?
                WHERE id = ?
            ''', (
                producto.nombre,
                producto.descripcion,
                producto.peso,
                producto.color,
                producto.tiempo_impresion,
                producto.material,
                producto.temperatura_extrusor,
                producto.temperatura_cama,
                producto.imagen_path,
                producto.guia_impresion,
                datetime.now().isoformat(),
                producto.id
            ))

            conn.commit()
            return cursor.rowcount > 0

    def eliminar_producto(self, producto_id: int) -> bool:
        """Eliminar un producto"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_producto(self, row) -> Producto:
        """Convertir una fila de la base de datos a objeto Producto"""
        return Producto(
            id=row[0],
            nombre=row[1],
            descripcion=row[2] or "",
            peso=row[3] or 0.0,
            color=row[4] or "",
            tiempo_impresion=row[5] or 0,
            material=row[6] or "PLA",
            temperatura_extrusor=row[7] or 200,
            temperatura_cama=row[8] or 60,
            imagen_path=row[9],
            guia_impresion=row[10] or "",
            fecha_creacion=datetime.fromisoformat(row[11]) if row[11] else None,
            fecha_modificacion=datetime.fromisoformat(row[12]) if row[12] else None
        )

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtener estadísticas de la base de datos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total de productos
            cursor.execute('SELECT COUNT(*) FROM productos')
            total_productos = cursor.fetchone()[0]

            # Productos por material
            cursor.execute('''
                SELECT material, COUNT(*) 
                FROM productos 
                GROUP BY material
            ''')
            productos_por_material = dict(cursor.fetchall())

            # Tiempo promedio de impresión
            cursor.execute('SELECT AVG(tiempo_impresion) FROM productos')
            tiempo_promedio = cursor.fetchone()[0] or 0

            return {
                'total_productos': total_productos,
                'productos_por_material': productos_por_material,
                'tiempo_promedio_impresion': round(tiempo_promedio, 2)
            }