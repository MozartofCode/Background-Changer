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
import uuid
from openai import Image as OpenAIImage
import openai


class TopicInput(BaseModel):
    topic: str = Field(..., description="The description or topic for the image to be generated")


class ImageGenerationTool(BaseTool):
    name: str = "Image Generation Tool"
    description: str = (
        "This tool generates desktop background images based on a given topic or description. "
        "The generated image is saved locally as a PNG file."
    )

    args_schema: Type[BaseModel] = TopicInput

    def _run(self, topic: str) -> str:
        try:
            client = openai.OpenAI()
            response = client.images.generate(
                prompt=topic,
                n=1,
                size="1024x1024",
                response_format="url" 
            )    
            
            # Get the URL of the generated image
            image_url = response.data[0].url

            # Download the image and save it locally
            filename = f"{uuid.uuid4().hex}.png"
            output_path = os.path.join("wallpapers", filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            print(f"Downloading image from: {image_url}")
            with open(output_path, "wb") as f:
                f.write(requests.get(image_url).content)
            
            return f"Images successfully generated and saved to: {output_path}"

        except Exception as e:
            return f"Error generating image: {str(e)}"



# Input Schema for the Changing Tool
class ChangeInput(BaseModel):
    folder_path: str = Field(..., description="Folder path containing desktop background images.")

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

            # Get a list of image files (supports jpg and png)
            images = list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
            if not images:
                return "No images found in the specified folder."

            # Select a random image
            choice = random.choice(images)

            # Ensure the path is absolute
            absolute_path = str(choice.resolve())

            # Set the desktop wallpaper
            SPI_SETDESKWALLPAPER = 20
            result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absolute_path, 3)

            if not result:
                return f"Failed to set desktop background. SystemParametersInfoW returned {result}."

            # Update the registry for wallpaper style
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")  # 10 = Fill
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")    # 0 = No tiling
            winreg.CloseKey(key)

            return f"Desktop background successfully changed to {choice.name}"

        except Exception as e:
            return f"Failed to change the desktop background: {e}"