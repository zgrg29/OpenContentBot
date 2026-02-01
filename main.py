import yaml
import os
from core.ingestor import Ingestor
from core.processor import Processor
from core.media_studio import MediaStudio
from core.publisher import PublishManager # 修改：导入 PublishManager 而不是基类
from utils.logger import logger

def load_config():
    # 确保路径指向你的配置文件
    config_path = os.path.join("config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_bot():
    config = load_config()
    logger.info("--- OpenContentBot 启动整合流程 ---")

    # 1. Ingestor: 数据采集 (获取原始新闻/趋势)
    raw_data = None
    if config['pipeline']['enable_ingestor']:
        logger.info("步骤 1: 正在采集数据...")
        ingestor = Ingestor(config['modules']['ingestor'])
        raw_data = ingestor.fetch()
    else:
        raw_data = "Manual seed prompt" # 手动模式占位

    # 2. Processor: AI 逻辑处理 (生成文案、图片提示词、标签)
    logger.info("步骤 2: AI 正在处理内容...")
    processor = Processor(config['modules']['processor'])
    # 注意：processor.process 返回的应当是解析后的字典（包含 caption, image_prompt, tags）
    ai_content = processor.process(raw_data)
    logger.info(f"生成文案概览: {ai_content.get('caption', '')[:30]}...")

    # 3. Media Studio: 多媒体生成 (DALL-E 3 生成图片)
    image_path = None
    if config['pipeline']['enable_image_gen']:
        logger.info("步骤 3: 正在生成 AI 图片...")
        # 修正：传递 ['image'] 层级配置
        studio = MediaStudio(config['modules']['media_studio']['image']) 
        
        # 修正：使用正确的类方法名 create_visual
        image_path = studio.create_visual(ai_content.get('image_prompt', ''))
    
    # 4. Publisher: 多平台自动化分发
    if config['pipeline']['enable_publisher']:
        logger.info("步骤 4: 正在执行分发任务...")
        # 使用 PublishManager 调度所有启用的渠道
        publisher_manager = PublishManager(config)
        
        # 构造各平台通用的数据包
        content_bundle = {
            "caption": ai_content.get('caption', ''),
            "image_path": image_path,
            "tags": ai_content.get('tags', [])
        }
        
        # 广播发布
        publisher_manager.broadcast(content_bundle)

    logger.info("--- 全流程任务完成 ---")

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        logger.error(f"程序运行崩溃: {e}", exc_info=True)