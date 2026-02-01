import tweepy
import os
from .base_publisher import BasePublisher
from utils.logger import logger

class Publisher(BasePublisher):
    def __init__(self, platform_config):
        super().__init__(platform_config)
        self.api_key = os.getenv("X_API_KEY")
        self.api_secret = os.getenv("X_API_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        
        # 初始化 V2 Client 用于发帖
        self.client = tweepy.Client(
            consumer_key=self.api_key, 
            consumer_secret=self.api_secret,
            access_token=self.access_token, 
            access_token_secret=self.access_token_secret
        )
        # 初始化 V1.1 用于上传图片
        auth = tweepy.OAuth1UserHandler(self.api_key, self.api_secret, self.access_token, self.access_token_secret)
        self.api_v1 = tweepy.API(auth)

    def post(self, content_bundle):
        caption = content_bundle.get('caption', '')
        tags = " ".join(content_bundle.get('tags', []))
        full_text = f"{caption}\n\n{tags}"
        image_path = content_bundle.get('image_path')

        # 从 config.yaml 读取是否允许发图，默认为 True
        allow_post_image = self.config.get('post_image', True)

        media_ids = []
        # 只有在开关打开且文件存在时才上传
        if allow_post_image and image_path and os.path.exists(image_path):
            try:
                logger.info(f"正在上传媒体文件: {image_path}")
                media = self.api_v1.media_upload(filename=image_path)
                media_ids = [media.media_id]
                logger.info(f"媒体上传成功，ID: {media_ids}")
            except Exception as e:
                logger.error(f"图片上传失败: {e}")

        # 发布推文：必须显式传入 media_ids 参数
        try:
            if media_ids:
                response = self.client.create_tweet(text=full_text, media_ids=media_ids)
            else:
                response = self.client.create_tweet(text=full_text)
            return response.data
        except Exception as e:
            logger.error(f"推文发布失败: {e}")
            raise e