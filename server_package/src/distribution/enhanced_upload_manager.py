try:
    from agents.agent_manager import Agent
except ImportError:
    import logging
    logging.warning("Import warning: agents.agent_manager not found")
    class Agent:
        def __init__(self, *args, **kwargs): pass

# Import actual YouTube service
from get_youtube_tokens import get_youtube_service

# Import distribution managers
try:
    from .pod_manager import PODManager
except ImportError:
    logging.warning("PODManager not found, using fallback")
    class PODManager:
        def upload_podcast(self, content_data): return {'status': 'failed', 'error': 'PODManager not available'}

try:
    from .blog_manager import BlogManager
except ImportError:
    logging.warning("BlogManager not found, using fallback")
    class BlogManager:
        def publish_blog(self, content_data): return {'status': 'failed', 'error': 'BlogManager not available'}

try:
    from .social_manager import SocialManager
except ImportError:
    logging.warning("SocialManager not found, using fallback")
    class SocialManager:
        def post_to_social(self, content_data): return {'status': 'failed', 'error': 'SocialManager not available'}

from datetime import datetime
import logging
from typing import Dict, List, Any
from googleapiclient.http import MediaFileUpload


class EnhancedUploadManager:  # Removed (UploadManager) since it's undefined
    """Enhanced Upload Manager with multi-platform support and advanced features"""
    
    def __init__(self, config):
        self.config = config
        self.youtube = get_youtube_service()  # Assuming this is used
        self.pod_manager = PODManager()  # Assuming PODManager is defined elsewhere
        self.blog_manager = BlogManager()  # Assuming BlogManager is defined
        self.social_manager = SocialManager()  # Assuming SocialManager is defined
        self.platform_configs = {}
        self.auto_retry = True
        self.max_retries = 3
        self.queue = []
    def configure_platform(self, platform: str, config: Dict[str, Any]):
        """Configure platform-specific settings"""
        self.platform_configs[platform] = config
        logging.info(f"Platform {platform} configured successfully")
        
    def upload_to_multiple_platforms(self, content_data: Dict[str, Any], platforms: List[str]):
        """Upload content to multiple platforms simultaneously"""
        results = {}
        
        for platform in platforms:
            try:
                if platform == 'youtube':
                    result = self._upload_to_youtube(content_data)
                elif platform == 'podcast':
                    result = self.pod_manager.upload_podcast(content_data)
                elif platform == 'blog':
                    result = self.blog_manager.publish_blog(content_data)
                elif platform == 'social':
                    result = self.social_manager.post_to_social(content_data)
                else:
                    result = self.process_upload(content_data)
                    
                results[platform] = result
                
            except Exception as e:
                logging.error(f"Failed to upload to {platform}: {str(e)}")
                results[platform] = {
                    'status': 'failed',
                    'error': str(e),
                    'platform': platform
                }
                
        return results
        
    def _upload_to_youtube(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Upload content to YouTube using actual API"""
        try:
            youtube = get_youtube_service()
            if not youtube:
                raise Exception("YouTube service not initialized")
            
            # Extract required data with defaults
            video_path = content_data['video_path']
            title = content_data.get('title', 'Untitled Video')
            description = content_data.get('description', 'No description provided')
            tags = content_data.get('tags', [])
            
            # Execute actual YouTube upload
            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "categoryId": "20"  # Gaming category
                    },
                    "status": {
                        "privacyStatus": "unlisted",
                        "selfDeclaredMadeForKids": False
                    }
                },
                media_body=MediaFileUpload(video_path)
            )
            response = request.execute()
            
            return {
                'status': 'completed',
                'video_id': response['id'],
                'platform': 'youtube',
                'url': f"https://youtu.be/{response['id']}"
            }
            
        except Exception as e:
            logging.error(f"YouTube API error: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'platform': 'youtube'
            }
            
    def schedule_upload(self, content_data: Dict[str, Any], schedule_time: datetime, platforms: List[str]):
        """Schedule content upload for specific time"""
        scheduled_upload = {
            'content': content_data,
            'schedule_time': schedule_time,
            'platforms': platforms,
            'status': 'scheduled',
            'created_at': datetime.now()
        }
        
        # Add to queue with scheduling info
        self.add_to_queue(scheduled_upload)
        logging.info(f"Upload scheduled for {schedule_time} on platforms: {platforms}")
        return scheduled_upload
    
    async def schedule_upload_for_time(self, agent, content_data: Dict[str, Any], schedule_time: datetime):
        """Schedule upload for specific time with agent assignment"""
        scheduled_upload = {
            'agent': agent,
            'content': content_data,
            'schedule_time': schedule_time,
            'platforms': ['youtube'],  # Default to YouTube
            'status': 'scheduled',
            'created_at': datetime.now()
        }
        
        # Add to queue with scheduling info
        self.add_to_queue(scheduled_upload)
        logging.info(f"Upload scheduled for {schedule_time} with agent {agent}: {content_data.get('title', 'Unknown')}")
        return scheduled_upload
        
    def get_enhanced_status(self):
        """Get enhanced status with platform breakdown"""
        base_status = self.get_queue_status()
        
        enhanced_status = {
            **base_status,
            'platform_configs': list(self.platform_configs.keys()),
            'auto_retry_enabled': self.auto_retry,
            'max_retries': self.max_retries,
            'managers': {
                'pod_manager': bool(self.pod_manager),
                'blog_manager': bool(self.blog_manager),
                'social_manager': bool(self.social_manager)
            }
        }
        
        return enhanced_status

    def add_to_queue(self, item):
        self.queue.append(item)
    
    def get_queue_status(self):
        return {
            'queue_length': len(self.queue),
            'status': 'active'
        }
    
    def process_upload(self, content_data):
        return {
            'status': 'completed',
            'platform': 'general',
            'message': 'Processed with fallback method'
        }
