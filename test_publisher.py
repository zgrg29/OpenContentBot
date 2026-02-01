import os
import yaml
import random
from dotenv import load_dotenv
from core.publisher import PublishManager

# 1. 加载环境变量
load_dotenv()

def generate_random_content():
    """
    模拟 AI 生成的随机内容
    """
    topics = ["AI 科技", "金融市场", "加密货币", "特斯拉动态", "自动化机器人"]
    actions = ["正在改变世界", "迎来重磅更新", "引发行业热议", "展现出惊人潜力", "今日行情走势回顾"]
    emojis = ["🤖", "🚀", "📊", "💡", "🌐", "🔥"]
    
    # 随机组合成一条推文文案
    topic = random.choice(topics)
    action = random.choice(actions)
    emoji = random.choice(emojis)
    
    caption = f"{topic}{action}！{emoji}\n这是由我的 AI 助手自动生成的随机测试内容。"
    
    # 定义可选的标签组
    tags_pool = [
        ["#AI", "#Tech", "#Future"],
        ["#Finance", "#Crypto", "#Market"],
        ["#Python", "#Automation", "#Bot"],
        ["#Tesla", "#ElonMusk", "#EV"]
    ]
    tags = random.choice(tags_pool)
    
    return caption, tags

def test_twitter_publish():
    # 2. 加载 config.yaml
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 3. 初始化分发管理器
    publisher_manager = PublishManager(config)

    # 4. 生成随机内容包
    random_caption, random_tags = generate_random_content()
    
    # 确保图片路径正确，或设为 None
    test_image_path = "outputs/images/test_shot.png" 
    if not os.path.exists(test_image_path):
        test_image_path = None

    test_content = {
        "caption": random_caption,
        "image_path": test_image_path,
        "tags": random_tags
    }

    print(f"--- 准备发布随机内容 ---\n内容: {random_caption}\n标签: {random_tags}")
    
    try:
        # 5. 调用广播方法
        publisher_manager.broadcast(test_content)
        print("--- 随机内容测试发布结束 ---")
    except Exception as e:
        print(f"测试过程中发生崩溃: {e}")

if __name__ == "__main__":
    test_twitter_publish()