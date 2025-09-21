from .adaptive_model_manager import AdaptiveModelManager
from typing import Dict, List
import logging
from datetime import datetime
import json

class EnhancedLearningSystem(AdaptiveModelManager):
    """Enhanced learning system that adapts based on video performance"""
    
    def __init__(self):
        super().__init__()
        self.performance_tracker = "video_performance.json"
        self.learning_data = self._load_learning_data()
        
    def _load_learning_data(self) -> Dict:
        """Load historical performance data"""
        try:
            with open(self.performance_tracker, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"videos": [], "patterns": {}, "successful_strategies": []}
    
    def learn_from_video_performance(self, video_data: Dict, performance_metrics: Dict):
        """Learn from video performance to improve future content"""
        learning_record = {
            "video_id": video_data.get('id'),
            "title": video_data.get('title'),
            "topic": video_data.get('topic'),
            "format_type": video_data.get('format_type'),
            "performance": performance_metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        self.learning_data["videos"].append(learning_record)
        
        # Analyze patterns
        self._analyze_performance_patterns()
        
        # Update model preferences based on performance
        self._update_model_preferences(video_data, performance_metrics)
        
        self._save_learning_data()
    
    def _analyze_performance_patterns(self):
        """Analyze patterns in successful content"""
        high_performers = [
            video for video in self.learning_data["videos"]
            if video["performance"].get("views", 0) > 1000  # Threshold for success
        ]
        
        # Analyze successful topics
        topic_performance = {}
        for video in high_performers:
            topic = video.get("topic", "unknown")
            if topic not in topic_performance:
                topic_performance[topic] = {"count": 0, "avg_views": 0}
            
            topic_performance[topic]["count"] += 1
            topic_performance[topic]["avg_views"] += video["performance"].get("views", 0)
        
        # Calculate averages
        for topic, data in topic_performance.items():
            if data["count"] > 0:
                data["avg_views"] = data["avg_views"] / data["count"]
        
        self.learning_data["patterns"]["successful_topics"] = topic_performance
    
    def get_content_recommendations(self) -> Dict:
        """Get AI-driven content recommendations based on learning"""
        patterns = self.learning_data.get("patterns", {})
        successful_topics = patterns.get("successful_topics", {})
        
        # Sort topics by performance
        sorted_topics = sorted(
            successful_topics.items(),
            key=lambda x: x[1]["avg_views"],
            reverse=True
        )
        
        recommendations = {
            "top_performing_topics": [topic for topic, _ in sorted_topics[:5]],
            "recommended_formats": self._get_format_recommendations(),
            "optimal_posting_times": self._analyze_posting_times(),
            "content_strategies": self._get_strategy_recommendations()
        }
        
        return recommendations
    
    def _save_learning_data(self):
        """Save learning data to file"""
        with open(self.performance_tracker, 'w') as f:
            json.dump(self.learning_data, f, indent=2)