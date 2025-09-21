"""
Auto-Blog Manager - Handles WordPress and Dev.to publishing
"""

import logging
import asyncio
from typing import Any, Dict, List
import requests
import os
from datetime import datetime

class BlogManager:
    """Manages automated blog posting"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.wordpress_api_key = os.getenv('WORDPRESS_API_KEY')
        self.devto_api_key = os.getenv('DEVTO_API_KEY')
        
    async def create_blog_post(self, content: Dict) -> Dict:
        """Create and publish blog post across platforms"""
        results = {}
        
        # WordPress
        if self.wordpress_api_key:
            wp_result = await self.publish_to_wordpress(content)
            results['wordpress'] = wp_result
        
        # Dev.to
        if self.devto_api_key:
            devto_result = await self.publish_to_devto(content)
            results['devto'] = devto_result
        
        return results
    
    async def publish_to_wordpress(self, content: Dict) -> Dict:
        """Publish to WordPress"""
        try:
            post_data = {
                'title': content['title'],
                'content': content['content'],
                'status': 'publish',
                'categories': content.get('categories', []),
                'tags': content.get('tags', []),
                'featured_media': content.get('featured_image_id')
            }
            
            headers = {
                'Authorization': f'Bearer {self.wordpress_api_key}',
                'Content-Type': 'application/json'
            }
            
            # WordPress REST API endpoint
            response = requests.post(
                f"{content.get('wordpress_url', 'https://your-site.com')}/wp-json/wp/v2/posts",
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 201:
                result = response.json()
                return {'success': True, 'post_id': result['id'], 'url': result['link']}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            self.logger.error(f"WordPress publishing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def publish_to_devto(self, content: Dict) -> Dict:
        """Publish to Dev.to"""
        try:
            article_data = {
                'article': {
                    'title': content['title'],
                    'body_markdown': content['content'],
                    'published': True,
                    'tags': content.get('tags', [])[:4],  # Dev.to allows max 4 tags
                    'canonical_url': content.get('canonical_url')
                }
            }
            
            headers = {
                'api-key': self.devto_api_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'https://dev.to/api/articles',
                headers=headers,
                json=article_data
            )
            
            if response.status_code == 201:
                result = response.json()
                return {'success': True, 'article_id': result['id'], 'url': result['url']}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            self.logger.error(f"Dev.to publishing failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def generate_blog_content(self, topic: str, content_type: str = 'tutorial') -> Dict:
        """Generate blog content from video content"""
        # Convert video content to blog format
        blog_content = {
            'title': f"Complete Guide to {topic}",
            'content': await self.create_blog_content(topic, content_type),
            'tags': await self.generate_tags(topic),
            'categories': [content_type.title()],
            'seo_description': f"Learn everything about {topic} in this comprehensive guide."
        }
        
        return blog_content
    
    async def create_blog_content(self, topic: str, content_type: str) -> str:
        """Create formatted blog content"""
        # Template for blog content
        content = f"""
# Complete Guide to {topic}

## Introduction

Welcome to this comprehensive guide about {topic}. In this article, we'll cover everything you need to know.

## What You'll Learn

- Key concepts and fundamentals
- Step-by-step implementation
- Best practices and tips
- Common pitfalls to avoid

## Getting Started

[Content will be generated based on the topic and video content]

## Conclusion

We've covered the essential aspects of {topic}. Apply these concepts to improve your skills.

---

*This content was automatically generated and optimized for SEO.*
        """
        
        return content
    
    async def generate_tags(self, topic: str) -> List[str]:
        """Generate relevant tags for the topic"""
        # Basic tag generation logic
        base_tags = ['tutorial', 'guide', 'howto']
        topic_tags = topic.lower().split()
        
        return base_tags + topic_tags[:3]

    # Add to BlogManager class
    async def create_seo_optimized_blog(self, content: Dict) -> Dict:
        """Create SEO-optimized blog post"""
        try:
            blog_content = {
                'title': f"💰 {content.get('title', 'Finance Guide')} - Neon Finance Tips",
                'content': f"""# {content.get('title', 'Finance Guide')}
                
    {content.get('description', 'Financial education content')}
    
    ## Key Takeaways
    - Master your money mindset
    - Build passive income streams  
    - Optimize your investment strategy
    
    *Watch the full video for detailed explanations!*
    """,
                'seo_keywords': ['finance tips', 'money management', 'passive income'],
                'meta_description': content.get('description', '')[:160],
                'status': 'published'
            }
            return blog_content
        except Exception as e:
            self.logger.error(f"Blog creation failed: {e}")
            return {'status': 'failed', 'error': str(e)}