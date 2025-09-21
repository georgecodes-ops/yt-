#!/usr/bin/env python3
"""
MINIMAL YOUTUBE UPLOADER - WORKING VERSION
Only includes what's needed to create and upload videos to YouTube
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MinimalYouTubeUploader:
    """Minimal working YouTube uploader"""
    
    def __init__(self):
        self.logger = logger
        
        # Initialize only essential components
        self.tts_generator = None
        self.video_processor = None
        self.wan_video_generator = None
        self.upload_manager = None
        
        # Initialize components
        self._init_components()
    
    def _init_components(self):
        """Initialize only working components"""
        try:
            # TTS Generator
            from content.tts_generator import TTSGenerator
            self.tts_generator = TTSGenerator()
            self.logger.info("✅ TTS Generator loaded")
        except Exception as e:
            self.logger.error(f"❌ TTS Generator failed: {e}")
        
        try:
            # Video Processor
            from content.video_processor import VideoProcessor
            self.video_processor = VideoProcessor()
            self.logger.info("✅ Video Processor loaded")
        except Exception as e:
            self.logger.error(f"❌ Video Processor failed: {e}")
        
        try:
            # WAN Video Generator
            from content.wan_video_generator import WanVideoGenerator
            self.wan_video_generator = WanVideoGenerator()
            self.logger.info("✅ WAN Video Generator loaded")
        except Exception as e:
            self.logger.error(f"❌ WAN Video Generator failed: {e}")
        
        try:
            # Upload Manager
            from distribution.enhanced_upload_manager import EnhancedUploadManager
            self.upload_manager = EnhancedUploadManager()
            self.logger.info("✅ Upload Manager loaded")
        except Exception as e:
            self.logger.error(f"❌ Upload Manager failed: {e}")
    
    async def create_and_upload_video(self, topic: str = "Finance Tips"):
        """Create and upload a single video"""
        try:
            self.logger.info(f"🎬 Starting video creation for: {topic}")
            
            # Step 1: Generate script
            script = f"""
            Welcome to MonAY Finance! Today we're talking about {topic}.
            
            Here are 3 key points:
            1. Always diversify your investments
            2. Start investing early for compound growth
            3. Keep emergency funds for unexpected expenses
            
            Thanks for watching! Subscribe for more finance tips!
            """
            
            self.logger.info("✅ Script generated")
            
            # Step 2: Generate audio
            if not self.tts_generator:
                raise Exception("TTS Generator not available")
            
            audio_path = await self.tts_generator.generate_audio(script)
            if not audio_path or not os.path.exists(audio_path):
                raise Exception(f"Audio generation failed: {audio_path}")
            
            self.logger.info(f"✅ Audio generated: {audio_path}")
            
            # Step 3: Create video
            if not self.video_processor:
                raise Exception("Video Processor not available")
            
            video_path = self.video_processor.create_shorts_video(script, audio_path)
            if not video_path or not os.path.exists(video_path):
                raise Exception(f"Video creation failed: {video_path}")
            
            self.logger.info(f"✅ Video created: {video_path}")
            
            # Step 4: Upload to YouTube
            if not self.upload_manager:
                raise Exception("Upload Manager not available")
            
            upload_result = await self.upload_manager.upload_video(
                video_path=video_path,
                title=f"{topic} - MonAY Finance Tips",
                description=f"Learn about {topic} with MonAY Finance. Subscribe for more tips!",
                tags=["finance", "money", "investing", "tips"]
            )
            
            self.logger.info(f"✅ Video uploaded: {upload_result}")
            
            return {
                'status': 'success',
                'video_path': video_path,
                'upload_result': upload_result
            }
            
        except Exception as e:
            error_msg = f"❌ Video creation/upload failed: {e}"
            self.logger.error(error_msg)
            
            # Send Discord alert
            await self._send_discord_alert("🚨 VIDEO UPLOAD FAILURE", error_msg)
            
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def _send_discord_alert(self, title: str, message: str):
        """Send Discord alert for failures"""
        try:
            import aiohttp
            
            discord_webhook = os.getenv('DISCORD_WEBHOOK_URL', 
                'https://discordapp.com/api/webhooks/1419039543092580353/Ezdmf0-_aZblEbJNCf2w1Ivr6Fo-Uax_rri3QUti4nkmmrJD6rmr6rP9tjN8wIIZscxA')
            
            payload = {
                "embeds": [{
                    "title": title,
                    "description": message,
                    "color": 16711680,  # Red
                    "timestamp": datetime.now().isoformat(),
                    "footer": {"text": "MonAY Minimal System"}
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(discord_webhook, json=payload) as response:
                    if response.status == 204:
                        self.logger.info("✅ Discord alert sent")
                    else:
                        self.logger.error(f"❌ Discord alert failed: {response.status}")
                        
        except Exception as e:
            self.logger.error(f"Discord alert error: {e}")

async def main():
    """Main function"""
    try:
        uploader = MinimalYouTubeUploader()
        
        # Test video creation and upload
        result = await uploader.create_and_upload_video("Smart Investing Strategies")
        
        if result['status'] == 'success':
            print("🎉 SUCCESS: Video created and uploaded!")
        else:
            print(f"❌ FAILED: {result['error']}")
            
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())