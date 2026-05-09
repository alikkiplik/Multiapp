import tkinter as tk
import pygame
from app import MultiToolApp

if __name__ == "__main__":
    # ✅ Безопасная инициализация аудио ДО создания интерфейса
    try:
        pygame.mixer.init()
    except pygame.error:
        print("⚠️ Аудио-подсистема недоступна. Медиаплеер запустится в ограниченном режиме.")

    try:
        root = tk.Tk()
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except: pass
        
        app = MultiToolApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Критическая ошибка запуска: {e}")
        input("Нажмите Enter для выхода...")
