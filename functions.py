import os
import ctypes
import time
from pathlib import Path
import random

def set_wallpaper(image_path):
    """Set desktop wallpaper to the given image."""
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

image_path = os.path.abspath('./wallpapers/1.jpg')

set_wallpaper(image_path)


# def get_random_image(folder_path):
#     """Get a random image from the folder."""
#     images = list(Path(folder_path).glob('*.jpg')) + list(Path(folder_path).glob('*.png'))
#     if not images:
#         raise ValueError("No images found in the specified folder.")
#     return random.choice(images)

# def run_wallpaper_changer(folder_path, interval=60):
#     """Change wallpaper periodically."""
#     while True:
#         try:
#             image_path = str(get_random_image(folder_path))
#             print(f"Changing wallpaper to: {image_path}")
#             set_wallpaper(image_path)
#             time.sleep(interval)  # Wait for the interval before changing again
#         except Exception as e:
#             print(f"Error: {e}")
#             break

# if __name__ == "__main__":
#     # Set the folder containing your wallpapers
#     wallpaper_folder = r"C:\Path\To\Your\Wallpapers"
#     run_wallpaper_changer(wallpaper_folder, interval=300)  # Change every 5 minutes
