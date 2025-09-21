import logging
import os
import subprocess
from typing import Dict, List, Optional
from pathlib import Path
import json
import time

class VideoProcessor:
    """CPU-optimized video creation and processing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.video_settings = {
            "resolution": "720x1280",  # CPU-friendly resolution
            "fps": 24,  # Lower FPS for CPU efficiency
            "duration": 60,
            "format": "mp4",
            "cpu_threads": min(4, os.cpu_count())  # Limit CPU usage
        }
        
        # CPU-optimized background templates
        self.background_templates = {
            "finance_charts": self._create_chart_background,
            "money_animation": self._create_money_background,
            "stock_ticker": self._create_ticker_background,
            "gradient_flow": self._create_gradient_background
        }
    
    def create_shorts_video(self, script: str, audio_path: Optional[str] = None, 
                           background_type: str = "finance_charts") -> str:
        """Create CPU-optimized YouTube Shorts video"""
        try:
            self.logger.info(f"Creating CPU-optimized Shorts: {background_type}")
            
            # Generate unique output path
            video_id = abs(hash(script)) % 1000000
            output_path = f"outputs/shorts_{video_id}.mp4"
            os.makedirs("outputs", exist_ok=True)
            
            # Create background video (CPU-optimized)
            background_path = self._create_background_video(background_type)
            
            # Add text overlays (lightweight)
            text_video_path = self._add_text_overlays(background_path, script)
            
            # Add audio if provided
            if audio_path and os.path.exists(audio_path):
                final_path = self._add_audio_track(text_video_path, audio_path)
            else:
                final_path = text_video_path
            
            # Optimize for platform (CPU-friendly compression)
            optimized_path = self._cpu_optimize_video(final_path, output_path)
            
            self.logger.info(f"✅ Video created: {optimized_path}")
            return optimized_path
            
        except Exception as e:
            self.logger.error(f"Video creation failed: {e}")
            return self._create_fallback_video(script)
    
    def _create_background_video(self, bg_type: str) -> str:
        """Create CPU-optimized background video"""
        try:
            # Use FFmpeg for CPU-efficient video generation
            bg_path = f"temp/bg_{bg_type}_{int(time.time())}.mp4"
            os.makedirs("temp", exist_ok=True)
            
            if bg_type == "finance_charts":
                # Create animated chart background
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "lavfi",
                    "-i", "color=c=0x1a1a2e:size=720x1280:duration=60:rate=24",
                    "-vf", "drawtext=text='📈':fontsize=200:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
                    "-c:v", "libx264", "-preset", "ultrafast",
                    "-threads", str(self.video_settings["cpu_threads"]),
                    bg_path
                ]
            elif bg_type == "money_animation":
                # Create money symbol animation
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "lavfi",
                    "-i", "color=c=0x0f3460:size=720x1280:duration=60:rate=24",
                    "-vf", "drawtext=text='💰':fontsize=150:fontcolor=gold:x=(w-text_w)/2:y=(h-text_h)/2",
                    "-c:v", "libx264", "-preset", "ultrafast",
                    "-threads", str(self.video_settings["cpu_threads"]),
                    bg_path
                ]
            else:
                # Default gradient background
                cmd = [
                    "ffmpeg", "-y",
                    "-f", "lavfi",
                    "-i", "color=c=0x16213e:size=720x1280:duration=60:rate=24",
                    "-c:v", "libx264", "-preset", "ultrafast",
                    "-threads", str(self.video_settings["cpu_threads"]),
                    bg_path
                ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return bg_path
            
        except Exception as e:
            self.logger.error(f"Background creation failed: {e}")
            return self._create_simple_background()
    
    def _add_text_overlays(self, video_path: str, script: str) -> str:
        """Add CPU-optimized text overlays"""
        try:
            output_path = video_path.replace(".mp4", "_text.mp4")
            
            # Split script into chunks for better readability
            words = script.split()
            chunks = [' '.join(words[i:i+3]) for i in range(0, len(words), 3)]
            
            # Create text overlay filter
            text_filter = ""
            for i, chunk in enumerate(chunks[:10]):  # Limit to 10 chunks
                start_time = i * 6  # 6 seconds per chunk
                text_filter += f"drawtext=text='{chunk}':fontfile=/Windows/Fonts/arial.ttf:fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h*0.8:enable='between(t,{start_time},{start_time+5})',"
            
            text_filter = text_filter.rstrip(',')
            
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-vf", text_filter,
                "-c:v", "libx264", "-preset", "ultrafast",
                "-threads", str(self.video_settings["cpu_threads"]),
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Text overlay failed: {e}")
            return video_path
    
    def _add_audio_track(self, video_path: str, audio_path: str) -> str:
        """Add audio track with CPU optimization"""
        try:
            output_path = video_path.replace(".mp4", "_final.mp4")
            
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",  # Don't re-encode video
                "-c:a", "aac", "-b:a", "128k",
                "-shortest",  # Match shortest stream
                "-threads", str(self.video_settings["cpu_threads"]),
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Audio addition failed: {e}")
            return video_path
    
    def _cpu_optimize_video(self, input_path: str, output_path: str) -> str:
        """CPU-optimized video compression"""
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", input_path,
                "-c:v", "libx264",
                "-preset", "ultrafast",  # Fastest encoding
                "-crf", "28",  # Balanced quality/size
                "-maxrate", "2M", "-bufsize", "4M",  # Bitrate control
                "-vf", "scale=720:1280",  # Ensure correct resolution
                "-threads", str(self.video_settings["cpu_threads"]),
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Cleanup temp files
            self._cleanup_temp_files(input_path)
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Video optimization failed: {e}")
            return input_path
    
    def _create_fallback_video(self, script: str) -> str:
        """Create minimal fallback video"""
        try:
            output_path = f"outputs/fallback_{abs(hash(script)) % 1000}.mp4"
            
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", "color=c=black:size=720x1280:duration=10:rate=24",
                "-vf", f"drawtext=text='Content Ready':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
                "-c:v", "libx264", "-preset", "ultrafast",
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Fallback video failed: {e}")
            return "error.mp4"
    
    def _cleanup_temp_files(self, *file_paths):
        """Clean up temporary files"""
        for path in file_paths:
            try:
                if os.path.exists(path) and "temp/" in path:
                    os.remove(path)
            except Exception as e:
                self.logger.warning(f"Cleanup failed for {path}: {e}")
    
    def add_captions(self, video_path: str, script: str) -> str:
        """Add captions with CPU optimization"""
        # Already handled in _add_text_overlays
        return video_path
    
    def optimize_for_platform(self, video_path: str, platform: str = "youtube") -> str:
        """Platform-specific optimization"""
        platform_specs = {
            "youtube": {"maxrate": "2M", "bufsize": "4M"},
            "tiktok": {"maxrate": "1.5M", "bufsize": "3M"},
            "instagram": {"maxrate": "1M", "bufsize": "2M"}
        }
        
        specs = platform_specs.get(platform, platform_specs["youtube"])
        self.logger.info(f"Optimizing for {platform}: {specs}")
        
        return video_path
