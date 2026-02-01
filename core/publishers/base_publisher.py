from abc import ABC, abstractmethod

class BasePublisher(ABC):
    def __init__(self, platform_config):
        self.config = platform_config

    @abstractmethod
    def post(self, content_bundle: dict):
        """
        子类必须实现此方法以执行具体的 API 调用
        """
        pass