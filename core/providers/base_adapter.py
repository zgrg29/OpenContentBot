from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    @abstractmethod
    def generate_content(self, raw_data: str, system_prompt: str) -> Dict[str, Any]:
        """
        要求子类必须返回统一格式的字典：
        {
            "caption": "文案内容",
            "image_prompt": "绘图提示词",
            "tags": ["标签1", "标签2"]
        }
        """
        pass