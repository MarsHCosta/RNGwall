import os
import glob
from os.path import join, isdir

WALLPAPERS_DIRECTORY = os.path.join(os.getenv('USERPROFILE'), "Pictures", "Wallhaver")
MAX_STORED_WALLPAPERS = 10  # Maximum number of wallpapers to keep locally

def ensure_wallpapers_directory():
    if not isdir(WALLPAPERS_DIRECTORY):
        os.makedirs(WALLPAPERS_DIRECTORY)

def clean_old_wallpapers():
    wallpapers = glob.glob(join(WALLPAPERS_DIRECTORY, "*"))
    wallpapers.sort(key=os.path.getctime, reverse=True)
    for wallpaper in wallpapers[MAX_STORED_WALLPAPERS:]:
        try:
            os.remove(wallpaper)
        except OSError as e:
            print(f"Error deleting {wallpaper}: {e}")

def get_wallpaper_path(filename):
    return join(WALLPAPERS_DIRECTORY, filename)

def clear_all_wallpapers():
    wallpapers = glob.glob(join(WALLPAPERS_DIRECTORY, "*"))
    for wallpaper in wallpapers:
        try:
            os.remove(wallpaper)
        except OSError as e:
            print(f"Error deleting {wallpaper}: {e}")

def get_wallpaper_count():
    return len(glob.glob(join(WALLPAPERS_DIRECTORY, "*")))