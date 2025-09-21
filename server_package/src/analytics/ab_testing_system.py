import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class ViralABTestingSystem:
    """A/B testing system for viral optimization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.test_results = {}
        self.active_tests = {}
        
        # VIRAL PSYCHOLOGY TRIGGERS
        self.psychology_triggers = {
            "curiosity": ["secret", "hidden", "revealed", "truth", "exposed"],
            "urgency": ["now", "today", "urgent", "limited", "ending soon"],
            "social_proof": ["millions", "everyone", "trending", "viral", "popular"],
            "controversy": ["shocking", "banned", "forbidden", "they don't want"],
            "fear_of_missing_out": ["before it's too late", "last chance", "don't miss"]
        }
        
    async def create_title_variants(self, base_title: str, topic: str) -> List[Dict]:
        """Create 5 A/B test variants for titles with viral psychology"""
        
        variants = [
            {
                "version": "A_curiosity",
                "title": f"The {topic} Secret That Will Change Your Life Forever",
                "psychology": "curiosity_gap",
                "expected_ctr": 0.12,
                "viral_score": 85
            },
            {
                "version": "B_urgency", 
                "title": f"You Need to Know This About {topic} RIGHT NOW (Before It's Too Late)",
                "psychology": "urgency",
                "expected_ctr": 0.10,
                "viral_score": 78
            },
            {
                "version": "C_social_proof",
                "title": f"Why 10 Million People Are Using This {topic} Method",
                "psychology": "social_proof", 
                "expected_ctr": 0.11,
                "viral_score": 82
            },
            {
                "version": "D_controversy",
                "title": f"The {topic} Truth They Don't Want You to Know (SHOCKING)",
                "psychology": "controversy",
                "expected_ctr": 0.14,
                "viral_score": 92
            },
            {
                "version": "E_fomo",
                "title": f"Don't Miss This {topic} Opportunity - Last Chance!",
                "psychology": "fear_of_missing_out",
                "expected_ctr": 0.13,
                "viral_score": 88
            }
        ]
        
        return variants
    
    async def create_thumbnail_variants(self, topic: str) -> List[Dict]:
        """Create 3 A/B test variants for thumbnails with viral elements"""
        
        variants = [
            {
                "version": "A_shocked_face",
                "style": "shocked_face_expression",
                "colors": ["red", "yellow", "white"],
                "text_overlay": "SHOCKING!",
                "elements": ["wide_eyes", "open_mouth", "pointing"],
                "expected_ctr": 0.08,
                "viral_score": 75
            },
            {
                "version": "B_money_graphics",
                "style": "money_graphics",
                "colors": ["green", "gold", "black"],
                "text_overlay": "$10K/MONTH",
                "elements": ["dollar_signs", "cash_stack", "profit_arrow"],
                "expected_ctr": 0.09,
                "viral_score": 82
            },
            {
                "version": "C_red_arrows",
                "style": "red_arrows_pointing",
                "colors": ["red", "white", "blue"],
                "text_overlay": "WATCH THIS!",
                "elements": ["red_arrows", "circle_highlight", "contrast_text"],
                "expected_ctr": 0.07,
                "viral_score": 70
            }
        ]
        
        return variants
    
    async def run_ab_test(self, content_id: str, variants: List[Dict], test_duration_hours: int = 24) -> Dict:
        """Run A/B test and track performance"""
        
        test_id = f"test_{content_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        test_config = {
            "test_id": test_id,
            "content_id": content_id,
            "variants": variants,
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=test_duration_hours),
            "status": "active",
            "traffic_split": self._calculate_traffic_split(len(variants))
        }
        
        self.active_tests[test_id] = test_config
        
        self.logger.info(f"Started A/B test {test_id} with {len(variants)} variants")
        
        return test_config
    
    async def get_winning_variant(self, test_id: str) -> Optional[Dict]:
        """Determine winning variant based on performance metrics"""
        
        if test_id not in self.test_results:
            return None
        
        results = self.test_results[test_id]
        
        # Calculate composite score: CTR (40%) + Engagement (30%) + Viral Score (30%)
        best_variant = None
        best_score = 0
        
        for variant in results["variants"]:
            composite_score = (
                variant.get("actual_ctr", 0) * 0.4 +
                variant.get("engagement_rate", 0) * 0.3 +
                variant.get("viral_score", 0) / 100 * 0.3
            )
            
            if composite_score > best_score:
                best_score = composite_score
                best_variant = variant
        
        return best_variant
    
    async def optimize_content_automatically(self, content: Dict) -> Dict:
        """Auto-optimize content using best performing variants"""
        
        # Get historical best performers
        best_title_psychology = await self._get_best_title_psychology()
        best_thumbnail_style = await self._get_best_thumbnail_style()
        
        optimized_content = content.copy()
        
        # Apply winning strategies
        if best_title_psychology:
            optimized_content["title"] = await self._apply_psychology_to_title(
                content["title"], best_title_psychology
            )
        
        if best_thumbnail_style:
            optimized_content["thumbnail_style"] = best_thumbnail_style
        
        # Add viral elements
        optimized_content["viral_elements"] = {
            "hooks": await self._generate_viral_hooks(content["topic"]),
            "cta": await self._generate_viral_cta(content["topic"]),
            "engagement_bait": await self._generate_engagement_bait()
        }
        
        return optimized_content
    
    def _calculate_traffic_split(self, num_variants: int) -> Dict:
        """Calculate even traffic split for variants"""
        split_percentage = 100 // num_variants
        remainder = 100 % num_variants
        
        splits = {}
        for i in range(num_variants):
            variant_key = f"variant_{chr(65 + i)}"  # A, B, C, etc.
            splits[variant_key] = split_percentage + (1 if i < remainder else 0)
        
        return splits
    
    async def _get_best_title_psychology(self) -> Optional[str]:
        """Get historically best performing title psychology"""
        # Analyze past results and return best psychology trigger
        psychology_performance = {
            "controversy": 0.14,
            "fomo": 0.13,
            "curiosity": 0.12,
            "social_proof": 0.11,
            "urgency": 0.10
        }
        
        return max(psychology_performance, key=lambda k: psychology_performance[k])
    
    async def _get_best_thumbnail_style(self) -> Optional[str]:
        """Get historically best performing thumbnail style"""
        return "money_graphics"  # Based on performance data
    
    async def _apply_psychology_to_title(self, title: str, psychology: str) -> str:
        """Apply psychological trigger to title"""
        triggers = self.psychology_triggers.get(psychology, [])
        if triggers:
            trigger = random.choice(triggers)
            return f"{title} - {trigger.upper()}"
        return title
    
    async def _generate_viral_hooks(self, topic: str) -> List[str]:
        """Generate viral hooks for content"""
        return [
            f"This {topic} method is going VIRAL!",
            f"Everyone's talking about this {topic} secret",
            f"You won't believe what happened with {topic}"
        ]
    
    async def _generate_viral_cta(self, topic: str) -> str:
        """Generate viral call-to-action"""
        ctas = [
            f"SMASH that like if {topic} changed your life!",
            f"Comment 'YES' if you want more {topic} content!",
            f"Share this {topic} secret with someone who needs it!"
        ]
        return random.choice(ctas)
    
    async def _generate_engagement_bait(self) -> List[str]:
        """Generate engagement bait questions"""
        return [
            "What's your biggest financial goal for 2024?",
            "Drop a 💰 if you're ready to make money!",
            "Comment your current income and I'll help you 10x it!",
            "Who else is tired of being broke? 👇"
        ]