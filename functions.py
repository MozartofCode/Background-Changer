import os
import ctypes
import time
from pathlib import Path
import random


import requests
from pathlib import Path


def download_image(url, save_path):
    """
    Download an image from a URL and save it to a specified path.
    
    Parameters:
    - url (str): The URL of the image.
    - save_path (str or Path): The file path where the image should be saved.
    
    Returns:
    - str: The absolute path to the saved image file.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        
        # Ensure the directory exists
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the image to the file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        print(f"Image successfully downloaded to {save_path.resolve()}")
        return str(save_path.resolve())
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image: {e}")
        return None



# image_url = "https://via.placeholder.com/800x600.jpg"
# save_path = "wallpapers/images.jpg"


# downloaded_image = download_image(image_url, save_path)

# if downloaded_image:
#     print(f"Image saved at: {downloaded_image}")
# else:
#     print("Failed to download the image.")










# def set_wallpaper(image_path):
#     """Set desktop wallpaper to the given image."""
#     SPI_SETDESKWALLPAPER = 20
#     ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

# image_path = os.path.abspath('wallpapers/images.jpg')

# set_wallpaper(image_path)


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
