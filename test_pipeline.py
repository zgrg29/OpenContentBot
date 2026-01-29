import yaml
from core.ingestor import Ingestor
from core.processor import Processor

def run_test():
    # 1. 加载配置
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 2. 初始化模块
    ingestor = Ingestor(config['modules']['ingestor'])
    # 注意：Processor 需要传入 modules.processor 这一层级
    processor = Processor(config['modules']['processor'])

    # 3. 执行抓取 (Ingestor)
    print("--- Step 1: Ingesting Data ---")
    raw_items = ingestor.fetch()
    
    if not raw_items:
        print("No items found. Check your RSS URLs or Keywords.")
        return

    # 4. 执行处理 (Processor)
    # 我们先拿第一条数据做测试
    test_item = raw_items[0]
    print(f"\n--- Step 2: Processing Item: {test_item['title']} ---")
    
    # 构造发给 AI 的原始上下文（包含标题和摘要）
    raw_context = f"Title: {test_item['title']}\nSummary: {test_item['summary']}"
    
    try:
        result = processor.process(raw_context)
        
        print("\n--- Step 3: AI Output Success ---")
        print(f"Caption: {result.get('caption')}")
        print(f"Image Prompt: {result.get('image_prompt')}")
        print(f"Tags: {result.get('tags')}")
        
    except Exception as e:
        print(f"\n[!] Error during processing: {e}")

if __name__ == "__main__":
    run_test()