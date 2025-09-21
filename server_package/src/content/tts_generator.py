import logging
import os
import subprocess
import asyncio
from typing import Optional
import tempfile
import time

class TTSGenerator:
    """CPU-optimized Text-to-Speech generation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.voice_settings = {
            "voice": "en-US-AriaNeural",
            "rate": "+20%",  # Slightly faster for engagement
            "pitch": "+0Hz",
            "volume": "+0%"
        }
        
        # Check available TTS engines
        self.tts_engine = self._detect_tts_engine()
        
    def _detect_tts_engine(self) -> str:
        """Detect best available TTS engine for CPU"""
        try:
            # Try edge-tts (fastest, best quality)
            subprocess.run(["edge-tts", "--version"], 
                         check=True, capture_output=True)
            return "edge-tts"
        except:
            try:
                # Try Windows SAPI
                import win32com.client
                return "sapi"
            except:
                # Fallback to espeak (cross-platform)
                try:
                    subprocess.run(["espeak", "--version"], 
                                 check=True, capture_output=True)
                    return "espeak"
                except:
                    return "none"
    
    async def generate_audio(self, text: str, output_path: Optional[str] = None) -> str:
        """Generate audio with CPU optimization"""
        if not output_path:
            output_path = f"outputs/audio_{abs(hash(text)) % 10000}.wav"
            
        os.makedirs("outputs", exist_ok=True)
        
        try:
            if self.tts_engine == "edge-tts":
                return await self._generate_edge_tts(text, output_path)
            elif self.tts_engine == "sapi":
                return self._generate_sapi_tts(text, output_path)
            elif self.tts_engine == "espeak":
                return self._generate_espeak_tts(text, output_path)
            else:
                return self._generate_fallback_audio(text, output_path)
                
        except Exception as e:
            self.logger.error(f"TTS generation failed: {e}")
            return self._generate_fallback_audio(text, output_path)
    
    async def _generate_edge_tts(self, text: str, output_path: str) -> str:
        """Generate using edge-tts (best quality, CPU efficient)"""
        try:
            self.logger.info(f"Generating edge-tts audio: {len(text)} chars")
            
            # Clean text for TTS
            clean_text = self._clean_text_for_tts(text)
            
            cmd = [
                "edge-tts",
                "--voice", self.voice_settings["voice"],
                "--rate", self.voice_settings["rate"],
                "--pitch", self.voice_settings["pitch"],
                "--text", clean_text,
                "--write-media", output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0 and os.path.exists(output_path):
                self.logger.info(f"✅ Edge-TTS audio generated: {output_path}")
                return output_path
            else:
                raise Exception(f"Edge-TTS failed: {stderr.decode()}")
                
        except Exception as e:
            self.logger.error(f"Edge-TTS failed: {e}")
            return self._generate_fallback_audio(text, output_path)
    
    def _generate_sapi_tts(self, text: str, output_path: str) -> str:
        """Generate using Windows SAPI"""
        try:
            import win32com.client # type: ignore
            
            self.logger.info(f"Generating SAPI audio: {len(text)} chars")
            
            # Initialize SAPI
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            
            # Configure voice settings
            voices = speaker.GetVoices()
            for voice in voices:
                if "Aria" in voice.GetDescription() or "Zira" in voice.GetDescription():
                    speaker.Voice = voice
                    break
            
            # Set rate (0-10, default 0)
            speaker.Rate = 2  # Slightly faster
            
            # Save to file
            file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
            file_stream.Open(output_path, 3)
            speaker.AudioOutputStream = file_stream
            
            # Generate speech
            clean_text = self._clean_text_for_tts(text)
            speaker.Speak(clean_text)
            
            file_stream.Close()
            
            if os.path.exists(output_path):
                self.logger.info(f"✅ SAPI audio generated: {output_path}")
                return output_path
            else:
                raise Exception("SAPI output file not created")
                
        except Exception as e:
            self.logger.error(f"SAPI TTS failed: {e}")
            return self._generate_fallback_audio(text, output_path)
    
    def _generate_espeak_tts(self, text: str, output_path: str) -> str:
        """Generate using espeak (cross-platform fallback)"""
        try:
            self.logger.info(f"Generating espeak audio: {len(text)} chars")
            
            clean_text = self._clean_text_for_tts(text)
            
            cmd = [
                "espeak",
                "-s", "160",  # Speed (words per minute)
                "-p", "50",   # Pitch
                "-a", "100",  # Amplitude
                "-w", output_path,  # Write to file
                clean_text
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            if os.path.exists(output_path):
                self.logger.info(f"✅ Espeak audio generated: {output_path}")
                return output_path
            else:
                raise Exception("Espeak output file not created")
                
        except Exception as e:
            self.logger.error(f"Espeak TTS failed: {e}")
            return self._generate_fallback_audio(text, output_path)
    
    def _generate_fallback_audio(self, text: str, output_path: str) -> str:
        """Generate silent audio as fallback"""
        try:
            # Create 60 seconds of silence
            duration = min(60, len(text) * 0.1)  # Estimate duration
            
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi",
                "-i", f"anullsrc=channel_layout=stereo:sample_rate=44100:duration={duration}",
                "-c:a", "pcm_s16le",
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            self.logger.warning(f"⚠️ Fallback silent audio created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Fallback audio failed: {e}")
            return "error.wav"
    
    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text for better TTS pronunciation"""
        # Remove problematic characters
        text = text.replace('"', '')
        text = text.replace("'", '')
        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')
        
        # Replace common abbreviations
        replacements = {
            '$': 'dollars',
            '%': 'percent',
            '&': 'and',
            '@': 'at',
            '#': 'number',
            'AI': 'A I',
            'CEO': 'C E O',
            'IPO': 'I P O',
            'ROI': 'R O I'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Limit length for CPU efficiency
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        return text.strip()
    
    def set_voice_settings(self, voice: str = None, rate: str = None, 
                          pitch: str = None, volume: str = None):
        """Configure voice settings"""
        if voice:
            self.voice_settings["voice"] = voice
        if rate:
            self.voice_settings["rate"] = rate
        if pitch:
            self.voice_settings["pitch"] = pitch
        if volume:
            self.voice_settings["volume"] = volume
            
        self.logger.info(f"Voice settings updated: {self.voice_settings}")
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if self.tts_engine == "edge-tts":
            try:
                result = subprocess.run(
                    ["edge-tts", "--list-voices"],
                    capture_output=True, text=True, check=True
                )
                return result.stdout.split('\n')[:10]  # First 10 voices
            except:
                return ["en-US-AriaNeural", "en-US-JennyNeural"]
        else:
            return ["Default Voice"]
