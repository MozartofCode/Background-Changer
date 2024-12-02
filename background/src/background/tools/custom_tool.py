from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import requests
from pathlib import Path
import random
import ctypes
import os
from PIL import Image
from io import BytesIO

# Input Schema for the Downloading Tool
class UrlInput(BaseModel):
    url: str = Field(..., description="URL of the desktop background image to download.")


class DownloadingTool(BaseTool):
    name: str = "Downloading Tool"
    description: str = (
        "This tool is useful for downloading desktop background photos given the URL of the photo"
    )
    args_schema: Type[BaseModel] = UrlInput

    def _run(self, url: str) -> str:
        save_folder = Path("wallpapers")
        save_folder.mkdir(parents=True, exist_ok=True)

        try:
            # Request the image
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Validate response content type
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                return f"The URL does not point to a valid image. Content-Type: {content_type}"

            # Load and validate the image
            image = Image.open(BytesIO(response.content))
            file_format = image.format.lower()
            if file_format not in ["jpeg", "png"]:
                return f"Unsupported image format: {file_format}"

            # Save the image
            save_path = save_folder / f"background.{file_format}"
            image.save(save_path)

            return f"Image successfully downloaded to {save_path.resolve()}"

        except requests.exceptions.RequestException as e:
            return f"Failed to download the image: {e}"

        except Exception as e:
            return f"An error occurred: {e}"

# Input Schema for the Changing Tool
class ChangeInput(BaseModel):
    folder_path: str = Field(..., description="Folder path containing desktop background images.")

# Changing Tool
class ChangingTool(BaseTool):
    name: str = "ChangingTool"
    description: str = "Changes the desktop background to a random photo from a specified folder."
    args_schema: Type[BaseModel] = ChangeInput

    def _run(self, folder_path: str) -> str:
        try:
            # Check if the folder exists
            folder = Path(folder_path)
            if not folder.is_dir():
                return f"The folder path {folder_path} is invalid or does not exist."

            # Get a list of image files
            images = list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
            if not images:
                return "No images found in the specified folder."

            # Select a random image
            choice = random.choice(images)

            # Change the desktop background
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(choice), 3)

            return f"Desktop background successfully changed to {choice.name}"

        except Exception as e:
            return f"Failed to change the desktop background: {e}"
