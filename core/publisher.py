import importlib
from utils.logger import logger

class PublishManager:
    """
    分发中控模块：负责根据 config 调度不同的平台发布器
    """
    def __init__(self, config):
        self.config = config
        self.publish_channels = config.get('modules', {}).get('publish_channels', {})
        self.active_publishers = {}
        self._load_publishers()

    def _load_publishers(self):
        """
        动态加载配置文件中 enabled 为 true 的发布器
        """
        for platform, settings in self.publish_channels.items():
            if settings.get('enabled'):
                try:
                    # 动态导入 core.publishers.twitter_pub 等模块
                    module_path = f"core.publishers.{platform}_pub"
                    module = importlib.import_module(module_path)
                    
                    # 约定：每个平台模块内都有一个名为 Publisher 的类
                    publisher_class = getattr(module, "Publisher")
                    # 传入该平台的特定配置进行初始化
                    self.active_publishers[platform] = publisher_class(settings)
                    logger.info(f"成功加载发布器: {platform}")
                except (Import_ModuleError, AttributeError) as e:
                    logger.error(f"无法加载平台 {platform} 的发布模块: {e}")

    def broadcast(self, content_bundle):
        """
        将内容发布到所有已启用的平台
        :param content_bundle: 包含文字、图片路径、标签等的字典
        """
        if not self.active_publishers:
            logger.warning("没有启用的发布渠道，跳过发布。")
            return

        for platform, pub_instance in self.active_publishers.items():
            logger.info(f"正在发布到: {platform}...")
            try:
                # content_bundle 结构应包含: {'caption': '...', 'image_path': '...', 'tags': [...]}
                result = pub_instance.post(content_bundle)
                if result:
                    logger.info(f"{platform} 发布成功。")
            except Exception as e:
                logger.error(f"{platform} 发布失败: {str(e)}")