from abc import ABC, abstractmethod

class BaseImageAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, quality_enhancers: str) -> str:
        """Should return the local path to the generated image."""
        pass