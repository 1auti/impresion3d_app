"""
Punto de entrada principal de la aplicación 3D Print Manager
"""
import sys
from pathlib import Path

# Configurar path para importaciones
sys.path.append(str(Path(__file__).parent))


from ui import ModernMainWindow, create_application, check_ui_dependencies
from config.app_config import setup_application_directories


def main():
    """Función principal de la aplicación"""
    try:
        # Configurar directorios necesarios
        setup_application_directories()

        # ✅ Verificar dependencias UI
        deps = check_ui_dependencies()
        if not deps['PIL']:
            print("⚠️ Advertencia: PIL/Pillow no está disponible. Algunas funciones de imagen pueden fallar.")

        # ✅ OPCIÓN 1: Crear aplicación manualmente
        import tkinter as tk
        root = tk.Tk()
        app = ModernMainWindow(root)
        root.mainloop()



    except ImportError as e:
        error_msg = f"Error de importación: {str(e)}\n\nVerifica que todos los módulos estén disponibles."
        print(error_msg)
        sys.exit(1)

    except Exception as e:
        # Manejar errores críticos
        import traceback
        error_msg = f"Error crítico al iniciar la aplicación:\n\n{str(e)}\n\n{traceback.format_exc()}"

        # Mostrar error en ventana si es posible
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            tk.messagebox.showerror("Error Crítico", error_msg)
        except:
            # Si no se puede mostrar GUI, imprimir en consola
            print(error_msg)

        sys.exit(1)


if __name__ == "__main__":
    main()