import asyncio
import logging
from typing import Dict, List
import random

class ViralGrowthEngine:
    """Advanced growth hacking techniques"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.viral_hooks = [
            "This will change everything you know about",
            "The secret that experts don't want you to know",
            "Why everyone is doing this wrong",
            "The truth about",
            "What happens when you"
        ]
    
    async def initialize(self):
        """Initialize the ViralGrowthEngine"""
        self.logger.info(f"Initializing ViralGrowthEngine...")
        try:
            # Basic initialization
            self.logger.info(f"ViralGrowthEngine initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"ViralGrowthEngine initialization failed: {e}")
            return False

    async def implement_viral_strategies(self, content: Dict) -> Dict:
        """Apply proven viral growth techniques"""
        strategies = {
            'hook_optimization': await self.optimize_hook(content),
            'cliffhanger_creation': await self.create_cliffhangers(content),
            'community_engagement': await self.boost_engagement(content),
            'cross_platform_amplification': await self.amplify_across_platforms(content),
            'trending_hijacking': await self.hijack_trends(content)
        }
        
        return strategies
    
    async def optimize_hook(self, content: Dict) -> Dict:
        """Optimize content hook for maximum engagement"""
        try:
            title = content.get('title', '')
            hook = random.choice(self.viral_hooks)
            optimized_title = f"{hook} {title.lower()}"
            
            return {
                'original_title': title,
                'optimized_title': optimized_title,
                'hook_strength': 0.85
            }
        except Exception as e:
            self.logger.error(f"Hook optimization failed: {e}")
            return {'hook_strength': 0.5}
    
    async def create_cliffhangers(self, content: Dict) -> Dict:
        """Add cliffhangers to increase watch time"""
        cliffhangers = [
            "But wait, there's something even more shocking...",
            "The next part will blow your mind...",
            "But here's what nobody tells you...",
            "And then something unexpected happened..."
        ]
        
        return {
            'cliffhanger_added': True,
            'cliffhanger_text': random.choice(cliffhangers),
            'expected_retention_boost': 0.25
        }
    
    async def boost_engagement(self, content: Dict) -> Dict:
        """Implement engagement boosting tactics"""
        engagement_tactics = {
            'comment_bait': "What's your experience with this? Let me know below!",
            'poll_question': "Which strategy worked best for you?",
            'challenge': "Try this for 7 days and report back!",
            'controversy': "This might be controversial, but..."
        }
        
        return {
            'tactics_applied': list(engagement_tactics.keys()),
            'expected_engagement_boost': 0.40
        }
    
    async def amplify_across_platforms(self, content: Dict) -> Dict:
        """Cross-platform amplification strategy"""
        platforms = {
            'youtube_shorts': 'Create 60-second version',
            'tiktok': 'Add trending sounds',
            'instagram_reels': 'Use trending hashtags',
            'twitter': 'Create thread version',
            'linkedin': 'Professional angle'
        }
        
        return {
            'platforms': platforms,
            'cross_promotion_strategy': 'Sequential release with 2-hour gaps',
            'expected_reach_multiplier': 3.5
        }
    
    async def hijack_trends(self, content: Dict) -> Dict:
        """Hijack trending topics for viral potential"""
        trending_angles = [
            "finance + current events",
            "money + viral memes",
            "investing + pop culture",
            "budgeting + trending challenges"
        ]
        
        return {
            'trend_angle': random.choice(trending_angles),
            'viral_potential': 0.75,
            'timing_strategy': 'Release within 24 hours of trend peak'
        }
    
    # Find the analyze_viral_potential method and add data validation at the beginning:
    async def analyze_viral_potential(self, content_data):
        """Analyze viral potential of content"""
        # Ensure content_data is a dictionary
        if isinstance(content_data, str):
            content_data = {"content": content_data, "type": "text"}
        elif not isinstance(content_data, dict):
            content_data = {"content": str(content_data), "type": "unknown"}
        
        try:
            viral_analysis = {
                'high_potential_trends': [],
                'viral_scores': {},
                'recommended_actions': [],
                'trending_elements': []
            }
            
            # Extract trends from content_data or use fallback
            trends = content_data.get('trends', [])
            if not trends:
                # Create fallback trend from content
                topic = content_data.get('topic', content_data.get('content', 'general'))
                trends = [{'topic': topic, 'viral_score': 50}]
            
            for trend in trends:
                if isinstance(trend, str):
                    trend = {'topic': trend, 'viral_score': 50}
                
                topic = trend.get('topic', '')
                
                # Calculate viral score based on multiple factors
                viral_score = 0.6  # Increased base score
                
                # Viral keywords boost (increased impact)
                viral_keywords = ['secret', 'shocking', 'exposed', 'truth', 'hidden', 
                                'millionaire', 'rich', 'money', 'passive', 'free', 'crypto',
                                'bitcoin', 'investment', 'profit', 'earn', 'make money']
                keyword_count = 0
                for keyword in viral_keywords:
                    if keyword.lower() in topic.lower():
                        viral_score += 0.15  # Increased from 0.1
                        keyword_count += 1
                
                # Bonus for multiple viral keywords
                if keyword_count > 1:
                    viral_score += 0.1
                
                # Trending boost (more generous)
                trend_score = trend.get('viral_score', 50)
                if trend_score > 60:  # Lowered threshold
                    viral_score += 0.15
                if trend_score > 80:
                    viral_score += 0.1  # Additional boost
                
                # Urgency boost (increased impact)
                urgency_words = ['now', 'today', 'urgent', '2025', 'new', 'breaking', 'latest']
                for word in urgency_words:
                    if word.lower() in topic.lower():
                        viral_score += 0.08  # Increased from 0.05
                
                # Finance/investment topics get automatic boost
                finance_topics = ['finance', 'investment', 'trading', 'stock', 'crypto', 'bitcoin']
                for finance_word in finance_topics:
                    if finance_word.lower() in topic.lower():
                        viral_score += 0.2
                        break
                
                viral_score = min(viral_score, 1.0)  # Cap at 1.0
                viral_analysis['viral_scores'][topic] = viral_score
                
                # High potential trends (lowered threshold from 0.7 to 0.6)
                if viral_score > 0.6:
                    viral_analysis['high_potential_trends'].append({
                        'topic': topic,
                        'viral_score': viral_score,
                        'recommended_format': 'short_form' if viral_score > 0.85 else 'long_form'
                    })
            
            # Generate recommendations
            if viral_analysis['high_potential_trends']:
                viral_analysis['recommended_actions'] = [
                    'Create content within 24 hours',
                    'Use trending hashtags and keywords',
                    'Apply viral hooks and cliffhangers',
                    'Cross-promote on all platforms'
                ]
            
            viral_analysis['trending_elements'] = [
                'curiosity_gaps', 'emotional_triggers', 'social_proof', 
                'urgency_factors', 'controversy_angles'
            ]
            
            self.logger.info(f"Analyzed {len(trends)} trends, found {len(viral_analysis['high_potential_trends'])} high-potential topics")
            return viral_analysis
            
        except Exception as e:
            self.logger.error(f"Viral potential analysis failed: {e}")
            return {
                'high_potential_trends': [],
                'viral_scores': {},
                'recommended_actions': ['Use fallback content strategy'],
                'error': str(e)
            }
    async def create_viral_series(self, topic: str) -> List[Dict]:
        """Create interconnected content series for binge-watching"""
        series_structure = [
            {'type': 'hook', 'title': f'This {topic} Secret Will Blow Your Mind'},
            {'type': 'education', 'title': f'The Truth About {topic} Nobody Tells You'},
            {'type': 'controversy', 'title': f'Why Everyone is Wrong About {topic}'},
            {'type': 'solution', 'title': f'How I Mastered {topic} in 30 Days'},
            {'type': 'results', 'title': f'My {topic} Results After 1 Year'}
        ]
        
        return series_structure
    async def apply_viral_strategies(self, content: Dict) -> Dict:
        """Alias for implement_viral_strategies for backward compatibility"""
        return await self.implement_viral_strategies(content)
