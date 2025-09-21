import requests
import json
from typing import Dict, Any, Optional
from .config import Config

class APIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or Config.AI_SERVICE_URL
    
    def check_ai_health(self) -> Dict[str, Any]:
        """Check if AI service is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except Exception as e:
            raise Exception(f"AI service unreachable: {str(e)}")
    
    def generate_image(self, prompt: str, model: str = "controlnet-canny", 
                      width: int = 512, height: int = 512, 
                      guidance_scale: float = 7.5, 
                      num_inference_steps: int = 20) -> Dict[str, Any]:
        """Generate image using AI service"""
        payload = {
            "prompt": prompt,
            "model": model,
            "width": width,
            "height": height,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/generate-image",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    def process_video(self, video_path: str, processing_type: str = "enhance") -> Dict[str, Any]:
        """Process video using AI service"""
        payload = {
            "video_path": video_path,
            "processing_type": processing_type
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/process-video",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Video processing failed: {str(e)}")