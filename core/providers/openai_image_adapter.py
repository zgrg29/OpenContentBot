import os
import requests
import time
from openai import OpenAI
from dotenv import load_dotenv
from core.providers.base_image_adapter import BaseImageAdapter

# 预先加载环境变量
load_dotenv()

class ImageAdapter(BaseImageAdapter):
    def __init__(self, config):
        self.config = config
        self.client = OpenAI() # Reads OPENAI_API_KEY from .env
        self.save_dir = config.get('save_dir', 'outputs/images/')
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def generate(self, prompt: str, quality_enhancers: str) -> str:
        full_prompt = f"{prompt}, {quality_enhancers}"
        try:
            response = self.client.images.generate(
                model=self.config.get('model', 'dall-e-3'),
                prompt=full_prompt,
                size=self.config.get('resolution', '1024x1024'),
                n=1
            )
            return self._download(response.data[0].url)
        except Exception as e:
            print(f"OpenAI Image Error: {e}")
            return ""

    def _download(self, url: str) -> str:
        path = os.path.join(self.save_dir, f"img_{int(time.time())}.png")
        img_data = requests.get(url).content
        with open(path, 'wb') as handler:
            handler.write(img_data)
        return path