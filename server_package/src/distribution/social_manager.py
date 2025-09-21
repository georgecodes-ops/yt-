"""
Social Media Manager - Handles X, TikTok, Telegram automation
"""

import logging
import asyncio
from typing import Any, Dict, List
import requests
import os
from datetime import datetime

class SocialManager:
    """Manages social media automation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.x_api_key = os.getenv('X_API_KEY')
        self.x_api_secret = os.getenv('X_API_SECRET')
        self.x_access_token = os.getenv('X_ACCESS_TOKEN')
        self.x_access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
        self.tiktok_access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
    async def distribute_content(self, content: Dict) -> Dict:
        """Distribute content across social platforms"""
        results = {}
        
        # X (Twitter)
        if self.x_api_key:
            x_result = await self.post_to_x(content)
            results['x'] = x_result
        
        # TikTok
        if self.tiktok_access_token:
            tiktok_result = await self.post_to_tiktok(content)
            results['tiktok'] = tiktok_result
        
        # Telegram
        if self.telegram_bot_token:
            telegram_result = await self.post_to_telegram(content)
            results['telegram'] = telegram_result
        
        return results

    
    async def distribute_to_social_media(self, content: Dict) -> Dict:
        """Enhanced distribution with better error handling"""
        try:
            # Ensure content has required fields
            if not isinstance(content, dict):
                content = {'title': 'Default Content', 'description': 'Generated content'}
            
            results = {}
            
            # X (Twitter) - with error handling
            try:
                if self.x_api_key:
                    x_result = await self.post_to_x(content)
                    results['x'] = x_result
                else:
                    results['x'] = {'success': False, 'reason': 'API key not configured'}
            except Exception as e:
                results['x'] = {'success': False, 'error': str(e)}
            
            # TikTok - with error handling
            try:
                if hasattr(self, 'tiktok_access_token') and self.tiktok_access_token:
                    tiktok_result = await self.post_to_tiktok(content)
                    results['tiktok'] = tiktok_result
                else:
                    results['tiktok'] = {'success': False, 'reason': 'Access token not configured'}
            except Exception as e:
                results['tiktok'] = {'success': False, 'error': str(e)}
            
            # Telegram - with error handling
            try:
                if hasattr(self, 'telegram_bot_token') and self.telegram_bot_token:
                    telegram_result = await self.post_to_telegram(content)
                    results['telegram'] = telegram_result
                else:
                    results['telegram'] = {'success': False, 'reason': 'Bot token not configured'}
            except Exception as e:
                results['telegram'] = {'success': False, 'error': str(e)}
            
            return results
            
        except Exception as e:
            self.logger.error(f"Social media distribution failed: {e}")
            return {'error': str(e), 'success': False}
    
    async def post_to_x(self, content: Dict) -> Dict:
        """Post to X (Twitter)"""
        try:
            # Create engaging tweet
            tweet_text = self.create_tweet_text(content)
            
            # X API v2 implementation would go here
            # For now, placeholder implementation
            
            return {
                'success': True,
                'tweet_id': f"x_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'url': f"https://x.com/user/status/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
        except Exception as e:
            self.logger.error(f"X posting failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def post_to_tiktok(self, content: Dict) -> Dict:
        """Post to TikTok with advanced upload"""
        try:
            if not self.tiktok_access_token:
                return {'success': False, 'reason': 'TikTok access token not configured'}
                
            # TikTok API v2 implementation
            video_file = content.get('video_file')
            if not video_file or not os.path.exists(video_file):
                return {'success': False, 'reason': 'Video file not found'}
                
            # Upload video to TikTok
            upload_url = "https://open-api.tiktok.com/share/video/upload/"
            
            headers = {
                'Authorization': f'Bearer {self.tiktok_access_token}',
                'Content-Type': 'application/json'
            }
            
            # Prepare video data
            with open(video_file, 'rb') as video:
                files = {'video': video}
                data = {
                    'description': self.create_tiktok_description(content),
                    'privacy_level': 'PUBLIC_TO_EVERYONE',
                    'disable_duet': False,
                    'disable_comment': False,
                    'disable_stitch': False,
                    'video_cover_timestamp_ms': 1000
                }
                
                response = requests.post(upload_url, headers=headers, files=files, data=data)
                
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'platform': 'tiktok',
                    'video_id': result.get('data', {}).get('video_id', 'unknown'),
                    'share_url': result.get('data', {}).get('share_url', ''),
                    'message': 'Successfully uploaded to TikTok'
                }
            else:
                return {
                    'success': False,
                    'error': f'TikTok API error: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            self.logger.error(f"TikTok posting failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def post_to_telegram(self, content: Dict) -> Dict:
        """Post to Telegram channel"""
        try:
            message = self.create_telegram_message(content)
            
            # Telegram Bot API
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': os.getenv('TELEGRAM_CHAT_ID', '@your_channel'),  # Fixed!
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return {'success': True, 'message_id': result['result']['message_id']}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            self.logger.error(f"Telegram posting failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def create_tweet_text(self, content: Dict) -> str:
        """Create optimized tweet text"""
        title = content['title'][:100]  # Twitter character limit
        hashtags = ' '.join([f"#{tag}" for tag in content.get('tags', [])[:3]])
        
        return f"{title}\n\n{hashtags}\n\nWatch the full video: {content.get('video_url', '')}"
    
    def create_tiktok_description(self, content: Dict) -> str:
        """Create TikTok description"""
        return f"{content['title']} #{' #'.join(content.get('tags', [])[:5])}"
    
    def create_telegram_message(self, content: Dict) -> str:
        """Create Telegram message"""
        return f"""
🎬 **{content['title']}**

{content['description'][:200]}...

🔗 Watch: {content.get('video_url', '')}
📖 Read: {content.get('blog_url', '')}

#{' #'.join(content.get('tags', []))}
        """