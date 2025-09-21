import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime

@dataclass
class BrandAsset:
    """Brand asset configuration"""
    asset_type: str
    name: str
    file_path: Optional[str]
    properties: Dict[str, Any]
    usage_guidelines: List[str]
    last_updated: str

@dataclass
class ContentTemplate:
    """Unified content template"""
    template_id: str
    name: str
    category: str
    brand_elements: List[str]
    style_requirements: Dict[str, Any]
    content_structure: Dict[str, Any]
    performance_metrics: Dict[str, float]

class PixelFinanceBrand:
    """Unified Pixel Finance Brand Management System - Central hub for all branding"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.brand_data_dir = Path("data/brand_assets")
        self.brand_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Core Brand Identity
        self.brand_identity = {
            "name": "Pixel Finance",
            "tagline": "Level Up Your Wealth",
            "mission": "Democratizing financial education through engaging, tech-forward content",
            "vision": "A world where everyone has access to premium financial knowledge",
            "values": ["Innovation", "Authenticity", "Accessibility", "Results", "Community"]
        }
        
        # Visual Brand System
        self.visual_system = {
            "primary_palette": {
                "neon_cyan": "#00FFFF",
                "neon_magenta": "#FF00FF", 
                "neon_yellow": "#FFFF00",
                "electric_blue": "#0080FF",
                "laser_green": "#00FF80"
            },
            "secondary_palette": {
                "dark_bg": "#0A0A0A",
                "medium_dark": "#1A1A1A",
                "accent_dark": "#2A2A2A",
                "white": "#FFFFFF",
                "light_gray": "#CCCCCC"
            },
            "gradients": {
                "cyber_gradient": "linear-gradient(45deg, #00FFFF, #FF00FF)",
                "wealth_gradient": "linear-gradient(135deg, #FFFF00, #00FF80)",
                "power_gradient": "linear-gradient(90deg, #FF00FF, #0080FF)"
            },
            "typography": {
                "primary_font": "Orbitron",
                "secondary_font": "Rajdhani",
                "accent_font": "Exo 2",
                "fallback_fonts": "Arial, sans-serif"
            }
        }
        
        # Content Brand Guidelines
        self.content_guidelines = {
            "tone_of_voice": {
                "primary_tone": "energetic_professional",
                "personality": "tech-savvy finance mentor",
                "communication_style": "direct, engaging, results-focused",
                "avoid": ["overly technical jargon", "boring corporate speak", "get-rich-quick promises"]
            },
            "content_pillars": [
                "Market Analysis & Insights",
                "Investment Strategies", 
                "Crypto & DeFi Education",
                "Personal Finance Optimization",
                "Wealth Building Psychology"
            ],
            "viral_elements": {
                "hooks": [
                    "The {topic} secret that changed everything",
                    "Why 99% of people fail at {topic}",
                    "This {topic} strategy is pure genius",
                    "The {topic} mistake costing you thousands"
                ],
                "emotional_triggers": ["FOMO", "curiosity", "aspiration", "urgency", "social proof"],
                "engagement_boosters": ["polls", "challenges", "behind-the-scenes", "live reactions"]
            }
        }
        
        # Platform-Specific Adaptations
        self.platform_adaptations = {
            "youtube": {
                "thumbnail_style": "high_contrast_neon",
                "title_format": "hook_based_clickable",
                "description_structure": "hook_value_cta",
                "branding_elements": ["logo_overlay", "consistent_intro", "end_screen"]
            },
            "instagram": {
                "visual_style": "neon_grid_aesthetic",
                "story_templates": "pixel_finance_branded",
                "hashtag_strategy": "finance_tech_lifestyle",
                "content_mix": "80_education_20_personal"
            },
            "tiktok": {
                "video_style": "fast_paced_visual",
                "hook_timing": "first_3_seconds",
                "trend_adaptation": "finance_angle_on_trends",
                "branding": "subtle_watermark"
            },
            "twitter": {
                "thread_style": "numbered_insights",
                "engagement_strategy": "question_based",
                "visual_consistency": "branded_graphics",
                "voice": "thought_leader"
            }
        }
        
        # Brand Assets Registry
        self.brand_assets: Dict[str, BrandAsset] = {}
        self.content_templates: Dict[str, ContentTemplate] = {}
        
        # Performance Tracking
        self.brand_performance = {
            "consistency_score": 0.0,
            "engagement_metrics": {},
            "brand_recognition": {},
            "conversion_rates": {}
        }
        
        # Initialize default assets and templates
        self._initialize_brand_assets()
        self._initialize_content_templates()
    
    def _initialize_brand_assets(self):
        """Initialize default brand assets"""
        # Logo variations
        self.brand_assets["primary_logo"] = BrandAsset(
            asset_type="logo",
            name="Pixel Finance Primary Logo",
            file_path="assets/logos/pixel_finance_primary.png",
            properties={
                "format": "PNG",
                "dimensions": "1200x400",
                "background": "transparent",
                "colors": ["#00FFFF", "#FF00FF"]
            },
            usage_guidelines=[
                "Use on dark backgrounds",
                "Maintain minimum 20px padding",
                "Never stretch or distort",
                "Always use high-resolution version"
            ],
            last_updated=datetime.now().isoformat()
        )
        
        # Thumbnail templates
        self.brand_assets["youtube_thumbnail_template"] = BrandAsset(
            asset_type="template",
            name="YouTube Thumbnail Template",
            file_path="assets/templates/youtube_thumbnail.psd",
            properties={
                "dimensions": "1280x720",
                "format": "PSD",
                "layers": ["background", "main_text", "accent_text", "logo", "effects"]
            },
            usage_guidelines=[
                "Use Orbitron font for main text",
                "Apply neon glow effects",
                "Maintain high contrast",
                "Include brand colors"
            ],
            last_updated=datetime.now().isoformat()
        )
    
    def _initialize_content_templates(self):
        """Initialize content templates"""
        self.content_templates["youtube_short_finance"] = ContentTemplate(
            template_id="yt_short_finance_001",
            name="YouTube Short - Finance Tips",
            category="educational_short_form",
            brand_elements=["logo_watermark", "neon_text_overlay", "brand_colors"],
            style_requirements={
                "duration": "15-60 seconds",
                "hook_timing": "0-3 seconds",
                "visual_style": "high_energy_neon",
                "text_style": "bold_contrasting"
            },
            content_structure={
                "hook": "attention_grabbing_question_or_statement",
                "problem": "relatable_finance_challenge",
                "solution": "actionable_tip_or_strategy",
                "cta": "follow_for_more_engage_comment"
            },
            performance_metrics={
                "avg_retention": 0.75,
                "engagement_rate": 0.08,
                "conversion_rate": 0.03
            }
        )
    
    def generate_branded_content(self, content_type: str, topic: str, platform: str = "youtube") -> Dict[str, Any]:
        """Generate content following unified brand guidelines"""
        try:
            # Get platform-specific adaptations
            platform_config = self.platform_adaptations.get(platform, {})
            
            # Get content template
            template_key = f"{platform}_{content_type}"
            template = self._get_best_template(template_key, content_type)
            
            # Generate branded content
            content = {
                "title": self._generate_branded_title(topic, platform),
                "description": self._generate_branded_description(topic, platform),
                "visual_guidelines": self._get_visual_guidelines(platform),
                "brand_elements": self._get_required_brand_elements(platform),
                "style_requirements": template.style_requirements if template else {},
                "performance_targets": template.performance_metrics if template else {}
            }
            
            # Add platform-specific elements
            if platform == "youtube":
                content["thumbnail_specs"] = self._get_thumbnail_specifications()
                content["end_screen_elements"] = self._get_end_screen_elements()
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating branded content: {e}")
            return {}
    
    def _generate_branded_title(self, topic: str, platform: str) -> str:
        """Generate platform-optimized branded title"""
        import random
        
        hooks = self.content_guidelines["viral_elements"]["hooks"]
        hook_template = random.choice(hooks)
        title = hook_template.format(topic=topic)
        
        # Platform-specific optimizations
        if platform == "youtube":
            # Add power words for YouTube algorithm
            power_words = ["REVEALED", "SECRET", "PROVEN", "ULTIMATE", "SHOCKING"]
            power_word = random.choice(power_words)
            title = f"{power_word}: {title}"
        
        return title
    
    def _generate_branded_description(self, topic: str, platform: str) -> str:
        """Generate platform-optimized branded description"""
        base_description = f"""
