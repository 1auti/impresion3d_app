# ui/config/styles.py
"""
Configuración centralizada de estilos y colores para la aplicación
"""

import tkinter as tk
from tkinter import ttk


class ModernTheme:
    """Tema moderno con colores y estilos configurables"""

    def __init__(self):
        self.colors = {
            'bg': '#F8FAFC',
            'card': '#FFFFFF',
            'primary': '#6366F1',
            'primary_hover': '#5558E3',
            'secondary': '#EC4899',
            'success': '#10B981',
            'warning': '#F59E0B',
            'danger': '#EF4444',
            'text': '#1E293B',
            'text_secondary': '#64748B',
            'border': '#E2E8F0',
            'accent': '#F1F5F9',
            'input_bg': '#FFFFFF',
            'modified': '#FEF3C7'
        }

        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'caption': ('Segoe UI', 8)
        }

    def setup_ttk_styles(self):
        """Configurar estilos TTK"""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook styles
        style.configure('Modern.TNotebook',
                        background=self.colors['card'],
                        borderwidth=0,
                        relief='flat')

        style.configure('Modern.TNotebook.Tab',
                        background=self.colors['accent'],
                        foreground=self.colors['text'],
                        padding=(20, 12),
                        borderwidth=0,
                        font=self.fonts['body'])

        style.map('Modern.TNotebook.Tab',
                  background=[('selected', self.colors['primary']),
                              ('active', self.colors['primary_hover'])],
                  foreground=[('selected', 'white'),
                              ('active', 'white')])

        # Entry styles
        style.configure('Modern.TEntry',
                        fieldbackground=self.colors['input_bg'],
                        borderwidth=1,
                        relief='flat',
                        bordercolor=self.colors['border'],
                        font=self.fonts['body'])

        style.map('Modern.TEntry',
                  bordercolor=[('focus', self.colors['primary'])])

        style.configure('Modified.TEntry',
                        fieldbackground=self.colors['modified'],
                        borderwidth=2,
                        relief='flat',
                        bordercolor=self.colors['warning'],
                        font=self.fonts['body'])

        # Combobox styles
        style.configure('Modern.TCombobox',
                        fieldbackground=self.colors['input_bg'],
                        borderwidth=1,
                        relief='flat',
                        bordercolor=self.colors['border'],
                        font=self.fonts['body'])

        # Spinbox styles
        style.configure('Modern.TSpinbox',
                        fieldbackground=self.colors['input_bg'],
                        borderwidth=1,
                        relief='flat',
                        bordercolor=self.colors['border'],
                        font=self.fonts['body'])


class ButtonStyles:
    """Estilos para botones personalizados"""

    @staticmethod
    def get_button_style(style_name, theme):
        """Obtener configuración de estilo para botones"""
        styles = {
            'primary': (theme.colors['primary'], 'white', theme.colors['primary_hover']),
            'secondary': (theme.colors['card'], theme.colors['text'], theme.colors['accent']),
            'danger': (theme.colors['danger'], 'white', '#DC2626'),
            'success': (theme.colors['success'], 'white', '#059669'),
            'warning': (theme.colors['warning'], 'white', '#D97706')
        }
        return styles.get(style_name, styles['secondary'])