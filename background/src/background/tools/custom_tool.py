from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import requests
from pathlib import Path
import random
import ctypes


class urlInput(BaseModel):
    url: str = Field(..., description="This is the url of the desktop background image you want to download")

class DownloadingTool(BaseTool):
    name: str = "Downloading Tool"
    description: str = (
        "This tool is useful for dowloading desktop background photos given the url of the photo"
    )
    args_schema: Type[BaseModel] = urlInput

    def _run(self, url: str) -> str:
        save_path = Path("../../../wallpapers")

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            print(f"Image successfully downloaded to {save_path.resolve()}")
            return str(save_path.resolve())
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the image: {e}")
            return None    
        


class changeInput(BaseModel):
    folder_path: str = Field(..., description="This is the folder path of the desktop background images you want to choose from and change")

class ChangingTool(BaseTool):
    name: str = "Changing Tool"
    description: str = (
        "This tool is useful for changing the desktop background photos based on the folder of photos"
    )
    args_schema: Type[BaseModel] = changeInput

    def _run(self, folder_path: str) -> str:

        # Get a random image from the folder            
        images = list(Path(folder_path).glob('*.jpg')) + list(Path(folder_path).glob('*.png'))
        if not images:
            raise ValueError("No images found in the specified folder.")
        choice = random.choice(images)
        
        # Change the desktop background
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, choice, 3)