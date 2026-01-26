import yaml
from core.ingestor import Ingestor
from core.processor import Processor
from core.media_studio import MediaStudio
from core.publisher import Publisher

def load_config():
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_bot():
    config = load_config()
    print("--- OpenContentBot Starting ---")

    # 1. Ingestor: 获取原始信息
    raw_data = None
    if config['pipeline']['enable_ingestor']:
        ingestor = Ingestor(config['modules']['ingestor'])
        raw_data = ingestor.fetch()
    else:
        raw_data = "Input prompt from manual mode"

    # 2. Processor: AI 文案生成
    processor = Processor(config['modules']['processor'])
    content = processor.process(raw_data)
    print(f"Generated Content: {content[:50]}...")

    # 3. Media Studio: 生成图片/视频
    media_files = []
    if config['pipeline']['enable_image_gen']:
        studio = MediaStudio(config['modules']['media_studio'])
        image_path = studio.create_image(content)
        media_files.append(image_path)

    # 4. Publisher: 发布
    if config['pipeline']['enable_publisher']:
        publisher = Publisher(config['modules']['publisher'])
        publisher.publish(content, media_files)

    print("--- Task Completed ---")

if __name__ == "__main__":
    run_bot()