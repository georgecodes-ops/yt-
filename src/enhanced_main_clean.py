#!/usr/bin/env python3
"""
Enhanced MonAY - CLEAN VERSION - YouTube Automation System
Only includes working modules, no broken imports
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Setup project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path, override=True)
sys.path.append(str(PROJECT_ROOT / "src"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ONLY IMPORT WORKING MODULES
try:
    from content.tts_generator import TTSGenerator
    TTS_AVAILABLE = True
    logging.info("✅ TTS Generator available")
except ImportError as e:
    TTS_AVAILABLE = False
    logging.warning(f"❌ TTS Generator not available: {e}")
    class TTSGenerator: pass

try:
    from content.video_processor import VideoProcessor
    VIDEO_PROCESSOR_AVAILABLE = True
    logging.info("✅ Video Processor available")
except ImportError as e:
    VIDEO_PROCESSOR_AVAILABLE = False
    logging.warning(f"❌ Video Processor not available: {e}")
    class VideoProcessor: pass

try:
    from content.wan_video_generator import WanVideoGenerator
    WAN_AVAILABLE = True
    logging.info("✅ WAN Video Generator available")
except ImportError as e:
    WAN_AVAILABLE = False
    logging.warning(f"❌ WAN Video Generator not available: {e}")
    class WanVideoGenerator: pass

try:
    from distribution.enhanced_upload_manager import EnhancedUploadManager
    UPLOAD_AVAILABLE = True
    logging.info("✅ Upload Manager available")
except ImportError as e:
    UPLOAD_AVAILABLE = False
    logging.warning(f"❌ Upload Manager not available: {e}")
    class EnhancedUploadManager: pass

try:
    from content.instant_viral_generator import InstantViralGenerator
    VIRAL_GENERATOR_AVAILABLE = True
    logging.info("✅ Viral Generator available")
except ImportError as e:
    VIRAL_GENERATOR_AVAILABLE = False
    logging.warning(f"❌ Viral Generator not available: {e}")
    class InstantViralGenerator: pass

class CleanMonAYSystem:
    """Clean MonAY system with only working components"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize only available components
        self.tts_generator = TTSGenerator() if TTS_AVAILABLE else None
        self.video_processor = VideoProcessor() if VIDEO_PROCESSOR_AVAILABLE else None
        self.wan_video_generator = WanVideoGenerator() if WAN_AVAILABLE else None
        self.upload_manager = EnhancedUploadManager() if UPLOAD_AVAILABLE else None
        self.viral_generator = InstantViralGenerator() if VIRAL_GENERATOR_AVAILABLE else None
        
        self.logger.info("🚀 Clean MonAY System initialized")
    
    async def create_and_upload_video(self, topic: str = "Finance Tips"):
        """Create and upload a video using only working components"""
        try:
            self.logger.info(f"🎬 Starting video creation: {topic}")
            
            # Step 1: Generate script
            if self.viral_generator:
                script_result = await self.viral_generator.create_viral_shorts_package(topic)
                script = script_result.get('script', f"Welcome to MonAY Finance! Today's topic: {topic}")
            else:
                script = f"""
                Welcome to MonAY Finance! Today we're discussing {topic}.
                
                Here are 3 key insights:
                1. Smart financial planning starts with clear goals
                2. Diversification reduces risk and maximizes returns  
                3. Consistent investing beats market timing
                
                Subscribe for more finance tips!
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
                title=f"{topic} - MonAY Finance",
                description=f"Learn about {topic} with MonAY Finance. Subscribe for more!",
                tags=["finance", "money", "investing", "tips"]
            )
            
            self.logger.info(f"✅ Video uploaded: {upload_result}")
            
            # Send success notification
            await self._send_discord_alert(
                "🎉 VIDEO UPLOAD SUCCESS",
                f"**Topic:** {topic}\n**Video:** {video_path}\n**Upload:** {upload_result}"
            )
            
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
        """Send Discord alert"""
        try:
            import aiohttp
            
            discord_webhook = os.getenv('DISCORD_WEBHOOK_URL', 
                'https://discordapp.com/api/webhooks/1419039543092580353/Ezdmf0-_aZblEbJNCf2w1Ivr6Fo-Uax_rri3QUti4nkmmrJD6rmr6rP9tjN8wIIZscxA')
            
            payload = {
                "embeds": [{
                    "title": title,
                    "description": message,
                    "color": 65280 if "SUCCESS" in title else 16711680,  # Green or Red
                    "timestamp": datetime.now().isoformat(),
                    "footer": {"text": "MonAY Clean System"}
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
        system = CleanMonAYSystem()
        
        # Test single video
        result = await system.create_and_upload_video("Smart Money Management")
        
        if result['status'] == 'success':
            print("🎉 SUCCESS: Video created and uploaded!")
        else:
            print(f"❌ FAILED: {result['error']}")
            
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())