import tkinter as tk
from tkinter import ttk

class SettingsModule(ttk.Frame):
    def __init__(self, parent, theme_mgr, on_toggle_theme):
        super().__init__(parent)
        self.theme_mgr = theme_mgr
        self.on_toggle_theme = on_toggle_theme
        self._setup_ui()

    def _setup_ui(self):
        doc_frame = ttk.LabelFrame(self, text="📖 Документация проекта", padding=10)
        doc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.doc_text = tk.Text(doc_frame, wrap=tk.WORD, font=("Consolas", 10), state=tk.DISABLED)
        scroll = ttk.Scrollbar(doc_frame, command=self.doc_text.yview)
        self.doc_text.config(yscrollcommand=scroll.set, state=tk.NORMAL)
        self.doc_text.insert(tk.END, self._get_docs())
        self.doc_text.config(state=tk.DISABLED)
        self.doc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        dev_frame = ttk.LabelFrame(self, text="👨‍💻 О системе", padding=10)
        dev_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(dev_frame, text="Команда: sahariadev", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=2)
        ttk.Label(dev_frame, text="Версия: v8.0 (Modern Edition)", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(dev_frame, text="Лицензия: MIT (Open Source)", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(dev_frame, text="Интерфейс: Современный кроссплатформенный дизайн", font=("Segoe UI", 10)).pack(anchor=tk.W, pady=(5, 0))
        
        ttk.Button(self, text="🌗 Переключить тему", command=self.on_toggle_theme).pack(pady=15)

    def apply_colors(self, colors):
        self.doc_text.config(bg=colors["text_bg"], fg=colors["fg"])

    def _get_docs(self):
        return """📌 ГОРЯЧИЕ КЛАВИШИ:
• Ctrl+N / Ctrl+O / Ctrl+S  - Новый / Открыть / Сохранить
• Ctrl+A / Ctrl+C / Ctrl+X / Ctrl+V - Выделить / Копировать / Вырезать / Вставить
• Ctrl+Z / Ctrl+Y           - Отмена / Повтор
• F1 / F2                   - Тёмная / Светлая тема
• Space                     - Play / Pause
📌 РЕДАКТОР: 15 шрифтов, таблицы до 20×20, подсветка Python, .docx поддержка
📌 PAINT: 11 инструментов (карандаш, маркер, стрелка, фигуры, звезда и др.)
📌 ПЛЕЕР: Аудио/Видео, плейлист, ffmpeg для видео-звука
✅ Современный UI, плавные анимации, адаптивная тема"""
