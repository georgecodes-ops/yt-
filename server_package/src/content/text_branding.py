import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re

@dataclass
class TextStyle:
    """Text styling configuration"""
    font_family: str
    font_size: int
    font_weight: str
    color: str
    line_height: float
    letter_spacing: float
    text_transform: str = "none"
    text_shadow: Optional[str] = None

@dataclass
class BrandVoice:
    """Brand voice and tone configuration"""
    tone: str
    personality_traits: List[str]
    vocabulary_style: str
    sentence_structure: str
    emotional_range: str

class TextBranding:
    """Advanced text branding system for consistent typography and voice across all content"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Pixel Finance Brand Typography System
        self.text_styles = {
            "hero_title": TextStyle(
                font_family="Orbitron",
                font_size=48,
                font_weight="bold",
                color="#00FFFF",
                line_height=1.2,
                letter_spacing=2.0,
                text_transform="uppercase",
                text_shadow="0 0 20px #00FFFF"
            ),
            "subtitle": TextStyle(
                font_family="Rajdhani",
                font_size=24,
                font_weight="medium",
                color="#FF00FF",
                line_height=1.4,
                letter_spacing=1.0,
                text_transform="capitalize"
            ),
            "body_text": TextStyle(
                font_family="Rajdhani",
                font_size=16,
                font_weight="normal",
                color="#FFFFFF",
                line_height=1.6,
                letter_spacing=0.5
            ),
            "accent_text": TextStyle(
                font_family="Orbitron",
                font_size=20,
                font_weight="bold",
                color="#FFFF00",
                line_height=1.3,
                letter_spacing=1.5,
                text_shadow="0 0 10px #FFFF00"
            ),
            "thumbnail_text": TextStyle(
                font_family="Orbitron",
                font_size=36,
                font_weight="black",
                color="#00FFFF",
                line_height=1.1,
                letter_spacing=2.0,
                text_transform="uppercase",
                text_shadow="0 0 15px #00FFFF, 0 0 30px #00FFFF"
            )
        }
        
        # Brand Voice Configuration
        self.brand_voice = BrandVoice(
            tone="energetic_professional",
            personality_traits=[
                "tech-savvy", "confident", "approachable", 
                "innovative", "results-driven", "authentic"
            ],
            vocabulary_style="modern_finance_tech",
            sentence_structure="dynamic_varied",
            emotional_range="optimistic_motivating"
        )
        
        # Content-specific text patterns
        self.content_patterns = {
            "youtube_title": {
                "hooks": [
                    "This {topic} Strategy Will Change Your Life",
                    "Why 99% of People Fail at {topic}",
                    "The {topic} Secret Nobody Talks About",
                    "How I Made ${amount} Using {topic}",
                    "{number} {topic} Tips That Actually Work"
                ],
                "power_words": [
                    "SECRET", "EXPOSED", "REVEALED", "SHOCKING", 
                    "PROVEN", "ULTIMATE", "INSTANT", "GUARANTEED"
                ]
            },
            "description": {
                "opening_hooks": [
                    "Ready to transform your financial future?",
                    "What if I told you there's a better way?",
                    "The finance game is changing, and here's how...",
                    "Stop making these costly mistakes..."
                ],
                "call_to_actions": [
                    "💰 SMASH that LIKE if this helped you!",
                    "🔔 SUBSCRIBE for daily finance tips!",
                    "💬 COMMENT your biggest finance question below!",
                    "📈 SHARE this with someone who needs to see it!"
                ]
            }
        }
        
        # Neon/Pixel aesthetic text effects
        self.neon_effects = {
            "glow_text": "text-shadow: 0 0 5px {color}, 0 0 10px {color}, 0 0 15px {color}",
            "pulse_text": "animation: pulse 2s infinite",
            "glitch_text": "animation: glitch 0.3s infinite",
            "neon_border": "border: 2px solid {color}; box-shadow: 0 0 10px {color}"
        }
    
    def apply_brand_voice(self, content: str, content_type: str = "general") -> str:
        """Apply brand voice characteristics to content"""
        try:
            # Apply tone adjustments
            if self.brand_voice.tone == "energetic_professional":
                content = self._add_energy_markers(content)
                content = self._ensure_professional_tone(content)
            
            # Apply personality traits
            content = self._inject_personality(content)
            
            # Apply content-specific patterns
            if content_type in self.content_patterns:
                content = self._apply_content_patterns(content, content_type)
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error applying brand voice: {e}")
            return content
    
    def generate_styled_title(self, topic: str, style: str = "youtube_title") -> str:
        """Generate brand-consistent titles"""
        try:
            if style == "youtube_title":
                import random
                hook_template = random.choice(self.content_patterns["youtube_title"]["hooks"])
                title = hook_template.format(topic=topic, amount="10,000", number="5")
                
                # Add power words
                power_word = random.choice(self.content_patterns["youtube_title"]["power_words"])
                title = f"{power_word}: {title}"
                
                return title
            
            return f"Master {topic} Like a Pro"
            
        except Exception as e:
            self.logger.error(f"Error generating styled title: {e}")
            return topic
    
    def get_text_style_css(self, style_name: str) -> str:
        """Get CSS for text style"""
        if style_name not in self.text_styles:
            return ""
        
        style = self.text_styles[style_name]
        css = f"""
        font-family: {style.font_family};
        font-size: {style.font_size}px;
        font-weight: {style.font_weight};
        color: {style.color};
        line-height: {style.line_height};
        letter-spacing: {style.letter_spacing}px;
        text-transform: {style.text_transform};
        """
        
        if style.text_shadow:
            css += f"text-shadow: {style.text_shadow};"
        
        return css
    
    def format_for_platform(self, content: str, platform: str) -> str:
        """Format content for specific platforms"""
        formatters = {
            "youtube": self._format_youtube,
            "instagram": self._format_instagram,
            "twitter": self._format_twitter,
            "blog": self._format_blog
        }
        
        formatter = formatters.get(platform, lambda x: x)
        return formatter(content)
    
    def _add_energy_markers(self, content: str) -> str:
        """Add energetic elements to content"""
        energy_markers = ["💰", "🚀", "⚡", "🔥", "💎", "📈"]
        import random
        
        # Add energy markers to key points
        sentences = content.split(". ")
        for i, sentence in enumerate(sentences):
            if i % 3 == 0 and len(sentence) > 20:  # Every 3rd sentence
                marker = random.choice(energy_markers)
                sentences[i] = f"{marker} {sentence}"
        
        return ". ".join(sentences)
    
    def _ensure_professional_tone(self, content: str) -> str:
        """Ensure professional tone while maintaining energy"""
        # Replace overly casual terms
        replacements = {
            "gonna": "going to",
            "wanna": "want to",
            "gotta": "need to",
            "yeah": "yes",
            "nah": "no"
        }
        
        for casual, professional in replacements.items():
            content = re.sub(r'\b' + casual + r'\b', professional, content, flags=re.IGNORECASE)
        
        return content
    
    def _inject_personality(self, content: str) -> str:
        """Inject brand personality traits"""
        # Add confidence markers
        confidence_phrases = [
            "Here's the truth:",
            "Let me be clear:",
            "This is proven:",
            "The data shows:"
        ]
        
        # Add authenticity markers
        authenticity_phrases = [
            "From my experience,",
            "I've seen this work because",
            "Real talk:",
            "Here's what actually happens:"
        ]
        
        # Randomly inject personality markers
        import random
        if random.random() < 0.3:  # 30% chance
            phrase = random.choice(confidence_phrases + authenticity_phrases)
            content = f"{phrase} {content}"
        
        return content
    
    def _apply_content_patterns(self, content: str, content_type: str) -> str:
        """Apply content-specific patterns"""
        patterns = self.content_patterns.get(content_type, {})
        
        if content_type == "description" and "call_to_actions" in patterns:
            import random
            cta = random.choice(patterns["call_to_actions"])
            content = f"{content}\n\n{cta}"
        
        return content
    
    def _format_youtube(self, content: str) -> str:
        """Format for YouTube"""
        # Add timestamps, chapters, etc.
        return content
    
    def _format_instagram(self, content: str) -> str:
        """Format for Instagram"""
        # Add hashtags, line breaks
        hashtags = "\n\n#PixelFinance #FinanceTips #WealthBuilding #InvestmentStrategy #MoneyMindset"
        return f"{content}{hashtags}"
    
    def _format_twitter(self, content: str) -> str:
        """Format for Twitter"""
        # Truncate and add thread markers
        if len(content) > 240:
            content = content[:237] + "..."
        return content
    
    def _format_blog(self, content: str) -> str:
        """Format for blog"""
        # Add proper paragraphs, headers
        return content
    
    def validate_brand_consistency(self, content: str) -> Dict[str, bool]:
        """Validate content against brand guidelines"""
        checks = {
            "has_brand_voice": any(trait in content.lower() for trait in ["finance", "money", "wealth", "invest"]),
            "appropriate_tone": not any(word in content.lower() for word in ["boring", "complicated", "impossible"]),
            "includes_energy": any(marker in content for marker in ["💰", "🚀", "⚡", "🔥", "💎", "📈"]),
            "professional_language": not any(word in content.lower() for word in ["gonna", "wanna", "gotta"])
        }
        
        return checks