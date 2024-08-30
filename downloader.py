import os
import time
import ctypes
from random import choice
from urllib.parse import urlparse
from os.path import basename, isfile
import requests
from dotenv import load_dotenv
import storage_manager

load_dotenv()

class WallpaperChanger:
    def __init__(self):
        self.is_running = False

    def download_and_set_wallpaper(self, resolution, keywords, interval):
        storage_manager.ensure_wallpapers_directory()
        self.is_running = True

        base_url = "https://wallhaven.cc/api/v1/"
        api_key = os.getenv('WALLHAVEN_API_KEY')

        search_params = {
            "q": keywords,
            "sorting": "random",
            "ratio": "16x9",
            "atleast": resolution,
            "purity": "100",
        }

        headers = {"X-API-KEY": api_key} if api_key else {}

        while self.is_running:
            try:
                response = requests.get(base_url + "search/", headers=headers, params=search_params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if not data["data"]:
                    return

                wp = choice(data["data"])
                wp_url = wp["path"]
                timestamp = time.strftime("%Y%m%d%H%M%S")
                filename = f"{timestamp}_{basename(urlparse(wp_url).path).removeprefix('wallhaven-')}"
                wp_file = storage_manager.get_wallpaper_path(filename)

                if not isfile(wp_file):
                    with requests.get(wp_url, stream=True, timeout=10) as r:
                        r.raise_for_status()
                        with open(wp_file, "wb") as f:
                            for chunk in r.iter_content(8192):
                                f.write(chunk)

                ctypes.windll.user32.SystemParametersInfoW(20, 0, wp_file, 0)

                storage_manager.clean_old_wallpapers()

                for _ in range(interval * 60):
                    if not self.is_running:
                        break
                    time.sleep(1)

            except requests.RequestException:
                time.sleep(60)
            except Exception:
                time.sleep(60)

    def stop(self):
        self.is_running = False

wallpaper_changer = WallpaperChanger()