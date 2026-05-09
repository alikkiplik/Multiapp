import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.current_theme = "light"
        
        # Универсальная современная палитра
        self.palettes = {
            "light": {
                "bg": "#f8f9fa", "fg": "#212529", "entry_bg": "#ffffff",
                "btn_bg": "#0d6efd", "btn_fg": "#ffffff", "btn_active": "#0b5ed7",
                "canvas_bg": "#ffffff", "text_bg": "#ffffff", "hl_bg": "#e9ecef",
                "panel_bg": "#f8f9fa", "border": "#ced4da", "accent": "#0d6efd",
                "select_bg": "#0d6efd", "select_fg": "#ffffff"
            },
            "dark": {
                "bg": "#212529", "fg": "#f8f9fa", "entry_bg": "#343a40",
                "btn_bg": "#0d6efd", "btn_fg": "#ffffff", "btn_active": "#0b5ed7",
                "canvas_bg": "#1e1e1e", "text_bg": "#343a40", "hl_bg": "#495057",
                "panel_bg": "#212529", "border": "#6c757d", "accent": "#0d6efd",
                "select_bg": "#0d6efd", "select_fg": "#ffffff"
            }
        }
        self.t = self.palettes[self.current_theme]
        self.apply_theme("light")

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        self.t = self.palettes[theme_name]
        t = self.t
        self.root.config(bg=t["bg"])
        
        self.style.theme_use("default")
        self.style.configure(".", background=t["bg"], foreground=t["fg"], font=("Segoe UI", 10))
        self.style.configure("TFrame", background=t["bg"])
        self.style.configure("TLabel", background=t["bg"], foreground=t["fg"])
        self.style.configure("TLabelframe", background=t["bg"], foreground=t["fg"])
        self.style.configure("TLabelframe.Label", background=t["bg"], foreground=t["fg"], font=("Segoe UI", 10, "bold"))
        self.style.configure("TSeparator", background=t["border"])
        
        self.style.configure("TButton", background=t["btn_bg"], foreground=t["btn_fg"],
                             borderwidth=0, relief="flat", padding=(10, 4))
        self.style.map("TButton", background=[("active", t["btn_active"]), ("pressed", "#0a58ca")])
        
        self.style.configure("TNotebook", background=t["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", padding=[12, 6], background=t["hl_bg"],
                             foreground=t["fg"], relief="flat")
        self.style.map("TNotebook.Tab", background=[("selected", t["bg"])])
        
        self.style.configure("TScale", background=t["bg"], troughcolor=t["border"])
        self.style.configure("Horizontal.TScale", background=t["bg"])

    def get_colors(self):
        return self.t.copy()
