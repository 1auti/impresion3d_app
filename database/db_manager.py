"""
Gestor de base de datos SQLite para la aplicación
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from models.producto import Producto, ColorEspecificacion


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

            # Crear tabla de especificaciones de color
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS color_especificaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER NOT NULL,
                    color_hex TEXT NOT NULL,
                    nombre_color TEXT,
                    peso_color REAL DEFAULT 0.0,
                    tiempo_adicional INTEGER DEFAULT 0,
                    notas TEXT,
                    FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
                )
            ''')

            # Crear tabla de piezas por color
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS color_piezas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    color_especificacion_id INTEGER NOT NULL,
                    nombre_pieza TEXT NOT NULL,
                    FOREIGN KEY (color_especificacion_id) REFERENCES color_especificaciones (id) ON DELETE CASCADE
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

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_color_hex 
                ON color_especificaciones(color_hex)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_producto_color 
                ON color_especificaciones(producto_id)
            ''')

            conn.commit()

    def crear_producto(self, producto: Producto) -> int:
        """Crear un nuevo producto en la base de datos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Insertar producto principal
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

            producto_id = cursor.lastrowid

            # Insertar especificaciones de color
            for color_spec in producto.colores_especificaciones:
                cursor.execute('''
                    INSERT INTO color_especificaciones (
                        producto_id, color_hex, nombre_color, peso_color, 
                        tiempo_adicional, notas
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    producto_id,
                    color_spec.color_hex,
                    color_spec.nombre_color,
                    color_spec.peso_color,
                    color_spec.tiempo_adicional,
                    color_spec.notas
                ))

                color_spec_id = cursor.lastrowid

                # Insertar piezas del color
                for pieza in color_spec.piezas:
                    cursor.execute('''
                        INSERT INTO color_piezas (color_especificacion_id, nombre_pieza)
                        VALUES (?, ?)
                    ''', (color_spec_id, pieza))

            conn.commit()
            return producto_id

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtener un producto por su ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
            row = cursor.fetchone()

            if row:
                producto = self._row_to_producto(row)

                # Obtener especificaciones de color
                cursor.execute('''
                    SELECT * FROM color_especificaciones 
                    WHERE producto_id = ?
                    ORDER BY peso_color DESC
                ''', (producto_id,))

                color_rows = cursor.fetchall()

                for color_row in color_rows:
                    color_spec = ColorEspecificacion(
                        color_hex=color_row[2],
                        nombre_color=color_row[3] or "",
                        peso_color=color_row[4] or 0.0,
                        tiempo_adicional=color_row[5] or 0,
                        notas=color_row[6] or ""
                    )

                    # Obtener piezas del color
                    cursor.execute('''
                        SELECT nombre_pieza FROM color_piezas
                        WHERE color_especificacion_id = ?
                    ''', (color_row[0],))

                    color_spec.piezas = [p[0] for p in cursor.fetchall()]
                    producto.colores_especificaciones.append(color_spec)

                return producto
            return None

    def obtener_todos_productos(self) -> List[Producto]:
        """Obtener todos los productos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM productos ORDER BY nombre')
            ids = cursor.fetchall()

            productos = []
            for (producto_id,) in ids:
                producto = self.obtener_producto(producto_id)
                if producto:
                    productos.append(producto)

            return productos

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

            # Actualizar producto principal
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

            # Eliminar especificaciones de color existentes
            cursor.execute('DELETE FROM color_especificaciones WHERE producto_id = ?', (producto.id,))

            # Insertar nuevas especificaciones de color
            for color_spec in producto.colores_especificaciones:
                cursor.execute('''
                    INSERT INTO color_especificaciones (
                        producto_id, color_hex, nombre_color, peso_color, 
                        tiempo_adicional, notas
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    producto.id,
                    color_spec.color_hex,
                    color_spec.nombre_color,
                    color_spec.peso_color,
                    color_spec.tiempo_adicional,
                    color_spec.notas
                ))

                color_spec_id = cursor.lastrowid

                # Insertar piezas del color
                for pieza in color_spec.piezas:
                    cursor.execute('''
                        INSERT INTO color_piezas (color_especificacion_id, nombre_pieza)
                        VALUES (?, ?)
                    ''', (color_spec_id, pieza))

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
            fecha_modificacion=datetime.fromisoformat(row[12]) if row[12] else None,
            colores_especificaciones=[]  # Se cargan por separado
        )

    def buscar_productos_por_color(self, color_hex: str) -> List[Producto]:
        """Buscar productos que contengan un color específico"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Buscar productos con el color especificado
            cursor.execute('''
                SELECT DISTINCT p.* 
                FROM productos p
                JOIN color_especificaciones ce ON p.id = ce.producto_id
                WHERE ce.color_hex = ?
                ORDER BY p.nombre
            ''', (color_hex,))

            rows = cursor.fetchall()
            productos = []

            for row in rows:
                producto = self.obtener_producto(row[0])  # Obtener producto completo con colores
                if producto:
                    productos.append(producto)

            return productos

    def obtener_colores_disponibles(self) -> List[Dict[str, Any]]:
        """Obtener lista de todos los colores disponibles con su frecuencia"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT color_hex, nombre_color, COUNT(DISTINCT producto_id) as cantidad
                FROM color_especificaciones
                GROUP BY color_hex
                ORDER BY cantidad DESC
            ''')

            return [
                {
                    'color_hex': row[0],
                    'nombre_color': row[1] or "Sin nombre",
                    'cantidad': row[2]
                }
                for row in cursor.fetchall()
            ]

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

            # Total de colores únicos
            cursor.execute('SELECT COUNT(DISTINCT color_hex) FROM color_especificaciones')
            total_colores = cursor.fetchone()[0] or 0

            # Promedio de colores por producto
            cursor.execute('''
                SELECT AVG(color_count) FROM (
                    SELECT COUNT(*) as color_count 
                    FROM color_especificaciones 
                    GROUP BY producto_id
                )
            ''')
            promedio_colores = cursor.fetchone()[0] or 0

            return {
                'total_productos': total_productos,
                'productos_por_material': productos_por_material,
                'tiempo_promedio_impresion': round(tiempo_promedio, 2),
                'total_colores': total_colores,
                'promedio_colores_por_producto': round(promedio_colores, 1)
            }