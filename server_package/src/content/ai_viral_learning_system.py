"""
AI Viral Learning System - Advanced machine learning for viral content optimization
Integrates with MonAY's existing ML components for continuous improvement
"""

import asyncio
import json
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import pickle
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import statistics

# Import existing MonAY components with error handling
try:
    from ml.enhanced_learning_system import EnhancedLearningSystem
    from analytics.predictive_analytics import PredictiveAnalytics
    from analytics.retention_analytics import RetentionAnalytics
    from growth.viral_growth_engine import ViralGrowthEngine
    from analytics.youtube_algorithm_analyzer import YouTubeAlgorithmAnalyzer
except ImportError as e:
    import logging
    logging.warning(f"Import warning in ai_viral_learning_system: {e}")
    # Fallback classes
    class EnhancedLearningSystem:
        async def initialize(self): pass
        async def learn_from_data(self, *args, **kwargs): return {}
    class PredictiveAnalytics:
        async def predict_performance(self, *args, **kwargs): return {}
    class RetentionAnalytics:
        async def analyze_retention(self, *args, **kwargs): return {}
    class ViralGrowthEngine:
        async def optimize_growth(self, *args, **kwargs): return {}
    class YouTubeAlgorithmAnalyzer:
        async def analyze_algorithm(self, *args, **kwargs): return {}

@dataclass
class ViralPattern:
    """Represents a learned viral content pattern"""
    pattern_id: str
    content_type: str
    viral_elements: Dict[str, Any]
    performance_metrics: Dict[str, float]
    success_rate: float
    confidence_score: float
    last_updated: datetime
    usage_count: int = 0

@dataclass
class LearningSession:
    """Represents a learning session from content performance"""
    session_id: str
    content_data: Dict[str, Any]
    performance_data: Dict[str, float]
    extracted_patterns: List[str]
    learning_score: float
    timestamp: datetime

