import feedparser
import requests
from datetime import datetime

class Ingestor:
    def __init__(self, config):
        self.config = config
        self.sources = config.get('sources', [])
        self.keywords = config.get('keywords', [])

    def fetch(self):
        """
        核心抓取方法：根据配置抓取所有源
        """
        print("Starting data ingestion...")
        all_items = []

        # 1. 处理 RSS 订阅
        if self.config.get('enable_rss'):
            all_items.extend(self._fetch_rss())

        # 2. 处理特定 API (以简单的热词模拟为例)
        if self.config.get('enable_trends'):
            all_items.extend(self._fetch_trends())

        # 这里的过滤逻辑可以根据关键词过滤，或者去除重复
        return self._filter(all_items)

    def _fetch_rss(self):
        rss_data = []
        for url in self.config.get('rss_urls', []):
            print(f"Fetching RSS: {url}")
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # 每个源取前5条
                rss_data.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get('summary', ''),
                    "source_type": "rss",
                    "timestamp": datetime.now().isoformat()
                })
        return rss_data

    def _fetch_trends(self):
        # 实际开发时这里可以集成 pytrends 或 微博热搜 API
        print("Fetching Google Trends...")
        # 模拟返回
        return [{
            "title": "AI Content Automation is Booming",
            "summary": "Recent trends show a 300% increase in automated media...",
            "source_type": "trends"
        }]

    def _filter(self, items):
        """
        简单的关键词过滤逻辑
        """
        if not self.keywords:
            return items
        
        filtered = [
            item for item in items 
            if any(kw.lower() in item['title'].lower() for kw in self.keywords)
        ]
        return filtered