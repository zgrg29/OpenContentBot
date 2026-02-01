import yaml
import os
from core.media_studio import MediaStudio

def test_media_studio():
    print("--- Starting MediaStudio Standalone Test ---")
    
    # 1. Load Configuration
    try:
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            full_config = yaml.safe_load(f)
            media_config = full_config['modules']['media_studio']['image']
    except Exception as e:
        print(f"[!] Error loading config: {e}")
        return

    # 2. Initialize MediaStudio
    # This should trigger the dynamic loading of openai_image_adapter
    try:
        studio = MediaStudio(media_config)
        print(f"[*] Successfully loaded provider: {studio.provider}")
    except Exception as e:
        print(f"[!] Initialization failed: {e}")
        return

    # 3. Define a Dummy Prompt
    # In a real run, this comes from the Processor
    test_prompt = "A high-tech financial trading floor with holographic AI charts and a sleek futuristic aesthetic"
    
    print(f"[*] Generating image for: '{test_prompt}'...")
    
    # 4. Run Generation
    image_path = studio.create_visual(test_prompt)

    # 5. Verify Results
    if image_path and os.path.exists(image_path):
        print("\n--- Test Success! ---")
        print(f"[+] Image generated and saved at: {image_path}")
        print(f"[+] File size: {os.path.getsize(image_path) // 1024} KB")
    else:
        print("\n--- Test Failed ---")
        print("[!] No image was created. Check OpenAI API keys and logs.")

if __name__ == "__main__":
    test_media_studio()