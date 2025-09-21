import requests
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List
import logging
from pytrends.request import TrendReq
import os

class SmartTrendDetector:
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.logger = logging.getLogger(__name__)
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.cache = {}
        self.cache_duration = 3600  # 1 hour
        
    def get_trending_topics(self, category: str = 'finance') -> List[str]:
        """Get real-time trending topics for specified category"""
        cache_key = f"trending_{category}"
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]['data']
            
        try:
            # Get Google Trends data
            google_trends = self._get_google_trends(category)
            
            # Get YouTube trending topics
            youtube_trends = self._get_youtube_trending(category)
            
            # Get social media trends
            social_trends = self._get_social_trends(category)
            
            # Combine and rank trends
            combined_trends = self._combine_trends(google_trends, youtube_trends, social_trends)
            
            self._cache_data(cache_key, combined_trends)
            return combined_trends
            
        except Exception as e:
            self.logger.error(f"Error getting trending topics: {e}")
            return self._get_fallback_trends(category)
    
    def _get_google_trends(self, category: str) -> List[str]:
        """Get trending topics from Google Trends - FIXED VERSION"""
        try:
            keywords = self._get_category_keywords(category)
            # FIX: Use proper pytrends methods
            self.pytrends.build_payload(keywords, cat=0, timeframe='now 1-d', geo='US')
            
            # FIX: Use interest_over_time instead of trending_searches
            try:
                trending_data = self.pytrends.interest_over_time()
                if not trending_data.empty:
                    # Get top trending keywords from the data
                    trending_keywords = trending_data.columns.tolist()
                    return trending_keywords[:10]
            except Exception:
                # Fallback to related queries
                related_queries = self.pytrends.related_queries()
                trends = []
                for keyword in keywords:
                    if keyword in related_queries and related_queries[keyword]['top'] is not None:
                        top_queries = related_queries[keyword]['top']['query'].tolist()[:3]
                        trends.extend(top_queries)
                return trends[:10]
                
        except Exception as e:
            self.logger.error(f"Google Trends error: {e}")
            # FIX: Return fallback trends instead of empty list
            return self._get_fallback_trends(category)[:10]
            
        return self._get_fallback_trends(category)[:10]
    
    def _get_youtube_trending(self, category: str) -> List[str]:
        """Get trending topics from YouTube API"""
        if not self.youtube_api_key:
            return []
            
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet',
                'chart': 'mostPopular',
                'regionCode': 'US',
                'videoCategoryId': self._get_youtube_category_id(category),
                'maxResults': 20,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            topics = []
            for item in data.get('items', []):
                title = item['snippet']['title']
                # Extract keywords from titles
                keywords = self._extract_keywords(title)
                topics.extend(keywords)
                
            return list(set(topics))[:10]
            
        except Exception as e:
            self.logger.error(f"YouTube trending error: {e}")
            return []
    
    def _get_social_trends(self, category: str) -> List[str]:
        """Get trending topics from social media APIs"""
        # Placeholder for social media trend detection
        # Can integrate with Twitter API, Reddit API, etc.
        return []
    
    def _combine_trends(self, *trend_lists) -> List[str]:
        """Combine and rank trends from multiple sources"""
        trend_scores = {}
        
        for trends in trend_lists:
            for i, trend in enumerate(trends):
                score = len(trends) - i  # Higher score for higher position
                trend_scores[trend] = trend_scores.get(trend, 0) + score
        
        # Sort by score and return top trends
        sorted_trends = sorted(trend_scores.items(), key=lambda x: x[1], reverse=True)
        return [trend for trend, score in sorted_trends[:15]]
    
    def _get_category_keywords(self, category: str) -> List[str]:
        """Get base keywords for category"""
        keyword_map = {
            'finance': ['investing', 'stocks', 'crypto', 'money', 'trading'],
            'tech': ['technology', 'AI', 'software', 'gadgets', 'innovation'],
            'business': ['entrepreneurship', 'startup', 'marketing', 'sales', 'leadership'],
            'lifestyle': ['health', 'fitness', 'travel', 'food', 'fashion']
        }
        return keyword_map.get(category, ['trending', 'popular', 'viral'])
    
    def _get_youtube_category_id(self, category: str) -> str:
        """Map category to YouTube category ID"""
        category_map = {
            'finance': '25',  # News & Politics
            'tech': '28',     # Science & Technology
            'business': '25', # News & Politics
            'lifestyle': '26' # Howto & Style
        }
        return category_map.get(category, '0')
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction - can be enhanced with NLP
        words = text.lower().split()
        keywords = [word for word in words if len(word) > 3 and word.isalpha()]
        return keywords[:3]
    
    def _get_fallback_trends(self, category: str) -> List[str]:
        """Fallback trends when API calls fail"""
        fallback_map = {
            'finance': ['market analysis', 'investment tips', 'crypto news', 'stock picks', 'financial planning'],
            'tech': ['AI breakthrough', 'new gadgets', 'software updates', 'tech reviews', 'innovation'],
            'business': ['startup success', 'marketing strategies', 'leadership tips', 'business growth', 'entrepreneurship']
        }
        return fallback_map.get(category, ['trending topics', 'viral content', 'popular news'])
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        return (datetime.now() - self.cache[key]['timestamp']).seconds < self.cache_duration
    
    def _cache_data(self, key: str, data: Any):
        """Cache data with timestamp"""
        self.cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }