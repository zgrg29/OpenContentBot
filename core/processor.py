import importlib
from typing import Dict, Any

class Processor:
    def __init__(self, config: Dict[str, Any]):
        """
        config 传入的是 config.yaml 中的 modules.processor 部分
        """
        # 强制要求配置项，如果 config.yaml 没写，这里会直接报 KeyError，拒绝运行
        self.provider = config['provider'] 
        self.system_prompt = config['system_prompt']
        self.config = config
        
        # 动态加载适配器
        self.adapter = self._load_adapter()

    def _load_adapter(self):
        """
        根据 provider 字符串动态导入模块
        例如：provider 为 'openai'，则导入 core.providers.openai_adapter
        """
        module_path = f"core.providers.{self.provider}_adapter"
        try:
            # 动态导入
            adapter_module = importlib.import_module(module_path)
            # 实例化适配器类
            return adapter_module.Adapter(self.config)
        except ImportError as e:
            raise ImportError(f"未找到适配器文件: {module_path}.py。请确保该文件存在于 core/providers/ 目录下。") from e
        except Exception as e:
            raise Exception(f"加载适配器 {self.provider} 时发生错误: {str(e)}")

    def process(self, raw_data: str) -> Dict[str, Any]:
        """
        主处理逻辑：调用适配器生成内容
        """
        if not raw_data:
            print("[!] Warning: No raw data provided to Processor.")
            return {}

        # 这里的返回结果将直接是适配器处理后的字典 (caption, image_prompt, tags)
        return self.adapter.generate_content(raw_data, self.system_prompt)