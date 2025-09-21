import requests
import json
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime, timedelta
import os
from dataclasses import dataclass
import re

@dataclass
class CompetitorChannel:
    channel_id: str
    channel_name: str
    subscriber_count: int
    video_count: int
    avg_views: float
    upload_frequency: float
    discovery_method: str
    relevance_score: float
    last_analyzed: datetime

class EnhancedCompetitorDiscovery:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.discovered_competitors = {}
        self.analysis_cache = {}
        
    def discover_competitors(self, niche_keywords: List[str], 
                           min_subscribers: int = 1000,
                           max_competitors: int = 20) -> List[CompetitorChannel]:
        """Discover competitors using multiple methods"""
        try:
            all_competitors = []
            
            # Method 1: Keyword-based discovery
            keyword_competitors = self._discover_by_keywords(niche_keywords, min_subscribers)
            all_competitors.extend(keyword_competitors)
            
            # Method 2: Content similarity discovery
            content_competitors = self._discover_by_content_similarity(niche_keywords)
            all_competitors.extend(content_competitors)
            
            # Method 3: Audience overlap discovery
            audience_competitors = self._discover_by_audience_overlap()
            all_competitors.extend(audience_competitors)
            
            # Method 4: Trending topic competitors
            trending_competitors = self._discover_by_trending_topics(niche_keywords)
            all_competitors.extend(trending_competitors)
            
            # Remove duplicates and rank by relevance
            unique_competitors = self._deduplicate_and_rank(all_competitors)
            
            # Filter and limit results
            filtered_competitors = [
                comp for comp in unique_competitors 
                if comp.subscriber_count >= min_subscribers
            ][:max_competitors]
            
            # Cache results
            for comp in filtered_competitors:
                self.discovered_competitors[comp.channel_id] = comp
            
            self.logger.info(f"Discovered {len(filtered_competitors)} competitors")
            return filtered_competitors
            
        except Exception as e:
            self.logger.error(f"Error discovering competitors: {e}")
            return []
    
    def _discover_by_keywords(self, keywords: List[str], min_subscribers: int) -> List[CompetitorChannel]:
        """Discover competitors by searching for niche keywords"""
        if not self.youtube_api_key:
            return []
            
        competitors = []
        
        for keyword in keywords[:5]:  # Limit to avoid API quota issues
            try:
                # Search for channels
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': keyword,
                    'type': 'channel',
                    'order': 'relevance',
                    'maxResults': 10,
                    'key': self.youtube_api_key
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                for item in data.get('items', []):
                    channel_id = item['id']['channelId']
                    channel_info = self._get_channel_details(channel_id)
                    
                    if channel_info and channel_info.subscriber_count >= min_subscribers:
                        channel_info.discovery_method = f"keyword: {keyword}"
                        channel_info.relevance_score = self._calculate_keyword_relevance(channel_info, keyword)
                        competitors.append(channel_info)
                        
            except Exception as e:
                self.logger.error(f"Error searching for keyword {keyword}: {e}")
                continue
        
        return competitors
    
    def _discover_by_content_similarity(self, keywords: List[str]) -> List[CompetitorChannel]:
        """Discover competitors by analyzing content similarity"""
        if not self.youtube_api_key:
            return []
            
        competitors = []
        
        try:
            # Search for videos with our keywords
            for keyword in keywords[:3]:
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': keyword,
                    'type': 'video',
                    'order': 'viewCount',
                    'maxResults': 15,
                    'key': self.youtube_api_key
                }
                
                response = requests.get(url, params=params)
                data = response.json()
                
                # Extract channel IDs from video results
                channel_ids = set()
                for item in data.get('items', []):
                    channel_ids.add(item['snippet']['channelId'])
                
                # Get details for each channel
                for channel_id in list(channel_ids)[:5]:  # Limit to avoid quota issues
                    channel_info = self._get_channel_details(channel_id)
                    if channel_info:
                        channel_info.discovery_method = f"content similarity: {keyword}"
                        channel_info.relevance_score = self._calculate_content_similarity(channel_info, keywords)
                        competitors.append(channel_info)
                        
        except Exception as e:
            self.logger.error(f"Error in content similarity discovery: {e}")
        
        return competitors
    
    def _discover_by_audience_overlap(self) -> List[CompetitorChannel]:
        """Discover competitors by analyzing audience overlap"""
        # This would require more advanced analytics
        # For now, return empty list - can be enhanced with social media APIs
        return []
    
    def _discover_by_trending_topics(self, keywords: List[str]) -> List[CompetitorChannel]:
        """Discover competitors from trending topics in the niche"""
        if not self.youtube_api_key:
            return []
            
        competitors = []
        
        try:
            # Get trending videos in relevant categories
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,statistics',
                'chart': 'mostPopular',
                'regionCode': 'US',
                'videoCategoryId': '25',  # News & Politics (good for finance)
                'maxResults': 20,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            # Filter videos that match our keywords
            relevant_channels = set()
            for item in data.get('items', []):
                title = item['snippet']['title'].lower()
                description = item['snippet']['description'].lower()
                
                # Check if any of our keywords appear in title/description
                for keyword in keywords:
                    if keyword.lower() in title or keyword.lower() in description:
                        relevant_channels.add(item['snippet']['channelId'])
                        break
            
            # Get channel details
            for channel_id in list(relevant_channels)[:5]:
                channel_info = self._get_channel_details(channel_id)
                if channel_info:
                    channel_info.discovery_method = "trending topics"
                    channel_info.relevance_score = self._calculate_trending_relevance(channel_info)
                    competitors.append(channel_info)
                    
        except Exception as e:
            self.logger.error(f"Error in trending topics discovery: {e}")
        
        return competitors
    
    def _get_channel_details(self, channel_id: str) -> Optional[CompetitorChannel]:
        """Get detailed information about a channel"""
        try:
            url = "https://www.googleapis.com/youtube/v3/channels"
            params = {
                'part': 'snippet,statistics',
                'id': channel_id,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if not data.get('items'):
                return None
            
            item = data['items'][0]
            stats = item['statistics']
            snippet = item['snippet']
            
            # Calculate average views (approximate)
            video_count = int(stats.get('videoCount', 1))
            view_count = int(stats.get('viewCount', 0))
            avg_views = view_count / max(video_count, 1)
            
            # Calculate upload frequency (videos per month)
            channel_age_days = (datetime.now() - datetime.strptime(snippet['publishedAt'][:10], '%Y-%m-%d')).days
            upload_frequency = (video_count / max(channel_age_days, 1)) * 30  # per month
            
            return CompetitorChannel(
                channel_id=channel_id,
                channel_name=snippet['title'],
                subscriber_count=int(stats.get('subscriberCount', 0)),
                video_count=video_count,
                avg_views=avg_views,
                upload_frequency=upload_frequency,
                discovery_method="",
                relevance_score=0.0,
                last_analyzed=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error getting channel details for {channel_id}: {e}")
            return None
    
    def _calculate_keyword_relevance(self, channel: CompetitorChannel, keyword: str) -> float:
        """Calculate relevance score based on keyword match"""
        score = 0.0
        
        # Check if keyword appears in channel name
        if keyword.lower() in channel.channel_name.lower():
            score += 0.5
        
        # Factor in subscriber count (normalized)
        subscriber_score = min(channel.subscriber_count / 100000, 1.0)  # Max score at 100k subs
        score += subscriber_score * 0.3
        
        # Factor in upload frequency
        frequency_score = min(channel.upload_frequency / 10, 1.0)  # Max score at 10 videos/month
        score += frequency_score * 0.2
        
        return score
    
    def _calculate_content_similarity(self, channel: CompetitorChannel, keywords: List[str]) -> float:
        """Calculate content similarity score"""
        # This is a simplified version - could be enhanced with NLP
        score = 0.0
        
        # Check keyword matches in channel name
        name_matches = sum(1 for keyword in keywords if keyword.lower() in channel.channel_name.lower())
        score += (name_matches / len(keywords)) * 0.4
        
        # Factor in channel metrics
        metrics_score = min((channel.avg_views / 10000) + (channel.subscriber_count / 50000), 1.0)
        score += metrics_score * 0.6
        
        return score
    
    def _calculate_trending_relevance(self, channel: CompetitorChannel) -> float:
        """Calculate relevance for trending-based discovery"""
        # Higher score for channels with good engagement
        engagement_ratio = channel.avg_views / max(channel.subscriber_count, 1)
        engagement_score = min(engagement_ratio * 100, 1.0)
        
        # Factor in upload consistency
        consistency_score = min(channel.upload_frequency / 5, 1.0)
        
        return (engagement_score * 0.7) + (consistency_score * 0.3)
    
    def _deduplicate_and_rank(self, competitors: List[CompetitorChannel]) -> List[CompetitorChannel]:
        """Remove duplicates and rank by relevance score"""
        # Remove duplicates by channel_id
        unique_competitors = {}
        for comp in competitors:
            if comp.channel_id not in unique_competitors:
                unique_competitors[comp.channel_id] = comp
            else:
                # Keep the one with higher relevance score
                if comp.relevance_score > unique_competitors[comp.channel_id].relevance_score:
                    unique_competitors[comp.channel_id] = comp
        
        # Sort by relevance score
        sorted_competitors = sorted(unique_competitors.values(), 
                                  key=lambda x: x.relevance_score, reverse=True)
        
        return sorted_competitors
    
    def get_competitor_insights(self, competitor: CompetitorChannel) -> Dict[str, Any]:
        """Get detailed insights about a competitor"""
        try:
            # Get recent videos for analysis
            recent_videos = self._get_recent_videos(competitor.channel_id)
            
            # Analyze content patterns
            content_analysis = self._analyze_content_patterns(recent_videos)
            
            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(recent_videos)
            
            return {
                'channel_info': {
                    'name': competitor.channel_name,
                    'subscribers': competitor.subscriber_count,
                    'avg_views': competitor.avg_views,
                    'upload_frequency': competitor.upload_frequency
                },
                'content_analysis': content_analysis,
                'performance_metrics': performance_metrics,
                'discovery_method': competitor.discovery_method,
                'relevance_score': competitor.relevance_score
            }
            
        except Exception as e:
            self.logger.error(f"Error getting competitor insights: {e}")
            return {}
    
    def _get_recent_videos(self, channel_id: str, max_results: int = 10) -> List[Dict]:
        """Get recent videos from a channel"""
        if not self.youtube_api_key:
            return []
            
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'channelId': channel_id,
                'type': 'video',
                'order': 'date',
                'maxResults': max_results,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            return data.get('items', [])
            
        except Exception as e:
            self.logger.error(f"Error getting recent videos: {e}")
            return []
    
    def _analyze_content_patterns(self, videos: List[Dict]) -> Dict[str, Any]:
        """Analyze content patterns from videos"""
        if not videos:
            return {}
        
        # Extract common keywords from titles
        all_titles = [video['snippet']['title'] for video in videos]
        common_keywords = self._extract_common_keywords(all_titles)
        
        # Analyze upload timing
        upload_times = [video['snippet']['publishedAt'] for video in videos]
        timing_analysis = self._analyze_upload_timing(upload_times)
        
        # Analyze title patterns
        title_patterns = self._analyze_title_patterns(all_titles)
        
        return {
            'common_keywords': common_keywords,
            'upload_timing': timing_analysis,
            'title_patterns': title_patterns,
            'video_count': len(videos)
        }
    
    def _calculate_performance_metrics(self, videos: List[Dict]) -> Dict[str, Any]:
        """Calculate performance metrics from videos"""
        if not videos:
            return {}
        
        # This would require additional API calls to get video statistics
        # For now, return basic metrics
        return {
            'recent_video_count': len(videos),
            'avg_title_length': sum(len(v['snippet']['title']) for v in videos) / len(videos),
            'upload_consistency': self._calculate_upload_consistency(videos)
        }
    
    def _extract_common_keywords(self, titles: List[str]) -> List[str]:
        """Extract common keywords from video titles"""
        word_freq = {}
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        for title in titles:
            words = re.findall(r'\b\w+\b', title.lower())
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:10]]
    
    def _analyze_upload_timing(self, upload_times: List[str]) -> Dict[str, Any]:
        """Analyze upload timing patterns"""
        if not upload_times:
            return {}
        
        # Parse timestamps and analyze patterns
        timestamps = []
        for time_str in upload_times:
            try:
                timestamp = datetime.strptime(time_str[:19], '%Y-%m-%dT%H:%M:%S')
                timestamps.append(timestamp)
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                continue
        
        if not timestamps:
            return {}
        
        # Analyze day of week and hour patterns
        days_of_week = [ts.weekday() for ts in timestamps]
        hours = [ts.hour for ts in timestamps]
        
        return {
            'most_common_day': max(set(days_of_week), key=days_of_week.count) if days_of_week else None,
            'most_common_hour': max(set(hours), key=hours.count) if hours else None,
            'upload_frequency_days': len(set(ts.date() for ts in timestamps))
        }
    
    def _analyze_title_patterns(self, titles: List[str]) -> Dict[str, Any]:
        """Analyze title patterns"""
        if not titles:
            return {}
        
        # Check for common patterns
        patterns = {
            'question_titles': sum(1 for title in titles if '?' in title),
            'number_titles': sum(1 for title in titles if any(char.isdigit() for char in title)),
            'caps_titles': sum(1 for title in titles if title.isupper()),
            'exclamation_titles': sum(1 for title in titles if '!' in title)
        }
        
        return patterns
    
    def _calculate_upload_consistency(self, videos: List[Dict]) -> float:
        """Calculate upload consistency score"""
        if len(videos) < 2:
            return 0.0
        
        # Calculate time differences between uploads
        timestamps = []
        for video in videos:
            try:
                timestamp = datetime.strptime(video['snippet']['publishedAt'][:19], '%Y-%m-%dT%H:%M:%S')
                timestamps.append(timestamp)
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                continue
        
        if len(timestamps) < 2:
            return 0.0
        
        timestamps.sort()
        differences = [(timestamps[i+1] - timestamps[i]).days for i in range(len(timestamps)-1)]
        
        # Calculate consistency (lower variance = higher consistency)
        if not differences:
            return 0.0
        
        avg_diff = sum(differences) / len(differences)
        variance = sum((d - avg_diff) ** 2 for d in differences) / len(differences)
        
        # Convert to 0-1 score (lower variance = higher score)
        consistency_score = 1 / (1 + variance / 10)
        
        return consistency_score