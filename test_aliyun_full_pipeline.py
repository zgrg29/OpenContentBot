#!/usr/bin/env python3
"""
Full pipeline test for OpenContentBot with Aliyun providers
This tests both text generation and image generation
"""

import os
import sys
import yaml
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def test_text_generation():
    """Test text content generation with Aliyun"""
    print("🧪 Testing Text Generation with Aliyun...")
    
    from core.providers.aliyun_adapter import Adapter
    
    config = load_config()
    processor_config = config['modules']['processor']
    
    # Initialize the adapter
    text_adapter = Adapter(processor_config)
    
    # Test raw data
    raw_data = "Scientists have discovered a new exoplanet in the habitable zone of a nearby star system. The planet shows signs of liquid water and potentially habitable conditions."
    
    # System prompt (simplified for testing)
    system_prompt = """
You are an automated social media manager. Based on the provided news, generate structured content in JSON format.

Requirements:
1. Platform: twitter
2. Style: catchy and concise  
3. Character Limit: Under 240 characters.
4. Content: The "caption" field must NOT include any hashtags.
5. Image: The "image_prompt" should be a highly detailed English description for a photorealistic AI image.
6. Tags: Provide 3-5 relevant hashtags in the "tags" list.

Return ONLY a JSON object:
{
  "caption": "your text here",
  "image_prompt": "description here", 
  "tags": ["#tag1", "#tag2"]
}
"""
    
    try:
        result = text_adapter.generate_content(raw_data, system_prompt)
        print("✅ Text generation successful!")
        print(f"Caption: {result.get('caption', 'N/A')}")
        print(f"Image Prompt: {result.get('image_prompt', 'N/A')}")
        print(f"Tags: {result.get('tags', [])}")
        return result
    except Exception as e:
        print(f"❌ Text generation failed: {e}")
        return None

def test_image_generation(image_prompt):
    """Test image generation with Aliyun"""
    print("\n🎨 Testing Image Generation with Aliyun...")
    
    from core.providers.aliyun_image_adapter import AliyunImageAdapter
    
    config = load_config()
    media_config = config['modules']['media_studio']
    
    # Initialize the image adapter
    image_adapter = AliyunImageAdapter(media_config)
    
    quality_enhancers = media_config.get('quality_enhancers', 'cinematic lighting, photorealistic, 8k, highly detailed')
    
    try:
        image_path = image_adapter.generate(image_prompt, quality_enhancers)
        if image_path and os.path.exists(image_path):
            print(f"✅ Image generated successfully: {image_path}")
            return image_path
        else:
            print("❌ Image generation failed or returned empty path")
            return None
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        return None

def main():
    print("=" * 60)
    print("🚀 Full Pipeline Test: OpenContentBot with Aliyun Providers")
    print("=" * 60)
    
    # Test 1: Text Generation
    text_result = test_text_generation()
    if not text_result:
        print("\n💥 Text generation failed. Exiting.")
        return
    
    # Test 2: Image Generation (if text succeeded)
    image_prompt = text_result.get('image_prompt', '')
    if image_prompt:
        image_path = test_image_generation(image_prompt)
        if image_path:
            print(f"\n🎉 Full pipeline test completed!")
            print(f"📄 Generated caption: {text_result.get('caption', 'N/A')}")
            print(f"🖼️  Generated image: {image_path}")
            print(f"🏷️  Tags: {', '.join(text_result.get('tags', []))}")
        else:
            print(f"\n⚠️  Text generation worked, but image generation failed.")
            print(f"📄 Generated caption: {text_result.get('caption', 'N/A')}")
            print(f"📝 Image prompt: {image_prompt}")
            print(f"🏷️  Tags: {', '.join(text_result.get('tags', []))}")
            print("\n💡 Note: Image generation may require additional setup in Alibaba Cloud Console")
    else:
        print("\n⚠️  No image prompt generated from text")

if __name__ == "__main__":
    main()