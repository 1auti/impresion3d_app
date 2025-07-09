"""
Controlador para la ventana de detalles de producto - Versión Refactorizada
"""
import os
import webbrowser
from pathlib import Path
from typing import Dict, List, Optional, Callable
from models.producto import Producto


class ProductDetailController:
    """Controlador para manejar la lógica de detalles de producto"""

    def __init__(self, producto: Producto):
        self.producto = producto

        # Callbacks
        self.on_error: Optional[Callable] = None
        self.on_success: Optional[Callable] = None

        # Estado
        self._color_groups_cache = None

    def get_basic_info(self) -> Dict[str, str]:
        """Obtener información básica del producto"""
        return {
            'descripcion': self.producto.descripcion or "Sin descripción",
            'material': self.producto.material,
            'peso_total': f"{self.producto.get_peso_total()} gramos",
            'tiempo_base': f"{self.producto.tiempo_impresion} min",
            'colores': f"{len(self.producto.colores_especificaciones)} colores" if self.producto.colores_especificaciones else "Sin especificar",
            'temp_extrusor': f"{self.producto.temperatura_extrusor}°C",
            'temp_cama': f"{self.producto.temperatura_cama}°C",
        }

    def get_color_groups(self) -> Dict[str, Dict]:
        """Obtener agrupaciones de color optimizadas"""
        if self._color_groups_cache is not None:
            return self._color_groups_cache

        color_groups = {}
        for color_spec in self.producto.colores_especificaciones:
            if color_spec.color_hex not in color_groups:
                color_groups[color_spec.color_hex] = {
                    'nombre': color_spec.nombre_color,
                    'piezas': [],
                    'peso_total': 0,
                    'tiempo_adicional': color_spec.tiempo_adicional
                }
            color_groups[color_spec.color_hex]['piezas'].extend(color_spec.piezas)
            color_groups[color_spec.color_hex]['peso_total'] += color_spec.peso_color

        self._color_groups_cache = color_groups
        return color_groups

    def get_color_summary(self) -> Dict[str, int]:
        """Obtener resumen de colores"""
        color_groups = self.get_color_groups()
        return {
            'total_colores': len(color_groups),
            'total_piezas': sum(len(g['piezas']) for g in color_groups.values()),
            'tiempo_cambios': sum(g['tiempo_adicional'] for g in color_groups.values())
        }

    def generate_recommendations(self) -> List[str]:
        """Generar recomendaciones basadas en el material y configuración"""
        recomendaciones = []

        # Recomendaciones por material
        material_recommendations = {
            "PLA": [
                "Ideal para principiantes - Fácil de imprimir",
                "Buena adhesión en cama fría (50-60°C)",
                "Velocidad recomendada: 40-60 mm/s",
                "Retracción: 1-2mm a 40-50 mm/s"
            ],
            "ABS": [
                "Requiere cama caliente (80-100°C) y ambiente cerrado",
                "Buena resistencia mecánica y térmica",
                "Cuidado con el warping - usar brim o raft",
                "Ventilación recomendada por vapores"
            ],
            "PETG": [
                "Combina facilidad del PLA con resistencia del ABS",
                "Temperatura cama: 70-80°C",
                "Excelente para piezas funcionales",
                "Resistente a químicos y rayos UV"
            ],
            "TPU": [
                "Material flexible - Imprimir lentamente (15-30 mm/s)",
                "Reducir retracción al mínimo (0.5-1mm)",
                "Direct drive preferible sobre bowden",
                "Cama a 40-50°C para mejor adhesión"
            ]
        }

        recomendaciones.extend(
            material_recommendations.get(
                self.producto.material,
                [f"Material {self.producto.material} - Consultar configuraciones específicas"]
            )
        )

        # Recomendaciones por tiempo de impresión
        tiempo_total = self.producto.get_tiempo_total()
        if tiempo_total > 480:  # Más de 8 horas
            recomendaciones.append("⏰ Impresión larga: Verificar filamento suficiente")
            recomendaciones.append("🔄 Considerar pausas para mantenimiento")

        # Recomendaciones por peso
        if self.producto.get_peso_total() > 100:
            recomendaciones.append("⚖️ Pieza pesada: Asegurar excelente adhesión a la cama")

        # Recomendaciones por múltiples colores
        if len(self.producto.colores_especificaciones) > 1:
            recomendaciones.append("🎨 Múltiples colores: Planificar cambios de filamento")
            recomendaciones.append("⏱️ Tiempo adicional por cambios incluido")

        return recomendaciones[:6]  # Limitar a 6 recomendaciones

    def open_image(self) -> bool:
        """Abrir la imagen en el visor predeterminado del sistema"""
        if not self.producto.imagen_path or not os.path.exists(self.producto.imagen_path):
            if self.on_error:
                self.on_error("No hay imagen disponible o el archivo no existe")
            return False

        try:
            if os.name == 'nt':
                os.startfile(self.producto.imagen_path)
            elif os.name == 'posix' and os.uname().sysname == 'Darwin':
                os.system(f'open "{self.producto.imagen_path}"')
            else:
                os.system(f'xdg-open "{self.producto.imagen_path}"')
            return True
        except Exception as e:
            if self.on_error:
                self.on_error(f"No se pudo abrir la imagen: {str(e)}")
            return False

    def copy_guide_to_clipboard(self, window_reference) -> bool:
        """Copiar la guía de impresión al portapapeles"""
        try:
            guia = self.producto.guia_impresion or "No hay guía disponible"
            window_reference.clipboard_clear()
            window_reference.clipboard_append(guia)
            if self.on_success:
                self.on_success("La guía de impresión se copió al portapapeles")
            return True
        except Exception as e:
            if self.on_error:
                self.on_error(f"Error al copiar: {str(e)}")
            return False

    def export_to_html(self) -> bool:
        """Generar un archivo HTML moderno con los detalles para imprimir"""
        try:
            from .services.html_export_service import HTMLExportService

            export_service = HTMLExportService()
            temp_path = export_service.generate_product_html(self.producto)

            webbrowser.open(str(temp_path.absolute()))
            if self.on_success:
                self.on_success(
                    "Documento generado y abierto en el navegador.\nUsa Ctrl+P (o Cmd+P en Mac) para imprimir.")
            return True

        except Exception as e:
            if self.on_error:
                self.on_error(f"Error al generar documento: {str(e)}")
            return False

    def get_guide_text(self) -> str:
        """Obtener texto de la guía con placeholder si no existe"""
        if self.producto.guia_impresion:
            return self.producto.guia_impresion

        return "📝 No hay guía de impresión disponible para este producto."