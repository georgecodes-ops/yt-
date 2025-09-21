import asyncio
import logging
from typing import Dict, List
from pathlib import Path

class PlatformOptimizer:
    """Optimize content for each platform's algorithm"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.platform_specs = {
            'youtube_shorts': {
                'max_duration': 60,
                'aspect_ratio': '9:16',
                'optimal_length': 15,
                'hook_time': 3
            },
            'tiktok': {
                'max_duration': 180,
                'aspect_ratio': '9:16',
                'optimal_length': 30,
                'hook_time': 2
            },
            'instagram_reels': {
                'max_duration': 90,
                'aspect_ratio': '9:16',
                'optimal_length': 30,
                'hook_time': 3
            }
        }
    
    async def initialize(self):
        """Initialize the PlatformOptimizer"""
        self.logger.info(f"Initializing PlatformOptimizer...")
        try:
            # Basic initialization
            self.logger.info(f"PlatformOptimizer initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"PlatformOptimizer initialization failed: {e}")
            return False

    async def optimize_for_platform(self, content: Dict, platform: str) -> Dict:
        """Automatically optimize content for specific platform"""
        specs = self.platform_specs.get(platform, self.platform_specs['youtube_shorts'])
        
        optimized_content = {
            'title': await self.optimize_title(content.get('title', ''), platform),
            'description': await self.optimize_description(content.get('description', ''), platform),
            'hashtags': await self.optimize_hashtags(content.get('tags', []), platform),
            'video': await self.optimize_video(content.get('video_path', ''), specs),
            'thumbnail': await self.optimize_thumbnail(content.get('thumbnail', ''), platform)
        }
        
        return optimized_content
    
    async def optimize_title(self, title: str, platform: str) -> str:
        """Optimize title for platform"""
        if platform == 'tiktok':
            return title[:100]  # TikTok title limit
        elif platform == 'youtube_shorts':
            return title[:100]  # YouTube Shorts title limit
        else:
            return title[:150]  # Instagram limit
    
    async def optimize_description(self, description: str, platform: str) -> str:
        """Optimize description for platform"""
        if platform == 'tiktok':
            return description[:2200]  # TikTok description limit
        elif platform == 'youtube_shorts':
            return description[:5000]  # YouTube description limit
        else:
            return description[:2200]  # Instagram limit
    
    async def optimize_hashtags(self, tags: list, platform: str) -> list:
        """Optimize hashtags for platform"""
        if platform == 'tiktok':
            return tags[:5]  # TikTok optimal hashtag count
        elif platform == 'instagram_reels':
            return tags[:10]  # Instagram optimal hashtag count
        else:
            return tags[:3]  # YouTube Shorts optimal hashtag count
    
    async def optimize_video(self, video_path: str, specs: Dict) -> str:
        """Optimize video for platform specifications"""
        try:
            if not video_path or not Path(video_path).exists():
                return video_path
            
            # Return original path for now - video optimization would require FFmpeg
            return video_path
        except Exception as e:
            self.logger.error(f"Video optimization failed: {e}")
            return video_path
    
    async def optimize_thumbnail(self, thumbnail_path: str, platform: str) -> str:
        """Optimize thumbnail for platform"""
        try:
            if not thumbnail_path or not Path(thumbnail_path).exists():
                return thumbnail_path
            # Return original path for now - thumbnail optimization would require PIL
            return thumbnail_path
        except Exception as e:
            self.logger.error(f"Thumbnail optimization failed: {e}")
            return thumbnail_path
    async def optimize_for_platforms(self, content: Dict, platforms: List[str]) -> Dict:
        """Optimize content for multiple platforms"""
        try:
            optimization_results = {
                'original_content': content,
                'platform_optimizations': {},
                'success_count': 0,
                'total_platforms': len(platforms)
            }
            
            for platform in platforms:
                try:
                    optimized = await self.optimize_for_platform(content, platform)
                    optimization_results['platform_optimizations'][platform] = {
                        'status': 'success',
                        'optimized_content': optimized,
                        'changes_applied': self._get_optimization_changes(content, optimized)
                    }
                    optimization_results['success_count'] += 1
                    
                except Exception as e:
                    optimization_results['platform_optimizations'][platform] = {
                        'status': 'failed',
                        'error': str(e),
                        'fallback_content': content
                    }
            
            optimization_results['success_rate'] = (
                optimization_results['success_count'] / optimization_results['total_platforms']
            ) if optimization_results['total_platforms'] > 0 else 0.0
            
            return optimization_results
            
        except Exception as e:
            self.logger.error(f"Multi-platform optimization failed: {e}")
            return {
                'error': str(e),
                'platform_optimizations': {},
                'success_count': 0,
                'total_platforms': len(platforms)
            }
    
    def _get_optimization_changes(self, original: Dict, optimized: Dict) -> List[str]:
        """Get list of changes applied during optimization"""
        changes = []
        
        if original.get('title') != optimized.get('title'):
            changes.append('title_optimized')
        if original.get('description') != optimized.get('description'):
            changes.append('description_optimized')
        if original.get('hashtags') != optimized.get('hashtags'):
            changes.append('hashtags_optimized')
            
        return changes

