from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import requests
from pathlib import Path


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