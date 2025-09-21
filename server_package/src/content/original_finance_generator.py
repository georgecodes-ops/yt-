try:
    from .ai_image_generator import AIImageGenerator # type: ignore
except ImportError:
    import logging
    logging.warning("Import warning: ai_image_generator not found")
    class AIImageGenerator:
        async def generate_image(self, *args, **kwargs): return {"image_path": "placeholder.jpg"}

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

class OriginalFinanceGenerator:
    """Original Finance Content Generator with unique perspectives and insights"""
    
    def __init__(self):
        self.ai_image_generator = AIImageGenerator()
        self.content_themes = [
            "Personal Finance Mastery",
            "Investment Psychology",
            "Wealth Building Strategies",
            "Financial Independence",
            "Market Analysis",
            "Cryptocurrency Insights",
            "Real Estate Investment",
            "Passive Income Streams",
            "Financial Planning",
            "Economic Trends"
        ]
        
        self.content_formats = [
            "educational_deep_dive",
            "quick_tips",
            "case_study",
            "market_analysis",
            "beginner_guide",
            "advanced_strategy",
            "myth_busting",
            "trend_spotlight"
        ]
    
    async def generate_original_content(self, topic: Optional[str] = None, format_type: Optional[str] = None) -> Dict[str, Any]:
        """Generate original finance content with unique insights"""
        try:
            # Select theme and format
            theme = topic or random.choice(self.content_themes)
            content_format = format_type or random.choice(self.content_formats)
            
            # Generate content based on format
            content = await self._create_content_by_format(theme, content_format)
            
            # Generate accompanying image
            image_result = await self.ai_image_generator.generate_image(
                prompt=f"Professional finance illustration for {theme}",
                style="modern_professional"
            )
            
            return {
                "theme": theme,
                "format": content_format,
                "title": content["title"],
                "content": content["body"],
                "key_points": content["key_points"],
                "call_to_action": content["cta"],
                "image_path": image_result.get("image_path", "placeholder.jpg"),
                "tags": content["tags"],
                "estimated_read_time": content["read_time"],
                "difficulty_level": content["difficulty"],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Content generation failed: {str(e)}",
                "fallback_content": await self._generate_fallback_content()
            }
    
    async def _create_content_by_format(self, theme: str, format_type: str) -> Dict[str, Any]:
        """Create content based on specific format requirements"""
        
        format_templates = {
            "educational_deep_dive": {
                "title": f"The Complete Guide to {theme}: Everything You Need to Know",
                "body": f"Understanding {theme} is crucial for financial success. This comprehensive guide covers the fundamentals, advanced strategies, and practical applications that can transform your financial future.",
                "key_points": [
                    f"Core principles of {theme}",
                    "Step-by-step implementation guide",
                    "Common mistakes to avoid",
                    "Advanced optimization techniques",
                    "Real-world success stories"
                ],
                "cta": "Start implementing these strategies today and see the difference in your financial growth!",
                "tags": ["education", "comprehensive", "finance", theme.lower().replace(" ", "_")],
                "read_time": "8-12 minutes",
                "difficulty": "intermediate"
            },
            
            "quick_tips": {
                "title": f"5 Quick {theme} Tips That Actually Work",
                "body": f"These proven {theme} strategies can be implemented immediately for fast results. No complex theories - just actionable advice that works.",
                "key_points": [
                    "Tip 1: Start with the basics",
                    "Tip 2: Automate your success",
                    "Tip 3: Track your progress",
                    "Tip 4: Optimize regularly",
                    "Tip 5: Stay consistent"
                ],
                "cta": "Try these tips this week and share your results!",
                "tags": ["quick_tips", "actionable", "finance", theme.lower().replace(" ", "_")],
                "read_time": "3-5 minutes",
                "difficulty": "beginner"
            },
            
            "market_analysis": {
                "title": f"Market Insights: How {theme} is Shaping Today's Economy",
                "body": f"Current market trends in {theme} reveal important opportunities and risks. This analysis breaks down what you need to know for informed decision-making.",
                "key_points": [
                    "Current market conditions",
                    "Key trend indicators",
                    "Risk assessment",
                    "Opportunity identification",
                    "Strategic recommendations"
                ],
                "cta": "Stay ahead of the market with these insights!",
                "tags": ["market_analysis", "trends", "finance", theme.lower().replace(" ", "_")],
                "read_time": "6-8 minutes",
                "difficulty": "advanced"
            }
        }
        
        # Return the template or a default one
        return format_templates.get(format_type, format_templates["educational_deep_dive"])
    
    async def _generate_fallback_content(self) -> Dict[str, Any]:
        """Generate basic fallback content when main generation fails"""
        return {
            "title": "Financial Success Fundamentals",
            "content": "Building wealth starts with understanding the basics of personal finance, investing, and smart money management.",
            "key_points": [
                "Start with a budget",
                "Build an emergency fund",
                "Invest consistently",
                "Educate yourself continuously"
            ],
            "call_to_action": "Take the first step towards financial freedom today!",
            "tags": ["finance", "basics", "wealth_building"],
            "estimated_read_time": "5 minutes",
            "difficulty_level": "beginner"
        }
    
    async def generate_series_content(self, series_theme: str, episode_count: int = 5) -> List[Dict[str, Any]]:
        """Generate a series of related finance content"""
        series_content = []
        
        for i in range(episode_count):
            episode_content = await self.generate_original_content(
                topic=f"{series_theme} - Part {i+1}",
                format_type=random.choice(self.content_formats)
            )
            episode_content["series_info"] = {
                "series_name": series_theme,
                "episode_number": i + 1,
                "total_episodes": episode_count
            }
            series_content.append(episode_content)
        
        return series_content
    
    def get_content_stats(self) -> Dict[str, Any]:
        """Get statistics about content generation capabilities"""
        return {
            "available_themes": len(self.content_themes),
            "content_formats": len(self.content_formats),
            "themes": self.content_themes,
            "formats": self.content_formats,
            "generator_status": "active",
            "last_updated": datetime.now().isoformat()
        }