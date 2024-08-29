import os
import time
import ctypes
import logging
from threading import Thread
from random import choice
from urllib.parse import urlparse
from os.path import basename, isfile, join, isdir
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from tkinter import messagebox
from PIL import Image

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

WALLPAPERS_DIRECTORY = os.path.join(os.getenv('USERPROFILE'), "Pictures", "Wallhaver")
API_KEY = os.getenv('API_KEY')
BASE_URL = "https://wallhaven.cc/api/v1/"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def ensure_wallpapers_directory():
    if not isdir(WALLPAPERS_DIRECTORY):
        os.makedirs(WALLPAPERS_DIRECTORY)
        logger.info(f"Created wallpapers directory: {WALLPAPERS_DIRECTORY}")


def get_wallpaper_data(resolution, keywords):
    search_params = {
        "q": keywords,
        "sorting": "random",
        "ratio": "16x9",
        "atleast": resolution,
        "purity": "100",  # SFW content
    }

    headers = {"X-API-KEY": API_KEY} if API_KEY else {}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(BASE_URL + "search/", headers=headers, params=search_params)
            response.raise_for_status()
            data = response.json()

            if not data["data"]:
                logger.warning("No wallpapers found with the given criteria.")
                return None

            return choice(data["data"])
        except RequestException as e:
            logger.error(f"Error fetching wallpaper data (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                messagebox.showerror("Error", "Failed to fetch wallpaper data. Please try again later.")
                return None


def download_wallpaper(wp_url, wp_file):
    try:
        with requests.get(wp_url, stream=True) as r:
            r.raise_for_status()
            with open(wp_file, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
        logger.info(f"Downloaded wallpaper: {wp_file}")
        return True
    except RequestException as e:
        logger.error(f"Error downloading wallpaper: {e}")
        return False


def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except:
        logger.error(f"Invalid image file: {file_path}")
        return False


def set_wallpaper(wp_file):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, wp_file, 0)
    logger.info(f"Wallpaper set to {wp_file}")


def cleanup_old_wallpapers(max_files=100):
    wallpapers = [f for f in os.listdir(WALLPAPERS_DIRECTORY) if f.endswith(('.png', '.jpg', '.jpeg'))]
    wallpapers.sort(key=lambda x: os.path.getmtime(join(WALLPAPERS_DIRECTORY, x)), reverse=True)

    for old_wp in wallpapers[max_files:]:
        os.remove(join(WALLPAPERS_DIRECTORY, old_wp))
        logger.info(f"Removed old wallpaper: {old_wp}")


def download_and_set_wallpaper(resolution, keywords, interval):
    ensure_wallpapers_directory()

    while True:
        wp_data = get_wallpaper_data(resolution, keywords)
        if not wp_data:
            time.sleep(interval * 60)
            continue

        wp_url = wp_data["path"]
        timestamp = time.strftime("%Y%m%d%H%M%S")
        wp_file = join(WALLPAPERS_DIRECTORY,
                       f"{timestamp}_{basename(urlparse(wp_url).path).removeprefix('wallhaven-')}")

        if download_wallpaper(wp_url, wp_file) and is_valid_image(wp_file):
            set_wallpaper(wp_file)
            cleanup_old_wallpapers()
        else:
            if isfile(wp_file):
                os.remove(wp_file)

        time.sleep(interval * 60)


# Usage
if __name__ == "__main__":
    resolution = "1920x1080"
    keywords = "nature,landscape"
    interval = 30  # minutes

    download_thread = Thread(target=download_and_set_wallpaper, args=(resolution, keywords, interval))
    download_thread.start()