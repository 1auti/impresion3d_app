"""
Servicio para exportar detalles de producto a HTML
"""
from pathlib import Path
from typing import Dict, Any
from models.producto import Producto


class HTMLExportService:
    """Servicio para generar exportaciones HTML de productos"""

    @staticmethod
    def generate_product_html(producto: Producto) -> Path:
        """Generar archivo HTML moderno con los detalles del producto"""

        # Generar agrupaciones de color
        color_groups = HTMLExportService._get_color_groups(producto)

        # Crear contenido HTML
        html_content = HTMLExportService._generate_html_template(producto, color_groups)

        # Guardar archivo
        temp_path = Path("temp_print_modern.html")
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return temp_path

    @staticmethod
    def _get_color_groups(producto: Producto) -> Dict[str, Dict]:
        """Agrupar especificaciones por color"""
        color_groups = {}
        for spec in producto.colores_especificaciones:
            if spec.color_hex not in color_groups:
                color_groups[spec.color_hex] = {
                    'nombre': spec.nombre_color,
                    'piezas': [],
                    'peso_total': 0,
                    'tiempo_adicional': spec.tiempo_adicional
                }
            color_groups[spec.color_hex]['piezas'].extend(spec.piezas)
            color_groups[spec.color_hex]['peso_total'] += spec.peso_color
        return color_groups

    @staticmethod
    def _generate_html_template(producto: Producto, color_groups: Dict[str, Dict]) -> str:
        """Generar plantilla HTML completa"""

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Detalles - {producto.nombre}</title>
    <style>
        {HTMLExportService._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {HTMLExportService._generate_header(producto)}
        <div class="content">
            {HTMLExportService._generate_basic_info_section(producto)}
            {HTMLExportService._generate_config_section(producto)}
            {HTMLExportService._generate_color_section(producto, color_groups)}
            {HTMLExportService._generate_guide_section(producto)}
        </div>
        {HTMLExportService._generate_footer(producto)}
    </div>
</body>
</html>"""
        return html_content

    @staticmethod
    def _get_css_styles() -> str:
        """Obtener estilos CSS modernos"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #1E293B;
            background: #F8FAFC;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #6366F1, #EC4899);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .content {
            padding: 30px;
        }

        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #F8FAFC;
            border-radius: 8px;
            border-left: 4px solid #6366F1;
        }

        .section h2 {
            color: #6366F1;
            font-size: 1.4em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .info-item {
            background: white;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #E2E8F0;
        }

        .info-label {
            font-weight: 600;
            color: #64748B;
            font-size: 0.9em;
            margin-bottom: 5px;
        }

        .info-value {
            font-size: 1.1em;
            color: #1E293B;
            font-weight: 500;
        }

        .color-spec {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }

        .color-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }

        .color-sample {
            width: 30px;
            height: 30px;
            border-radius: 6px;
            border: 2px solid #E2E8F0;
        }

        .color-info h3 {
            font-size: 1.1em;
            margin-bottom: 5px;
        }

        .color-meta {
            color: #64748B;
            font-size: 0.9em;
        }

        .pieces {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .piece {
            background: #F1F5F9;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            color: #475569;
        }

        .guide {
            white-space: pre-wrap;
            background: #F8FAFC;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            line-height: 1.5;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #64748B;
            border-top: 1px solid #E2E8F0;
            font-size: 0.9em;
        }

        .badges {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .badge {
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }

        @media print {
            body { background: white; padding: 0; }
            .container { box-shadow: none; }
            .header { background: #6366F1 !important; }
        }"""

    @staticmethod
    def _generate_header(producto: Producto) -> str:
        """Generar header HTML"""
        return f"""
        <div class="header">
            <h1>🖨️ {producto.nombre}</h1>
            <p class="subtitle">Especificaciones Técnicas de Impresión 3D</p>
            <div class="badges">
                <span class="badge">📦 ID: {producto.id}</span>
                <span class="badge">🔧 {producto.material}</span>
                <span class="badge">⚖️ {producto.get_peso_total()}g</span>
                <span class="badge">⏱️ {producto.tiempo_impresion_formato()}</span>
            </div>
        </div>"""

    @staticmethod
    def _generate_basic_info_section(producto: Producto) -> str:
        """Generar sección de información básica"""
        return f"""
        <div class="section">
            <h2>ℹ️ Información Básica</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Descripción</div>
                    <div class="info-value">{producto.descripcion or 'Sin descripción'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Material</div>
                    <div class="info-value">{producto.material}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Peso Total</div>
                    <div class="info-value">{producto.get_peso_total()} gramos</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Tiempo Base</div>
                    <div class="info-value">{producto.tiempo_impresion} minutos</div>
                </div>
            </div>
        </div>"""

    @staticmethod
    def _generate_config_section(producto: Producto) -> str:
        """Generar sección de configuración"""
        return f"""
        <div class="section">
            <h2>⚙️ Configuración de Impresión</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Temperatura Extrusor</div>
                    <div class="info-value">{producto.temperatura_extrusor}°C</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Temperatura Cama</div>
                    <div class="info-value">{producto.temperatura_cama}°C</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Tiempo Total Estimado</div>
                    <div class="info-value">{producto.get_tiempo_total()} minutos</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Colores Diferentes</div>
                    <div class="info-value">{len(producto.colores_especificaciones)}</div>
                </div>
            </div>
        </div>"""

    @staticmethod
    def _generate_color_section(producto: Producto, color_groups: Dict[str, Dict]) -> str:
        """Generar sección de especificaciones de color"""
        if not color_groups:
            return ""

        color_specs_html = ""
        for color_hex, group in color_groups.items():
            pieces_html = ''.join([f'<span class="piece">{pieza}</span>' for pieza in group['piezas']])

            tiempo_adicional_text = ""
            if group['tiempo_adicional'] > 0:
                tiempo_adicional_text = f" • +{group['tiempo_adicional']} min"

            color_specs_html += f"""
            <div class="color-spec">
                <div class="color-header">
                    <div class="color-sample" style="background-color: {color_hex};"></div>
                    <div class="color-info">
                        <h3>{group['nombre'] or 'Sin nombre'}</h3>
                        <div class="color-meta">{color_hex} • {group['peso_total']:.1f}g{tiempo_adicional_text}</div>
                    </div>
                </div>
                <div class="pieces">{pieces_html}</div>
            </div>"""

        return f"""
        <div class="section">
            <h2>🎨 Especificaciones de Color</h2>
            {color_specs_html}
        </div>"""

    @staticmethod
    def _generate_guide_section(producto: Producto) -> str:
        """Generar sección de guía"""
        guide_text = producto.guia_impresion or 'No hay guía disponible'
        return f"""
        <div class="section">
            <h2>📖 Guía de Impresión</h2>
            <div class="guide">{guide_text}</div>
        </div>"""

    @staticmethod
    def _generate_footer(producto: Producto) -> str:
        """Generar footer HTML"""
        fecha_creacion = producto.fecha_creacion.strftime('%d/%m/%Y %H:%M') if producto.fecha_creacion else 'N/A'
        fecha_modificacion = producto.fecha_modificacion.strftime(
            '%d/%m/%Y %H:%M') if producto.fecha_modificacion else 'N/A'

        return f"""
        <div class="footer">
            <p>Generado el {fecha_creacion}</p>
            <p>Última modificación: {fecha_modificacion}</p>
        </div>"""