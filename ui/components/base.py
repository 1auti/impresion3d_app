# ui/components/base_components.py
"""
Componentes base reutilizables para la interfaz
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict, Any, List
from config.styles import ModernTheme, ButtonStyles


class ModernFrame(tk.Frame):
    """Frame base con tema moderno aplicado"""

    def __init__(self, parent, theme: ModernTheme, card_style=True, **kwargs):
        self.theme = theme
        bg_color = theme.colors['card'] if card_style else theme.colors['bg']

        super().__init__(
            parent,
            bg=bg_color,
            highlightbackground=theme.colors['border'],
            highlightthickness=1 if card_style else 0,
            **kwargs
        )


class ModernButton:
    """Factory para crear botones modernos"""

    @staticmethod
    def create(parent, text: str, command: Callable, style: str = 'secondary',
               theme: ModernTheme = None) -> tk.Frame:
        """Crear botón moderno con efectos hover"""
        if theme is None:
            theme = ModernTheme()

        bg, fg, hover = ButtonStyles.get_button_style(style, theme)

        btn_frame = tk.Frame(
            parent,
            bg=bg,
            highlightbackground=theme.colors['border'],
            highlightthickness=1 if style == 'secondary' else 0
        )

        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            font=theme.fonts['body'],
            bg=bg,
            fg=fg,
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2',
            activebackground=hover,
            activeforeground=fg
        )
        btn.pack(fill=tk.BOTH)

        # Efectos hover
        def on_enter(e):
            btn.config(bg=hover)
            btn_frame.config(bg=hover)

        def on_leave(e):
            btn.config(bg=bg)
            btn_frame.config(bg=bg)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        return btn_frame


class ModernField:
    """Factory para crear campos de entrada modernos"""

    @staticmethod
    def create_field(parent, field_name: str, label_text: str,
                     widget_type: str, variable: tk.Variable,
                     theme: ModernTheme, options: Dict = None) -> tk.Widget:
        """Crear campo moderno con etiqueta"""
        field_frame = tk.Frame(parent, bg=theme.colors['card'])
        field_frame.pack(fill=tk.X, pady=(0, 20))

        # Etiqueta
        label = tk.Label(
            field_frame,
            text=label_text,
            font=theme.fonts['body'],
            bg=theme.colors['card'],
            fg=theme.colors['text']
        )
        label.pack(anchor=tk.W, pady=(0, 8))

        # Widget según tipo
        widget = ModernField._create_widget(
            field_frame, widget_type, variable, theme, options or {}
        )
        widget.pack(fill=tk.X, ipady=8)

        return widget

    @staticmethod
    def _create_widget(parent, widget_type: str, variable: tk.Variable,
                       theme: ModernTheme, options: Dict) -> tk.Widget:
        """Crear widget específico según tipo"""
        if widget_type == 'entry':
            return ttk.Entry(
                parent,
                textvariable=variable,
                style='Modern.TEntry',
                font=theme.fonts['body']
            )

        elif widget_type == 'combobox':
            return ttk.Combobox(
                parent,
                textvariable=variable,
                values=options.get('values', []),
                style='Modern.TCombobox',
                font=theme.fonts['body'],
                state='readonly'
            )

        elif widget_type == 'spinbox':
            spinbox_options = {k: v for k, v in options.items()
                               if k in ['from_', 'to', 'increment']}
            return ttk.Spinbox(
                parent,
                textvariable=variable,
                style='Modern.TSpinbox',
                font=theme.fonts['body'],
                **spinbox_options
            )

        else:
            raise ValueError(f"Tipo de widget desconocido: {widget_type}")


class StatusBadge:
    """Componente de badge de estado"""

    def __init__(self, parent, theme: ModernTheme):
        self.theme = theme
        self.badge_frame = None
        self.status_label = None
        self.parent = parent

    def create(self, text: str, icon: str, color: str) -> tk.Frame:
        """Crear badge de estado"""
        self.badge_frame = tk.Frame(self.parent, bg=color, highlightthickness=0)

        content = tk.Frame(self.badge_frame, bg=color)
        content.pack(padx=15, pady=8)

        tk.Label(
            content,
            text=icon,
            font=self.theme.fonts['body'],
            bg=color,
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.status_label = tk.Label(
            content,
            text=text,
            font=self.theme.fonts['small'],
            bg=color,
            fg='white'
        )
        self.status_label.pack(side=tk.LEFT)

        return self.badge_frame

    def update(self, text: str, icon: str, color: str):
        """Actualizar badge de estado"""
        if self.badge_frame and self.status_label:
            self.badge_frame.configure(bg=color)
            self.status_label.configure(text=text, bg=color)

            # Actualizar color de todos los hijos
            for child in self.badge_frame.winfo_children():
                child.configure(bg=color)
                for subchild in child.winfo_children():
                    subchild.configure(bg=color)


class MessageDialog:
    """Diálogos de mensaje modernos"""

    @staticmethod
    def show_message(parent, title: str, message: str, msg_type: str = 'info',
                     theme: ModernTheme = None):
        """Mostrar mensaje moderno"""
        if theme is None:
            theme = ModernTheme()

        msg_window = tk.Toplevel(parent)
        msg_window.title(title)
        msg_window.geometry("400x200")
        msg_window.transient(parent)
        msg_window.grab_set()
        msg_window.configure(bg=theme.colors['card'])

        colors = {
            'success': ('#10B981', '✅'),
            'error': ('#EF4444', '❌'),
            'info': ('#6366F1', 'ℹ️'),
            'warning': ('#F59E0B', '⚠️')
        }

        color, icon = colors.get(msg_type, colors['info'])

        content = tk.Frame(msg_window, bg=theme.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        tk.Label(
            content,
            text=icon,
            font=('Segoe UI', 32),
            bg=theme.colors['card'],
            fg=color
        ).pack(pady=(0, 15))

        tk.Label(
            content,
            text=title,
            font=theme.fonts['subheading'],
            bg=theme.colors['card'],
            fg=theme.colors['text']
        ).pack()

        tk.Label(
            content,
            text=message,
            font=theme.fonts['body'],
            bg=theme.colors['card'],
            fg=theme.colors['text_secondary'],
            wraplength=340,
            justify=tk.CENTER
        ).pack(pady=(10, 20))

        btn = ModernButton.create(content, "Aceptar", msg_window.destroy, 'primary', theme)
        btn.pack()

        # Centrar ventana
        MessageDialog._center_window(msg_window)

        if msg_type == 'success':
            msg_window.after(3000, msg_window.destroy)

    @staticmethod
    def show_confirmation(parent, title: str, message: str,
                          theme: ModernTheme = None) -> bool:
        """Mostrar diálogo de confirmación"""
        if theme is None:
            theme = ModernTheme()

        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("450x250")
        dialog.transient(parent)
        dialog.grab_set()
        dialog.configure(bg=theme.colors['card'])

        content = tk.Frame(dialog, bg=theme.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        tk.Label(
            content,
            text="⚠️",
            font=('Segoe UI', 32),
            bg=theme.colors['card'],
            fg=theme.colors['warning']
        ).pack(pady=(0, 15))

        tk.Label(
            content,
            text=title,
            font=theme.fonts['subheading'],
            bg=theme.colors['card'],
            fg=theme.colors['text']
        ).pack()

        tk.Label(
            content,
            text=message,
            font=theme.fonts['body'],
            bg=theme.colors['card'],
            fg=theme.colors['text_secondary'],
            wraplength=380,
            justify=tk.CENTER
        ).pack(pady=(10, 20))

        btn_frame = tk.Frame(content, bg=theme.colors['card'])
        btn_frame.pack()

        result = {'confirmed': False}

        def confirm():
            result['confirmed'] = True
            dialog.destroy()

        btn_cancel = ModernButton.create(btn_frame, "Cancelar", dialog.destroy, 'secondary', theme)
        btn_cancel.pack(side=tk.LEFT, padx=5)

        btn_confirm = ModernButton.create(btn_frame, "Confirmar", confirm, 'primary', theme)
        btn_confirm.pack(side=tk.LEFT, padx=5)

        MessageDialog._center_window(dialog)
        dialog.wait_window()

        return result['confirmed']

    @staticmethod
    def _center_window(window):
        """Centrar ventana en pantalla"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
        y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
        window.geometry(f'+{x}+{y}')


class ScrollableFrame:
    """Frame con scroll personalizable"""

    def __init__(self, parent, theme: ModernTheme):
        self.theme = theme
        self.canvas = tk.Canvas(parent, bg=theme.colors['bg'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=theme.colors['bg'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def pack(self, **kwargs):
        """Pack canvas y scrollbar"""
        self.canvas.pack(side="left", fill="both", expand=True, **kwargs)
        self.scrollbar.pack(side="right", fill="y")

    def get_frame(self) -> tk.Frame:
        """Obtener frame scrollable"""
        return self.scrollable_frame