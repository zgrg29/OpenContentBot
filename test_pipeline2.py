import yaml
import os
from dotenv import load_dotenv
from core.ingestor import Ingestor
from core.processor import Processor
from core.media_studio import MediaStudio

# 0. 初始化环境
load_dotenv()

def run_full_pipeline_test():
    print("=== [PHASE 1] Loading Configuration ===")
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 初始化三个核心模块
    ingestor = Ingestor(config['modules']['ingestor'])
    processor = Processor(config['modules']['processor'])
    studio = MediaStudio(config['modules']['media_studio'])

    print("\n=== [PHASE 2] Ingesting Hot News ===")
    raw_items = ingestor.fetch()
    if not raw_items:
        print("[!] No news items found. Exiting.")
        return
    
    # 选取第一条最新新闻进行测试
    target_news = raw_items[0]
    print(f"[*] Target News: {target_news['title']}")

    print("\n=== [PHASE 3] AI Processing (Text & Prompt) ===")
    # 构造上下文：将标题和摘要传给 AI
    raw_context = f"Title: {target_news['title']}\nSummary: {target_news['summary']}"
    ai_result = processor.process(raw_context)

    if not ai_result:
        print("[!] Processor failed to return JSON.")
        return

    print(f"[+] AI Caption: {ai_result.get('caption')}")
    print(f"[+] AI Tags: {ai_result.get('tags')}")

    print("\n=== [PHASE 4] Generating Visual Content ===")
    # 获取 AI 生成的绘图描述语
    image_prompt = ai_result.get('image_prompt')
    if image_prompt:
        image_path = studio.create_visual(image_prompt)
        
        if image_path and os.path.exists(image_path):
            print(f"\n✅ SUCCESS!")
            print(f"Final Output Ready:")
            print(f"- Text: {ai_result['caption']}")
            print(f"- Image: {image_path}")
        else:
            print("[!] MediaStudio failed to generate image.")
    else:
        print("[!] No image_prompt found in AI result.")

if __name__ == "__main__":
    run_full_pipeline_test()