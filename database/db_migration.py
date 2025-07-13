# database/db_migration.py
"""
Migración de base de datos para soporte avanzado de piezas
"""

import sqlite3
from pathlib import Path
from typing import Dict, Any


class DatabaseMigrator:
    """Manejador de migraciones de base de datos"""
    
    def __init__(self, db_path: str = "data/productos.db"):
        self.db_path = Path(db_path)
        self.migrations = {
            1: self._migration_001_add_piece_details,
            # Aquí puedes agregar más migraciones futuras
        }
    
    def get_connection(self):
        """Obtener conexión a la base de datos"""
        return sqlite3.connect(str(self.db_path))
    
    def get_current_version(self) -> int:
        """Obtener versión actual de la base de datos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Crear tabla de versiones si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schema_versions (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Obtener versión actual
            cursor.execute('SELECT MAX(version) FROM schema_versions')
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0
    
    def set_version(self, version: int):
        """Establecer versión de la base de datos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO schema_versions (version) VALUES (?)', 
                (version,)
            )
            conn.commit()
    
    def run_migrations(self) -> Dict[str, Any]:
        """Ejecutar todas las migraciones pendientes"""
        current_version = self.get_current_version()
        results = {
            'success': True,
            'migrations_applied': [],
            'errors': []
        }
        
        print(f"📊 Versión actual de la base de datos: {current_version}")
        
        for version, migration_func in self.migrations.items():
            if version > current_version:
                try:
                    print(f"🔄 Ejecutando migración {version}...")
                    migration_func()
                    self.set_version(version)
                    results['migrations_applied'].append(version)
                    print(f"✅ Migración {version} completada")
                except Exception as e:
                    error_msg = f"Migración {version} falló: {str(e)}"
                    print(f"❌ {error_msg}")
                    results['errors'].append(error_msg)
                    results['success'] = False
                    break
        
        if not results['migrations_applied']:
            print("✅ Base de datos actualizada, no hay migraciones pendientes")
        
        return results
    
    def _migration_001_add_piece_details(self):
        """Migración 001: Agregar campos detallados para piezas"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Verificar si ya están los nuevos campos
            cursor.execute("PRAGMA table_info(color_piezas)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Lista de nuevos campos a agregar
            new_fields = [
                ('peso_pieza', 'REAL DEFAULT 0.0'),
                ('descripcion_pieza', 'TEXT'),
                ('tiempo_impresion_pieza', 'INTEGER DEFAULT 0'),
                ('orientacion_recomendada', 'TEXT'),
                ('requiere_soportes', 'BOOLEAN DEFAULT 0'),
                ('nivel_dificultad', 'TEXT DEFAULT "Fácil"'),
                ('notas_postproceso', 'TEXT'),
                ('orden_ensamblaje', 'INTEGER DEFAULT 0'),
                ('tipo_union', 'TEXT DEFAULT "Encaje"'),  # Encaje, Pegamento, Tornillo, etc.
                ('tolerancia_encaje', 'REAL DEFAULT 0.2'),  # mm de tolerancia
            ]
            
            # Agregar campos que no existan
            for field_name, field_definition in new_fields:
                if field_name not in columns:
                    query = f'ALTER TABLE color_piezas ADD COLUMN {field_name} {field_definition}'
                    cursor.execute(query)
                    print(f"   ✅ Agregado campo: {field_name}")
            
            # Crear índices para mejorar rendimiento
            indexes = [
                'CREATE INDEX IF NOT EXISTS idx_piezas_peso ON color_piezas(peso_pieza)',
                'CREATE INDEX IF NOT EXISTS idx_piezas_dificultad ON color_piezas(nivel_dificultad)',
                'CREATE INDEX IF NOT EXISTS idx_piezas_orden ON color_piezas(orden_ensamblaje)',
            ]
            
            for index_query in indexes:
                cursor.execute(index_query)
            
            conn.commit()
    
    def backup_database(self) -> str:
        """Crear backup de la base de datos antes de migrar"""
        import shutil
        from datetime import datetime
        
        if not self.db_path.exists():
            return ""
        
        # Crear directorio de backup
        backup_dir = Path("data/backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Generar nombre del backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"productos_backup_{timestamp}.db"
        
        # Copiar base de datos
        shutil.copy2(self.db_path, backup_path)
        print(f"📋 Backup creado: {backup_path}")
        
        return str(backup_path)


def run_database_migration():
    """Función principal para ejecutar migraciones"""
    print("🚀 Iniciando migración de base de datos...")
    
    migrator = DatabaseMigrator()
    
    # Crear backup
    backup_path = migrator.backup_database()
    
    # Ejecutar migraciones
    results = migrator.run_migrations()
    
    if results['success']:
        print("🎉 ¡Migración completada exitosamente!")
        if results['migrations_applied']:
            print(f"Migraciones aplicadas: {results['migrations_applied']}")
    else:
        print("💥 Error durante la migración:")
        for error in results['errors']:
            print(f"   ❌ {error}")
        if backup_path:
            print(f"💾 Restaure desde el backup: {backup_path}")
    
    return results


# Script independiente para ejecutar migración
if __name__ == "__main__":
    run_database_migration()