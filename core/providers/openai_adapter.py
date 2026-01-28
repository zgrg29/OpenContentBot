import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 预先加载环境变量
load_dotenv()

class Adapter:
    def __init__(self, config):
        """
        config 同样是 modules.processor 的内容
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("环境变量 OPENAI_API_KEY 未设置，请检查 .env 文件。")
        
        self.client = OpenAI(api_key=api_key)
        self.model = config['model']
        self.temperature = config.get('temperature', 0.7)

    def generate_content(self, raw_data, system_prompt):
        """
        请求 OpenAI 并返回结构化数据
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"请处理以下原始数据并按 JSON 格式输出：\n{raw_data}"}
                ],
                # 关键：强制返回 JSON 格式
                response_format={"type": "json_object"},
                temperature=self.temperature
            )
            
            # 将字符串转换为 Python 字典
            content_str = response.choices[0].message.content
            return json.loads(content_str)
            
        except Exception as e:
            print(f"[!] OpenAI API 错误: {e}")
            return {
                "caption": "内容生成失败，请检查日志。",
                "image_prompt": "Error placeholder",
                "tags": []
            }