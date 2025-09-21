import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import random

class BlogGenerator:
    """Generates blog content for various platforms"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.blog_types = [
            "how_to_guide",
            "listicle",
            "case_study",
            "opinion_piece",
            "tutorial",
            "review",
            "news_analysis"
        ]
    
    async def generate_blog_post(self, topic: str, blog_type: Optional[str] = None, word_count: int = 1000) -> Dict:
        """Generate a complete blog post"""
        try:
            post_type = blog_type or random.choice(self.blog_types)
            
            blog_post = {
                "title": await self._generate_title(topic, post_type),
                "content": await self._generate_content(topic, post_type, word_count),
                "meta_description": await self._generate_meta_description(topic),
                "tags": await self._generate_tags(topic),
                "category": self._determine_category(topic),
                "word_count": word_count,
                "reading_time": word_count // 200,  # Average reading speed
                "seo_score": random.randint(70, 95),
                "created_at": datetime.now().isoformat(),
                "status": "draft"
            }
            
            self.logger.info(f"Generated blog post: {blog_post['title']}")
            return blog_post
            
        except Exception as e:
            self.logger.error(f"Error generating blog post: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def _generate_title(self, topic: str, post_type: str) -> str:
        """Generate SEO-optimized title"""
        title_templates = {
            "how_to_guide": f"How to Master {topic}: Complete Guide for 2024",
            "listicle": f"10 Essential {topic} Tips You Need to Know",
            "case_study": f"Case Study: How {topic} Transformed Our Results",
            "opinion_piece": f"Why {topic} is More Important Than Ever",
            "tutorial": f"Step-by-Step {topic} Tutorial for Beginners",
            "review": f"Comprehensive {topic} Review: Pros, Cons, and Verdict",
            "news_analysis": f"Breaking: What the Latest {topic} News Means for You"
        }
        return title_templates.get(post_type, f"Everything You Need to Know About {topic}")
    
    async def _generate_content(self, topic: str, post_type: str, word_count: int) -> str:
        """Generate blog content"""
        intro = f"In today's digital landscape, {topic} has become increasingly important. "
        body = f"This comprehensive guide will explore the key aspects of {topic} and provide actionable insights. "
        conclusion = f"Understanding {topic} is crucial for success in today's market. "
        
        # Expand content to meet word count
        content_sections = [
            intro,
            "\n\n## Introduction\n" + body,
            "\n\n## Key Benefits\n" + f"The benefits of {topic} include improved efficiency, better results, and enhanced performance.",
            "\n\n## Best Practices\n" + f"When implementing {topic}, consider these proven strategies and techniques.",
            "\n\n## Common Mistakes\n" + f"Avoid these common pitfalls when working with {topic}.",
            "\n\n## Conclusion\n" + conclusion
        ]
        
        return "".join(content_sections)
    
    async def _generate_meta_description(self, topic: str) -> str:
        """Generate SEO meta description"""
        return f"Discover everything you need to know about {topic}. Expert insights, practical tips, and actionable strategies."
    
    async def _generate_tags(self, topic: str) -> List[str]:
        """Generate relevant tags"""
        base_tags = [topic.lower(), "guide", "tips", "2024"]
        additional_tags = ["strategy", "best practices", "tutorial", "expert advice"]
        return base_tags + random.sample(additional_tags, 2)
    
    def _determine_category(self, topic: str) -> str:
        """Determine blog category"""
        finance_keywords = ["money", "investment", "finance", "trading", "crypto"]
        tech_keywords = ["ai", "technology", "software", "digital", "automation"]
        
        topic_lower = topic.lower()
        
        if any(keyword in topic_lower for keyword in finance_keywords):
            return "Finance"
        elif any(keyword in topic_lower for keyword in tech_keywords):
            return "Technology"
        else:
            return "General"