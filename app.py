import tkinter as tk
from tkinter import ttk
import pygame
from theme_manager import ThemeManager
from modules import TextEditorModule, PaintModule, MediaPlayerModule, SettingsModule

class MultiToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖥️ MultiTool Desktop v8.1")
        self.root.geometry("1150x800")
        self.root.minsize(900, 600)
        self.is_running = True

        self.theme_mgr = ThemeManager(root)
        self._setup_top_panel()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.editor = TextEditorModule(self.notebook, self.theme_mgr)
        self.notebook.add(self.editor, text="📝 Редактор")

        self.paint = PaintModule(self.notebook, self.theme_mgr)
        self.notebook.add(self.paint, text="🎨 Paint")

        self.media = MediaPlayerModule(self.notebook, self.theme_mgr)
        self.notebook.add(self.media, text="🎬 Плеер")

        self.settings = SettingsModule(self.notebook, self.theme_mgr, self.toggle_theme)
        self.notebook.add(self.settings, text="⚙️ Настройки")

        self._apply_module_themes()
        self._setup_global_hotkeys()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _setup_top_panel(self):
        panel = ttk.Frame(self.root, relief="raised", borderwidth=1)
        panel.pack(fill=tk.X, side=tk.TOP)
        ttk.Label(panel, text="MultiTool Desktop | Профессиональный набор утилит", font=("Segoe UI", 11, "bold"), padding=(10, 2)).pack(side=tk.LEFT)
        self.theme_btn = ttk.Button(panel, text="Светлая", command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT, padx=10)

    def toggle_theme(self):
        new = "dark" if self.theme_mgr.current_theme == "light" else "light"
        self.theme_mgr.apply_theme(new)
        self.theme_btn.config(text="Тёмная" if new == "dark" else "Светлая")
        self._apply_module_themes()

    def _apply_module_themes(self):
        t = self.theme_mgr.get_colors()
        self.editor.apply_colors(t)
        self.paint.apply_colors(t)
        self.media.apply_colors(t)
        self.settings.apply_colors(t)

    def _setup_global_hotkeys(self):
        # ✅ bind_all + паттерн `func() or "break"` гарантирует срабатывание и остановкуPropagation
        self.root.bind_all("<Control-n>", lambda e: self.editor.new_file() or "break")
        self.root.bind_all("<Control-o>", lambda e: self.editor.open_file() or "break")
        self.root.bind_all("<Control-s>", lambda e: self.editor.save_file() or "break")
        self.root.bind_all("<F1>", lambda e: (self.theme_mgr.apply_theme("dark"), self._apply_module_themes()) or "break")
        self.root.bind_all("<F2>", lambda e: (self.theme_mgr.apply_theme("light"), self._apply_module_themes()) or "break")
        self.root.bind_all("<space>", lambda e: (self.media.play_media() if not self.media.is_playing else self.media.pause_media()) or "break")

    def on_close(self):
        self.is_running = False
        if self.media.temp_audio_path and self.media.temp_audio_path:
            import os
            if os.path.exists(self.media.temp_audio_path): os.remove(self.media.temp_audio_path)
        if self.media.video_cap: self.media.video_cap.release()
        try: pygame.mixer.quit()
        except: pass
        self.root.destroy()
