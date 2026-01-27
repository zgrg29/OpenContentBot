import yaml
from core.ingestor import Ingestor

def load_config():
    # 直接读取你项目中的实际配置文件
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def test_fetch_with_config():
    print("=== 正在从 config.yaml 加载配置进行测试 ===")
    
    # 1. 加载真实配置
    config = load_config()
    
    # 2. 提取 ingestor 模块需要的参数
    # 注意：这里要对应你 main.py 里的传参方式
    ingestor_params = config['modules']['ingestor']
    
    # 3. 初始化并运行
    ingestor = Ingestor(ingestor_params)
    results = ingestor.fetch()
    
    # 4. 展示结果
    if results:
        print(f"成功！根据 config.yaml 的配置抓取到了 {len(results)} 条数据。")
        for i, item in enumerate(results, 1): 
            print(f"[{i}] {item['title']} ({item['source_type']})")
    else:
        print("未抓取到数据，请检查 config.yaml 中的 rss_urls 或 keywords 是否正确。")

if __name__ == "__main__":
    test_fetch_with_config()