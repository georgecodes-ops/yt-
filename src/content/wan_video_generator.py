import os
import logging
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
from pathlib import Path

class WanVideoGenerator:
    """WAN-powered video generation from Ollama prompts"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Remove token requirements for local WAN installation
        self.wan_api_base = "http://localhost:7860"  # Local WAN endpoint
        self.device = os.getenv('WAN_DEVICE', 'auto')
        self.precision = os.getenv('WAN_PRECISION', 'fp16')
        self.version = os.getenv('WAN_VERSION', '2.2')
        
        # Video generation settings
        self.video_settings = {
            "resolution": "720x1280",  # Shorts format
            "fps": 30,
            "duration": 60,
            "style": "finance_viral",
            "quality": "high"
        }
        
    async def create_video_from_script(self, script: str, topic: str, style: str = "finance_viral") -> Dict:
        """Create video from Ollama-generated script"""
        try:
            self.logger.info(f"🎬 Creating video for topic: {topic}")
            
            # Parse script into scenes
            scenes = self._parse_script_to_scenes(script)
            
            # Generate visual prompts for each scene
            visual_prompts = await self._create_visual_prompts(scenes, topic, style)
            
            # Send to WAN for video generation
            video_result = await self._generate_with_wan(visual_prompts, script, topic)
            
            return {
                "status": "success",
                "video_path": video_result.get("video_path"),
                "thumbnail_path": video_result.get("thumbnail_path"),
                "duration": video_result.get("duration", 60),
                "topic": topic,
                "style": style,
                "created_at": datetime.now().isoformat(),
                "wan_job_id": video_result.get("job_id")
            }
            
        except Exception as e:
            self.logger.error(f"Video generation failed: {e}")
            return await self._create_fallback_video(script, topic)
    
    def _parse_script_to_scenes(self, script: str) -> List[Dict]:
        """Parse Ollama script into video scenes"""
        scenes = []
        
        # Extract different sections from script
        sections = {
            "hook": self._extract_section(script, "HOOK", "hook"),
            "problem": self._extract_section(script, "PROBLEM", "problem"),
            "solution": self._extract_section(script, "SOLUTION", "solution"),
            "cta": self._extract_section(script, "CALL TO ACTION", "call to action")
        }
        
        for scene_type, content in sections.items():
            if content:
                scenes.append({
                    "type": scene_type,
                    "content": content,
                    "duration": self._get_scene_duration(scene_type),
                    "visual_style": self._get_visual_style(scene_type)
                })
        
        return scenes
    
    def _extract_section(self, script: str, marker1: str, marker2: str) -> str:
        """Extract content between markers"""
        import re
        
        patterns = [
            rf"\[{marker1}.*?\](.*?)(?=\[|$)",
            rf"{marker2}[:\-]?\s*(.*?)(?=\n\n|\[|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, script, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _get_scene_duration(self, scene_type: str) -> int:
        """Get duration for scene type"""
        durations = {
            "hook": 3,
            "problem": 12,
            "solution": 35,
            "cta": 10
        }
        return durations.get(scene_type, 5)
    
    def _get_visual_style(self, scene_type: str) -> str:
        """Get visual style for scene type"""
        styles = {
            "hook": "dynamic_intro_with_money_graphics",
            "problem": "concerned_presenter_with_charts",
            "solution": "confident_explanation_with_visuals",
            "cta": "engaging_outro_with_subscribe_button"
        }
        return styles.get(scene_type, "professional_finance")
    
    async def _create_visual_prompts(self, scenes: List[Dict], topic: str, style: str) -> List[Dict]:
        """Create visual prompts for WAN"""
        visual_prompts = []
        
        for scene in scenes:
            prompt = {
                "scene_type": scene["type"],
                "duration": scene["duration"],
                "text_content": scene["content"],
                "visual_description": self._create_scene_visual_description(
                    scene, topic, style
                ),
                "camera_movement": self._get_camera_movement(scene["type"]),
                "background": self._get_background_style(scene["type"]),
                "text_overlay": self._create_text_overlay(scene["content"])
            }
            visual_prompts.append(prompt)
        
        return visual_prompts
    
    def _create_scene_visual_description(self, scene: Dict, topic: str, style: str) -> str:
        """Create detailed visual description for WAN"""
        base_style = "Professional finance presenter, modern studio background, "
        
        scene_visuals = {
            "hook": f"{base_style}dynamic opening with money graphics, attention-grabbing visuals about {topic}",
            "problem": f"{base_style}concerned expression, charts showing problems, red warning graphics",
            "solution": f"{base_style}confident explanation, green success graphics, step-by-step visuals",
            "cta": f"{base_style}friendly outro, subscribe button animation, engaging call-to-action"
        }
        
        return scene_visuals.get(scene["type"], f"{base_style}professional presentation about {topic}")
    
    def _get_camera_movement(self, scene_type: str) -> str:
        """Get camera movement for scene"""
        movements = {
            "hook": "zoom_in_dynamic",
            "problem": "steady_medium_shot",
            "solution": "slow_zoom_confident",
            "cta": "pull_back_friendly"
        }
        return movements.get(scene_type, "steady_shot")
    
    def _get_background_style(self, scene_type: str) -> str:
        """Get background style for scene"""
        backgrounds = {
            "hook": "dynamic_money_graphics",
            "problem": "concerned_charts_red",
            "solution": "success_charts_green",
            "cta": "friendly_subscribe_graphics"
        }
        return backgrounds.get(scene_type, "professional_finance")
    
    def _create_text_overlay(self, content: str) -> Dict:
        """Create text overlay configuration"""
        return {
            "text": content[:100] + "..." if len(content) > 100 else content,
            "font_size": "large",
            "color": "white",
            "background": "semi_transparent_black",
            "position": "bottom_center",
            "animation": "fade_in"
        }
    
    async def _generate_with_wan(self, visual_prompts: List[Dict], script: str, topic: str) -> Dict:
        """Send prompts to WAN for video generation"""
        try:
            # Prepare WAN API request
            wan_request = {
                "model": "wan-video-2.2",
                "prompt": {
                    "topic": topic,
                    "script": script,
                    "scenes": visual_prompts,
                    "style": "finance_viral_shorts",
                    "duration": sum(scene["duration"] for scene in visual_prompts),
                    "resolution": self.video_settings["resolution"],
                    "fps": self.video_settings["fps"]
                },
                "settings": {
                    "device": self.device,
                    "precision": self.precision,
                    "quality": self.video_settings["quality"]
                }
            }
            
            # Make API call to local WAN (no token needed)
            headers = {
                "Content-Type": "application/json"
                # Removed: "Authorization": f"Bearer {self.wan_token}"
            }
            
            self.logger.info("🚀 Sending request to WAN API...")
            
            # Use proper async HTTP client
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.wan_api_base}/generate-video",
                    json=wan_request,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    response_text = await response.text()
                    
                    if response.status == 200:
                        result = await response.json()
                        self.logger.info(f"✅ WAN video generation successful: {result.get('job_id')}")
                        
                        # Wait for video completion
                        video_result = await self._wait_for_completion(result.get('job_id'))
                        return video_result
                    else:
                         raise Exception(f"WAN API error: {response.status} - {response_text}")
                
        except Exception as e:
            self.logger.error(f"WAN generation failed: {e}")
            raise
    
    async def _wait_for_completion(self, job_id: str) -> Dict:
        """Wait for WAN video generation to complete"""
        max_attempts = 60  # 5 minutes with 5-second intervals
        
        for attempt in range(max_attempts):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.wan_api_base}/jobs/{job_id}",
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        if response.status == 200:
                            job_status = await response.json()
                            
                            if job_status.get('status') == 'completed':
                                self.logger.info(f"✅ Video generation completed: {job_id}")
                                return {
                                    "video_path": job_status.get('output_url'),
                                    "thumbnail_path": job_status.get('thumbnail_url'),
                                    "duration": job_status.get('duration'),
                                    "job_id": job_id
                                }
                            elif job_status.get('status') == 'failed':
                                raise Exception(f"WAN job failed: {job_status.get('error')}")
                            
                            # Still processing
                            self.logger.info(f"⏳ Video generation in progress... ({attempt + 1}/{max_attempts})")
                            await asyncio.sleep(5)
                        else:
                            raise Exception(f"Status check failed: {response.status}")
                    
            except Exception as e:
                self.logger.warning(f"Status check attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(5)
        
        raise Exception("Video generation timeout")
    
    async def _create_fallback_video(self, script: str, topic: str) -> Dict:
        """Create fallback video if WAN fails"""
        self.logger.warning("Creating fallback video using local processor")
        
        try:
            # Use absolute import and sync method
            import sys
            import os
            sys.path.append(os.path.dirname(__file__))
            
            from video_processor import VideoProcessor
            processor = VideoProcessor()
            
            # Use sync method since VideoProcessor.create_shorts_video is sync
            fallback_path = processor.create_shorts_video(script, None)
            
            return {
                "status": "fallback_success",
                "video_path": fallback_path,
                "thumbnail_path": None,
                "duration": 60,
                "topic": topic,
                "style": "fallback",
                "created_at": datetime.now().isoformat(),
                "note": "Generated with fallback processor"
            }
            
        except Exception as e:
            self.logger.error(f"Fallback video creation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "topic": topic
            }
    
    async def daily_model_check(self):
        """Daily check for better WAN models"""
        try:
            self.logger.info("🔍 Checking for WAN model updates...")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.wan_api_base}/models",
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        models = await response.json()
                        self.logger.info(f"✅ Available WAN models: {len(models.get('models', []))}")
                    else:
                        self.logger.warning(f"⚠️ Model check failed: {response.status}")
                
        except Exception as e:
            self.logger.error(f"Daily model check failed: {e}")
    
    async def generate_viral_shorts_batch(self, topics: List[str], count: int = 5) -> List[Dict]:
        """Generate multiple viral shorts for batch processing"""
        results = []
        
        for i, topic in enumerate(topics[:count]):
            try:
                self.logger.info(f"🎬 Generating video {i+1}/{count}: {topic}")
                
                # Generate simple script for the topic
                script = f"""
[HOOK] {topic} - The Secret Strategy Everyone's Talking About!

[PROBLEM] Most people struggle with {topic.lower()} because they don't know the right approach. Traditional methods are outdated and ineffective.

[SOLUTION] Here's the game-changing strategy: Focus on automation and AI-powered tools. This approach has helped thousands of people achieve financial success.

[CALL TO ACTION] Want to learn more? Subscribe for daily finance tips and strategies that actually work!
"""
                
                video_result = await self.create_video_from_script(script, topic)
                results.append(video_result)
                
                # Brief pause between generations
                await asyncio.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Batch video {i+1} failed: {e}")
                results.append({
                    "status": "error",
                    "topic": topic,
                    "error": str(e)
                })
        
        return results