class AIViralLearningSystem:
    """Advanced AI system that learns from viral content patterns and optimizes future content"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_dir = Path("data/ai_learning")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Core learning components
        self.viral_patterns: Dict[str, ViralPattern] = {}
        self.learning_history: deque = deque(maxlen=1000)
        self.performance_memory: Dict[str, List[float]] = defaultdict(list)
        
        # Learning parameters
        self.learning_rate = 0.1
        self.pattern_threshold = 0.7
        self.confidence_threshold = 0.8
        self.max_patterns = 500
        
        # Integration with existing systems
        self.enhanced_learning = None
        self.predictive_analytics = None
        self.retention_analytics = None
        self.viral_growth_engine = None
        self.algorithm_analyzer = None
        
        # Performance tracking
        self.learning_metrics = {
            'patterns_learned': 0,
            'successful_predictions': 0,
            'total_predictions': 0,
            'accuracy_rate': 0.0,
            'last_learning_session': None
        }
        
        self.load_learning_data()
    
    async def initialize(self):
        """Initialize the AI Viral Learning System"""
        self.logger.info("Initializing AI Viral Learning System...")
        try:
            await self.initialize_integrations()
            self.logger.info("AI Viral Learning System initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize AI Viral Learning System: {e}")
            return False
    
    async def initialize_integrations(self):
        """Initialize connections to other MonAY systems"""
        try:
            self.enhanced_learning = EnhancedLearningSystem()
            self.predictive_analytics = PredictiveAnalytics()
            self.retention_analytics = RetentionAnalytics()
            self.viral_growth_engine = ViralGrowthEngine()
            self.algorithm_analyzer = YouTubeAlgorithmAnalyzer()
            
            self.logger.info("AI Viral Learning System integrations initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize integrations: {e}")
    
    def load_learning_data(self):
        """Load previously learned patterns and data"""
        try:
            patterns_file = self.data_dir / "viral_patterns.pkl"
            if patterns_file.exists():
                with open(patterns_file, 'rb') as f:
                    self.viral_patterns = pickle.load(f)
            
            metrics_file = self.data_dir / "learning_metrics.json"
            if metrics_file.exists():
                with open(metrics_file, 'r') as f:
                    self.learning_metrics.update(json.load(f))
            
            self.logger.info(f"Loaded {len(self.viral_patterns)} viral patterns")
        except Exception as e:
            self.logger.error(f"Failed to load learning data: {e}")
    
    def save_learning_data(self):
        """Save learned patterns and metrics"""
        try:
            patterns_file = self.data_dir / "viral_patterns.pkl"
            with open(patterns_file, 'wb') as f:
                pickle.dump(self.viral_patterns, f)
            
            metrics_file = self.data_dir / "learning_metrics.json"
            with open(metrics_file, 'w') as f:
                json.dump(self.learning_metrics, f, default=str, indent=2)
            
            self.logger.info("Learning data saved successfully")
        except Exception as e:
            self.logger.error(f"Failed to save learning data: {e}")
    
    async def learn_from_content_performance(self, content_data: Dict[str, Any],
                                           performance_data: Dict[str, float]) -> Optional[LearningSession]:
        """Learn from content performance and extract viral patterns"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Extract key performance indicators
            viral_score = self._calculate_viral_score(performance_data)
            
            # Only learn from high-performing content
            if viral_score >= self.pattern_threshold:
                patterns = await self._extract_viral_patterns(content_data, performance_data)
                
                # Update existing patterns or create new ones
                for pattern in patterns:
                    await self._update_pattern_knowledge(pattern, performance_data)
                
                learning_score = len(patterns) * viral_score
                self.learning_metrics['patterns_learned'] += len(patterns)
            else:
                patterns = []
                learning_score = 0.0
            
            # Create learning session
            session = LearningSession(
                session_id=session_id,
                content_data=content_data,
                performance_data=performance_data,
                extracted_patterns=[p.pattern_id for p in patterns],
                learning_score=learning_score,
                timestamp=datetime.now()
            )
            
            self.learning_history.append(session)
            self.learning_metrics['last_learning_session'] = datetime.now()
            
            # Update performance memory
            content_type = content_data.get('type', 'unknown')
            self.performance_memory[content_type].append(viral_score)
            
            self.logger.info(f"Learning session completed: {len(patterns)} patterns extracted")
            return session
            
        except Exception as e:
            self.logger.error(f"Failed to learn from content performance: {e}")
            return None
    
    def _calculate_viral_score(self, performance_data: Dict[str, float]) -> float:
        """Calculate viral score based on performance metrics"""
        try:
            # Weighted viral score calculation
            weights = {
                'views': 0.25,
                'engagement_rate': 0.20,
                'retention_rate': 0.15,
                'ctr': 0.15,
                'shares': 0.10,
                'comments': 0.10,
                'viral_coefficient': 0.05
            }
            
            score = 0.0
            total_weight = 0.0
            
            for metric, weight in weights.items():
                if metric in performance_data:
                    # Normalize metrics to 0-1 scale
                    normalized_value = min(performance_data[metric] / 100.0, 1.0)
                    score += normalized_value * weight
                    total_weight += weight
            
            return score / total_weight if total_weight > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate viral score: {e}")
            return 0.0
    
    async def _extract_viral_patterns(self, content_data: Dict[str, Any], 
                                    performance_data: Dict[str, float]) -> List[ViralPattern]:
        """Extract viral patterns from high-performing content"""
        patterns = []
        
        try:
            # Title patterns
            if 'title' in content_data:
                title_pattern = await self._analyze_title_pattern(content_data['title'], performance_data)
                if title_pattern:
                    patterns.append(title_pattern)
            
            # Thumbnail patterns
            if 'thumbnail_data' in content_data:
                thumbnail_pattern = await self._analyze_thumbnail_pattern(content_data['thumbnail_data'], performance_data)
                if thumbnail_pattern:
                    patterns.append(thumbnail_pattern)
            
            # Content structure patterns
            if 'structure' in content_data:
                structure_pattern = await self._analyze_structure_pattern(content_data['structure'], performance_data)
                if structure_pattern:
                    patterns.append(structure_pattern)
            
            # Timing patterns
            if 'upload_time' in content_data:
                timing_pattern = await self._analyze_timing_pattern(content_data['upload_time'], performance_data)
                if timing_pattern:
                    patterns.append(timing_pattern)
            
            # Topic patterns
            if 'topics' in content_data:
                topic_pattern = await self._analyze_topic_pattern(content_data['topics'], performance_data)
                if topic_pattern:
                    patterns.append(topic_pattern)
            
            return patterns
            
        except Exception as e:
            self.logger.error(f"Failed to extract viral patterns: {e}")
            return []
    
    async def _analyze_title_pattern(self, title: str, performance_data: Dict[str, float]) -> Optional[ViralPattern]:
        """Analyze title patterns for viral elements"""
        try:
            viral_elements = {
                'length': len(title),
                'word_count': len(title.split()),
                'has_numbers': any(char.isdigit() for char in title),
                'has_caps': any(char.isupper() for char in title),
                'has_question': '?' in title,
                'has_exclamation': '!' in title,
                'urgency_words': sum(1 for word in ['NOW', 'URGENT', 'BREAKING', 'INSTANT'] if word in title.upper()),
                'emotion_words': sum(1 for word in ['AMAZING', 'SHOCKING', 'INCREDIBLE', 'UNBELIEVABLE'] if word in title.upper())
            }
            
            pattern_id = f"title_{hash(str(viral_elements)) % 10000}"
            
            return ViralPattern(
                pattern_id=pattern_id,
                content_type='title',
                viral_elements=viral_elements,
                performance_metrics=performance_data.copy(),
                success_rate=self._calculate_viral_score(performance_data),
                confidence_score=0.8,
                last_updated=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze title pattern: {e}")
            return None
    
    async def _analyze_thumbnail_pattern(self, thumbnail_data: Dict[str, Any], 
                                       performance_data: Dict[str, float]) -> Optional[ViralPattern]:
        """Analyze thumbnail patterns for viral elements"""
        try:
            viral_elements = {
                'has_face': thumbnail_data.get('has_face', False),
                'face_emotion': thumbnail_data.get('face_emotion', 'neutral'),
                'color_scheme': thumbnail_data.get('dominant_colors', []),
                'text_overlay': thumbnail_data.get('has_text', False),
                'contrast_level': thumbnail_data.get('contrast', 0.5),
                'brightness': thumbnail_data.get('brightness', 0.5)
            }
            
            pattern_id = f"thumbnail_{hash(str(viral_elements)) % 10000}"
            
            return ViralPattern(
                pattern_id=pattern_id,
                content_type='thumbnail',
                viral_elements=viral_elements,
                performance_metrics=performance_data.copy(),
                success_rate=self._calculate_viral_score(performance_data),
                confidence_score=0.7,
                last_updated=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze thumbnail pattern: {e}")
            return None
    
    async def _analyze_structure_pattern(self, structure: Dict[str, Any], 
                                       performance_data: Dict[str, float]) -> Optional[ViralPattern]:
        """Analyze content structure patterns"""
        try:
            viral_elements = {
                'hook_duration': structure.get('hook_duration', 0),
                'total_duration': structure.get('total_duration', 0),
                'segment_count': len(structure.get('segments', [])),
                'has_cliffhanger': structure.get('has_cliffhanger', False),
                'pacing_score': structure.get('pacing_score', 0.5),
                'engagement_peaks': len(structure.get('engagement_peaks', []))
            }
            
            pattern_id = f"structure_{hash(str(viral_elements)) % 10000}"
            
            return ViralPattern(
                pattern_id=pattern_id,
                content_type='structure',
                viral_elements=viral_elements,
                performance_metrics=performance_data.copy(),
                success_rate=self._calculate_viral_score(performance_data),
                confidence_score=0.9,
                last_updated=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze structure pattern: {e}")
            return None
    
    async def _analyze_timing_pattern(self, upload_time: datetime, 
                                    performance_data: Dict[str, float]) -> Optional[ViralPattern]:
        """Analyze upload timing patterns"""
        try:
            viral_elements = {
                'hour': upload_time.hour,
                'day_of_week': upload_time.weekday(),
                'is_weekend': upload_time.weekday() >= 5,
                'is_prime_time': 18 <= upload_time.hour <= 22,
                'month': upload_time.month,
                'season': (upload_time.month % 12 + 3) // 3
            }
            
            pattern_id = f"timing_{hash(str(viral_elements)) % 10000}"
            
            return ViralPattern(
                pattern_id=pattern_id,
                content_type='timing',
                viral_elements=viral_elements,
                performance_metrics=performance_data.copy(),
                success_rate=self._calculate_viral_score(performance_data),
                confidence_score=0.6,
                last_updated=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze timing pattern: {e}")
            return None
    
    async def _analyze_topic_pattern(self, topics: List[str], 
                                   performance_data: Dict[str, float]) -> Optional[ViralPattern]:
        """Analyze topic patterns for viral potential"""
        try:
            viral_elements = {
                'primary_topic': topics[0] if topics else 'unknown',
                'topic_count': len(topics),
                'trending_topics': sum(1 for topic in topics if self._is_trending_topic(topic)),
                'evergreen_topics': sum(1 for topic in topics if self._is_evergreen_topic(topic)),
                'niche_specificity': self._calculate_niche_specificity(topics)
            }
            
            pattern_id = f"topic_{hash(str(viral_elements)) % 10000}"
            
            return ViralPattern(
                pattern_id=pattern_id,
                content_type='topic',
                viral_elements=viral_elements,
                performance_metrics=performance_data.copy(),
                success_rate=self._calculate_viral_score(performance_data),
                confidence_score=0.8,
                last_updated=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze topic pattern: {e}")
            return None
    
    def _is_trending_topic(self, topic: str) -> bool:
        """Check if topic is currently trending"""
        trending_keywords = ['AI', 'crypto', 'finance', 'investing', 'money', 'wealth', 'passive income']
        return any(keyword.lower() in topic.lower() for keyword in trending_keywords)
    
    def _is_evergreen_topic(self, topic: str) -> bool:
        """Check if topic is evergreen"""
        evergreen_keywords = ['how to', 'tutorial', 'guide', 'tips', 'basics', 'beginner']
        return any(keyword.lower() in topic.lower() for keyword in evergreen_keywords)
    
    def _calculate_niche_specificity(self, topics: List[str]) -> float:
        """Calculate how niche-specific the topics are"""
        if not topics:
            return 0.0
        
        # Simple heuristic: longer, more specific topics are more niche
        avg_length = sum(len(topic.split()) for topic in topics) / len(topics)
        return min(avg_length / 5.0, 1.0)  # Normalize to 0-1
    
    async def _update_pattern_knowledge(self, pattern: ViralPattern, performance_data: Dict[str, float]):
        """Update existing pattern knowledge or add new pattern"""
        try:
            if pattern.pattern_id in self.viral_patterns:
                # Update existing pattern
                existing = self.viral_patterns[pattern.pattern_id]
                existing.usage_count += 1
                
                # Update success rate with exponential moving average
                new_success = self._calculate_viral_score(performance_data)
                existing.success_rate = (existing.success_rate * 0.8) + (new_success * 0.2)
                
                # Update confidence based on usage
                existing.confidence_score = min(existing.confidence_score + 0.1, 1.0)
                existing.last_updated = datetime.now()
                
                # Update performance metrics
                for metric, value in performance_data.items():
                    if metric in existing.performance_metrics:
                        existing.performance_metrics[metric] = (existing.performance_metrics[metric] * 0.7) + (value * 0.3)
                    else:
                        existing.performance_metrics[metric] = value
            else:
                # Add new pattern
                if len(self.viral_patterns) >= self.max_patterns:
                    # Remove least successful pattern
                    worst_pattern = min(self.viral_patterns.values(), key=lambda p: p.success_rate)
                    del self.viral_patterns[worst_pattern.pattern_id]
                
                self.viral_patterns[pattern.pattern_id] = pattern
            
        except Exception as e:
            self.logger.error(f"Failed to update pattern knowledge: {e}")
    
    async def predict_viral_potential(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict viral potential of content based on learned patterns"""
        try:
            predictions = {
                'overall_score': 0.0,
                'confidence': 0.0,
                'matching_patterns': [],
                'recommendations': [],
                'risk_factors': []
            }
            
            matching_patterns = []
            total_score = 0.0
            total_confidence = 0.0
            
            # Check against learned patterns
            for pattern in self.viral_patterns.values():
                match_score = await self._calculate_pattern_match(content_data, pattern)
                
                if match_score > 0.5:  # Significant match
                    matching_patterns.append({
                        'pattern_id': pattern.pattern_id,
                        'content_type': pattern.content_type,
                        'match_score': match_score,
                        'success_rate': pattern.success_rate,
                        'confidence': pattern.confidence_score
                    })
                    
                    weighted_score = match_score * pattern.success_rate * pattern.confidence_score
                    total_score += weighted_score
                    total_confidence += pattern.confidence_score
            
            if matching_patterns:
                predictions['overall_score'] = total_score / len(matching_patterns)
                predictions['confidence'] = total_confidence / len(matching_patterns)
                predictions['matching_patterns'] = sorted(matching_patterns, 
                                                        key=lambda x: x['match_score'], reverse=True)
            
            # Generate recommendations
            predictions['recommendations'] = await self._generate_recommendations(content_data, matching_patterns)
            
            # Identify risk factors
            predictions['risk_factors'] = await self._identify_risk_factors(content_data)
            
            self.learning_metrics['total_predictions'] += 1
            
            return predictions
            
        except Exception as e:
            self.logger.error(f"Failed to predict viral potential: {e}")
            return {'overall_score': 0.0, 'confidence': 0.0, 'error': str(e)}
    
    async def _calculate_pattern_match(self, content_data: Dict[str, Any], pattern: ViralPattern) -> float:
        """Calculate how well content matches a learned pattern"""
        try:
            if pattern.content_type == 'title' and 'title' in content_data:
                return self._match_title_pattern(content_data['title'], pattern.viral_elements)
            elif pattern.content_type == 'thumbnail' and 'thumbnail_data' in content_data:
                return self._match_thumbnail_pattern(content_data['thumbnail_data'], pattern.viral_elements)
            elif pattern.content_type == 'structure' and 'structure' in content_data:
                return self._match_structure_pattern(content_data['structure'], pattern.viral_elements)
            elif pattern.content_type == 'timing' and 'upload_time' in content_data:
                return self._match_timing_pattern(content_data['upload_time'], pattern.viral_elements)
            elif pattern.content_type == 'topic' and 'topics' in content_data:
                return self._match_topic_pattern(content_data['topics'], pattern.viral_elements)
            
            return 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate pattern match: {e}")
            return 0.0
    
    def _match_title_pattern(self, title: str, pattern_elements: Dict[str, Any]) -> float:
        """Match title against learned pattern"""
        try:
            current_elements = {
                'length': len(title),
                'word_count': len(title.split()),
                'has_numbers': any(char.isdigit() for char in title),
                'has_caps': any(char.isupper() for char in title),
                'has_question': '?' in title,
                'has_exclamation': '!' in title,
                'urgency_words': sum(1 for word in ['NOW', 'URGENT', 'BREAKING', 'INSTANT'] if word in title.upper()),
                'emotion_words': sum(1 for word in ['AMAZING', 'SHOCKING', 'INCREDIBLE', 'UNBELIEVABLE'] if word in title.upper())
            }
            
            matches = 0
            total = 0
            
            for key, pattern_value in pattern_elements.items():
                if key in current_elements:
                    current_value = current_elements[key]
                    
                    if isinstance(pattern_value, bool):
                        matches += 1 if current_value == pattern_value else 0
                    elif isinstance(pattern_value, (int, float)):
                        # Allow 20% variance for numeric values
                        variance = abs(current_value - pattern_value) / max(pattern_value, 1)
                        matches += max(0, 1 - variance / 0.2)
                    
                    total += 1
            
            return matches / total if total > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to match title pattern: {e}")
            return 0.0
    
    def _match_thumbnail_pattern(self, thumbnail_data: Dict[str, Any], pattern_elements: Dict[str, Any]) -> float:
        """Match thumbnail against learned pattern"""
        try:
            matches = 0
            total = 0
            
            for key, pattern_value in pattern_elements.items():
                if key in thumbnail_data:
                    current_value = thumbnail_data[key]
                    
                    if isinstance(pattern_value, bool):
                        matches += 1 if current_value == pattern_value else 0
                    elif isinstance(pattern_value, str):
                        matches += 1 if current_value == pattern_value else 0
                    elif isinstance(pattern_value, (int, float)):
                        variance = abs(current_value - pattern_value) / max(pattern_value, 1)
                        matches += max(0, 1 - variance / 0.3)
                    
                    total += 1
            
            return matches / total if total > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to match thumbnail pattern: {e}")
            return 0.0
    
    def _match_structure_pattern(self, structure: Dict[str, Any], pattern_elements: Dict[str, Any]) -> float:
        """Match content structure against learned pattern"""
        try:
            matches = 0
            total = 0
            
            for key, pattern_value in pattern_elements.items():
                if key == 'hook_duration' and 'hook_duration' in structure:
                    variance = abs(structure['hook_duration'] - pattern_value) / max(pattern_value, 1)
                    matches += max(0, 1 - variance / 0.5)
                elif key == 'total_duration' and 'total_duration' in structure:
                    variance = abs(structure['total_duration'] - pattern_value) / max(pattern_value, 1)
                    matches += max(0, 1 - variance / 0.3)
                elif key == 'segment_count' and 'segments' in structure:
                    current_count = len(structure['segments'])
                    variance = abs(current_count - pattern_value) / max(pattern_value, 1)
                    matches += max(0, 1 - variance / 0.4)
                elif key in structure:
                    if isinstance(pattern_value, bool):
                        matches += 1 if structure[key] == pattern_value else 0
                    elif isinstance(pattern_value, (int, float)):
                        variance = abs(structure[key] - pattern_value) / max(pattern_value, 1)
                        matches += max(0, 1 - variance / 0.3)
                
                total += 1
            
            return matches / total if total > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to match structure pattern: {e}")
            return 0.0
    
    def _match_timing_pattern(self, upload_time: datetime, pattern_elements: Dict[str, Any]) -> float:
        """Match upload timing against learned pattern"""
        try:
            current_elements = {
                'hour': upload_time.hour,
                'day_of_week': upload_time.weekday(),
                'is_weekend': upload_time.weekday() >= 5,
                'is_prime_time': 18 <= upload_time.hour <= 22,
                'month': upload_time.month,
                'season': (upload_time.month % 12 + 3) // 3
            }
            
            matches = 0
            total = 0
            
            for key, pattern_value in pattern_elements.items():
                if key in current_elements:
                    current_value = current_elements[key]
                    
                    if isinstance(pattern_value, bool):
                        matches += 1 if current_value == pattern_value else 0
                    elif key == 'hour':
                        # Allow 2-hour variance for timing
                        hour_diff = min(abs(current_value - pattern_value), 
                                      24 - abs(current_value - pattern_value))
                        matches += max(0, 1 - hour_diff / 2)
                    elif isinstance(pattern_value, int):
                        matches += 1 if current_value == pattern_value else 0
                    
                    total += 1
            
            return matches / total if total > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to match timing pattern: {e}")
            return 0.0
    
    def _match_topic_pattern(self, topics: List[str], pattern_elements: Dict[str, Any]) -> float:
        """Match topics against learned pattern"""
        try:
            current_elements = {
                'primary_topic': topics[0] if topics else 'unknown',
                'topic_count': len(topics),
                'trending_topics': sum(1 for topic in topics if self._is_trending_topic(topic)),
                'evergreen_topics': sum(1 for topic in topics if self._is_evergreen_topic(topic)),
                'niche_specificity': self._calculate_niche_specificity(topics)
            }
            
            matches = 0
            total = 0
            
            for key, pattern_value in pattern_elements.items():
                if key in current_elements:
                    current_value = current_elements[key]
                    
                    if key == 'primary_topic':
                        matches += 1 if current_value == pattern_value else 0
                    elif isinstance(pattern_value, (int, float)):
                        variance = abs(current_value - pattern_value) / max(pattern_value, 1)
                        matches += max(0, 1 - variance / 0.5)
                    
                    total += 1
            
            return matches / total if total > 0 else 0.0
            
        except Exception as e:
            self.logger.error(f"Failed to match topic pattern: {e}")
            return 0.0
    
    async def _generate_recommendations(self, content_data: Dict[str, Any], 
                                      matching_patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on learned patterns"""
        recommendations = []
        
        try:
            # Analyze what's missing from high-performing patterns
            if 'title' in content_data:
                title_recs = self._get_title_recommendations(content_data['title'], matching_patterns)
                recommendations.extend(title_recs)
            
            if 'thumbnail_data' in content_data:
                thumbnail_recs = self._get_thumbnail_recommendations(content_data['thumbnail_data'], matching_patterns)
                recommendations.extend(thumbnail_recs)
            
            # General recommendations based on top patterns
            top_patterns = sorted(self.viral_patterns.values(), key=lambda p: p.success_rate, reverse=True)[:5]
            for pattern in top_patterns:
                if pattern.success_rate > 0.8:
                    recommendations.append(f"Consider applying {pattern.content_type} strategy with {pattern.success_rate:.1%} success rate")
            
            return recommendations[:10]  # Limit to top 10 recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to generate recommendations: {e}")
            return []
    
    def _get_title_recommendations(self, title: str, matching_patterns: List[Dict[str, Any]]) -> List[str]:
        """Get title-specific recommendations"""
        recommendations = []
        
        try:
            # Check title length
            if len(title) < 40:
                recommendations.append("Consider making title longer (40-60 characters optimal)")
            elif len(title) > 70:
                recommendations.append("Consider shortening title (40-60 characters optimal)")
            
            # Check for viral elements
            if not any(char.isdigit() for char in title):
                recommendations.append("Consider adding numbers to title for higher engagement")
            
            if '?' not in title and '!' not in title:
                recommendations.append("Consider adding question marks or exclamation points for emotional impact")
            
            # Check for urgency/emotion words
            urgency_words = ['NOW', 'URGENT', 'BREAKING', 'INSTANT']
            if not any(word in title.upper() for word in urgency_words):
                recommendations.append("Consider adding urgency words like 'NOW' or 'INSTANT'")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to get title recommendations: {e}")
            return []
    
    def _get_thumbnail_recommendations(self, thumbnail_data: Dict[str, Any], 
                                     matching_patterns: List[Dict[str, Any]]) -> List[str]:
        """Get thumbnail-specific recommendations"""
        recommendations = []
        
        try:
            if not thumbnail_data.get('has_face', False):
                recommendations.append("Consider adding a face to thumbnail for higher CTR")
            
            if thumbnail_data.get('contrast', 0.5) < 0.7:
                recommendations.append("Increase thumbnail contrast for better visibility")
            
            if not thumbnail_data.get('has_text', False):
                recommendations.append("Consider adding text overlay to thumbnail")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Failed to get thumbnail recommendations: {e}")
            return []
    
    async def _identify_risk_factors(self, content_data: Dict[str, Any]) -> List[str]:
        """Identify potential risk factors that might hurt viral potential"""
        risk_factors = []
        
        try:
            # Title risks
            if 'title' in content_data:
                title = content_data['title']
                if len(title) > 100:
                    risk_factors.append("Title too long - may be truncated in search results")
                if title.isupper():
                    risk_factors.append("All-caps title may appear spammy")
            
            # Timing risks
            if 'upload_time' in content_data:
                upload_time = content_data['upload_time']
                if upload_time.hour < 6 or upload_time.hour > 23:
                    risk_factors.append("Upload time outside optimal hours (6 AM - 11 PM)")
            
            # Content structure risks
            if 'structure' in content_data:
                structure = content_data['structure']
                if structure.get('total_duration', 0) > 1200:  # 20 minutes
                    risk_factors.append("Video too long - may hurt retention rate")
                if structure.get('hook_duration', 0) > 30:
                    risk_factors.append("Hook too long - viewers may lose interest")
            
            return risk_factors
            
        except Exception as e:
            self.logger.error(f"Failed to identify risk factors: {e}")
            return []
    
    async def optimize_content_for_virality(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize content based on learned viral patterns"""
        try:
            # Get viral potential prediction
            prediction = await self.predict_viral_potential(content_data)
            
            optimized_content = content_data.copy()
            optimization_log = []
            
            # Apply optimizations based on top patterns
            if prediction['overall_score'] < 0.7:  # Needs optimization
                # Title optimization
                if 'title' in optimized_content:
                    optimized_title = await self._optimize_title(optimized_content['title'])
                    if optimized_title != optimized_content['title']:
                        optimized_content['title'] = optimized_title
                        optimization_log.append("Title optimized for viral potential")
                
                # Thumbnail optimization suggestions
                if 'thumbnail_data' in optimized_content:
                    thumbnail_suggestions = await self._optimize_thumbnail(optimized_content['thumbnail_data'])
                    optimized_content['thumbnail_suggestions'] = thumbnail_suggestions
                    optimization_log.append("Thumbnail optimization suggestions added")
                
                # Structure optimization
                if 'structure' in optimized_content:
                    optimized_structure = await self._optimize_structure(optimized_content['structure'])
                    optimized_content['structure'] = optimized_structure
                    optimization_log.append("Content structure optimized")
            
            return {
                'optimized_content': optimized_content,
                'optimization_log': optimization_log,
                'viral_prediction': prediction,
                'improvement_score': prediction['overall_score']
            }
            
        except Exception as e:
            self.logger.error(f"Failed to optimize content for virality: {e}")
            return {'error': str(e)}
    
    async def _optimize_title(self, title: str) -> str:
        """Optimize title based on learned patterns"""
        try:
            optimized = title
            
            # Find best performing title patterns
            title_patterns = [p for p in self.viral_patterns.values() 
                            if p.content_type == 'title' and p.success_rate > 0.8]
            
            if title_patterns:
                best_pattern = max(title_patterns, key=lambda p: p.success_rate)
                elements = best_pattern.viral_elements
                
                # Apply optimizations
                if elements.get('has_numbers', False) and not any(char.isdigit() for char in optimized):
                    # Add a number if high-performing patterns have them
                    optimized = f"7 {optimized}" if not optimized.startswith(('How', 'Why', 'What')) else optimized
                
                if elements.get('has_question', False) and '?' not in optimized:
                    # Convert to question if beneficial
                    if optimized.startswith(('How', 'Why', 'What', 'When', 'Where')):
                        optimized = optimized.rstrip('.') + '?'
                
                if elements.get('urgency_words', 0) > 0 and not any(word in optimized.upper() for word in ['NOW', 'URGENT', 'INSTANT']):
                    # Add urgency if pattern shows it works
                    optimized = f"{optimized} (MUST WATCH)"
            
            return optimized
            
        except Exception as e:
            self.logger.error(f"Failed to optimize title: {e}")
            return title
    
    async def _optimize_thumbnail(self, thumbnail_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate thumbnail optimization suggestions"""
        suggestions = {}
        
        try:
            # Find best performing thumbnail patterns
            thumbnail_patterns = [p for p in self.viral_patterns.values() 
                                if p.content_type == 'thumbnail' and p.success_rate > 0.8]
            
            if thumbnail_patterns:
                best_pattern = max(thumbnail_patterns, key=lambda p: p.success_rate)
                elements = best_pattern.viral_elements
                
                if elements.get('has_face', False) and not thumbnail_data.get('has_face', False):
                    suggestions['add_face'] = "Add a human face for higher engagement"
                
                if elements.get('has_text', False) and not thumbnail_data.get('has_text', False):
                    suggestions['add_text'] = "Add text overlay for clarity"
                
                if elements.get('contrast_level', 0.5) > 0.8:
                    suggestions['increase_contrast'] = "Increase contrast for better visibility"
                
                if elements.get('face_emotion') == 'surprised' and thumbnail_data.get('face_emotion') != 'surprised':
                    suggestions['emotion'] = "Consider surprised facial expression for higher CTR"
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Failed to optimize thumbnail: {e}")
            return {}
    
    async def _optimize_structure(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize content structure based on learned patterns"""
        try:
            optimized = structure.copy()
            
            # Find best performing structure patterns
            structure_patterns = [p for p in self.viral_patterns.values() 
                                if p.content_type == 'structure' and p.success_rate > 0.8]
            
            if structure_patterns:
                best_pattern = max(structure_patterns, key=lambda p: p.success_rate)
                elements = best_pattern.viral_elements
                
                # Optimize hook duration
                optimal_hook = elements.get('hook_duration', 15)
                if abs(optimized.get('hook_duration', 0) - optimal_hook) > 5:
                    optimized['suggested_hook_duration'] = optimal_hook
                
                # Optimize total duration
                optimal_duration = elements.get('total_duration', 600)
                if abs(optimized.get('total_duration', 0) - optimal_duration) > 120:
                    optimized['suggested_total_duration'] = optimal_duration
                
                # Add engagement peaks if missing
                if elements.get('engagement_peaks', 0) > optimized.get('engagement_peaks', 0):
                    optimized['suggested_engagement_peaks'] = elements['engagement_peaks']
            
            return optimized
            
        except Exception as e:
            self.logger.error(f"Failed to optimize structure: {e}")
            return structure
    
    async def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from the learning system"""
        try:
            insights = {
                'total_patterns': len(self.viral_patterns),
                'learning_metrics': self.learning_metrics.copy(),
                'top_patterns': [],
                'performance_trends': {},
                'recommendations': []
            }
            
            # Get top performing patterns
            top_patterns = sorted(self.viral_patterns.values(), 
                                key=lambda p: p.success_rate, reverse=True)[:10]
            
            for pattern in top_patterns:
                insights['top_patterns'].append({
                    'pattern_id': pattern.pattern_id,
                    'content_type': pattern.content_type,
                    'success_rate': pattern.success_rate,
                    'confidence_score': pattern.confidence_score,
                    'usage_count': pattern.usage_count,
                    'key_elements': list(pattern.viral_elements.keys())[:5]
                })
            
            # Calculate performance trends
            for content_type, scores in self.performance_memory.items():
                if len(scores) >= 5:
                    recent_avg = statistics.mean(scores[-5:])
                    overall_avg = statistics.mean(scores)
                    insights['performance_trends'][content_type] = {
                        'recent_average': recent_avg,
                        'overall_average': overall_avg,
                        'trend': 'improving' if recent_avg > overall_avg else 'declining',
                        'sample_size': len(scores)
                    }
            
            # Generate system recommendations
            if self.learning_metrics['total_predictions'] > 0:
                accuracy = self.learning_metrics['successful_predictions'] / self.learning_metrics['total_predictions']
                if accuracy < 0.7:
                    insights['recommendations'].append("System needs more training data for better accuracy")
                if len(self.viral_patterns) < 50:
                    insights['recommendations'].append("Collect more viral content examples to improve pattern recognition")
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Failed to get learning insights: {e}")
            return {'error': str(e)}
    
    async def export_learned_patterns(self, file_path: str = None) -> Optional[str]:
        """Export learned patterns to file"""
        try:
            if not file_path:
                file_path = self.data_dir / f"patterns_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'total_patterns': len(self.viral_patterns),
                'learning_metrics': self.learning_metrics,
                'patterns': []
            }
            
            for pattern in self.viral_patterns.values():
                pattern_dict = asdict(pattern)
                pattern_dict['last_updated'] = pattern_dict['last_updated'].isoformat()
                export_data['patterns'].append(pattern_dict)
            
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            self.logger.info(f"Patterns exported to {file_path}")
            return str(file_path)
            
        except Exception as e:
            self.logger.error(f"Failed to export patterns: {e}")
            return None
    
    async def import_learned_patterns(self, file_path: str) -> bool:
        """Import learned patterns from file"""
        try:
            with open(file_path, 'r') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for pattern_dict in import_data.get('patterns', []):
                pattern_dict['last_updated'] = datetime.fromisoformat(pattern_dict['last_updated'])
                pattern = ViralPattern(**pattern_dict)
                
                # Only import if better than existing or new
                if (pattern.pattern_id not in self.viral_patterns or 
                    pattern.success_rate > self.viral_patterns[pattern.pattern_id].success_rate):
                    self.viral_patterns[pattern.pattern_id] = pattern
                    imported_count += 1
            
            self.logger.info(f"Imported {imported_count} patterns from {file_path}")
            self.save_learning_data()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import patterns: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            'status': 'active',
            'total_patterns': len(self.viral_patterns),
            'learning_metrics': self.learning_metrics,
            'memory_usage': len(self.learning_history),
            'last_save': datetime.now().isoformat(),
            'integrations_active': all([
                self.enhanced_learning is not None,
                self.predictive_analytics is not None,
                self.retention_analytics is not None,
                self.viral_growth_engine is not None,
                self.algorithm_analyzer is not None
            ])
        }
    
    async def cleanup_old_patterns(self, days_old: int = 30):
        """Clean up old, low-performing patterns"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            removed_count = 0
            
            patterns_to_remove = []
            for pattern_id, pattern in self.viral_patterns.items():
                if (pattern.last_updated < cutoff_date and 
                    pattern.success_rate < 0.5 and 
                    pattern.usage_count < 5):
                    patterns_to_remove.append(pattern_id)
            
            for pattern_id in patterns_to_remove:
                del self.viral_patterns[pattern_id]
                removed_count += 1
            
            if removed_count > 0:
                self.save_learning_data()
                self.logger.info(f"Cleaned up {removed_count} old patterns")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old patterns: {e}")

# Example usage and integration
if __name__ == "__main__":
    async def test_ai_viral_learning():
        system = AIViralLearningSystem()
        await system.initialize_integrations()
        
        # Test learning from content
        test_content = {
            'title': 'How I Made $10,000 in 30 Days with AI!',
            'thumbnail_data': {
                'has_face': True,
                'face_emotion': 'surprised',
                'has_text': True,
                'contrast': 0.8
            },
            'structure': {
                'hook_duration': 15,
                'total_duration': 480,
                'segments': ['hook', 'story', 'proof', 'call_to_action'],
                'has_cliffhanger': True
            },
            'topics': ['AI', 'money', 'passive income'],
            'upload_time': datetime.now()
        }
        
        test_performance = {
            'views': 50000,
            'engagement_rate': 8.5,
            'retention_rate': 75,
            'ctr': 12.3,
            'shares': 250,
            'comments': 180
        }
        
        # Learn from performance
        session = await system.learn_from_content_performance(test_content, test_performance)
        print(f"Learning session: {session.session_id if session else 'Failed'}")
        
        # Predict viral potential
        prediction = await system.predict_viral_potential(test_content)
        print(f"Viral potential: {prediction['overall_score']:.2f}")
        
        # Get insights
        insights = await system.get_learning_insights()
        print(f"Total patterns learned: {insights['total_patterns']}")
    
    # Run test
    asyncio.run(test_ai_viral_learning())