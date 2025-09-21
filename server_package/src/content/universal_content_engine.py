import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import random
from .ollama_client import OllamaClient

class UniversalContentEngine:
    """Universal content generation engine for multiple formats with AI integration"""
    
    def __init__(self, use_ai: bool = True):
        self.logger = logging.getLogger(__name__)
        self.use_ai = use_ai
        self.ollama_client = OllamaClient() if use_ai else None
        self.content_formats = [
            "video_script",
            "blog_post",
            "social_media",
            "email_newsletter",
            "podcast_script",
            "infographic_content",
            "course_material"
        ]
    
    def set_research_context(self, research_data: Dict):
        """Set research data context for AI content generation"""
        self._current_research_data = research_data
        
    async def generate_universal_content(self, 
                                       topic: str, 
                                       format_type: str = "video_script",
                                       target_audience: str = "general",
                                       tone: str = "professional",
                                       research_data: Optional[Dict] = None) -> Dict:
        """Generate content in any format"""
        try:
            # Set research context if provided
            if research_data:
                self.set_research_context(research_data)
                
            content = {
                "topic": topic,
                "format": format_type,
                "audience": target_audience,
                "tone": tone,
                "content": await self._generate_format_specific_content(topic, format_type, target_audience, tone),
                "metadata": await self._generate_metadata(topic, format_type),
                "optimization_suggestions": await self._generate_optimization_tips(format_type),
                "created_at": datetime.now().isoformat(),
                "version": "1.0",
                "ai_generated": self.use_ai and self.ollama_client and self.ollama_client.check_health()
            }
            
            self.logger.info(f"Generated universal content: {format_type} for {topic}")
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating universal content: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def _generate_format_specific_content(self, topic: str, format_type: str, audience: str, tone: str) -> Dict:
        """Generate content specific to format"""
        generators = {
            "video_script": self._generate_video_script,
            "blog_post": self._generate_blog_content,
            "social_media": self._generate_social_content,
            "email_newsletter": self._generate_email_content,
            "podcast_script": self._generate_podcast_script,
            "infographic_content": self._generate_infographic_content,
            "course_material": self._generate_course_content
        }
        
        generator = generators.get(format_type, self._generate_generic_content)
        return await generator(topic, audience, tone)
    
    async def _generate_video_script(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate video script using AI or templates"""
        if self.use_ai and self.ollama_client and self.ollama_client.check_health():
            # Use AI generation with research context
            research_data = getattr(self, '_current_research_data', {})
            ai_result = await self.ollama_client.generate_video_script(
                topic=topic,
                research_data=research_data,
                target_audience=audience,
                tone=tone
            )
            
            if ai_result.get('status') == 'success':
                return ai_result['content']
            else:
                self.logger.warning("AI generation failed, falling back to template")
        
        # Fallback to template-based generation
        return {
            "hook": f"Are you ready to master {topic}? In the next few minutes, I'll show you exactly how.",
            "introduction": f"Welcome back to the channel! Today we're diving deep into {topic}.",
            "main_content": f"Let's break down {topic} into actionable steps you can implement today.",
            "call_to_action": "If you found this helpful, smash that like button and subscribe for more content!",
            "estimated_duration": "8-12 minutes",
            "scene_directions": ["Close-up intro", "Screen recording", "B-roll footage", "Outro with subscribe button"]
        }
    
    async def _generate_blog_content(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate blog post content"""
        return {
            "title": f"The Ultimate Guide to {topic} in 2024",
            "introduction": f"In this comprehensive guide, we'll explore everything you need to know about {topic}.",
            "main_sections": [
                f"What is {topic}?",
                f"Why {topic} Matters",
                f"How to Get Started with {topic}",
                f"Advanced {topic} Strategies",
                "Conclusion and Next Steps"
            ],
            "word_count": 2000,
            "reading_time": "10 minutes"
        }
    
    async def _generate_social_content(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate social media content"""
        return {
            "twitter": f"🚀 Just discovered this game-changing approach to {topic}! Thread below 👇",
            "linkedin": f"Professional insight: How {topic} is transforming the industry",
            "instagram": f"✨ {topic} made simple! Swipe for tips ➡️",
            "facebook": f"Let's talk about {topic} - what's your experience?",
            "hashtags": [f"#{topic.replace(' ', '')}", "#tips", "#strategy", "#growth"]
        }
    
    async def _generate_email_content(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate email newsletter content"""
        return {
            "subject_line": f"Your {topic} strategy needs this update",
            "preview_text": f"The latest insights on {topic} you can't miss",
            "body": f"Hi there! This week I want to share some exciting developments in {topic}...",
            "cta": "Read the full article",
            "footer": "Thanks for reading! Reply with your thoughts."
        }
    
    async def _generate_podcast_script(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate podcast script"""
        return {
            "intro_music": "[Upbeat intro music]",
            "host_intro": f"Welcome to the show! I'm your host, and today we're exploring {topic}.",
            "main_discussion": f"Let's dive into the fascinating world of {topic}...",
            "sponsor_break": "[Sponsor message]",
            "conclusion": "That's a wrap on today's episode!",
            "outro_music": "[Outro music]",
            "estimated_length": "25-30 minutes"
        }
    
    async def _generate_infographic_content(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate infographic content"""
        return {
            "title": f"{topic}: By the Numbers",
            "sections": [
                {"header": "Key Statistics", "content": "Important numbers and data"},
                {"header": "Step-by-Step Process", "content": "Visual workflow"},
                {"header": "Tips & Tricks", "content": "Quick actionable advice"},
                {"header": "Resources", "content": "Links and references"}
            ],
            "color_scheme": "Professional blue and white",
            "layout": "Vertical flow"
        }
    
    async def _generate_course_content(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate course material"""
        return {
            "course_title": f"Mastering {topic}: Complete Course",
            "modules": [
                f"Introduction to {topic}",
                f"Fundamentals of {topic}",
                f"Advanced {topic} Techniques",
                f"Real-world {topic} Applications",
                f"Final Project and Assessment"
            ],
            "duration": "4-6 hours",
            "difficulty": "Beginner to Intermediate",
            "learning_objectives": [f"Understand {topic} basics", f"Apply {topic} strategies", f"Master {topic} tools"]
        }
    
    async def _generate_generic_content(self, topic: str, audience: str, tone: str) -> Dict:
        """Generate generic content"""
        return {
            "content": f"Comprehensive content about {topic} tailored for {audience} with a {tone} tone.",
            "type": "generic",
            "customizable": True
        }
    
    async def _generate_metadata(self, topic: str, format_type: str) -> Dict:
        """Generate content metadata"""
        return {
            "keywords": [topic, format_type, "content", "strategy"],
            "category": self._categorize_topic(topic),
            "difficulty_level": "intermediate",
            "target_platforms": self._suggest_platforms(format_type)
        }
    
    async def _generate_optimization_tips(self, format_type: str) -> List[str]:
        """Generate optimization suggestions"""
        tips = {
            "video_script": ["Add engaging hooks", "Include clear CTAs", "Optimize for retention"],
            "blog_post": ["Use SEO keywords", "Add internal links", "Include images"],
            "social_media": ["Use trending hashtags", "Post at optimal times", "Engage with comments"],
            "email_newsletter": ["A/B test subject lines", "Personalize content", "Mobile optimize"]
        }
        return tips.get(format_type, ["Create quality content", "Know your audience", "Be consistent"])
    
    def _categorize_topic(self, topic: str) -> str:
        """Categorize the topic"""
        categories = {
            "finance": ["money", "investment", "trading", "crypto", "finance"],
            "technology": ["ai", "tech", "software", "digital", "automation"],
            "business": ["marketing", "sales", "strategy", "growth", "startup"],
            "lifestyle": ["health", "fitness", "travel", "food", "wellness"]
        }
        
        topic_lower = topic.lower()
        for category, keywords in categories.items():
            if any(keyword in topic_lower for keyword in keywords):
                return category
        return "general"
    
    def _suggest_platforms(self, format_type: str) -> List[str]:
        """Suggest optimal platforms for content type"""
        platform_mapping = {
            "video_script": ["YouTube", "TikTok", "Instagram Reels"],
            "blog_post": ["Website", "Medium", "LinkedIn Articles"],
            "social_media": ["Twitter", "LinkedIn", "Instagram", "Facebook"],
            "email_newsletter": ["Mailchimp", "ConvertKit", "Substack"],
            "podcast_script": ["Spotify", "Apple Podcasts", "Google Podcasts"]
        }
        return platform_mapping.get(format_type, ["Multiple platforms"])