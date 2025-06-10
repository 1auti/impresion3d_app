#!/usr/bin/env python3
"""
Aplicación de Gestión de Productos para Impresión 3D
Punto de entrada principal
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from database.db_manager import DatabaseManager
import tkinter as tk
from tkinter import messagebox


def setup_directories():
    """Crear directorios necesarios si no existen"""
    directories = [
        Path("data"),
        Path("assets"),
        Path("assets/images")
    ]

    for directory in directories:
        directory.mkdir(exist_ok=True)


def main():
    """Función principal"""
    try:
        # Configurar directorios
        setup_directories()

        # Inicializar base de datos
        db_manager = DatabaseManager()
        db_manager.init_database()

        # Crear ventana principal
        root = tk.Tk()
        app = MainWindow(root)

        # Centrar ventana
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')

        # Iniciar aplicación
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar la aplicación: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()