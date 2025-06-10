"""
Utilidades para manejo de archivos e imágenes
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import hashlib
from typing import Optional, Tuple, Dict


class FileUtils:
    """Utilidades para manejo de archivos"""

    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    MAX_IMAGE_SIZE = (800, 800)  # Tamaño máximo para las imágenes

    # Mapa de colores comunes a hexadecimal
    COLOR_NAME_TO_HEX = {
        'negro': '#000000',
        'blanco': '#FFFFFF',
        'rojo': '#FF0000',
        'verde': '#00FF00',
        'azul': '#0000FF',
        'amarillo': '#FFFF00',
        'naranja': '#FFA500',
        'morado': '#800080',
        'púrpura': '#800080',
        'rosa': '#FFC0CB',
        'gris': '#808080',
        'marrón': '#A52A2A',
        'café': '#A52A2A',
        'cyan': '#00FFFF',
        'cian': '#00FFFF',
        'magenta': '#FF00FF',
        'plata': '#C0C0C0',
        'dorado': '#FFD700',
        'oro': '#FFD700',
        'turquesa': '#40E0D0',
        'violeta': '#EE82EE',
        'lima': '#32CD32',
        'navy': '#000080',
        'azul marino': '#000080',
        'beige': '#F5F5DC',
        'crema': '#FFFDD0',
        'salmon': '#FA8072',
        'salmón': '#FA8072',
        'coral': '#FF7F50',
        'oliva': '#808000',
        'chocolate': '#D2691E',
        'índigo': '#4B0082',
        'lavanda': '#E6E6FA',
        'menta': '#98FF98',
        'cielo': '#87CEEB',
        'arena': '#F4A460',
        'bronce': '#CD7F32',
        'cobre': '#B87333',
        'vino': '#722F37',
        'carbón': '#36454F',
        'perla': '#F8F8FF',
        'marfil': '#FFFFF0',
        'esmeralda': '#50C878',
        'rubí': '#E0115F',
        'zafiro': '#0F52BA'
    }

    @staticmethod
    def color_name_to_hex(color_name: str) -> str:
        """
        Convertir un nombre de color a hexadecimal
        Retorna el código hex si encuentra coincidencia, o #808080 (gris) por defecto
        """
        if not color_name:
            return '#808080'

        # Si ya es hexadecimal, devolverlo
        if color_name.startswith('#') and len(color_name) in [4, 7]:
            return color_name.upper()

        # Buscar en el mapa de colores
        color_lower = color_name.lower().strip()

        # Coincidencia exacta
        if color_lower in FileUtils.COLOR_NAME_TO_HEX:
            return FileUtils.COLOR_NAME_TO_HEX[color_lower]

        # Coincidencia parcial
        for key, value in FileUtils.COLOR_NAME_TO_HEX.items():
            if key in color_lower or color_lower in key:
                return value

        # Color por defecto
        return '#808080'

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convertir color hexadecimal a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convertir RGB a hexadecimal"""
        return f"#{r:02x}{g:02x}{b:02x}".upper()

    @staticmethod
    def get_contrasting_text_color(bg_hex: str) -> str:
        """
        Determinar si usar texto negro o blanco basado en el color de fondo
        Usa el algoritmo de luminancia para determinar el contraste
        """
        r, g, b = FileUtils.hex_to_rgb(bg_hex)

        # Calcular luminancia relativa
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255

        # Si el fondo es oscuro, usar texto blanco; si es claro, usar negro
        return '#FFFFFF' if luminance < 0.5 else '#000000'

    @staticmethod
    def is_valid_image(file_path: str) -> bool:
        """Verificar si un archivo es una imagen válida"""
        path = Path(file_path)

        # Verificar extensión
        if path.suffix.lower() not in FileUtils.ALLOWED_IMAGE_EXTENSIONS:
            return False

        # Verificar que se puede abrir como imagen
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except:
            return False

    @staticmethod
    def save_product_image(source_path: str, product_name: str) -> Optional[str]:
        """
        Guardar imagen de producto en la carpeta de assets
        Retorna la ruta relativa de la imagen guardada
        """
        try:
            # Verificar que es una imagen válida
            if not FileUtils.is_valid_image(source_path):
                return None

            # Generar nombre único para la imagen
            source_path = Path(source_path)
            timestamp = hashlib.md5(str(Path(source_path).stat().st_mtime).encode()).hexdigest()[:8]
            safe_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')[:50]  # Limitar longitud

            new_filename = f"{safe_name}_{timestamp}{source_path.suffix.lower()}"
            dest_path = Path("assets/images") / new_filename

            # Crear directorio si no existe
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Abrir y redimensionar imagen si es necesario
            with Image.open(source_path) as img:
                # Convertir a RGB si es necesario (para manejar PNGs con transparencia)
                if img.mode in ('RGBA', 'LA'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img

                # Redimensionar manteniendo proporción
                img.thumbnail(FileUtils.MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)

                # Guardar imagen optimizada
                img.save(dest_path, quality=85, optimize=True)

            return str(dest_path)

        except Exception as e:
            print(f"Error al guardar imagen: {e}")
            return None

    @staticmethod
    def delete_product_image(image_path: str) -> bool:
        """Eliminar imagen de producto"""
        try:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar imagen: {e}")
            return False

    @staticmethod
    def get_image_thumbnail(image_path: str, size: Tuple[int, int] = (150, 150)) -> Optional[Image.Image]:
        """Obtener miniatura de una imagen"""
        try:
            if not image_path or not os.path.exists(image_path):
                return None

            img = Image.open(image_path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            return img

        except Exception as e:
            print(f"Error al crear miniatura: {e}")
            return None

    @staticmethod
    def export_product_data(product_data: dict, export_path: str) -> bool:
        """Exportar datos de producto a archivo"""
        try:
            import json

            export_path = Path(export_path)
            export_path.parent.mkdir(parents=True, exist_ok=True)

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(product_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"Error al exportar datos: {e}")
            return False

    @staticmethod
    def import_product_data(import_path: str) -> Optional[dict]:
        """Importar datos de producto desde archivo"""
        try:
            import json

            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return data

        except Exception as e:
            print(f"Error al importar datos: {e}")
            return None

    @staticmethod
    def get_file_size_readable(file_path: str) -> str:
        """Obtener tamaño de archivo en formato legible"""
        try:
            size_bytes = os.path.getsize(file_path)

            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0

            return f"{size_bytes:.1f} TB"

        except:
            return "0 B"