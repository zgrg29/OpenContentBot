#!/usr/bin/env python3
"""
完整的OpenContentBot流水线测试
测试从配置加载到内容生成的完整流程
"""

import os
import sys
import yaml
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.processor import Processor

def test_full_pipeline():
    """测试完整的流水线"""
    print("=== 测试完整OpenContentBot流水线 ===")
    
    # 加载配置
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        print(f"错误: 配置文件不存在: {config_path}")
        return
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    print(f"加载配置文件: {config_path}")
    print(f"应用模式: {config.get('app_mode', 'N/A')}")
    print(f"领域: {config.get('niche', 'N/A')}")
    
    # 获取processor配置
    processor_config = config['modules']['processor']
    print(f"\nProcessor配置:")
    print(f"  提供商: {processor_config['provider']}")
    print(f"  模型: {processor_config['model']}")
    print(f"  温度: {processor_config.get('temperature', '默认')}")
    print(f"  目标平台: {processor_config.get('target_platform', 'N/A')}")
    
    # 初始化Processor
    print("\n正在初始化Processor...")
    try:
        processor = Processor(processor_config)
        print("Processor初始化成功")
    except Exception as e:
        print(f"Processor初始化失败: {type(e).__name__}: {e}")
        return
    
    # 测试用例
    test_cases = [
        {
            "name": "科技新闻",
            "data": "OpenAI 发布了新的语言模型 GPT-5，在推理能力和多模态理解方面有显著提升。"
        },
        {
            "name": "金融新闻", 
            "data": "美联储宣布维持利率不变，但暗示未来可能降息以刺激经济增长。"
        },
        {
            "name": "产品发布",
            "data": "苹果公司发布了新款 MacBook Pro，搭载 M4 芯片，性能提升 30%，电池续航达 20 小时。"
        },
        {
            "name": "市场动态",
            "data": "比特币价格突破 70,000 美元，创历史新高，加密货币市场整体上涨。"
        }
    ]
    
    # 测试不同的平台
    platforms = ["twitter", "instagram"]
    
    for platform in platforms:
        print(f"\n--- 测试平台: {platform} ---")
        
        # 更新配置中的平台
        processor.config['target_platform'] = platform
        
        for test_case in test_cases:
            print(f"\n测试案例: {test_case['name']}")
            print(f"输入数据: {test_case['data'][:80]}...")
            
            try:
                result = processor.process(test_case['data'])
                
                print(f"生成结果:")
                print(f"  Caption: {result.get('caption', 'N/A')}")
                print(f"  长度: {len(result.get('caption', ''))} 字符")
                
                # 检查字符限制
                max_length = 240 if platform == "twitter" else 1000
                caption = result.get('caption', '')
                if len(caption) > max_length:
                    print(f"  ⚠️ 警告: Caption长度({len(caption)})超过{platform}限制({max_length})")
                else:
                    print(f"  ✅ Caption长度符合{platform}限制")
                
                print(f"  Image Prompt: {result.get('image_prompt', 'N/A')[:100]}...")
                print(f"  Tags: {result.get('tags', [])}")
                print(f"  Tags数量: {len(result.get('tags', []))}")
                
                # 验证结构
                required_fields = ['caption', 'image_prompt', 'tags']
                missing_fields = [f for f in required_fields if f not in result]
                if missing_fields:
                    print(f"  ⚠️ 警告: 缺少字段: {missing_fields}")
                else:
                    print(f"  ✅ 所有必需字段都存在")
                
            except Exception as e:
                print(f"  处理失败: {type(e).__name__}: {e}")

def test_config_validation():
    """测试配置验证"""
    print("\n\n=== 测试配置验证 ===")
    
    # 测试无效配置
    invalid_configs = [
        {
            "name": "缺少provider",
            "config": {"model": "deepseek-r1"}
        },
        {
            "name": "无效provider",
            "config": {"provider": "invalid-provider", "model": "deepseek-r1"}
        },
        {
            "name": "缺少model",
            "config": {"provider": "aliyun"}
        },
        {
            "name": "空配置",
            "config": {}
        }
    ]
    
    for test in invalid_configs:
        print(f"\n测试: {test['name']}")
        print(f"配置: {test['config']}")
        
        try:
            processor = Processor(test['config'])
            print(f"结果: Processor初始化成功")
        except Exception as e:
            print(f"结果: {type(e).__name__}: {e}")

def test_system_prompt_formatting():
    """测试系统提示词格式化"""
    print("\n\n=== 测试系统提示词格式化 ===")
    
    # 从配置文件加载
    config_path = "config/config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    processor_config = config['modules']['processor']
    
    # 查看系统提示词
    system_prompt = processor_config['system_prompt']
    print("系统提示词内容:")
    print("-" * 50)
    print(system_prompt[:500] + "..." if len(system_prompt) > 500 else system_prompt)
    print("-" * 50)
    
    # 检查平台配置
    platform_configs = processor_config.get('platform_configs', {})
    print(f"\n支持的平台配置: {list(platform_configs.keys())}")
    
    for platform, config in platform_configs.items():
        print(f"\n{platform}平台配置:")
        for key, value in config.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    print("开始完整流水线测试...")
    
    # 启用调试模式
    os.environ["ALIYUN_DEBUG"] = "false"
    
    test_full_pipeline()
    test_config_validation()
    test_system_prompt_formatting()
    
    print("\n=== 所有测试完成 ===")