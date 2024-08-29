import tkinter as tk
from gui import WallpaperChangerGUI

def main():
    root = tk.Tk()
    app = WallpaperChangerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()