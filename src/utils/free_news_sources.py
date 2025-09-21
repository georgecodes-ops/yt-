import requests
from typing import List, Dict
import json

try:
    import feedparser
except ImportError:
    feedparser = None
    print("Warning: feedparser not installed. RSS feeds will be disabled.")

class FreeNewsAggregator:
    """Completely free news aggregation without API keys"""
    
    def __init__(self):
        self.sources = {
            'reddit': 'https://www.reddit.com/r/finance/hot.json',
            'hackernews': 'https://hacker-news.firebaseio.com/v0/topstories.json',
            'rss_feeds': [
                'http://feeds.reuters.com/reuters/businessNews',
                'http://feeds.bbci.co.uk/news/business/rss.xml',
                'https://feeds.finance.yahoo.com/rss/2.0/headline'
            ]
        }
    
    def get_free_finance_news(self) -> List[Dict]:
        """Get finance news from free sources"""
        news = []
        
        # Reddit Finance
        try:
            response = requests.get(self.sources['reddit'], headers={'User-agent': 'MonAY Bot 1.0'})
            if response.status_code == 200:
                data = response.json()
                for post in data['data']['children'][:10]:
                    news.append({
                        'title': post['data']['title'],
                        'url': f"https://reddit.com{post['data']['permalink']}",
                        'source': 'reddit',
                        'timestamp': post['data']['created_utc']
                    })
        except Exception as e:
            print(f"Reddit error: {e}")
        
        # RSS Feeds (only if feedparser is available)
        if feedparser is not None:
            for rss_url in self.sources['rss_feeds']:
                try:
                    feed = feedparser.parse(rss_url)
                    for entry in feed.entries[:5]:
                        news.append({
                            'title': entry.title,
                            'url': entry.link,
                            'source': rss_url.split('/')[2],
                            'timestamp': entry.published_parsed
                        })
                except Exception as e:
                    print(f"RSS error: {e}")
        
        return news

# Usage in your system
if __name__ == "__main__":
    aggregator = FreeNewsAggregator()
    news = aggregator.get_free_finance_news()
    print(f"Found {len(news)} free news articles")