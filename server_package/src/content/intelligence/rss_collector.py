import feedparser
import requests
from datetime import datetime, timedelta
import logging
from typing import List, Dict
import time

class RSSCollector:
    """Collects content from various RSS feeds for unique content discovery"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Free finance and economic RSS feeds
        self.feeds = {
            'reuters_business': 'http://feeds.reuters.com/reuters/businessNews',
            'cnbc_top_news': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
            'wsj_markets': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
            'bloomberg_economics': 'https://news.google.com/rss/search?q=economics+when:7d&hl=en-US&gl=US&ceid=US:en',
            'investing_com': 'https://www.investing.com/rss/news_0.rss',
            'financial_times': 'https://www.ft.com/?format=rss',
            'economist_finance': 'https://www.economist.com/finance-and-economics/rss.xml',
            'market_watch': 'https://www.marketwatch.com/rss/topstories',
            'yahoo_finance': 'https://finance.yahoo.com/rss/',
            'sec_news': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom'
        }
        
    def collect_all_feeds(self, hours_back: int = 24) -> List[Dict]:
        """Collect articles from all RSS feeds"""
        all_articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        for feed_name, feed_url in self.feeds.items():
            try:
                articles = self._collect_single_feed(feed_name, feed_url, cutoff_time)
                all_articles.extend(articles)
                self.logger.info(f"Collected {len(articles)} articles from {feed_name}")
                # Be respectful to servers
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error collecting from {feed_name}: {e}")
                
        return all_articles
    
    def _collect_single_feed(self, feed_name: str, feed_url: str, cutoff_time: datetime) -> List[Dict]:
        """Collect articles from a single RSS feed"""
        articles = []
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                # Parse publication date
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                
                # Skip old articles
                if pub_date and pub_date < cutoff_time:
                    continue
                
                # Extract content
                content = ""
                if hasattr(entry, 'summary'):
                    content = entry.summary
                elif hasattr(entry, 'content') and entry.content:
                    content = entry.content[0].value if isinstance(entry.content, list) else entry.content
                
                article = {
                    'title': entry.title if hasattr(entry, 'title') else '',
                    'content': content,
                    'url': entry.link if hasattr(entry, 'link') else '',
                    'published': pub_date.isoformat() if pub_date else '',
                    'source': feed_name,
                    'keywords': self._extract_keywords(entry.title + ' ' + content)
                }
                
                articles.append(article)
                
        except Exception as e:
            self.logger.error(f"Error parsing feed {feed_name}: {e}")
            
        return articles
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract potential keywords from text"""
        # Simple keyword extraction - can be enhanced with NLP
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        # Simple extraction - words longer than 4 characters
        words = text.lower().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').split()
        keywords = [word for word in words if len(word) > 4 and word not in common_words]
        return list(set(keywords))[:10]  # Return unique keywords, limit to 10

    def find_trending_topics(self, hours_back: int = 24) -> List[Dict]:
        """Find trending topics from RSS feeds"""
        articles = self.collect_all_feeds(hours_back)
        
        # Count keyword frequency
        keyword_count = {}
        for article in articles:
            for keyword in article['keywords']:
                keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        # Sort by frequency
        sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
        
        # Create trending topics
        trending_topics = []
        for keyword, count in sorted_keywords[:20]:  # Top 20 keywords
            if count > 1:  # Only include keywords that appear more than once
                trending_topics.append({
                    'topic': keyword,
                    'frequency': count,
                    'sources': len([a for a in articles if keyword in a['keywords']]),
                    'type': 'rss_trend'
                })
        
        return trending_topics

if __name__ == "__main__":
    # Test the RSS collector
    collector = RSSCollector()
    topics = collector.find_trending_topics(48)  # Last 48 hours
    print(f"Found {len(topics)} trending topics:")
    for topic in topics[:10]:
        print(f"- {topic['topic']} (frequency: {topic['frequency']})")