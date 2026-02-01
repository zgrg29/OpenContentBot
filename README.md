# OpenContentBot
The all-in-one modular AI engine for autonomous content creation and distribution.

## 1. Project Overview
OpenContentBot is a Python-based autonomous content machine designed to monitor global trends (Finance, Fashion, Sports, etc.) in real-time. It leverages Generative AI to produce high-quality copy, images, and videos, achieving automated scheduling and multi-platform distribution without human intervention.

## 2. Core Features
* **Real-time Trend Scanning:** 24/7 monitoring of Google Trends, social media hot topics, and industry RSS feeds.
* **Multimodal AI Generation:**
    * **Text:** Simulates professional blogger personas with support for various domain-specific styles.
    * **Visuals:** Automatically generates high-quality images contextualized to the text.
    * **Motion:** Synthesizes short videos including voiceovers (TTS), subtitles, and background music.
* **Cross-platform Distribution:** Seamless integration with X (Twitter), Instagram, TikTok, and Telegram.
* **Unattended Operation:** Reliable automated scheduling designed for server environments.

## 3. Technical Architecture
### A. Ingestion Layer
* **Tech Stack:** `pytrends`, `tweepy`, `feedparser`.
* **Logic:** Implements keyword weighting algorithms to identify high-potential viral topics.

### B. Intelligence Layer
* **Text Processing:** Deep rewriting and creation via GPT-4 or Claude 3 APIs.
* **Image Creation:** Visual asset production using Stable Diffusion (local) or DALL-E 3 (API).
* **Video Editing:** Merging TTS and images into MP4 format using the `MoviePy` library.

### C. Deployment & Distribution
* **Containerization:** Environment encapsulation using Docker for stable cloud deployment (AWS/GCP).
* **Task Scheduling:** Triggering workflows via `Celery` or `APScheduler`.



---

## 4. Configuration Setup

To run the bot, you need to configure the environment variables and the application settings.

### A. Environment Variables (`.env`)
Create a `.env` file in the root directory to store your sensitive API keys:

```env
# LLM & Image Provider Keys
OPENAI_API_KEY=sk-xxxx...
ANTHROPIC_API_KEY=sk-ant-xxxx...

# Social Media API Credentials
TWITTER_API_KEY=xxxx...
TWITTER_API_SECRET=xxxx...
TWITTER_ACCESS_TOKEN=xxxx...
TWITTER_ACCESS_SECRET=xxxx...

TELEGRAM_BOT_TOKEN=xxxx...
TELEGRAM_CHAT_ID=xxxx...

# Instagram (Instagrapi) Credentials
INSTA_USERNAME=your_username
INSTA_PASSWORD=your_password
```

### B. Application Logic (config/config.yaml)
change rss source
change keywords
```
rss_urls:
  - "[https://techcrunch.com/feed/](https://techcrunch.com/feed/)"
keywords: ["AI", "Tech", "Startup"]
```
change text and image generator
```
  processor:
    provider: "openai"     # Options: openai, gemini, deepseek
    model: "gpt-4"
    system_prompt: "You are a professional tech blogger..."

  media_studio:
    image:
      provider: "openai_image" # Options: openai_image, sd_local
      quality_enhancers: "high quality, 4k, cinematic"
```
change publish_channels
```
  publish_channels:
    twitter:
      enabled: true
    telegram:
      enabled: false
    instagram:
      enabled: true
```