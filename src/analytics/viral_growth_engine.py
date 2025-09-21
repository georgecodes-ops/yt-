"""
Viral Growth Engine for Analytics - Compatible version for enhanced_main.py
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

class ViralGrowthEngine:
    """Engine for tracking and optimizing viral content performance in analytics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.viral_metrics = {}
        self.growth_patterns = []
        
    async def initialize(self):
        """Initialize the ViralGrowthEngine"""
        self.logger.info("Initializing ViralGrowthEngine for analytics...")
        return True
    
    def track_viral_performance(self, content_id: str, metrics: Dict[str, Any]) -> Dict:
        """Track viral performance metrics for content"""
        try:
            self.viral_metrics[content_id] = {
                'views': metrics.get('views', 0),
                'shares': metrics.get('shares', 0),
                'engagement_rate': metrics.get('engagement_rate', 0.0),
                'viral_score': metrics.get('viral_score', 0.0),
                'timestamp': datetime.now().isoformat()
            }
            
            return {
                'status': 'success',
                'content_id': content_id,
                'metrics': self.viral_metrics[content_id]
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking viral performance: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def analyze_growth_patterns(self, content_ids: List[str]) -> Dict:
        """Analyze growth patterns across multiple content pieces"""
        try:
            patterns = []
            for content_id in content_ids:
                if content_id in self.viral_metrics:
                    patterns.append(self.viral_metrics[content_id])
            
            return {
                'status': 'success',
                'total_analyzed': len(patterns),
                'patterns': patterns,
                'recommendations': self._generate_recommendations(patterns)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing growth patterns: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def _generate_recommendations(self, patterns: List[Dict]) -> List[str]:
        """Generate optimization recommendations based on patterns"""
        recommendations = []
        
        if patterns:
            avg_engagement = sum(p.get('engagement_rate', 0) for p in patterns) / len(patterns)
            avg_shares = sum(p.get('shares', 0) for p in patterns) / len(patterns)
            
            if avg_engagement < 0.05:
                recommendations.append("Increase engagement by improving hooks and CTAs")
            
            if avg_shares < 100:
                recommendations.append("Boost shareability with trending hashtags")
                
            recommendations.append("Monitor performance metrics daily for optimization")
        
        return recommendations
    
    def get_viral_score(self, content_id: str) -> float:
        """Get viral score for specific content"""
        return self.viral_metrics.get(content_id, {}).get('viral_score', 0.0)
    
    def reset_metrics(self) -> Dict:
        """Reset all viral metrics"""
        self.viral_metrics.clear()
        self.growth_patterns.clear()
        return {'status': 'success', 'message': 'All metrics reset'}

class ViralOptimizer:
    """Legacy class for backward compatibility"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = ViralGrowthEngine()
        
    def optimize_content(self, content_data: Dict) -> Dict:
        """Legacy optimization method"""
        return {'status': 'success', 'optimized': True}