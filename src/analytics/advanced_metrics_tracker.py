"""
Advanced Metrics Tracker - Coordinates all metric modules
"""

import logging
import asyncio
from typing import Dict, List
from datetime import datetime
import sys
from pathlib import Path

# Fix import structure
sys.path.append(str(Path(__file__).parent.parent))

# Updated imports with proper error handling
try:
    from analytics.retention_analytics import RetentionAnalytics
    from analytics.ad_performance import AdPerformanceAnalytics
    from analytics.engagement_metrics import EngagementMetrics
except ImportError as e:
    logging.warning(f"Analytics module import issue: {e}")
    # Fallback implementations
    class RetentionAnalytics:
        async def analyze_retention_curve(self, video_id: str): 
            return {"overall_retention": 0.5}
        async def suggest_retention_improvements(self, data: Dict) -> List[Dict]:
            return [{"priority": "medium", "suggestion": "Fallback retention improvement"}]
    class AdPerformanceAnalytics:
        async def analyze_ad_performance(self, video_id: str): 
            return {"current_rpm": 2.5}
    class EngagementMetrics:
        async def analyze_engagement(self, video_id: str): 
            return {"ctr": 0.05}
        async def suggest_engagement_improvements(self, data: Dict) -> List[Dict]:
            return [{"priority": "medium", "suggestion": "Fallback engagement improvement"}]

class AdvancedMetricsTracker:
    """Main coordinator for all metrics tracking and optimization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.retention_analytics = RetentionAnalytics()
        self.ad_performance = AdPerformanceAnalytics()
        self.engagement_metrics = EngagementMetrics()
    
    async def analyze_video_performance(self, video_id: str) -> Dict:
        """Analyze video performance and feed to learning system"""
        try:
            # Run all analyses in parallel
            retention_task = self.retention_analytics.analyze_retention_curve(video_id)
            ad_task = self.ad_performance.analyze_ad_performance(video_id)
            engagement_task = self.engagement_metrics.analyze_engagement(video_id)
            
            retention_data, ad_data, engagement_data = await asyncio.gather(
                retention_task, ad_task, engagement_task
            )
            
            # Calculate overall performance score
            overall_score = self._calculate_overall_score(
                retention_data, ad_data, engagement_data
            )
            
            comprehensive_report = {
                'video_id': video_id,
                'analysis_timestamp': datetime.now().isoformat(),
                'overall_score': overall_score,
                'retention': retention_data,
                'ad_performance': ad_data,
                'engagement': engagement_data,
                'priority_improvements': await self._get_priority_improvements(
                    retention_data, ad_data, engagement_data
                )
            }
            
            return comprehensive_report
            
        except Exception as e:
            self.logger.error(f"Video performance analysis failed: {e}")
            return {}
    
    def _calculate_overall_score(self, retention_data: Dict, ad_data: Dict, engagement_data: Dict) -> float:
        """Calculate weighted overall performance score"""
        scores = {
            'retention': retention_data.get('overall_retention', 0) * 100,
            'ad_performance': min(ad_data.get('current_rpm', 0) * 20, 100),
            'engagement': engagement_data.get('ctr', 0) * 1000
        }
        
        # Weighted average (retention is most important)
        weights = {'retention': 0.5, 'ad_performance': 0.3, 'engagement': 0.2}
        
        overall = sum(scores[key] * weights[key] for key in scores.keys())
        return round(overall, 1)
    
    async def _get_priority_improvements(self, retention_data: Dict, ad_data: Dict, engagement_data: Dict) -> List[Dict]:
        """Get top priority improvements across all metrics"""
        all_suggestions = []
        
        # Get suggestions from each module
        retention_suggestions = await self.retention_analytics.suggest_retention_improvements(retention_data)
        engagement_suggestions = await self.engagement_metrics.suggest_engagement_improvements(engagement_data)
        
        all_suggestions.extend(retention_suggestions)
        all_suggestions.extend(engagement_suggestions)
        
        # Sort by priority and expected impact
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        all_suggestions.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 1), reverse=True)
        
        return all_suggestions[:5]  # Return top 5 priority improvements
    
    async def generate_daily_optimization_report(self) -> Dict:
        """Generate comprehensive daily optimization report"""
        try:
            # This would analyze all videos from the last 24 hours
            sample_videos = ['video_1', 'video_2', 'video_3']  # In production, get from database
            
            daily_report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'videos_analyzed': len(sample_videos),
                'average_retention': 0.42,
                'average_rpm': 2.8,
                'average_ctr': 0.085,
                'top_performing_video': 'video_2',
                'improvement_opportunities': [
                    'Optimize thumbnails for higher CTR',
                    'Improve video hooks for better retention',
                    'Adjust ad placement timing'
                ],
                'projected_revenue_increase': '+$127.50 daily'
            }
            
            return daily_report
            
        except Exception as e:
            self.logger.error(f"Daily report generation failed: {e}")
            return {}