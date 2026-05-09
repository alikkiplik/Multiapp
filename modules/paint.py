import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import ImageGrab
import math

class PaintModule(ttk.Frame):
    def __init__(self, parent, theme_mgr):
        super().__init__(parent)
        self.theme_mgr = theme_mgr
        self.last_x = self.last_y = self.start_x = self.start_y = self.preview_id = None
        self.brush_size = tk.IntVar(value=3)
        self.brush_color = tk.StringVar(value="black")
        self._setup_ui()

    def _setup_ui(self):
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(toolbar, text="🌈 Цвет", command=self.choose_color).pack(side=tk.LEFT, padx=2)
        ttk.Label(toolbar, text="Толщина:").pack(side=tk.LEFT, padx=2)
        ttk.Spinbox(toolbar, from_=1, to=30, textvariable=self.brush_size, width=3).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        tools = {
            "pencil": "✏️ Карандаш", "marker": "🖊 Маркер", "line": "📏 Линия",
            "arrow": "➡️ Стрелка", "rect": "⬜ Прямоуг.", "rect_fill": "🟦 Прямоуг.Цвет",
            "oval": "⭕ Овал", "oval_fill": "🔵 Овал.Цвет", "triangle": "🔺 Треугольник",
            "star": "⭐ Звезда", "eraser": "🧹 Ластик"
        }
        self.tool_combo = ttk.Combobox(toolbar, values=list(tools.values()), state="readonly", width=14)
        self.tool_combo.current(0)
        self.tool_map = {v: k for k, v in tools.items()}
        self.tool_combo.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(toolbar, text="💾 PNG", command=self.save_png).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 SVG", command=self.save_svg).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑 Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
        
        canvas_wrapper = ttk.Frame(self, relief="solid", borderwidth=1)
        canvas_wrapper.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.canvas = tk.Canvas(canvas_wrapper, bg="white", cursor="cross", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def apply_colors(self, colors):
        self.canvas.config(bg=colors["canvas_bg"])

    def choose_color(self):
        color = colorchooser.askcolor(title="Цвет кисти")
        if color[1]: self.brush_color.set(color[1])

    def clear_canvas(self): self.canvas.delete("all"); self.preview_id = None

    def start_draw(self, event):
        self.last_x = self.start_x = event.x
        self.last_y = self.start_y = event.y
        tool = self.tool_map[self.tool_combo.get()]
        if tool not in ("pencil", "eraser", "marker"): return
        color = "white" if tool == "eraser" else self.brush_color.get()
        r = self.brush_size.get() if tool == "pencil" else self.brush_size.get() * 3
        self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill=color, outline=color)

    def draw(self, event):
        tool = self.tool_map[self.tool_combo.get()]
        color = "white" if tool == "eraser" else self.brush_color.get()
        size = self.brush_size.get()
        
        if tool in ("pencil", "eraser"):
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=color, width=size, capstyle=tk.ROUND, smooth=True)
        elif tool == "marker":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=color, width=size*3, capstyle=tk.ROUND, smooth=True)
        else:
            if self.preview_id: self.canvas.delete(self.preview_id)
            x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y

            # ✅ Явное разделение параметров для линий и фигур
            if tool == "line":
                self.preview_id = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=size)
            elif tool == "arrow":
                self.preview_id = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=size, arrow=tk.LAST)
            elif tool in ("rect", "rect_fill"):
                kw = {"outline": color, "width": size}
                if tool == "rect_fill": kw["fill"] = color
                self.preview_id = self.canvas.create_rectangle(x1, y1, x2, y2, **kw)
            elif tool in ("oval", "oval_fill"):
                kw = {"outline": color, "width": size}
                if tool == "oval_fill": kw["fill"] = color
                self.preview_id = self.canvas.create_oval(x1, y1, x2, y2, **kw)
            elif tool == "triangle":
                cx, cy = (x1+x2)/2, (y1+y2)/2
                self.preview_id = self.canvas.create_polygon(x1, y2, cx, y1, x2, y2, outline=color, width=size)
            elif tool == "star":
                pts = self._get_star_points(x1, y1, x2, y2)
                self.preview_id = self.canvas.create_polygon(pts, outline=color, width=size)
            return
        self.last_x, self.last_y = event.x, event.y

    def end_draw(self, event): self.last_x = self.last_y = self.preview_id = self.start_x = self.start_y = None

    def _get_star_points(self, x1, y1, x2, y2):
        cx, cy = (x1+x2)/2, (y1+y2)/2
        outer_r = max(abs(x2-x1), abs(y2-y1)) / 2
        inner_r = outer_r * 0.4
        pts = []
        for i in range(10):
            r = outer_r if i % 2 == 0 else inner_r
            angle = math.pi / 2 + i * math.pi / 5
            pts.extend([cx + r * math.cos(angle), cy - r * math.sin(angle)])
        return pts

    def save_png(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if not path: return
        try:
            x = self.master.winfo_rootx() + self.canvas.winfo_x() + 2
            y = self.master.winfo_rooty() + self.canvas.winfo_y() + 2
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            ImageGrab.grab(bbox=(x, y, x+w, y+h)).save(path)
            messagebox.showinfo("Успех", f"Сохранено в {path}")
        except Exception as e: messagebox.showerror("Ошибка", str(e))

    def save_svg(self):
        path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG", "*.svg")])
        if not path: return
        try:
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
            for item in self.canvas.find_all():
                ctype = self.canvas.type(item)
                opts = self.canvas.itemconfig(item)
                fill = opts.get("fill", ("", "", "", "", "none"))[-1]
                outline = opts.get("outline", ("", "", "", "", "none"))[-1]
                width = opts.get("width", (1,))[-1]
                coords = self.canvas.coords(item)
                if ctype == "line": svg.append(f'<line x1="{coords[0]}" y1="{coords[1]}" x2="{coords[2]}" y2="{coords[3]}" stroke="{fill}" stroke-width="{width}"/>')
                elif ctype == "rectangle": svg.append(f'<rect x="{min(coords[0], coords[2])}" y="{min(coords[1], coords[3])}" width="{abs(coords[2]-coords[0])}" height="{abs(coords[3]-coords[1])}" fill="{fill}" stroke="{outline}" stroke-width="{width}"/>')
                elif ctype == "oval": svg.append(f'<ellipse cx="{(coords[0]+coords[2])/2}" cy="{(coords[1]+coords[3])/2}" rx="{abs(coords[2]-coords[0])/2}" ry="{abs(coords[3]-coords[1])/2}" fill="{fill}" stroke="{outline}" stroke-width="{width}"/>')
                elif ctype == "polygon":
                    pts = " ".join(f"{x},{y}" for x, y in zip(coords[::2], coords[1::2]))
                    svg.append(f'<polygon points="{pts}" fill="{fill}" stroke="{outline}" stroke-width="{width}"/>')
            svg.append("</svg>")
            with open(path, "w", encoding="utf-8") as f: f.write("\n".join(svg))
            messagebox.showinfo("Успех", f"SVG сохранён в {path}")
        except Exception as e: messagebox.showerror("Ошибка", str(e))
