import logging
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np
from pathlib import Path

class AIDataInterpreter:
    """Interprets and processes various data sources for content optimization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_cache = {}
        self.interpretation_rules = self._load_interpretation_rules()
        
    def _load_interpretation_rules(self) -> Dict:
        """Load data interpretation rules"""
        return {
            'engagement_patterns': {
                'high_engagement': {'likes_ratio': 0.05, 'comments_ratio': 0.02},
                'viral_threshold': {'views_growth': 2.0, 'share_ratio': 0.01}
            },
            'content_signals': {
                'trending_keywords': ['finance', 'money', 'investing', 'crypto', 'stocks'],
                'viral_formats': ['shorts', 'tutorials', 'reactions', 'news']
            },
            'audience_behavior': {
                'peak_hours': [18, 19, 20, 21],
                'optimal_length': {'shorts': 60, 'regular': 480}
            }
        }
    
    def interpret_analytics_data(self, analytics_data: Dict) -> Dict:
        """Interpret raw analytics data into actionable insights"""
        try:
            insights = {
                'engagement_score': self._calculate_engagement_score(analytics_data),
                'viral_potential': self._assess_viral_potential(analytics_data),
                'audience_insights': self._extract_audience_insights(analytics_data),
                'content_recommendations': self._generate_content_recommendations(analytics_data),
                'optimization_suggestions': self._suggest_optimizations(analytics_data)
            }
            
            self.logger.info(f"Interpreted analytics data with {len(insights)} insight categories")
            return insights
            
        except Exception as e:
            self.logger.error(f"Error interpreting analytics data: {e}")
            return self._get_fallback_insights()
    
    def _calculate_engagement_score(self, data: Dict) -> float:
        """Calculate overall engagement score"""
        try:
            views = data.get('views', 1)
            likes = data.get('likes', 0)
            comments = data.get('comments', 0)
            shares = data.get('shares', 0)
            
            if views == 0:
                return 0.0
            
            engagement_rate = (likes + comments * 2 + shares * 3) / views
            normalized_score = min(engagement_rate * 100, 10.0)  # Cap at 10
            
            return round(normalized_score, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating engagement score: {e}")
            return 0.0
    
    def _assess_viral_potential(self, data: Dict) -> Dict:
        """Assess the viral potential of content"""
        try:
            viral_indicators = {
                'growth_rate': self._calculate_growth_rate(data),
                'share_velocity': self._calculate_share_velocity(data),
                'comment_sentiment': self._analyze_comment_sentiment(data),
                'trending_alignment': self._check_trending_alignment(data)
            }
            
            # Calculate overall viral score
            viral_score = sum(viral_indicators.values()) / len(viral_indicators)
            viral_indicators['overall_score'] = round(viral_score, 2)
            viral_indicators['potential_level'] = self._categorize_viral_potential(viral_score)
            
            return viral_indicators
            
        except Exception as e:
            self.logger.error(f"Error assessing viral potential: {e}")
            return {'overall_score': 0.0, 'potential_level': 'low'}
    
    def _calculate_growth_rate(self, data: Dict) -> float:
        """Calculate content growth rate"""
        try:
            current_views = data.get('views', 0)
            previous_views = data.get('previous_views', 0)
            
            if previous_views == 0:
                return 1.0 if current_views > 0 else 0.0
            
            growth_rate = (current_views - previous_views) / previous_views
            return min(growth_rate, 5.0)  # Cap at 500% growth
            
        except Exception:
            return 0.0
    
    def _calculate_share_velocity(self, data: Dict) -> float:
        """Calculate how fast content is being shared"""
        try:
            shares = data.get('shares', 0)
            views = data.get('views', 1)
            time_since_publish = data.get('hours_since_publish', 1)
            
            share_rate = shares / views if views > 0 else 0
            velocity = share_rate / time_since_publish if time_since_publish > 0 else 0
            
            return min(velocity * 1000, 1.0)  # Normalize and cap
            
        except Exception:
            return 0.0
    
    def _analyze_comment_sentiment(self, data: Dict) -> float:
        """Analyze sentiment of comments"""
        try:
            comments = data.get('recent_comments', [])
            if not comments:
                return 0.5  # Neutral
            
            positive_keywords = ['great', 'amazing', 'love', 'awesome', 'perfect']
            negative_keywords = ['bad', 'terrible', 'hate', 'awful', 'worst']
            
            sentiment_scores = []
            for comment in comments[:50]:  # Analyze up to 50 recent comments
                comment_text = comment.lower()
                positive_count = sum(1 for word in positive_keywords if word in comment_text)
                negative_count = sum(1 for word in negative_keywords if word in comment_text)
                
                if positive_count + negative_count > 0:
                    sentiment = positive_count / (positive_count + negative_count)
                    sentiment_scores.append(sentiment)
            
            return np.mean(sentiment_scores) if sentiment_scores else 0.5
            
        except Exception:
            return 0.5
    
    def _check_trending_alignment(self, data: Dict) -> float:
        """Check how well content aligns with trending topics"""
        try:
            title = data.get('title', '').lower()
            description = data.get('description', '').lower()
            content_text = f"{title} {description}"
            
            trending_keywords = self.interpretation_rules['content_signals']['trending_keywords']
            keyword_matches = sum(1 for keyword in trending_keywords if keyword in content_text)
            
            alignment_score = min(keyword_matches / len(trending_keywords), 1.0)
            return alignment_score
            
        except Exception:
            return 0.0
    
    def _categorize_viral_potential(self, score: float) -> str:
        """Categorize viral potential based on score"""
        if score >= 0.8:
            return 'very_high'
        elif score >= 0.6:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        elif score >= 0.2:
            return 'low'
        else:
            return 'very_low'
    
    def _extract_audience_insights(self, data: Dict) -> Dict:
        """Extract insights about the audience"""
        try:
            return {
                'peak_engagement_hours': self._find_peak_hours(data),
                'audience_demographics': self._analyze_demographics(data),
                'content_preferences': self._identify_preferences(data),
                'retention_patterns': self._analyze_retention(data)
            }
        except Exception as e:
            self.logger.error(f"Error extracting audience insights: {e}")
            return {}
    
    def _find_peak_hours(self, data: Dict) -> List[int]:
        """Find peak engagement hours"""
        try:
            hourly_data = data.get('hourly_engagement', {})
            if not hourly_data:
                return self.interpretation_rules['audience_behavior']['peak_hours']
            
            # Sort hours by engagement and return top 4
            sorted_hours = sorted(hourly_data.items(), key=lambda x: x[1], reverse=True)
            return [int(hour) for hour, _ in sorted_hours[:4]]
            
        except Exception:
            return self.interpretation_rules['audience_behavior']['peak_hours']
    
    def _analyze_demographics(self, data: Dict) -> Dict:
        """Analyze audience demographics"""
        try:
            demographics = data.get('demographics', {})
            return {
                'primary_age_group': demographics.get('age_groups', {}).get('primary', '25-34'),
                'gender_distribution': demographics.get('gender', {'male': 60, 'female': 40}),
                'top_countries': demographics.get('countries', ['US', 'UK', 'CA'])
            }
        except Exception:
            return {
                'primary_age_group': '25-34',
                'gender_distribution': {'male': 60, 'female': 40},
                'top_countries': ['US', 'UK', 'CA']
            }
    
    def _identify_preferences(self, data: Dict) -> Dict:
        """Identify content preferences"""
        try:
            return {
                'preferred_length': self._calculate_optimal_length(data),
                'popular_topics': self._extract_popular_topics(data),
                'engagement_triggers': self._find_engagement_triggers(data)
            }
        except Exception:
            return {
                'preferred_length': 300,
                'popular_topics': ['finance', 'investing'],
                'engagement_triggers': ['questions', 'tutorials']
            }
    
    def _calculate_optimal_length(self, data: Dict) -> int:
        """Calculate optimal video length based on retention"""
        try:
            retention_data = data.get('retention_curve', [])
            if not retention_data:
                return 300  # Default 5 minutes
            
            # Find where retention drops below 50%
            for i, retention in enumerate(retention_data):
                if retention < 0.5:
                    return i * 10  # Assuming 10-second intervals
            
            return len(retention_data) * 10
            
        except Exception:
            return 300
    
    def _extract_popular_topics(self, data: Dict) -> List[str]:
        """Extract popular topics from successful content"""
        try:
            successful_videos = data.get('top_performing_videos', [])
            topics = []
            
            for video in successful_videos:
                title = video.get('title', '').lower()
                for keyword in self.interpretation_rules['content_signals']['trending_keywords']:
                    if keyword in title and keyword not in topics:
                        topics.append(keyword)
            
            return topics[:5]  # Return top 5
            
        except Exception:
            return ['finance', 'investing']
    
    def _find_engagement_triggers(self, data: Dict) -> List[str]:
        """Find what triggers high engagement"""
        try:
            high_engagement_videos = data.get('high_engagement_videos', [])
            triggers = []
            
            trigger_patterns = {
                'question': r'\?',
                'tutorial': r'how to|tutorial|guide',
                'urgent': r'now|urgent|breaking|alert',
                'personal': r'my|i |me '
            }
            
            for video in high_engagement_videos:
                title = video.get('title', '').lower()
                for trigger_name, pattern in trigger_patterns.items():
                    if re.search(pattern, title) and trigger_name not in triggers:
                        triggers.append(trigger_name)
            
            return triggers
            
        except Exception:
            return ['question', 'tutorial']
    
    def _analyze_retention(self, data: Dict) -> Dict:
        """Analyze audience retention patterns"""
        try:
            retention_data = data.get('average_retention', {})
            return {
                'average_view_duration': retention_data.get('average_duration', 180),
                'drop_off_points': retention_data.get('major_drops', [30, 120]),
                'retention_rate': retention_data.get('overall_rate', 0.45)
            }
        except Exception:
            return {
                'average_view_duration': 180,
                'drop_off_points': [30, 120],
                'retention_rate': 0.45
            }
    
    def _generate_content_recommendations(self, data: Dict) -> List[Dict]:
        """Generate content recommendations based on data"""
        try:
            recommendations = []
            
            # Analyze successful patterns
            viral_potential = self._assess_viral_potential(data)
            audience_insights = self._extract_audience_insights(data)
            
            # Generate recommendations
            if viral_potential['overall_score'] < 0.3:
                recommendations.append({
                    'type': 'engagement_boost',
                    'suggestion': 'Add more interactive elements like polls or questions',
                    'priority': 'high'
                })
            
            if audience_insights.get('retention_patterns', {}).get('retention_rate', 0) < 0.4:
                recommendations.append({
                    'type': 'retention_improvement',
                    'suggestion': 'Create stronger hooks in the first 15 seconds',
                    'priority': 'high'
                })
            
            recommendations.append({
                'type': 'trending_alignment',
                'suggestion': f"Focus on topics: {', '.join(audience_insights.get('content_preferences', {}).get('popular_topics', []))}",
                'priority': 'medium'
            })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return [{
                'type': 'general',
                'suggestion': 'Focus on trending finance topics with strong hooks',
                'priority': 'medium'
            }]
    
    def _suggest_optimizations(self, data: Dict) -> List[Dict]:
        """Suggest specific optimizations"""
        try:
            optimizations = []
            
            engagement_score = self._calculate_engagement_score(data)
            
            if engagement_score < 2.0:
                optimizations.append({
                    'area': 'title_optimization',
                    'action': 'Use more compelling titles with numbers or questions',
                    'expected_impact': 'medium'
                })
            
            if engagement_score < 1.0:
                optimizations.append({
                    'area': 'thumbnail_optimization',
                    'action': 'Create more eye-catching thumbnails with bright colors',
                    'expected_impact': 'high'
                })
            
            optimizations.append({
                'area': 'posting_schedule',
                'action': f"Post during peak hours: {self._find_peak_hours(data)}",
                'expected_impact': 'medium'
            })
            
            return optimizations
            
        except Exception as e:
            self.logger.error(f"Error suggesting optimizations: {e}")
            return []
    
    def _get_fallback_insights(self) -> Dict:
        """Return fallback insights when interpretation fails"""
        return {
            'engagement_score': 1.0,
            'viral_potential': {'overall_score': 0.3, 'potential_level': 'low'},
            'audience_insights': {
                'peak_engagement_hours': [18, 19, 20, 21],
                'content_preferences': {'popular_topics': ['finance', 'investing']}
            },
            'content_recommendations': [{
                'type': 'general',
                'suggestion': 'Focus on trending finance topics',
                'priority': 'medium'
            }],
            'optimization_suggestions': [{
                'area': 'content_quality',
                'action': 'Improve video quality and engagement',
                'expected_impact': 'medium'
            }]
        }
    
    def interpret_trend_data(self, trend_data: List[Dict]) -> Dict:
        """Interpret trending data for content strategy"""
        try:
            interpreted_trends = {
                'hot_topics': self._extract_hot_topics(trend_data),
                'emerging_trends': self._identify_emerging_trends(trend_data),
                'content_opportunities': self._find_content_opportunities(trend_data),
                'competitive_gaps': self._identify_competitive_gaps(trend_data)
            }
            
            self.logger.info(f"Interpreted {len(trend_data)} trends")
            return interpreted_trends
            
        except Exception as e:
            self.logger.error(f"Error interpreting trend data: {e}")
            return {'hot_topics': [], 'emerging_trends': [], 'content_opportunities': []}
    
    def _extract_hot_topics(self, trends: List[Dict]) -> List[Dict]:
        """Extract currently hot topics"""
        try:
            hot_topics = []
            for trend in trends[:10]:  # Top 10 trends
                hot_topics.append({
                    'topic': trend.get('keyword', ''),
                    'search_volume': trend.get('volume', 0),
                    'growth_rate': trend.get('growth', 0),
                    'competition': trend.get('competition', 'medium')
                })
            return hot_topics
        except Exception:
            return []
    
    def _identify_emerging_trends(self, trends: List[Dict]) -> List[Dict]:
        """Identify emerging trends with high growth potential"""
        try:
            emerging = []
            for trend in trends:
                growth_rate = trend.get('growth', 0)
                if growth_rate > 1.5:  # 150% growth
                    emerging.append({
                        'topic': trend.get('keyword', ''),
                        'growth_rate': growth_rate,
                        'opportunity_score': min(growth_rate * 0.5, 1.0)
                    })
            return sorted(emerging, key=lambda x: x['growth_rate'], reverse=True)[:5]
        except Exception:
            return []
    
    def _find_content_opportunities(self, trends: List[Dict]) -> List[Dict]:
        """Find content creation opportunities"""
        try:
            opportunities = []
            for trend in trends:
                competition = trend.get('competition', 'high')
                volume = trend.get('volume', 0)
                
                if competition in ['low', 'medium'] and volume > 1000:
                    opportunities.append({
                        'keyword': trend.get('keyword', ''),
                        'opportunity_type': 'low_competition_high_volume',
                        'recommended_action': 'Create content immediately',
                        'priority': 'high' if competition == 'low' else 'medium'
                    })
            
            return opportunities[:10]
        except Exception:
            return []
    
    def _identify_competitive_gaps(self, trends: List[Dict]) -> List[Dict]:
        """Identify gaps in competitive landscape"""
        try:
            gaps = []
            for trend in trends:
                if trend.get('content_saturation', 1.0) < 0.3:  # Low content saturation
                    gaps.append({
                        'topic': trend.get('keyword', ''),
                        'saturation_level': trend.get('content_saturation', 0),
                        'opportunity_size': 'large' if trend.get('volume', 0) > 5000 else 'medium'
                    })
            return gaps[:5]
        except Exception:
            return []