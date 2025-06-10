"""
Utilidades para manejo de archivos e imágenes
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import hashlib
from typing import Optional, Tuple


class FileUtils:
    """Utilidades para manejo de archivos"""

    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    MAX_IMAGE_SIZE = (800, 800)  # Tamaño máximo para las imágenes

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