🚀 Ready to level up your {topic} game?

In this video, I break down the exact strategies that actually work for {topic}. No fluff, just results.

💰 What you'll learn:
✅ The #1 mistake people make with {topic}
✅ My proven {topic} framework
✅ Real examples and case studies
✅ Action steps you can implement today

🔥 TIMESTAMPS:
0:00 - Hook & Overview
0:30 - The Problem
1:00 - The Solution
2:00 - Real Examples
3:00 - Action Steps

💎 CONNECT WITH ME:
📱 Follow for daily finance tips
💬 Drop your questions in the comments
🔔 Hit that notification bell

#PixelFinance #FinanceTips #{topic.replace(' ', '')}
        """
        
        return base_description.strip()
    
    def _get_visual_guidelines(self, platform: str) -> Dict[str, Any]:
        """Get visual guidelines for platform"""
        base_guidelines = {
            "color_palette": self.visual_system["primary_palette"],
            "typography": self.visual_system["typography"],
            "style": "neon_pixel_aesthetic"
        }
        
        platform_specific = self.platform_adaptations.get(platform, {})
        base_guidelines.update(platform_specific)
        
        return base_guidelines
    
    def _get_required_brand_elements(self, platform: str) -> List[str]:
        """Get required brand elements for platform"""
        base_elements = ["logo", "brand_colors", "consistent_typography"]
        
        platform_elements = self.platform_adaptations.get(platform, {}).get("branding_elements", [])
        
        return base_elements + platform_elements
    
    def _get_thumbnail_specifications(self) -> Dict[str, Any]:
        """Get YouTube thumbnail specifications"""
        return {
            "dimensions": "1280x720",
            "format": "JPG or PNG",
            "file_size": "< 2MB",
            "style_requirements": {
                "background": "dark with neon accents",
                "text": "large, bold, high contrast",
                "colors": "brand palette with high saturation",
                "composition": "rule of thirds, clear focal point"
            },
            "brand_elements": {
                "logo_placement": "bottom right corner",
                "logo_size": "10% of thumbnail width",
                "color_scheme": "neon_cyber_aesthetic"
            }
        }
    
    def _get_end_screen_elements(self) -> Dict[str, Any]:
        """Get YouTube end screen elements"""
        return {
            "subscribe_button": {
                "position": "center_left",
                "style": "neon_glow_effect",
                "text": "LEVEL UP YOUR WEALTH"
            },
            "related_video": {
                "position": "center_right",
                "selection": "best_performing_similar_topic"
            },
            "playlist": {
                "position": "bottom_center",
                "title": "Complete Finance Mastery Series"
            }
        }
    
    def _get_best_template(self, template_key: str, content_type: str) -> Optional[ContentTemplate]:
        """Get best matching content template"""
        # Try exact match first
        if template_key in self.content_templates:
            return self.content_templates[template_key]
        
        # Try partial matches
        for key, template in self.content_templates.items():
            if content_type in key or content_type in template.category:
                return template
        
        return None
    
    def validate_brand_compliance(self, content: Dict[str, Any]) -> Dict[str, float]:
        """Validate content against brand guidelines"""
        scores = {
            "visual_consistency": 0.0,
            "voice_alignment": 0.0,
            "brand_element_usage": 0.0,
            "platform_optimization": 0.0,
            "overall_score": 0.0
        }
        
        try:
            # Check visual consistency
            if "visual_guidelines" in content:
                scores["visual_consistency"] = 0.9  # Placeholder scoring
            
            # Check voice alignment
            if "description" in content:
                description = content["description"].lower()
                voice_keywords = ["level up", "proven", "results", "strategy"]
                voice_score = sum(1 for keyword in voice_keywords if keyword in description) / len(voice_keywords)
                scores["voice_alignment"] = voice_score
            
            # Check brand elements
            if "brand_elements" in content:
                scores["brand_element_usage"] = 0.8  # Placeholder scoring
            
            # Calculate overall score
            scores["overall_score"] = sum(scores.values()) / len([s for s in scores.values() if s > 0])
            
        except Exception as e:
            self.logger.error(f"Error validating brand compliance: {e}")
        
        return scores
    
    def get_brand_summary(self) -> Dict[str, Any]:
        """Get comprehensive brand summary"""
        return {
            "identity": self.brand_identity,
            "visual_system": self.visual_system,
            "content_guidelines": self.content_guidelines,
            "platform_adaptations": self.platform_adaptations,
            "asset_count": len(self.brand_assets),
            "template_count": len(self.content_templates),
            "performance": self.brand_performance
        }
    
    def update_brand_performance(self, metrics: Dict[str, Any]):
        """Update brand performance metrics"""
        try:
            self.brand_performance.update(metrics)
            
            # Save to file for persistence
            performance_file = self.brand_data_dir / "brand_performance.json"
            with open(performance_file, 'w') as f:
                json.dump(self.brand_performance, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error updating brand performance: {e}")