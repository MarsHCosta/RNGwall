import os
import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread
from downloader import download_and_set_wallpaper
import json

class WallpaperChangerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RNGwall")
        self.root.configure(bg="#1e1e1e")  # Dark background

        self.current_wallpaper = None
        self.previous_wallpaper = None
        self.wallpaper_thread = None
        self.paused = False

        self.selected_resolution = tk.StringVar(value="1920x1080")
        self.load_config()

        self.create_widgets()
        self.apply_styles()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                'default_resolution': '1920x1080',
                'default_keywords': 'nature,landscape',
                'default_interval': '30'
            }

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    def create_widgets(self):
        self.create_resolution_section()
        self.create_keyword_section()
        self.create_interval_section()
        self.create_control_buttons()
        self.create_credit_label()

    def create_resolution_section(self):
        tk.Label(self.root, text="Select Resolution:", bg="#1e1e1e", fg="white").pack(padx=5, pady=5)
        resolution_frame = tk.Frame(self.root, bg="#1e1e1e")
        resolution_frame.pack(pady=5)

        for res in ["1920x1080", "3840x2160"]:
            ttk.Button(resolution_frame, text=res, command=lambda r=res: self.set_resolution(r)).pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Or Enter Custom Resolution:", bg="#1e1e1e", fg="white").pack(padx=5, pady=5)
        self.custom_resolution_entry = ttk.Entry(self.root)
        self.custom_resolution_entry.pack(padx=5, pady=5)

    def create_keyword_section(self):
        tk.Label(self.root, text="Keywords (e.g., nature, abstract):", bg="#1e1e1e", fg="white").pack(padx=5, pady=5)
        self.keyword_entry = ttk.Entry(self.root)
        self.keyword_entry.pack(padx=5, pady=5)
        self.keyword_entry.insert(0, self.config['default_keywords'])

    def create_interval_section(self):
        tk.Label(self.root, text="Interval (minutes):", bg="#1e1e1e", fg="white").pack(padx=5, pady=5)
        self.interval_entry = ttk.Entry(self.root)
        self.interval_entry.pack(padx=5, pady=5)
        self.interval_entry.insert(0, self.config['default_interval'])

    def create_control_buttons(self):
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=5)

        buttons = [
            ("⏮", self.go_back_wallpaper),
            ("▶", self.start_wallpaper_change),
            ("⏸", self.pause_wallpaper_change),
            ("⏹", self.stop_wallpaper_change),
            ("⏭", self.skip_forward_wallpaper)
        ]

        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

    def create_credit_label(self):
        credit_label = tk.Label(self.root, text="by Mars H.C.", bg="#1e1e1e", fg="white", anchor="se")
        credit_label.pack(side=tk.BOTTOM, anchor="se", padx=5, pady=5)

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background="#333333", foreground="white")
        style.configure('TEntry', fieldbackground="#333333", foreground="white")

    def set_resolution(self, res):
        self.selected_resolution.set(res)
        self.custom_resolution_entry.delete(0, tk.END)

    def start_wallpaper_change(self):
        self.paused = False
        resolution = self.custom_resolution_entry.get().strip() or self.selected_resolution.get()
        keywords = self.keyword_entry.get()
        interval = self.interval_entry.get()

        if not resolution or not keywords or not interval:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            interval = int(interval)
        except ValueError:
            messagebox.showwarning("Input Error", "Interval must be a number.")
            return

        self.wallpaper_thread = Thread(target=download_and_set_wallpaper, args=(resolution, keywords, interval), daemon=True)
        self.wallpaper_thread.start()

        self.config['default_resolution'] = resolution
        self.config['default_keywords'] = keywords
        self.config['default_interval'] = str(interval)
        self.save_config()

    def pause_wallpaper_change(self):
        self.paused = True
        if self.wallpaper_thread:
            messagebox.showinfo("Pause", "Wallpaper change paused. The current wallpaper will stay on the screen.")

    def stop_wallpaper_change(self):
        self.paused = True
        self.wallpaper_thread = None
        messagebox.showinfo("Stop", "Wallpaper changing has been stopped.")

    def go_back_wallpaper(self):
        if self.previous_wallpaper:
            self.current_wallpaper, self.previous_wallpaper = self.previous_wallpaper, self.current_wallpaper
            os.system(f'gsettings set org.gnome.desktop.background picture-uri file://{self.current_wallpaper}')
            messagebox.showinfo("Back", "Reverted to the previous wallpaper.")

    def skip_forward_wallpaper(self):
        self.paused = False
        self.start_wallpaper_change()

def main():
    root = tk.Tk()
    app = WallpaperChangerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()