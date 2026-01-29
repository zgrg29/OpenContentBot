import importlib
from typing import Dict, Any

class MediaStudio:
    def __init__(self, config: Dict[str, Any]):
        self.provider = config['provider']
        self.quality_enhancers = config.get('quality_enhancers', '')
        self.config = config
        self.adapter = self._load_adapter()

    def _load_adapter(self):
        # Dynamically loads core.providers.{provider}_image_adapter
        module_path = f"core.providers.{self.provider}_image_adapter"
        try:
            adapter_module = importlib.import_module(module_path)
            return adapter_module.ImageAdapter(self.config)
        except ImportError as e:
            raise ImportError(f"Image adapter {module_path}.py not found.") from e

    def create_visual(self, prompt: str) -> str:
        """Main entry point to generate an image."""
        if not prompt:
            return ""
        return self.adapter.generate(prompt, self.quality_enhancers)