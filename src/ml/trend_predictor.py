"""
Trend Predictor - ML-powered trend analysis and prediction
"""

import asyncio
import logging
import os
import requests
from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

class TrendPredictor:
    """Predicts trending topics using ML and social media analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.scaler = StandardScaler()
        self.trend_sources = {
            'youtube': self.get_youtube_trends,
            'twitter': self.get_twitter_trends,
            'reddit': self.get_reddit_trends,
            'google': self.get_google_trends
        }
        
    async def initialize(self):
        """Initialize the trend predictor"""
        self.logger.info("Initializing Trend Predictor...")
        await self.load_or_train_model()
        
    async def get_trending_topics(self, limit: int = 10) -> List[str]:
        """Get current trending topics from multiple sources"""
        all_trends = []
        
        # Collect trends from all sources
        for source_name, source_func in self.trend_sources.items():
            try:
                trends = await source_func()
                for trend in trends:
                    trend['source'] = source_name
                    trend['collected_at'] = datetime.now()
                all_trends.extend(trends)
            except Exception as e:
                self.logger.error(f"Error collecting trends from {source_name}: {e}")
        
        # Score and rank trends
        scored_trends = await self.score_trends(all_trends)
        
        # Return top trending topics
        top_trends = sorted(scored_trends, key=lambda x: x['score'], reverse=True)[:limit]
        return [trend['topic'] for trend in top_trends]
    
    async def get_youtube_trends(self) -> List[Dict]:
        """Get trending topics from YouTube"""
        # Using YouTube API to get trending videos
        api_key = os.getenv('YOUTUBE_API_KEY')
        url = f"https://www.googleapis.com/youtube/v3/videos"
        
        params = {
            'part': 'snippet,statistics',
            'chart': 'mostPopular',
            'regionCode': 'US',
            'maxResults': 50,
            'key': api_key
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            trends = []
            for item in data.get('items', []):
                snippet = item['snippet']
                stats = item['statistics']
                
                trends.append({
                    'topic': snippet['title'],
                    'category': snippet.get('categoryId', 'unknown'),
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'engagement_rate': self.calculate_engagement_rate(stats)
                })
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Error fetching YouTube trends: {e}")
            return []
    
    async def get_twitter_trends(self) -> List[Dict]:
        """Get trending topics from Twitter"""
        # Placeholder for Twitter API integration
        # In production, use Twitter API v2
        return [
            {'topic': 'AI Trading Strategies', 'mentions': 15000, 'sentiment': 0.7},
            {'topic': 'Sustainable Finance', 'mentions': 12000, 'sentiment': 0.3},
            {'topic': 'Cryptocurrency Trading', 'mentions': 18000, 'sentiment': 0.5}
        ]
    
    async def get_reddit_trends(self) -> List[Dict]:
        """Get trending topics from Reddit"""
        return [
            {'topic': 'Cryptocurrency Investment Strategies', 'upvotes': 5000, 'comments': 800},
            {'topic': 'Personal Finance Tips for 2025', 'upvotes': 7000, 'comments': 1200},
            {'topic': 'Stock Market Analysis', 'upvotes': 4500, 'comments': 600},
            {'topic': 'Real Estate Investment', 'upvotes': 6200, 'comments': 950},
            {'topic': 'Retirement Planning Strategies', 'upvotes': 5800, 'comments': 720}
        ]
    
    async def get_google_trends(self) -> List[Dict]:
        """Get trending topics from Google Trends"""
        return [
            {'topic': 'AI Trading Algorithms', 'search_volume': 100000, 'growth_rate': 0.15},
            {'topic': 'Digital Banking Solutions', 'search_volume': 80000, 'growth_rate': 0.08},
            {'topic': 'Sustainable Investing', 'search_volume': 60000, 'growth_rate': 0.12},
            {'topic': 'DeFi Protocols', 'search_volume': 75000, 'growth_rate': 0.18},
            {'topic': 'Financial Independence', 'search_volume': 90000, 'growth_rate': 0.10}
        ]
    
    async def score_trends(self, trends: List[Dict]) -> List[Dict]:
        """Score trends based on multiple factors"""
        scored_trends = []
        
        for trend in trends:
            score = 0
            
            # Base score from engagement metrics
            if 'views' in trend:
                score += min(trend['views'] / 1000000, 10)  # Max 10 points for views
            if 'likes' in trend:
                score += min(trend['likes'] / 100000, 5)  # Max 5 points for likes
            if 'mentions' in trend:
                score += min(trend['mentions'] / 10000, 5)  # Max 5 points for mentions
            if 'upvotes' in trend:
                score += min(trend['upvotes'] / 1000, 5)  # Max 5 points for upvotes
            
            # Bonus for positive sentiment
            if 'sentiment' in trend and trend['sentiment'] > 0.5:
                score += 2
            
            # Bonus for growth rate
            if 'growth_rate' in trend:
                score += trend['growth_rate'] * 10
            
            # Source reliability weight
            source_weights = {'youtube': 1.2, 'twitter': 1.0, 'reddit': 0.9, 'google': 1.1}
            score *= source_weights.get(trend.get('source', 'unknown'), 1.0)
            
            scored_trends.append({
                **trend,
                'score': score
            })
        
        return scored_trends
    
    def calculate_engagement_rate(self, stats: Dict) -> float:
        """Calculate engagement rate from video statistics"""
        views = int(stats.get('viewCount', 0))
        likes = int(stats.get('likeCount', 0))
        comments = int(stats.get('commentCount', 0))
        
        if views == 0:
            return 0
        
        return (likes + comments) / views
    
    async def load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = "models/trend_predictor.joblib"
        
        try:
            self.model = joblib.load(model_path)
            self.logger.info("Loaded existing trend prediction model")
        except FileNotFoundError:
            self.logger.info("Training new trend prediction model...")
            await self.train_model()
            
    async def train_model(self):
        """Train the trend prediction model"""
        # Generate synthetic training data for demonstration
        # In production, use historical trend data
        
        np.random.seed(42)
        n_samples = 1000
        
        # Features: views, likes, comments, sentiment, source_score
        X = np.random.rand(n_samples, 5)
        X[:, 0] *= 10000000  # views
        X[:, 1] *= 500000   # likes
        X[:, 2] *= 50000    # comments
        X[:, 3] = X[:, 3] * 2 - 1  # sentiment (-1 to 1)
        X[:, 4] *= 5        # source_score
        
        # Target: viral score (combination of features with noise)
        y = (X[:, 0] / 1000000 + X[:, 1] / 100000 + X[:, 2] / 10000 + 
             X[:, 3] * 2 + X[:, 4]) + np.random.normal(0, 0.5, n_samples)
        
        # Train model
        X_scaled = self.scaler.fit_transform(X)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_scaled, y)
        
        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, "models/trend_predictor.joblib")
        joblib.dump(self.scaler, "models/trend_scaler.joblib")
        
        self.logger.info("Trend prediction model trained and saved")

    async def get_viral_keywords_realtime(self) -> List[str]:
        """Get real-time viral keywords from multiple sources"""
        viral_keywords = []
        
        # YouTube trending analysis
        youtube_trends = await self.get_youtube_trends()
        for trend in youtube_trends[:10]:
            # Extract keywords from trending titles
            keywords = self._extract_keywords_from_title(trend['topic'])
            viral_keywords.extend(keywords)
        
        # Social media trending hashtags
        social_trends = await self._get_social_media_trends()
        viral_keywords.extend(social_trends)
        
        # Google Trends integration
        google_trends = await self._get_google_trending_keywords()
        viral_keywords.extend(google_trends)
        
        # Filter and rank by viral potential
        return self._rank_keywords_by_viral_score(viral_keywords)[:20]
    
    def _extract_keywords_from_title(self, title: str) -> List[str]:
        """Extract keywords from video title"""
        # Simple keyword extraction - remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        words = title.lower().split()
        keywords = [word.strip('.,!?()[]{}"') for word in words if word.lower() not in stop_words and len(word) > 2]
        return keywords[:5]  # Return top 5 keywords
    
    async def _get_social_media_trends(self) -> List[str]:
        """Get trending hashtags from social media"""
        # Placeholder for social media API integration
        return ['#AI', '#investing', '#finance', '#crypto', '#stocks']
    
    async def _get_google_trending_keywords(self) -> List[str]:
        """Get trending keywords from Google Trends"""
        # Placeholder for Google Trends API integration
        return ['artificial intelligence', 'stock market', 'cryptocurrency', 'investment tips', 'financial planning']
    
    def _rank_keywords_by_viral_score(self, keywords: List[str]) -> List[str]:
        """Rank keywords by viral potential"""
        # Simple scoring based on keyword characteristics
        scored_keywords = []
        for keyword in keywords:
            score = len(keyword) * 0.1  # Longer keywords might be more specific
            if any(viral_word in keyword.lower() for viral_word in ['ai', 'crypto', 'money', 'invest', 'profit']):
                score += 1.0  # Boost for viral finance terms
            scored_keywords.append((keyword, score))
        
        # Sort by score and return keywords
        scored_keywords.sort(key=lambda x: x[1], reverse=True)
        return [keyword for keyword, score in scored_keywords]