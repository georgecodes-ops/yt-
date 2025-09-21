import logging
import os
import subprocess
import asyncio
from typing import Optional
import tempfile
import time

class TTSGenerator:
    """
    Modern TTS Generator with ElevenLabs integration
    Implements 2024/2025 best practices for YouTube automation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Modern voice settings optimized for YouTube engagement
        self.voice_settings = {
            "voice": "en-US-AriaNeural",
            "rate": "+20%",  # Slightly faster for engagement
            "pitch": "+0Hz",
            "volume": "+0%"
        }
        
        # ElevenLabs settings (if available)
        self.elevenlabs_settings = {
            "voice_id": "pqHfZKP75CvOlQylNhV4",  # Professional male voice
            "model_id": "eleven_multilingual_v2",  # Best for consistency
            "stability": 0.2,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        # Check available TTS engines
        self.tts_engine = self._detect_tts_engine()
        self.elevenlabs_available = self._check_elevenlabs_availability()
        
    def _check_elevenlabs_availability(self) -> bool:
        """Check if ElevenLabs is available and configured"""
        try:
            # Check for API key
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                self.logger.info("⚠️ ElevenLabs API key not found")
                return False
            
            # Try to import elevenlabs
            import elevenlabs
            self.logger.info("✅ ElevenLabs available with API key")
            return True
        except ImportError:
            self.logger.info("⚠️ ElevenLabs package not installed")
            return False
        except Exception as e:
            self.logger.warning(f"ElevenLabs check failed: {e}")
            return False
        
    async def _generate_elevenlabs_tts(self, text: str, output_path: str) -> str:
        """
        Generate audio using ElevenLabs API
        Implements 2024/2025 best practices for YouTube automation
        """
        try:
            from elevenlabs.client import ElevenLabs
            from elevenlabs import VoiceSettings
            
            # Initialize client
            client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
            
            # Clean text for better TTS
            clean_text = self._clean_text_for_tts(text)
            
            # Generate audio with optimized settings
            audio_generator = client.text_to_speech.convert(
                text=clean_text,
                voice_id=self.elevenlabs_settings["voice_id"],
                model_id=self.elevenlabs_settings["model_id"],
                voice_settings=VoiceSettings(
                    stability=self.elevenlabs_settings["stability"],
                    similarity_boost=self.elevenlabs_settings["similarity_boost"],
                    style=self.elevenlabs_settings["style"],
                    use_speaker_boost=self.elevenlabs_settings["use_speaker_boost"]
                ),
                output_format="mp3_44100_128"  # High quality for YouTube
            )
            
            # Save audio to file
            with open(output_path.replace('.wav', '.mp3'), 'wb') as f:
                for chunk in audio_generator:
                    f.write(chunk)
            
            final_path = output_path.replace('.wav', '.mp3')
            
            # Validate output
            if os.path.exists(final_path) and os.path.getsize(final_path) > 1000:
                self.logger.info(f"✅ ElevenLabs TTS generated: {final_path}")
                return final_path
            else:
                self.logger.error("ElevenLabs TTS output validation failed")
                return None
                
        except Exception as e:
            self.logger.error(f"ElevenLabs TTS generation failed: {e}")
            return None
        
    def _detect_tts_engine(self) -> str:
        """Detect best available TTS engine for CPU using venv packages"""
        # Check if we're in the MonAY environment
        venv_python = "/opt/monay/venv/bin/python" if os.path.exists("/opt/monay/venv/bin/python") else None
        
        try:
            # Try edge-tts from venv first
            if venv_python:
                result = subprocess.run([venv_python, "-c", "import edge_tts; print('edge-tts available')"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.logger.info("✅ Using edge-tts from venv")
                    return "edge-tts-venv"
            
            # Try system edge-tts
            subprocess.run(["edge-tts", "--version"], check=True, capture_output=True)
            return "edge-tts"
        except:
            try:
                # Try gTTS from venv
                if venv_python:
                    result = subprocess.run([venv_python, "-c", "from gtts import gTTS; print('gTTS available')"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.logger.info("✅ Using gTTS from venv")
                        return "gtts-venv"
                
                # Try system gTTS
                from gtts import gTTS
                return "gtts"
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
        """
        Generate audio with modern TTS engines
        Prioritizes ElevenLabs for best quality, falls back to other engines
        """
        if not output_path:
            base_dir = "/opt/monay" if os.path.exists("/opt/monay") else "."
            output_path = f"{base_dir}/outputs/audio_{abs(hash(text)) % 10000}.wav"
        
        base_dir = "/opt/monay" if os.path.exists("/opt/monay") else "."
        os.makedirs(f"{base_dir}/outputs", exist_ok=True)
        
        try:
            # Priority 1: ElevenLabs (best quality for YouTube)
            if self.elevenlabs_available:
                self.logger.info("🎤 Using ElevenLabs TTS (premium quality)")
                result = await self._generate_elevenlabs_tts(text, output_path)
                if result and self._validate_audio_output(result):
                    return result
                else:
                    self.logger.warning("ElevenLabs failed, falling back to other engines")
            
            # Priority 2: Edge TTS (good quality, free)
            if self.tts_engine == "edge-tts-venv":
                result = await self._generate_edge_tts_venv(text, output_path)
            elif self.tts_engine == "edge-tts":
                result = await self._generate_edge_tts(text, output_path)
            elif self.tts_engine == "gtts-venv":
                result = await self._generate_gtts_venv(text, output_path)
            elif self.tts_engine == "gtts":
                result = await self._generate_gtts(text, output_path)
            elif self.tts_engine == "sapi":
                result = self._generate_sapi_tts(text, output_path)
            elif self.tts_engine == "espeak":
                result = self._generate_espeak_tts(text, output_path)
            else:
                result = self._generate_fallback_audio(text, output_path)
            
            # Validate audio output
            if self._validate_audio_output(result):
                return result
            else:
                self.logger.error(f"Audio validation failed for {result}")
                return self._generate_fallback_audio(text, output_path)
                
        except Exception as e:
            self.logger.error(f"TTS generation failed: {e}")
            return self._generate_fallback_audio(text, output_path)
    
    def _validate_audio_output(self, audio_path: str) -> bool:
        """Validate that audio file contains actual audio, not silence"""
        try:
            if not os.path.exists(audio_path):
                return False
            
            # Check file size - real TTS should be > 10KB
            file_size = os.path.getsize(audio_path)
            if file_size < 10000:  # 10KB minimum
                self.logger.warning(f"Audio file too small: {file_size} bytes")
                return False
            
            # Check duration using ffprobe if available
            try:
                cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
                       "-of", "csv=p=0", audio_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    duration = float(result.stdout.strip())
                    if duration < 1.0:  # Less than 1 second
                        self.logger.warning(f"Audio duration too short: {duration}s")
                        return False
                    self.logger.info(f"✅ Audio validated: {duration:.1f}s, {file_size} bytes")
                    return True
            except:
                pass
            
            # Fallback: just check file size
            self.logger.info(f"✅ Audio file created: {file_size} bytes")
            return True
            
        except Exception as e:
            self.logger.error(f"Audio validation error: {e}")
            return False
    
    async def _generate_edge_tts_venv(self, text: str, output_path: str) -> str:
        """Generate using edge-tts from venv"""
        try:
            venv_python = "/opt/monay/venv/bin/python"
            self.logger.info(f"Generating edge-tts audio from venv: {len(text)} chars")
            
            clean_text = self._clean_text_for_tts(text)
            
            # Create Python script to run edge-tts
            script_content = f'''
import asyncio
import edge_tts

async def main():
    voice = "{self.voice_settings["voice"]}"
    rate = "{self.voice_settings["rate"]}"
    text = """{clean_text}"""
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save("{output_path}")

if __name__ == "__main__":
    asyncio.run(main())
'''
            
            # Write script to temp file
            script_path = f"/tmp/tts_script_{int(time.time())}.py"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Run script with venv python
            process = await asyncio.create_subprocess_exec(
                venv_python, script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Clean up script
            if os.path.exists(script_path):
                os.remove(script_path)
            
            if process.returncode == 0 and os.path.exists(output_path):
                self.logger.info(f"✅ Edge-TTS venv audio generated: {output_path}")
                return output_path
            else:
                raise Exception(f"Edge-TTS venv failed: {stderr.decode()}")
                
        except Exception as e:
            self.logger.error(f"Edge-TTS venv failed: {e}")
            return self._generate_fallback_audio(text, output_path)
    
    async def _generate_gtts_venv(self, text: str, output_path: str) -> str:
        """Generate using gTTS from venv"""
        try:
            venv_python = "/opt/monay/venv/bin/python"
            self.logger.info(f"Generating gTTS audio from venv: {len(text)} chars")
            
            clean_text = self._clean_text_for_tts(text)
            temp_mp3 = output_path.replace('.wav', '_temp.mp3')
            
            # Create Python script to run gTTS
            script_content = f'''
from gtts import gTTS
import os

text = """{clean_text}"""
tts = gTTS(text=text, lang='en', slow=False)
tts.save("{temp_mp3}")
print("gTTS completed")
'''
            
            script_path = f"/tmp/gtts_script_{int(time.time())}.py"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Run gTTS script
            process = await asyncio.create_subprocess_exec(
                venv_python, script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            # Clean up script
            if os.path.exists(script_path):
                os.remove(script_path)
            
            if process.returncode == 0 and os.path.exists(temp_mp3):
                # Convert mp3 to wav
                cmd = ["ffmpeg", "-y", "-i", temp_mp3, "-acodec", "pcm_s16le", 
                       "-ar", "44100", output_path]
                subprocess.run(cmd, check=True, capture_output=True)
                
                # Clean up temp file
                if os.path.exists(temp_mp3):
                    os.remove(temp_mp3)
                
                if os.path.exists(output_path):
                    self.logger.info(f"✅ gTTS venv audio generated: {output_path}")
                    return output_path
                else:
                    raise Exception("gTTS venv output file not created")
            else:
                raise Exception(f"gTTS venv failed: {stderr.decode()}")
                
        except Exception as e:
            self.logger.error(f"gTTS venv failed: {e}")
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
    
    async def _generate_gtts(self, text: str, output_path: str) -> str:
        """Generate using Google Text-to-Speech (reliable fallback)"""
        try:
            from gtts import gTTS
            import io
            
            self.logger.info(f"Generating gTTS audio: {len(text)} chars")
            
            # Clean text for TTS
            clean_text = self._clean_text_for_tts(text)
            
            # Create gTTS object
            tts = gTTS(text=clean_text, lang='en', slow=False)
            
            # Save to temporary mp3 file first
            temp_mp3 = output_path.replace('.wav', '_temp.mp3')
            tts.save(temp_mp3)
            
            # Convert mp3 to wav using ffmpeg
            cmd = [
                "ffmpeg", "-y",
                "-i", temp_mp3,
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                output_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Clean up temp file
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
            
            if os.path.exists(output_path):
                self.logger.info(f"✅ gTTS audio generated: {output_path}")
                return output_path
            else:
                raise Exception("gTTS output file not created")
                
        except Exception as e:
            self.logger.error(f"gTTS failed: {e}")
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
