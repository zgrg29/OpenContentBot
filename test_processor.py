import yaml
from core.processor import Processor
from dotenv import load_dotenv

def test():
    # 1. 加载配置
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 2. 初始化 Processor
    print(f"[*] 正在初始化 Processor, 使用提供商: {config['modules']['processor']['provider']}")
    proc = Processor(config['modules']['processor'])
    
    # 3. 模拟 Ingestor 抓取的原始数据
    mock_raw_data = "Tesla 发布了最新的人形机器人 Optimus Gen 3，展示了其在工厂搬运零件的能力。"
    
    # 4. 执行处理
    print("[*] 正在请求 AI 生成内容...")
    result = proc.process(mock_raw_data)
    
    # 5. 打印结果
    print("\n=== 测试结果 ===")
    print(f"文案 (Caption): {result.get('caption')}")
    print(f"绘图建议 (Image Prompt): {result.get('image_prompt')}")
    print(f"标签 (Tags): {result.get('tags')}")

if __name__ == "__main__":
    test()