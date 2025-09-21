import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

class SmartAdOptimizer:
    """AI-powered ad placement for maximum revenue and retention"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ad_performance_history = []
        self.optimization_rules = self.load_optimization_rules()
    
    async def initialize(self):
        """Initialize the SmartAdOptimizer"""
        self.logger.info(f"Initializing SmartAdOptimizer...")
        try:
            # Basic initialization
            self.logger.info(f"SmartAdOptimizer initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"SmartAdOptimizer initialization failed: {e}")
            return False

    def load_optimization_rules(self) -> Dict:
        """Load optimization rules for ad placement"""
        try:
            # Default optimization rules
            default_rules = {
                'preroll': {
                    'max_duration': 15,
                    'skip_threshold': 5,
                    'targeting_enabled': True
                },
                'midroll': {
                    'min_video_duration': 480,  # 8 minutes
                    'max_frequency': 4,
                    'min_spacing': 120,  # 2 minutes
                    'avoid_key_moments': True
                },
                'overlay': {
                    'max_concurrent': 1,
                    'mobile_optimized': True,
                    'engagement_threshold': 0.7
                },
                'revenue': {
                    'target_rpm': 3.0,
                    'optimization_threshold': 0.8
                }
            }
            
            # Try to load from config file if it exists
            config_path = Path('config/ad_optimization_rules.json')
            if config_path.exists():
                with open(config_path, 'r') as f:
                    loaded_rules = json.load(f)
                    # Merge with defaults
                    for category, rules in loaded_rules.items():
                        if category in default_rules:
                            default_rules[category].update(rules)
                        else:
                            default_rules[category] = rules
            
            self.logger.info("[OK] Ad optimization rules loaded successfully")
            return default_rules
            
        except Exception as e:
            self.logger.warning(f"Failed to load optimization rules, using defaults: {e}")
            return {
                'preroll': {'max_duration': 15, 'skip_threshold': 5},
                'midroll': {'min_video_duration': 480, 'max_frequency': 2},
                'overlay': {'max_concurrent': 1},
                'revenue': {'target_rpm': 2.0}
            }
    
    async def optimize_ad_placement(self, video_data: Dict) -> Dict:
        """Dynamically optimize ad placement based on content analysis"""
        try:
            self.logger.info(f"Optimizing ad placement for video: {video_data.get('title', 'Unknown')}")
            
            # Analyze content for optimal ad breaks
            content_analysis = await self.analyze_content_structure(video_data)
            
            optimizations = {
                'pre_roll': {
                    'enabled': True,
                    'max_duration': await self.calculate_optimal_preroll_duration(video_data),
                    'targeting': await self.optimize_pre_roll_targeting(video_data),
                    'skip_threshold': self.optimization_rules['preroll']['skip_threshold']
                },
                'mid_roll': {
                    'placements': await self.calculate_optimal_midroll_points(content_analysis),
                    'frequency_cap': self.calculate_optimal_frequency(video_data),
                    'content_aware': True,
                    'min_spacing': self.optimization_rules['midroll']['min_spacing']
                },
                'overlay': {
                    'timing': await self.optimize_overlay_timing(content_analysis),
                    'mobile_optimization': True,
                    'engagement_based': True,
                    'max_concurrent': self.optimization_rules['overlay']['max_concurrent']
                },
                'end_screen': {
                    'enabled': True,
                    'duration': 20,
                    'related_videos': await self.get_related_video_suggestions(video_data)
                }
            }
            
            # Calculate expected revenue impact
            revenue_projection = await self.calculate_revenue_projection(optimizations, video_data)
            optimizations['revenue_projection'] = revenue_projection
            
            return optimizations
            
        except Exception as e:
            self.logger.error(f"Ad optimization failed: {e}")
            return self.get_fallback_ad_strategy()
    
    async def analyze_content_structure(self, video_data: Dict) -> Dict:
        """Analyze content structure for optimal ad placement"""
        try:
            duration = video_data.get('duration', 300)
            script = video_data.get('script', '')
            
            # Basic content analysis
            segments = await self.segment_content(script, duration)
            key_moments = await self.identify_key_moments(script, segments)
            engagement_scores = await self.predict_segment_engagement(segments)
            
            return {
                'duration': duration,
                'segments': segments,
                'key_moments': key_moments,
                'engagement_scores': engagement_scores,
                'safe_ad_zones': await self.identify_safe_ad_zones(segments, key_moments)
            }
            
        except Exception as e:
            self.logger.error(f"Content analysis failed: {e}")
            return self.get_fallback_content_analysis(video_data.get('duration', 300))
    
    async def segment_content(self, script: str, duration: int) -> List[Dict]:
        """Segment content into logical parts"""
        segments = []
        
        # Handle case where script might be a dict instead of string
        if isinstance(script, dict):
            script = script.get('script', '') or script.get('content', '') or str(script)
        elif not isinstance(script, str):
            script = str(script) if script else ''
        
        if script:
            words = script.split()
            words_per_segment = max(50, len(words) // 4)
            
            for i in range(0, len(words), words_per_segment):
                segment_words = words[i:i + words_per_segment]
                start_time = (i / len(words)) * duration
                end_time = min(((i + words_per_segment) / len(words)) * duration, duration)
                
                segments.append({
                    'start': start_time,
                    'end': end_time,
                    'content': ' '.join(segment_words),
                    'type': self.classify_segment_type(segment_words, i == 0)
                })
        else:
            segment_duration = duration / 4
            for i in range(4):
                segments.append({
                    'start': i * segment_duration,
                    'end': (i + 1) * segment_duration,
                    'content': f"Segment {i + 1}",
                    'type': 'main_content'
                })
        
        return segments
    
    def classify_segment_type(self, words: List[str], is_first: bool) -> str:
        """Classify segment type for ad placement optimization"""
        if is_first:
            return 'introduction'
        
        content = ' '.join(words).lower()
        
        if any(word in content for word in ['conclusion', 'summary', 'final', 'end']):
            return 'conclusion'
        elif any(word in content for word in ['transition', 'next', 'now', 'moving']):
            return 'transition'
        else:
            return 'main_content'
    
    async def identify_key_moments(self, script: str, segments: List[Dict]) -> List[Dict]:
        """Identify key moments to avoid placing ads"""
        key_moments = []
        
        if segments:
            total_duration = segments[-1]['end']
            key_moments.extend([
                {'start': 0, 'end': 60, 'reason': 'opening_hook'},
                {'start': max(0, total_duration - 60), 'end': total_duration, 'reason': 'conclusion'}
            ])
        
        return key_moments
    
    async def predict_segment_engagement(self, segments: List[Dict]) -> Dict:
        """Predict engagement for each segment"""
        engagement_scores = {}
        
        for i, segment in enumerate(segments):
            segment_type = segment.get('type', 'main_content')
            base_score = self.estimate_segment_engagement(segment_type)
            
            if i == 0:
                base_score *= 1.2
            elif i == len(segments) - 1:
                base_score *= 1.1
            
            engagement_scores[f"segment_{i}"] = min(1.0, base_score)
        
        return engagement_scores
    
    def estimate_segment_engagement(self, segment_type: str) -> float:
        """Estimate engagement level for different segment types"""
        engagement_map = {
            'introduction': 0.9,
            'main_content': 0.7,
            'conclusion': 0.8,
            'transition': 0.4
        }
        return engagement_map.get(segment_type, 0.6)
    
    async def identify_safe_ad_zones(self, segments: List[Dict], key_moments: List[Dict]) -> List[Dict]:
        """Identify safe zones for ad placement"""
        safe_zones = []
        
        for segment in segments:
            is_safe = True
            for key_moment in key_moments:
                if (segment['start'] < key_moment['end'] and segment['end'] > key_moment['start']):
                    is_safe = False
                    break
            
            if is_safe and segment.get('type') in ['main_content', 'transition']:
                safe_zones.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'engagement_score': self.estimate_segment_engagement(segment.get('type', 'main_content'))
                })
        
        return safe_zones
    
    async def calculate_optimal_preroll_duration(self, video_data: Dict) -> int:
        """Calculate optimal preroll duration"""
        duration = video_data.get('duration', 300)
        
        if duration < 300:
            return 5
        elif duration < 600:
            return 10
        else:
            return self.optimization_rules['preroll']['max_duration']
    
    async def optimize_pre_roll_targeting(self, video_data: Dict) -> Dict:
        """Optimize preroll targeting"""
        return {
            'demographics': 'auto',
            'interests': video_data.get('topic', 'general'),
            'behavior': 'engaged_viewers'
        }
    
    async def calculate_optimal_midroll_points(self, content_analysis: Dict) -> List[float]:
        """Calculate best midroll placement points"""
        try:
            duration = content_analysis['duration']
            safe_zones = content_analysis.get('safe_ad_zones', [])
            
            if duration < self.optimization_rules['midroll']['min_video_duration']:
                return []
            
            max_midrolls = min(self.optimization_rules['midroll']['max_frequency'], duration // 300)
            optimal_points = []
            
            if safe_zones:
                sorted_zones = sorted(safe_zones, key=lambda x: x.get('engagement_score', 0.5))
                
                for zone in sorted_zones[:max_midrolls]:
                    ad_time = (zone['start'] + zone['end']) / 2
                    optimal_points.append(round(ad_time, 1))
            else:
                if max_midrolls >= 1:
                    optimal_points = [duration / 2]
            
            return optimal_points
            
        except Exception as e:
            self.logger.error(f"Midroll calculation failed: {e}")
            return [300.0] if content_analysis.get('duration', 0) > 480 else []
    
    def calculate_optimal_frequency(self, video_data: Dict) -> int:
        """Calculate optimal ad frequency"""
        duration = video_data.get('duration', 300)
        return min(self.optimization_rules['midroll']['max_frequency'], max(1, duration // 300))
    
    async def optimize_overlay_timing(self, content_analysis: Dict) -> List[Dict]:
        """Optimize overlay ad timing"""
        safe_zones = content_analysis.get('safe_ad_zones', [])
        overlay_timings = []
        
        for zone in safe_zones[:2]:
            overlay_timings.append({
                'start': zone['start'] + 10,
                'duration': 15,
                'position': 'bottom_right'
            })
        
        return overlay_timings
    
    async def get_related_video_suggestions(self, video_data: Dict) -> List[str]:
        """Get related video suggestions for end screen"""
        topic = video_data.get('topic', 'general')
        return [f"Related {topic} video {i+1}" for i in range(3)]
    
    async def calculate_revenue_projection(self, optimizations: Dict, video_data: Dict) -> Dict:
        """Calculate expected revenue from optimizations"""
        try:
            expected_views = video_data.get('expected_views', 1000)
            base_rpm = self.optimization_rules['revenue']['target_rpm']
            
            preroll_revenue = expected_views * 0.8 * (base_rpm / 1000)
            midroll_revenue = len(optimizations.get('mid_roll', {}).get('placements', [])) * expected_views * 0.6 * (base_rpm / 1000)
            overlay_revenue = len(optimizations.get('overlay', {}).get('timing', [])) * expected_views * 0.3 * (base_rpm / 1000)
            
            total_revenue = preroll_revenue + midroll_revenue + overlay_revenue
            
            return {
                'total_projected_revenue': round(total_revenue, 2),
                'preroll_revenue': round(preroll_revenue, 2),
                'midroll_revenue': round(midroll_revenue, 2),
                'overlay_revenue': round(overlay_revenue, 2),
                'revenue_per_view': round(total_revenue / expected_views, 4) if expected_views > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Revenue projection failed: {e}")
            return {'total_projected_revenue': 0, 'error': str(e)}
    
    def get_fallback_ad_strategy(self) -> Dict:
        """Fallback ad strategy when optimization fails"""
        return {
            'pre_roll': {'enabled': True, 'max_duration': 15, 'skip_threshold': 5},
            'mid_roll': {'placements': [300.0], 'frequency_cap': 1},
            'overlay': {'timing': [], 'max_concurrent': 1},
            'end_screen': {'enabled': True, 'duration': 20},
            'revenue_projection': {'total_projected_revenue': 0, 'fallback': True}
        }
    
    def get_fallback_content_analysis(self, duration: int) -> Dict:
        """Fallback content analysis"""
        return {
            'duration': duration,
            'segments': [{'start': 0, 'end': duration, 'type': 'main_content'}],
            'key_moments': [],
            'engagement_scores': {'segment_0': 0.7},
            'safe_ad_zones': [{'start': 60, 'end': duration - 60, 'engagement_score': 0.7}] if duration > 120 else []
        }
