"""
Widgets modernos reutilizables para la aplicación
"""
import tkinter as tk
from tkinter import ttk
from ..style.color_palette  import ColorPalette


class ModernWidgets:
    """Factory para crear widgets modernos"""

    def __init__(self, colors=None, fonts=None):
        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {
            'title': ('Segoe UI', 24, 'bold'),
            'heading': ('Segoe UI', 14, 'bold'),
            'subheading': ('Segoe UI', 12),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9)
        }

    def create_modern_button(self, parent, text, command, style='secondary'):
        """Crear botón moderno con efectos"""
        colors = {
            'primary': (self.colors['primary'], 'white', self.colors['primary_hover']),
            'secondary': (self.colors['card'], self.colors['text'], self.colors['bg']),
            'danger': (self.colors['danger'], 'white', '#DC2626')
        }

        bg, fg, hover = colors.get(style, colors['secondary'])

        btn_frame = tk.Frame(parent, bg=bg, highlightbackground=self.colors['border'],
                             highlightthickness=1 if style == 'secondary' else 0)

        btn = tk.Button(btn_frame, text=text, command=command,
                        font=self.fonts['body'], bg=bg, fg=fg,
                        bd=0, padx=20, pady=12, cursor='hand2',
                        activebackground=hover, activeforeground=fg)
        btn.pack(fill=tk.BOTH)

        # Efectos hover
        def on_enter(e):
            if btn['state'] != 'disabled':
                btn.config(bg=hover)
                btn_frame.config(bg=hover)

        def on_leave(e):
            if btn['state'] != 'disabled':
                btn.config(bg=bg)
                btn_frame.config(bg=bg)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        # Guardar referencia al botón interno
        btn_frame.inner_button = btn

        return btn_frame

    def create_modern_entry(self, parent, textvariable, placeholder):
        """Crear entry moderno con placeholder"""
        entry_frame = tk.Frame(parent, bg='white', highlightbackground=self.colors['border'],
                               highlightthickness=1)

        entry = tk.Entry(entry_frame, textvariable=textvariable,
                         font=self.fonts['body'], bd=0, bg='white',
                         fg=self.colors['text'])
        entry.pack(fill=tk.BOTH, padx=10, pady=10)

        # Placeholder
        def on_focus_in(e):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=self.colors['text'])

        def on_focus_out(e):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=self.colors['text_secondary'])

        entry.insert(0, placeholder)
        entry.config(fg=self.colors['text_secondary'])
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        # Efectos hover
        entry_frame.bind('<Enter>', lambda e: entry_frame.config(
            highlightbackground=self.colors['primary']))
        entry_frame.bind('<Leave>', lambda e: entry_frame.config(
            highlightbackground=self.colors['border']))

        return entry_frame

    def create_header_button(self, parent, text, command):
        """Crear botón moderno para el header"""
        btn = tk.Button(parent, text=text, command=command,
                        font=self.fonts['body'],
                        bg='white', fg=self.colors['primary'],
                        bd=0, padx=20, pady=8,
                        cursor='hand2',
                        activebackground=self.colors['bg'])

        # Efectos hover
        btn.bind('<Enter>', lambda e: btn.config(bg=self.colors['bg']))
        btn.bind('<Leave>', lambda e: btn.config(bg='white'))

        return btn

    def create_stat_card(self, parent, value, label, color, row, col):
        """Crear tarjeta de estadística"""
        card = tk.Frame(parent, bg=color, highlightthickness=0)
        card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        parent.grid_columnconfigure(col, weight=1)

        # Contenido
        content = tk.Frame(card, bg=color)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(content, text=value, font=('Segoe UI', 20, 'bold'),
                 bg=color, fg='white').pack()
        tk.Label(content, text=label, font=self.fonts['small'],
                 bg=color, fg='white').pack()

    def create_tooltip(self, widget, text):
        """Crear tooltip para widget"""

        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

            label = tk.Label(tooltip, text=text, font=self.fonts['small'],
                             bg=self.colors['text'], fg='white',
                             padx=10, pady=5)
            label.pack()

            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def create_color_sample(self, parent, color_hex, color_name):
        """Crear muestra de color con tooltip"""
        color_frame = tk.Frame(parent, bg=color_hex, width=30, height=30,
                               highlightthickness=1, highlightbackground=self.colors['border'])
        color_frame.pack(side=tk.LEFT, padx=2)
        color_frame.pack_propagate(False)

        # Tooltip
        self.create_tooltip(color_frame, color_name)

        return color_frame

    def create_floating_action_button(self, parent, command):
        """Crear Floating Action Button"""
        fab = tk.Button(parent, text="➕", font=('Segoe UI', 20),
                        bg=self.colors['secondary'], fg='white',
                        bd=0, padx=20, pady=15,
                        cursor='hand2', command=command)

        # Hacer el botón circular
        fab.config(width=3, height=2)

        # Efectos hover
        def on_enter(e):
            fab.config(bg='#C026D3')

        def on_leave(e):
            fab.config(bg=self.colors['secondary'])

        fab.bind('<Enter>', on_enter)
        fab.bind('<Leave>', on_leave)

        return fab


class ModernTreeview:
    """Treeview moderno con funcionalidades adicionales"""

    def __init__(self, parent, columns, colors=None, fonts=None):
        self.colors = colors or ColorPalette.get_colors_dict()
        self.fonts = fonts or {'body': ('Segoe UI', 10)}

        # Crear Treeview
        self.tree = ttk.Treeview(parent, columns=columns, show='tree headings',
                                 style='Modern.Treeview', height=15)

        # Configurar scrollbar
        self.vsb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)

        # Tags para colores alternados
        self.tree.tag_configure('oddrow', background=self.colors['bg'])
        self.tree.tag_configure('evenrow', background='white')

    def pack_with_scrollbar(self):
        """Empaquetar treeview con scrollbar"""
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def configure_columns(self, column_config):
        """Configurar columnas del treeview

        Args:
            column_config: dict con configuración de columnas
            Ejemplo: {
                '#0': {'width': 0, 'stretch': False},
                'ID': {'width': 60, 'anchor': 'center', 'heading': 'ID'},
                'Nombre': {'width': 300, 'heading': 'Nombre del Producto'}
            }
        """
        for col, config in column_config.items():
            if 'width' in config:
                self.tree.column(col, width=config['width'])
            if 'anchor' in config:
                self.tree.column(col, anchor=config['anchor'])
            if 'stretch' in config:
                self.tree.column(col, stretch=config['stretch'])
            if 'heading' in config and col != '#0':
                self.tree.heading(col, text=config['heading'])

    def clear_and_populate(self, data_list):
        """Limpiar y poblar el treeview con datos"""
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Poblar con colores alternados
        for i, item_data in enumerate(data_list):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=item_data, tags=(tag,))

    def get_selected_values(self):
        """Obtener valores del item seleccionado"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None