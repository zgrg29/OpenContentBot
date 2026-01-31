#!/usr/bin/env python3
"""
Test script for Aliyun Image Provider
Tests the image generation functionality using Aliyun's Tongyi Wanxiang API.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.providers.aliyun_image_adapter import AliyunImageAdapter

def test_aliyun_image_provider():
    """Test the Aliyun image provider functionality."""
    print("🧪 Testing Aliyun Image Provider for OpenContentBot")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('ALIYUN_API_KEY')
    if not api_key:
        print("❌ ALIYUN_API_KEY not found in environment variables")
        return False
    
    print(f"✅ Found ALIYUN_API_KEY: {api_key[:12]}...")
    
    # Test configuration
    config = {
        'model': 'wanx-v1',
        'resolution': '1024*1024',
        'quality_enhancers': 'cinematic lighting, photorealistic, 8k, highly detailed',
        'save_dir': 'outputs/images/'
    }
    
    try:
        adapter = AliyunImageAdapter(config)
        print("✅ Adapter initialized successfully")
    except Exception as e:
        print(f"❌ Adapter initialization failed: {e}")
        return False
    
    # Test prompt from previous text generation
    test_prompt = "A photorealistic depiction of a newly discovered exoplanet in the habitable zone, with blue and green hues suggesting oceans and vegetation, orbiting a distant sun-like star, viewed from space with stars in the background."
    quality_enhancers = config['quality_enhancers']
    
    print("⏳ Testing image generation...")
    print(f"   Prompt: {test_prompt[:100]}...")
    print(f"   Quality enhancers: {quality_enhancers}")
    
    try:
        image_path = adapter.generate(test_prompt, quality_enhancers)
        if image_path and os.path.exists(image_path):
            print(f"✅ Image generated successfully!")
            print(f"   Saved to: {image_path}")
            
            # Get file size
            file_size = os.path.getsize(image_path)
            print(f"   File size: {file_size} bytes")
            
            return True
        else:
            print("❌ Image generation failed or returned empty path")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error during image generation: {e}")
        return False

if __name__ == "__main__":
    success = test_aliyun_image_provider()
    print("=" * 60)
    if success:
        print("🎉 Test passed! Aliyun image provider is working correctly.")
    else:
        print("💥 Test failed! Check the errors above.")
        print("\n💡 Note: If you get 'AccessDenied' error, it may be because:")
        print("   - Your API key doesn't have access to Tongyi Wanxiang (通义万相)")
        print("   - Synchronous calls are not supported for your account")
        print("   - You need to enable the service in Alibaba Cloud Console")
        sys.exit(1)