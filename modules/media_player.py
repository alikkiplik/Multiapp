import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame, os, cv2, tempfile, subprocess
from PIL import Image, ImageTk

class MediaPlayerModule(ttk.Frame):
    def __init__(self, parent, theme_mgr):
        super().__init__(parent)
        self.theme_mgr = theme_mgr
        self.playlist = []
        self.current_idx = -1
        self.media_file = None
        self.is_video = False
        self.is_playing = False
        self.video_cap = None
        self.media_length = 0.0
        self.temp_audio_path = None
        self._setup_ui()
        self._start_progress_loop()

    def _setup_ui(self):
        main = ttk.Frame(self)
        main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        left = ttk.Frame(main); left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right = ttk.Frame(main); right.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        self.video_frame = ttk.Frame(left, relief="solid", borderwidth=2)
        self.video_label = tk.Label(self.video_frame, bg="black")
        self.video_label.pack(fill=tk.BOTH, expand=True)
        
        ctrl = ttk.Frame(left)
        ctrl.pack(fill=tk.X, pady=5)
        self.file_label = ttk.Label(ctrl, text="Файл не выбран", wraplength=500)
        self.file_label.pack(fill=tk.X, pady=(0, 5))
        self.audio_status = ttk.Label(ctrl, text="", foreground="#0d6efd")
        self.audio_status.pack(pady=(0, 5))
        
        btns = ttk.Frame(ctrl)
        btns.pack(fill=tk.X, pady=5)
        ttk.Button(btns, text="⏮ Пред.", command=self.prev_track).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="▶️ Играть", command=self.play_media).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="⏸ Пауза", command=self.pause_media).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="⏹ Стоп", command=self.stop_media).pack(side=tk.LEFT, padx=2)
        ttk.Button(btns, text="⏭ След.", command=self.next_track).pack(side=tk.LEFT, padx=2)
        
        self.progress = ttk.Scale(ctrl, from_=0, to=100, orient=tk.HORIZONTAL, state="disabled")
        self.progress.pack(fill=tk.X, pady=5)
        self.progress.bind("<ButtonRelease-1>", self.seek_media)
        
        vol = ttk.Frame(ctrl)
        vol.pack(fill=tk.X, pady=5)
        ttk.Label(vol, text="🔊").pack(side=tk.LEFT)
        self.vol_label = ttk.Label(vol, text="70%")
        self.vol_label.pack(side=tk.RIGHT)
        self.vol_scale = ttk.Scale(vol, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.vol_scale.set(0.7)
        self.vol_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.time_label = ttk.Label(ctrl, text="00:00 / 00:00")
        self.time_label.pack(pady=2)
        
        self.listbox = tk.Listbox(right, bg="#fcfcfc", fg="#212529", selectbackground="#0d6efd", selectforeground="#fff", font=("Segoe UI", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.listbox.bind("<<ListboxSelect>>", self.play_selected)
        
        pl_tb = ttk.Frame(right)
        pl_tb.pack(fill=tk.X)
        ttk.Button(pl_tb, text="+ Добавить", command=self.add_to_playlist).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(pl_tb, text="- Удалить", command=self.remove_from_playlist).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(pl_tb, text="Очистить", command=self.clear_playlist).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def apply_colors(self, colors):
        self.listbox.config(bg=colors["entry_bg"], fg=colors["fg"], selectbackground=colors["select_bg"])
        self.file_label.config(foreground=colors["fg"])
        self.video_label.config(bg="#000000")

    def set_volume(self, val):
        try:
            pygame.mixer.music.set_volume(float(val))
            self.vol_label.config(text=f"{int(float(val)*100)}%")
        except pygame.error:
            pass  # Игнорируем, если микшер недоступен

    def seek_media(self, event=None):
        if self.media_length > 0 and self.is_playing:
            pos = (self.progress.get() / 100.0) * self.media_length
            try: pygame.mixer.music.set_pos(pos)
            except pygame.error: 
                pygame.mixer.music.rewind()
                pygame.mixer.music.play(start=pos)
            if self.is_video and self.video_cap: self.video_cap.set(cv2.CAP_PROP_POS_MSEC, pos * 1000)

    def add_to_playlist(self):
        files = filedialog.askopenfilenames(filetypes=[("Media", "*.mp3 *.wav *.ogg *.mp4 *.avi *.mkv *.mov")])
        for f in files:
            if f not in self.playlist: self.playlist.append(f); self.listbox.insert(tk.END, os.path.basename(f))

    def remove_from_playlist(self):
        idx = self.listbox.curselection()
        if idx: self.playlist.pop(idx[0]); self.listbox.delete(idx[0])

    def clear_playlist(self): self.playlist.clear(); self.listbox.delete(0, tk.END); self.stop_media()

    def play_selected(self, event=None):
        idx = self.listbox.curselection()
        if idx: self.current_idx = idx[0]; self.load_media(self.playlist[idx[0]])

    def load_media(self, path=None):
        if path is None: return
        self.stop_media()
        self.media_file = path
        self.file_label.config(text=f"📁 {os.path.basename(path)}")
        self.progress.config(state="normal"); self.progress.set(0)
        self.time_label.config(text="00:00 / 00:00")
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext in {".mp3", ".wav", ".ogg"}:
                self.is_video = False; self._load_audio(path)
                temp = pygame.mixer.Sound(path); self.media_length = temp.get_length()
                self.video_frame.pack_forget()
            elif ext in {".mp4", ".avi", ".mkv", ".mov"}:
                self.is_video = True; self._load_audio(path)
                if self.video_cap: self.video_cap.release()
                self.video_cap = cv2.VideoCapture(path)
                fps = self.video_cap.get(cv2.CAP_PROP_FPS)
                frames = self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
                self.media_length = frames / fps if fps > 0 else 10
                self.video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
                self._show_first_frame()
        except Exception as e: messagebox.showerror("Ошибка", str(e))

    def _has_ffmpeg(self):
        try: subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True); return True
        except: return False

    def _load_audio(self, path):
        try: pygame.mixer.music.load(path); self.audio_status.config(text="✅ Встроенный кодек")
        except pygame.error:
            if self._has_ffmpeg():
                self.temp_audio_path = tempfile.mktemp(suffix=".wav")
                subprocess.run(["ffmpeg", "-i", path, "-vn", "-acodec", "pcm_s16le", "-y", self.temp_audio_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                pygame.mixer.music.load(self.temp_audio_path); self.audio_status.config(text="✅ Извлечено через ffmpeg")
            else: self.audio_status.config(text="⚠️ ffmpeg не найден")

    def _show_first_frame(self):
        ret, frame = self.video_cap.read()
        if ret:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img.thumbnail((700, 400))
            self.tk_img = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=self.tk_img)

    def play_media(self):
        if not self.media_file or self.is_playing: return
        try:
            self.is_playing = True; pygame.mixer.music.play()
            if self.is_video: self._play_video_loop()
        except pygame.error: messagebox.showerror("Аудио", "Микшер не инициализирован")

    def pause_media(self):
        if self.is_playing: 
            try: pygame.mixer.music.pause()
            except: pass
            self.is_playing = False

    def stop_media(self):
        self.is_playing = False
        try: pygame.mixer.music.stop()
        except: pass
        if self.is_video and self.video_cap: self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0); self._show_first_frame()
        self.progress.set(0); self.time_label.config(text="00:00 / 00:00")

    def next_track(self):
        idx = self.current_idx + 1
        if 0 <= idx < len(self.playlist): self.current_idx = idx; self.listbox.selection_clear(0, tk.END); self.listbox.selection_set(idx); self.load_media(self.playlist[idx])

    def prev_track(self):
        idx = self.current_idx - 1
        if 0 <= idx < len(self.playlist): self.current_idx = idx; self.listbox.selection_clear(0, tk.END); self.listbox.selection_set(idx); self.load_media(self.playlist[idx])

    def _play_video_loop(self):
        if not self.is_playing or not self.is_video or not self.video_cap: return
        ret, frame = self.video_cap.read()
        if ret:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img.thumbnail((700, 400))
            self.tk_img = ImageTk.PhotoImage(image=img)
            self.video_label.config(image=self.tk_img)
            fps = self.video_cap.get(cv2.CAP_PROP_FPS)
            self.after(int(1000 / max(fps, 1)), self._play_video_loop)
        else: self.next_track()

    def _start_progress_loop(self):
        if self.is_playing and self.media_length > 0:
            try:
                pos = pygame.mixer.music.get_pos() / 1000.0
                if pos < 0: pos = 0
                self.progress.set(min((pos / self.media_length) * 100, 100))
                c_m, c_s = divmod(int(pos), 60)
                t_m, t_s = divmod(int(self.media_length), 60)
                self.time_label.config(text=f"{c_m:02d}:{c_s:02d} / {t_m:02d}:{t_s:02d}")
            except: pass
        self.after(100, self._start_progress_loop)
