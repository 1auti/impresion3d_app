#!/usr/bin/env python3
"""
Script de migración para convertir productos antiguos al nuevo sistema de especificaciones de color
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from models.producto import ColorEspecificacion


def get_color_hex_from_name(color_name):
    """Convertir nombres de colores comunes a hexadecimal"""
    color_map = {
        'negro': '#000000',
        'blanco': '#FFFFFF',
        'rojo': '#FF0000',
        'verde': '#00FF00',
        'azul': '#0000FF',
        'amarillo': '#FFFF00',
        'naranja': '#FFA500',
        'morado': '#800080',
        'rosa': '#FFC0CB',
        'gris': '#808080',
        'marrón': '#A52A2A',
        'café': '#A52A2A',
        'cyan': '#00FFFF',
        'magenta': '#FF00FF',
        'plata': '#C0C0C0',
        'dorado': '#FFD700',
        'turquesa': '#40E0D0',
        'violeta': '#EE82EE',
        'lima': '#32CD32',
        'navy': '#000080',
        'beige': '#F5F5DC'
    }

    # Buscar coincidencia (case insensitive)
    color_lower = color_name.lower().strip()

    # Buscar coincidencia exacta
    if color_lower in color_map:
        return color_map[color_lower]

    # Buscar coincidencia parcial
    for key, value in color_map.items():
        if key in color_lower or color_lower in key:
            return value

    # Si no se encuentra, devolver un color por defecto
    return '#808080'  # Gris por defecto


def migrate_products():
    """Migrar productos antiguos al nuevo sistema de especificaciones de color"""
    print("🔄 Iniciando migración de colores...")

    try:
        db = DatabaseManager()

        # Obtener todos los productos
        productos = db.obtener_todos_productos()

        migrados = 0
        sin_color = 0
        ya_migrados = 0

        for producto in productos:
            # Verificar si ya tiene especificaciones de color
            if producto.colores_especificaciones:
                ya_migrados += 1
                continue

            # Si tiene un color antiguo, crear especificación
            if producto.color and producto.color.strip():
                print(f"\n📦 Migrando: {producto.nombre}")
                print(f"   Color antiguo: {producto.color}")

                # Obtener código hexadecimal
                color_hex = get_color_hex_from_name(producto.color)
                print(f"   Color hex: {color_hex}")

                # Crear especificación de color
                color_spec = ColorEspecificacion(
                    color_hex=color_hex,
                    nombre_color=producto.color,
                    peso_color=producto.peso,  # Usar el peso total como peso del color
                    tiempo_adicional=0,
                    piezas=["Producto completo"],  # Pieza genérica
                    notas="Migrado automáticamente del sistema anterior"
                )

                # Agregar especificación al producto
                producto.colores_especificaciones = [color_spec]

                # Actualizar en la base de datos
                if db.actualizar_producto(producto):
                    print("   ✅ Migrado exitosamente")
                    migrados += 1
                else:
                    print("   ❌ Error al migrar")
            else:
                sin_color += 1

        print("\n" + "=" * 50)
        print("📊 Resumen de migración:")
        print(f"   ✅ Productos migrados: {migrados}")
        print(f"   ⏭️  Ya tenían especificaciones: {ya_migrados}")
        print(f"   ⚪ Sin color definido: {sin_color}")
        print(f"   📦 Total de productos: {len(productos)}")

        if migrados > 0:
            print("\n✅ Migración completada exitosamente")
            print("   Los productos migrados ahora tienen especificaciones de color.")
            print("   Puedes editarlos para agregar más detalles o colores adicionales.")

    except Exception as e:
        print(f"\n❌ Error durante la migración: {e}")
        return False

    return True


def main():
    """Función principal"""
    print("🖨️  MIGRACIÓN DE ESPECIFICACIONES DE COLOR")
    print("=" * 50)
    print("\nEste script migrará productos antiguos al nuevo sistema")
    print("de especificaciones de color.")
    print("\nLos productos que ya tienen especificaciones no serán modificados.")

    response = input("\n¿Desea continuar? (s/n): ").lower()

    if response == 's':
        if migrate_products():
            print("\n✅ Proceso completado")
        else:
            print("\n❌ El proceso falló")
    else:
        print("\n❌ Migración cancelada")


if __name__ == "__main__":
    main()