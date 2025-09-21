import requests
import asyncio
from datetime import datetime
import json
from typing import List, Dict
import yfinance as yf
import feedparser
from pytrends.request import TrendReq

class AdvancedTrendPredictor:
    """Free real-time trend analysis using only free APIs from requirements.txt"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.trend_sources = {
            'google_trends': self.get_google_trends,
            'finance_news': self.get_finance_news,
            'market_data': self.get_market_trends,
            'rss_feeds': self.get_rss_trends
        }
    
    async def predict_viral_topics(self) -> List[Dict]:
        """Predict what will go viral in the next 24-48 hours"""
        all_trends = []
        
        # Gather trends from all free sources
        for source, getter in self.trend_sources.items():
            try:
                trends = await getter()
                all_trends.extend(trends)
            except Exception as e:
                print(f"Error getting {source} trends: {e}")
        
        # AI analysis to predict viral potential
        viral_predictions = await self.analyze_viral_potential(all_trends)
        
        return sorted(viral_predictions, key=lambda x: x['viral_score'], reverse=True)
    
    async def get_google_trends(self) -> List[Dict]:
        """Get real Google Trends data using pytrends (free API)"""
        try:
            # Finance-related keywords
            keywords = ['investing', 'cryptocurrency', 'stocks', 'trading', 'finance']
            self.pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='US')
            
            # Get interest over time
            interest_data = self.pytrends.interest_over_time()
            trends = []
            
            if not interest_data.empty:
                for keyword in keywords:
                    if keyword in interest_data.columns:
                        avg_interest = interest_data[keyword].mean()
                        trends.append({
                            'topic': keyword.title(),
                            'search_volume': int(avg_interest * 1000),  # Scale up for readability
                            'growth_rate': 0.1,
                            'source': 'google_trends'
                        })
            
            return trends[:5]  # Top 5
        except Exception as e:
            print(f"Google Trends API error: {e}")
            return []
    
    async def get_finance_news(self) -> List[Dict]:
        """Get real finance news using feedparser (free RSS)"""
        try:
            # Free finance RSS feeds
            feeds = [
                'https://feeds.finance.yahoo.com/rss/2.0/headline',
                'https://www.marketwatch.com/rss/topstories',
                'https://feeds.bloomberg.com/markets/news.rss'
            ]
            
            trends = []
            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:3]:  # Top 3 from each feed
                        trends.append({
                            'title': entry.title,
                            'engagement': 1000,  # Default engagement
                            'source': 'finance_news',
                            'url': entry.link
                        })
                except Exception as e:
                    print(f"RSS feed error for {feed_url}: {e}")
                    continue
            
            return trends[:10]  # Top 10 total
        except Exception as e:
            print(f"Finance news error: {e}")
            return []
    
    async def get_market_trends(self) -> List[Dict]:
        """Get real market data using yfinance (free API)"""
        try:
            # Popular finance tickers
            tickers = ['SPY', 'QQQ', 'BTC-USD', 'ETH-USD', 'TSLA']
            trends = []
            
            for ticker in tickers:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    hist = stock.history(period='1d')
                    
                    if not hist.empty:
                        price_change = ((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100
                        trends.append({
                            'topic': f"{ticker} Market Analysis",
                            'price_change': round(price_change, 2),
                            'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0,
                            'source': 'market_data'
                        })
                except Exception as e:
                    print(f"Market data error for {ticker}: {e}")
                    continue
            
            return trends
        except Exception as e:
            print(f"Market trends error: {e}")
            return []
    
    async def get_rss_trends(self) -> List[Dict]:
        """Get trending topics from free RSS feeds"""
        try:
            # Free financial RSS feeds
            rss_feeds = [
                'https://www.cnbc.com/id/100003114/device/rss/rss.html',
                'https://www.reuters.com/business/finance/rss',
                'https://www.fool.com/feeds/index.aspx'
            ]
            
            trends = []
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:2]:  # Top 2 from each
                        trends.append({
                            'title': entry.title,
                            'engagement': 500,  # Default engagement
                            'source': 'rss_feeds',
                            'published': entry.get('published', 'Unknown')
                        })
                except Exception as e:
                    print(f"RSS error for {feed_url}: {e}")
                    continue
            
            return trends[:8]  # Top 8 total
        except Exception as e:
            print(f"RSS trends error: {e}")
            return []
    
    async def analyze_viral_potential(self, trends: List[Dict]) -> List[Dict]:
        """Analyze viral potential of trends"""
        viral_predictions = []
        
        for trend in trends:
            # Calculate viral score based on engagement metrics
            viral_score = 0.5  # Base score
            
            # Add score based on source metrics
            if 'score' in trend:  # Reddit
                viral_score += min(trend['score'] / 10000, 0.3)
            if 'mentions' in trend:  # X (formerly Twitter)
                viral_score += min(trend['mentions'] / 20000, 0.3)
            if 'views' in trend:  # YouTube
                viral_score += min(trend['views'] / 1000000, 0.3)
            if 'search_volume' in trend:  # Google
                viral_score += min(trend['search_volume'] / 100000, 0.3)
            
            viral_predictions.append({
                'title': trend.get('title', trend.get('topic', 'Unknown')),
                'viral_score': min(viral_score, 1.0),
                'source': trend.get('source', 'unknown'),
                'original_data': trend
            })
        
        return viral_predictions