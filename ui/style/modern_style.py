""" Configuracion de estilos modernos para la aplicaicon """

from tkinter import ttk
from .color_palette import ColorPalette

class ModernStyle:
    """ Configuracion de los colores de la aplicacion """

    def __init__(self):
        self.colors =  ColorPalette.get_colors_dict()
        self.fonts =  self._setup_fonts()

    def _setup_fonts(self):
        """Configurar fuentes del sistema"""
        return {
            'title': ('Segoe UI', 24, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9)
        }

    def apply_styles(self, root):
        """Aplicar estilos a la aplicación"""
        # Configurar fondo principal
        root.configure(bg=self.colors['bg'])

        # Configurar estilo ttk
        style = ttk.Style()
        style.theme_use('clam')

        self._configure_frame_styles(style)
        self._configure_label_styles(style)
        self._configure_button_styles(style)
        self._configure_entry_styles(style)
        self._configure_treeview_styles(style)

    def _configure_frame_styles(self, style):
        """Configurar estilos de frames"""
        style.configure('Card.TFrame',
                        background=self.colors['card'],
                        relief='flat',
                        borderwidth=1)

        style.configure('Sidebar.TFrame',
                        background=self.colors['card'],
                        relief='flat',
                        borderwidth=0)

    def _configure_label_styles(self, style):
        """Configurar estilos de labels"""
        style.configure('Title.TLabel',
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        font=self.fonts['title'])

        style.configure('Heading.TLabel',
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        font=self.fonts['heading'])

        style.configure('Body.TLabel',
                        background=self.colors['card'],
                        foreground=self.colors['text_secondary'],
                        font=self.fonts['body'])

    def _configure_button_styles(self, style):
        """Configurar estilos de botones"""
        # Botón primario
        style.configure('Primary.TButton',
                        font=self.fonts['body'],
                        borderwidth=0,
                        relief='flat',
                        background=self.colors['primary'],
                        foreground='white',
                        padding=(15, 10),
                        anchor='center')

        style.map('Primary.TButton',
                  background=[('active', self.colors['primary_hover']),
                              ('pressed', self.colors['primary_hover'])],
                  foreground=[('active', 'white')])

        # Botón secundario
        style.configure('Secondary.TButton',
                        font=self.fonts['body'],
                        borderwidth=1,
                        relief='flat',
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        padding=(15, 10))

        style.map('Secondary.TButton',
                  background=[('active', self.colors['bg'])],
                  bordercolor=[('focus', self.colors['primary'])])

        # Botón de peligro
        style.configure('Danger.TButton',
                        font=self.fonts['body'],
                        borderwidth=0,
                        relief='flat',
                        background=self.colors['danger'],
                        foreground='white',
                        padding=(15, 10))

        style.map('Danger.TButton',
                  background=[('active', '#DC2626')])

    def _configure_entry_styles(self, style):
        """Configurar estilos de campos de entrada"""
        style.configure('Modern.TEntry',
                        fieldbackground='white',
                        borderwidth=1,
                        relief='flat',
                        padding=10)

        style.map('Modern.TEntry',
                  bordercolor=[('focus', self.colors['primary'])])

    def _configure_treeview_styles(self, style):
        """Configurar estilos del Treeview"""
        style.configure('Modern.Treeview',
                        background='white',
                        foreground=self.colors['text'],
                        rowheight=50,
                        fieldbackground='white',
                        borderwidth=0,
                        relief='flat',
                        font=self.fonts['body'])

        style.configure('Modern.Treeview.Heading',
                        background=self.colors['bg'],
                        foreground=self.colors['text'],
                        relief='flat',
                        font=self.fonts['subheading'])

        style.map('Modern.Treeview',
                  background=[('selected', self.colors['primary'])],
                  foreground=[('selected', 'white')])