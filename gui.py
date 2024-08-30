import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import styles
from downloader import wallpaper_changer
from threading import Thread
import storage_manager


class ModernUIElements:
    @staticmethod
    def create_tooltip(widget, text):
        def enter(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = ttk.Label(tooltip, text=text, background=styles.COLORS['accent1'],
                              foreground=styles.COLORS['background'], padding=(5, 3))
            label.pack()
            widget.tooltip = tooltip

        def leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)


class WallpaperChangerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RNGwall")
        self.root.configure(bg=styles.COLORS['background'])

        self.wallpaper_thread = None
        self.selected_resolution = tk.StringVar(value="1920x1080")

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure('TFrame', background=styles.COLORS['background'])
        self.style.configure('TLabel', background=styles.COLORS['background'], foreground=styles.COLORS['text'])
        self.style.configure('TButton', background=styles.COLORS['button'], foreground=styles.COLORS['text'])
        self.style.map('TButton', background=[('active', styles.COLORS['button_hover'])])
        self.style.configure('TEntry', fieldbackground=styles.COLORS['foreground'],
                             foreground=styles.COLORS['background'])

        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family=styles.FONTS['default'][0], size=styles.FONTS['default'][1])
        self.root.option_add("*Font", default_font)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=f"{styles.PADDING['large']} {styles.PADDING['large']} {styles.PADDING['large']} {styles.PADDING['large']}")
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Select Resolution:", font=styles.FONTS['header']).grid(column=0, row=0, sticky=tk.W,
                                                                                           pady=(
                                                                                           0, styles.PADDING['medium']))
        resolution_frame = ttk.Frame(main_frame)
        resolution_frame.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=(0, styles.PADDING['large']))
        ttk.Button(resolution_frame, text="1920x1080", command=lambda: self.set_resolution("1920x1080")).grid(column=0,
                                                                                                              row=0,
                                                                                                              padx=(0,
                                                                                                                    styles.PADDING[
                                                                                                                        'medium']))
        ttk.Button(resolution_frame, text="3840x2160", command=lambda: self.set_resolution("3840x2160")).grid(column=1,
                                                                                                              row=0)

        ttk.Label(main_frame, text="Or Enter Custom Resolution:").grid(column=0, row=2, sticky=tk.W,
                                                                       pady=(0, styles.PADDING['small']))
        self.custom_resolution_entry = ttk.Entry(main_frame)
        self.custom_resolution_entry.grid(column=0, row=3, sticky=(tk.W, tk.E), pady=(0, styles.PADDING['large']))

        ttk.Label(main_frame, text="Keywords:").grid(column=0, row=4, sticky=tk.W, pady=(0, styles.PADDING['small']))
        self.keyword_entry = ttk.Entry(main_frame)
        self.keyword_entry.grid(column=0, row=5, sticky=(tk.W, tk.E), pady=(0, styles.PADDING['large']))

        ttk.Label(main_frame, text="Change Interval (minutes):").grid(column=0, row=6, sticky=tk.W,
                                                                      pady=(0, styles.PADDING['small']))
        self.interval_entry = ttk.Entry(main_frame)
        self.interval_entry.grid(column=0, row=7, sticky=(tk.W, tk.E), pady=(0, styles.PADDING['large']))

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(column=0, row=8, sticky=(tk.W, tk.E))

        play_button = ttk.Button(control_frame, text="▶", command=self.start_wallpaper_change)
        play_button.grid(column=0, row=0, padx=(0, styles.PADDING['small']))

        stop_button = ttk.Button(control_frame, text="⏹", command=self.stop_wallpaper_change)
        stop_button.grid(column=1, row=0, padx=(0, styles.PADDING['small']))

        next_button = ttk.Button(control_frame, text="⏭", command=self.skip_forward_wallpaper)
        next_button.grid(column=2, row=0, padx=(0, styles.PADDING['small']))

        clear_button = ttk.Button(control_frame, text="🗑", command=self.clear_stored_wallpapers)
        clear_button.grid(column=3, row=0)

        ModernUIElements.create_tooltip(play_button, "Start changing wallpapers")
        ModernUIElements.create_tooltip(stop_button, "Stop changing wallpapers")
        ModernUIElements.create_tooltip(next_button, "Skip to next wallpaper")
        ModernUIElements.create_tooltip(clear_button, "Clear all stored wallpapers")

        attribution_label = ttk.Label(main_frame, text="by Mars H.C.", font=styles.FONTS['small'], foreground=styles.COLORS['text'])
        attribution_label.grid(column=0, row=9, sticky=tk.SE, pady=(styles.PADDING['large'], 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=styles.PADDING['small'])

    def set_resolution(self, res):
        self.selected_resolution.set(res)
        self.custom_resolution_entry.delete(0, tk.END)

    def start_wallpaper_change(self):
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

        def run_wallpaper_change():
            wallpaper_changer.download_and_set_wallpaper(resolution, keywords, interval)

        self.wallpaper_thread = Thread(target=run_wallpaper_change, daemon=True)
        self.wallpaper_thread.start()

    def stop_wallpaper_change(self):
        if self.wallpaper_thread and self.wallpaper_thread.is_alive():
            wallpaper_changer.stop()
            self.wallpaper_thread.join()

    def skip_forward_wallpaper(self):
        self.stop_wallpaper_change()
        self.start_wallpaper_change()

    def clear_stored_wallpapers(self):
        storage_manager.clear_all_wallpapers()
        messagebox.showinfo("Wallpapers Cleared", "All stored wallpapers have been removed.")


def main():
    root = tk.Tk()
    app = WallpaperChangerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()