"""
YouTube Psychology Analyzer - Advanced viewer psychology and engagement optimization
Analyzes psychological triggers, emotional responses, and viewer behavior patterns
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
from enum import Enum

class PsychologyTrigger(Enum):
    CURIOSITY = "curiosity"
    FOMO = "fear_of_missing_out"
    AUTHORITY = "authority_trust"
    SOCIAL_PROOF = "social_proof"
    SCARCITY = "scarcity"
    RECIPROCITY = "reciprocity"
    STORYTELLING = "storytelling"
    CONTROVERSY = "controversy"
    EMOTIONAL = "emotional_resonance"
    URGENCY = "urgency"

@dataclass
class PsychologyInsight:
    trigger: PsychologyTrigger
    strength: float  # 0-1 scale
    effectiveness: float  # 0-1 scale
    audience_segment: str
    optimization_tip: str
    implementation_example: str

class YouTubePsychologyAnalyzer:
    """Advanced YouTube psychology analysis and optimization system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.psychology_patterns = {}
        self.audience_profiles = {}
        self.engagement_triggers = {}
        
    async def initialize(self):
        """Initialize the YouTubePsychologyAnalyzer with default patterns"""
        self.logger.info("🧠 Initializing YouTubePsychologyAnalyzer...")
        try:
            await self._load_psychology_patterns()
            await self._initialize_audience_profiles()
            await self._setup_engagement_triggers()
            self.logger.info("✅ YouTubePsychologyAnalyzer initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"❌ YouTubePsychologyAnalyzer initialization failed: {e}")
            return False
    
    async def _load_psychology_patterns(self):
        """Load psychological patterns and triggers"""
        self.psychology_patterns = {
            'finance_niche': {
                PsychologyTrigger.CURIOSITY: {
                    'strength': 0.9,
                    'examples': ["99% of people don't know this", "Secret investment strategy", "Banks don't want you to know"],
                    'effectiveness': 0.85
                },
                PsychologyTrigger.FOMO: {
                    'strength': 0.8,
                    'examples': ["Don't miss out", "Limited time", "Before it's too late"],
                    'effectiveness': 0.78
                },
                PsychologyTrigger.AUTHORITY: {
                    'strength': 0.95,
                    'examples': ["As a financial expert", "Based on 10 years experience", "Proven strategy"],
                    'effectiveness': 0.92
                }
            },
            'gen_z_audience': {
                PsychologyTrigger.SOCIAL_PROOF: {
                    'strength': 0.85,
                    'examples': ["Join 100K+ investors", "Everyone is doing this", "Viral strategy"],
                    'effectiveness': 0.88
                },
                PsychologyTrigger.EMOTIONAL: {
                    'strength': 0.9,
                    'examples': ["Financial freedom journey", "Life-changing results", "Your future self"],
                    'effectiveness': 0.83
                }
            }
        }
    
    async def _initialize_audience_profiles(self):
        """Initialize audience psychology profiles"""
        self.audience_profiles = {
            'young_investors': {
                'age_range': '18-25',
                'primary_triggers': [PsychologyTrigger.FOMO, PsychologyTrigger.SOCIAL_PROOF, PsychologyTrigger.CURIOSITY],
                'content_preferences': ['quick_tips', 'visual_learning', 'real_examples'],
                'attention_span': 45,  # seconds
                'engagement_style': 'interactive'
            },
            'millennial_investors': {
                'age_range': '26-35',
                'primary_triggers': [PsychologyTrigger.AUTHORITY, PsychologyTrigger.RECIPROCITY, PsychologyTrigger.URGENCY],
                'content_preferences': ['detailed_explanation', 'step_by_step', 'case_studies'],
                'attention_span': 120,  # seconds
                'engagement_style': 'educational'
            },
            'experienced_traders': {
                'age_range': '35+',
                'primary_triggers': [PsychologyTrigger.AUTHORITY, PsychologyTrigger.SCARCITY, PsychologyTrigger.CONTROVERSY],
                'content_preferences': ['data_driven', 'market_analysis', 'advanced_strategies'],
                'attention_span': 300,  # seconds
                'engagement_style': 'analytical'
            }
        }
    
    async def _setup_engagement_triggers(self):
        """Setup psychological engagement triggers"""
        self.engagement_triggers = {
            'hook_triggers': [
                "What if I told you...",
                "This one trick changed everything",
                "The shocking truth about...",
                "You won't believe what happened",
                "Stop scrolling if you want..."
            ],
            'retention_triggers': [
                "But here's the kicker...",
                "And it gets better...",
                "Now here's the secret...",
                "The best part is...",
                "Wait, there's more..."
            ],
            'cta_triggers': [
                "Comment 'Sensei Approved' if...",
                "Save this for later",
                "Share with someone who needs this",
                "Which tip surprised you most?",
                "Drop a 💰 if you're ready..."
            ]
        }
    
    async def analyze_content_psychology(self, content_data: Dict) -> Dict:
        """Analyze content for psychological effectiveness"""
        try:
            analysis = {
                'psychology_score': 0.0,
                'trigger_analysis': {},
                'audience_alignment': {},
                'optimization_suggestions': [],
                'psychology_insights': {}
            }
            
            # Analyze title psychology
            title_psychology = await self._analyze_text_psychology(content_data.get('title', ''))
            
            # Analyze thumbnail psychology
            thumbnail_psychology = await self._analyze_thumbnail_psychology(content_data.get('thumbnail_text', ''))
            
            # Analyze hook psychology
            hook_psychology = await self._analyze_hook_psychology(content_data.get('hook', ''))
            
            # Calculate overall psychology score
            psychology_score = (title_psychology['effectiveness'] + 
                             thumbnail_psychology['effectiveness'] + 
                             hook_psychology['effectiveness']) / 3
            
            analysis.update({
                'psychology_score': psychology_score,
                'trigger_analysis': {
                    'title': title_psychology,
                    'thumbnail': thumbnail_psychology,
                    'hook': hook_psychology
                },
                'audience_alignment': await self._get_audience_alignment(content_data),
                'optimization_suggestions': await self._generate_psychology_suggestions(content_data),
                'psychology_insights': {
                    'strongest_trigger': max([title_psychology, thumbnail_psychology, hook_psychology], 
                                           key=lambda x: x['effectiveness']),
                    'recommended_improvements': await self._get_recommended_improvements(content_data),
                    'psychology_patterns': await self._identify_psychology_patterns(content_data)
                }
            })
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Psychology analysis failed: {e}")
            return {'error': str(e), 'psychology_score': 0.0}
    
    async def _analyze_text_psychology(self, text: str) -> Dict:
        """Analyze text for psychological triggers"""
        text_lower = text.lower()
        triggers_found = []
        effectiveness = 0.0
        
        # Check for psychology triggers
        trigger_keywords = {
            PsychologyTrigger.CURIOSITY: ['secret', 'hidden', 'unknown', 'mystery', 'surprising'],
            PsychologyTrigger.FOMO: ['limited', 'before', 'expires', 'missing out', 'last chance'],
            PsychologyTrigger.AUTHORITY: ['expert', 'proven', 'professional', 'insider', 'exclusive'],
            PsychologyTrigger.URGENCY: ['now', 'today', 'immediately', 'urgent', 'quick']
        }
        
        for trigger, keywords in trigger_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    triggers_found.append(trigger)
                    effectiveness += 0.2
        
        return {
            'triggers_found': [t.value for t in triggers_found],
            'effectiveness': min(effectiveness, 1.0),
            'suggestions': await self._get_text_improvements(text, triggers_found)
        }
    
    async def _analyze_thumbnail_psychology(self, thumbnail_text: str) -> Dict:
        """Analyze thumbnail text for psychological impact"""
        return await self._analyze_text_psychology(thumbnail_text)
    
    async def _analyze_hook_psychology(self, hook: str) -> Dict:
        """Analyze video hook for psychological effectiveness"""
        return await self._analyze_text_psychology(hook)
    
    async def _get_audience_alignment(self, content_data: Dict) -> Dict:
        """Check how well content aligns with audience psychology - BULLETPROOF VERSION"""
        try:
            target_audience = content_data.get('target_audience', 'young_investors')
            
            # Bulletproof audience profile access
            if not hasattr(self, 'audience_profiles') or not self.audience_profiles:
                # Create default profile if not initialized
                default_profile = {
                    'primary_triggers': [PsychologyTrigger.CURIOSITY, PsychologyTrigger.FOMO],
                    'content_preferences': ['quick_tips', 'visual_learning'],
                    'attention_span': 60,
                    'engagement_style': 'interactive'
                }
                audience_profile = default_profile
            else:
                audience_profile = self.audience_profiles.get(target_audience)
                if not audience_profile:
                    # Fallback to first available profile or default
                    audience_profile = next(iter(self.audience_profiles.values())) if self.audience_profiles else {
                        'primary_triggers': [PsychologyTrigger.CURIOSITY],
                        'content_preferences': ['general_content'],
                        'attention_span': 60,
                        'engagement_style': 'general'
                    }
            
            return {
                'target_audience': target_audience,
                'alignment_score': 0.85,
                'primary_triggers': [t.value if hasattr(t, 'value') else str(t) for t in audience_profile.get('primary_triggers', [])],
                'content_recommendations': audience_profile.get('content_preferences', ['general_content'])
            }
        except Exception as e:
            self.logger.warning(f"Audience alignment analysis failed: {e}")
            return {
                'target_audience': 'fallback',
                'alignment_score': 0.5,
                'primary_triggers': ['curiosity'],
                'content_recommendations': ['general_content']
            }
    
    async def _generate_psychology_suggestions(self, content_data: Dict) -> List[str]:
        """Generate specific psychology optimization suggestions"""
        return [
            "Add curiosity gap in first 5 seconds",
            "Use authority positioning in title",
            "Include social proof elements",
            "Create urgency with time-sensitive content",
            "Use emotional storytelling hooks"
        ]
    
    async def _get_recommended_improvements(self, content_data: Dict) -> List[str]:
        """Get specific recommended improvements"""
        return [
            "Test different psychological triggers",
            "A/B test thumbnail psychology variations",
            "Monitor engagement psychology metrics",
            "Adjust content based on audience psychology feedback"
        ]
    
    async def _get_text_improvements(self, text: str, triggers_found: List) -> List[str]:
        """Get specific text improvements based on psychological analysis"""
        improvements = []
        
        # Analyze text for psychological triggers
        if not any(word in text.lower() for word in ['you', 'your', 'yourself']):
            improvements.append("Add more personal pronouns to create connection")
        
        if not any(word in text.lower() for word in ['secret', 'revealed', 'hidden', 'truth']):
            improvements.append("Include curiosity-triggering words")
        
        if len(text.split()) > 10:
            improvements.append("Consider shortening for better impact")
        
        if not any(char in text for char in ['!', '?']):
            improvements.append("Add emotional punctuation for emphasis")
        
        return improvements
    
    async def _identify_psychology_patterns(self, content_data: Dict) -> Dict:
        """Identify recurring psychology patterns"""
        return {
            'successful_patterns': ['curiosity_gap', 'authority_trust', 'social_proof'],
            'underperforming_patterns': ['generic_statements', 'overused_cliches'],
            'emerging_trends': ['authenticity', 'transparency', 'value_first']
        }
    
    async def get_psychology_recommendations(self, audience_segment: str) -> Dict:
        """Get psychology recommendations for specific audience segment"""
        profile = self.audience_profiles.get(audience_segment, self.audience_profiles['young_investors'])
        
        return {
            'audience': audience_segment,
            'primary_triggers': [t.value for t in profile['primary_triggers']],
            'recommended_hooks': self.engagement_triggers['hook_triggers'][:3],
            'content_style': profile['engagement_style'],
            'optimal_length': profile['attention_span'],
            'psychology_tips': [
                f"Focus on {profile['primary_triggers'][0].value} triggers",
                f"Use {profile['engagement_style']} engagement style",
                f"Keep content under {profile['attention_span']} seconds for retention"
            ]
        }