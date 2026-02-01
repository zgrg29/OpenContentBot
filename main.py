import yaml
import os
from core.ingestor import Ingestor
from core.processor import Processor
from core.media_studio import MediaStudio
from core.publisher import PublishManager
from utils.logger import logger

def load_config():
    # 使用绝对路径确保脚本在不同目录下运行都能找到配置
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config", "config.yaml")
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"未找到配置文件: {config_path}")
        
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_bot():
    config = load_config()
    logger.info("--- OpenContentBot 启动整合流程 ---")

    # 1. Ingestor: 数据采集
    raw_data = "Manual seed prompt"
    if config['pipeline'].get('enable_ingestor'):
        logger.info("步骤 1: 正在采集数据...")
        ingestor = Ingestor(config['modules']['ingestor'])
        raw_data = ingestor.fetch()
        if not raw_data:
            logger.warning("未采集到有效数据，流程终止。")
            return

    # 2. Processor: AI 逻辑处理
    logger.info("步骤 2: AI 正在处理内容...")
    processor = Processor(config['modules']['processor'])
    ai_content = processor.process(str(raw_data)) # 确保传入字符串
    
    if not ai_content or 'caption' not in ai_content:
        logger.error("AI 内容生成失败，缺少必要字段。")
        return
        
    logger.info(f"生成文案概览: {ai_content.get('caption', '')[:30]}...")

    # 3. Media Studio: 多媒体生成
    image_path = None
    if config['pipeline'].get('enable_image_gen'):
        logger.info("步骤 3: 正在生成 AI 图片...")
        # 注意：这里要确保 config.yaml 中存在 modules.media_studio.image 节点
        image_config = config['modules']['media_studio'].get('image')
        if image_config:
            studio = MediaStudio(image_config) 
            image_path = studio.create_visual(ai_content.get('image_prompt', ''))
        else:
            logger.warning("未找到图像生成配置，跳过此步骤。")
    
    # 4. Publisher: 分发
    if config['pipeline'].get('enable_publisher'):
        logger.info("步骤 4: 正在执行分发任务...")
        publisher_manager = PublishManager(config)
        
        content_bundle = {
            "caption": ai_content.get('caption', ''),
            "image_path": image_path,
            "tags": ai_content.get('tags', [])
        }
        
        publisher_manager.broadcast(content_bundle)

    logger.info("--- 全流程任务完成 ---")

if __name__ == "__main__":
    try:
        run_bot()
    except Exception as e:
        logger.error(f"程序运行崩溃: {e}", exc_info=True)