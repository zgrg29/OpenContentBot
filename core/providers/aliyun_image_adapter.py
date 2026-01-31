import os
import requests
import time
import json
from dotenv import load_dotenv
from core.providers.base_image_adapter import BaseImageAdapter

# 预先加载环境变量
load_dotenv()

class AliyunImageAdapter(BaseImageAdapter):
    def __init__(self, config):
        self.config = config
        self.api_key = os.getenv('ALIYUN_API_KEY')
        if not self.api_key:
            raise ValueError("ALIYUN_API_KEY not found in environment variables")
        
        # 阿里云通义万相API端点
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
        self.save_dir = config.get('save_dir', 'outputs/images/')
        
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def generate(self, prompt: str, quality_enhancers: str) -> str:
        full_prompt = f"{prompt}, {quality_enhancers}"
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # 通义万相API参数
            payload = {
                "model": self.config.get('model', 'wanx-v1'),
                "input": {
                    "prompt": full_prompt
                },
                "parameters": {
                    "size": self.config.get('resolution', '1024*1024'),
                    "n": 1
                }
            }
            
            print(f"Calling Aliyun Wanxiang API with model: {payload['model']}")
            print(f"Prompt: {full_prompt}")
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"API Response: {json.dumps(result, indent=2)}")
                if 'output' in result and 'results' in result['output']:
                    image_url = result['output']['results'][0]['url']
                    return self._download(image_url)
                else:
                    print(f"Unexpected response format: {result}")
                    return ""
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                print(error_msg)
                
                # 检查是否是同步调用不支持的错误
                if "does not support synchronous calls" in response.text:
                    print("⚠️  阿里云通义万相可能需要异步调用或您的API密钥未开通同步权限")
                    print("💡 建议：检查阿里云控制台是否已开通通义万相服务，或联系阿里云支持")
                
                return ""
                
        except Exception as e:
            print(f"Aliyun Image Generation Error: {e}")
            return ""

    def _download(self, url: str) -> str:
        try:
            path = os.path.join(self.save_dir, f"img_{int(time.time())}.png")
            print(f"Downloading image from: {url}")
            img_data = requests.get(url, timeout=30).content
            with open(path, 'wb') as handler:
                handler.write(img_data)
            print(f"Image saved to: {path}")
            return path
        except Exception as e:
            print(f"Image Download Error: {e}")
            return ""