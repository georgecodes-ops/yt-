import requests
import logging
from typing import Dict, Optional, List
import json
import time

class OllamaClient:
    """Client for interacting with Ollama API for content generation"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        
    async def generate_content(self, prompt: str, model: str = "mistral", 
                             max_tokens: int = 1000, temperature: float = 0.7) -> Optional[str]:
        """Generate content using Ollama model with retry logic"""
        
        # First check if Ollama is running
        if not self.check_health():
            self.logger.error("Ollama service is not running or accessible")
            return None
            
        max_retries = 3
        for attempt in range(max_retries):
            try:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature
                    }
                }
                
                self.logger.info(f"Attempting Ollama generation (attempt {attempt + 1}/{max_retries})")
                
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=300  # Increased from 60 to 300 seconds
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result.get("response", "").strip()
                    if content:
                        self.logger.info("Ollama generation successful")
                        return content
                    else:
                        self.logger.warning("Ollama returned empty response")
                else:
                    self.logger.error(f"Ollama API error: {response.status_code}")
                    
            except requests.exceptions.Timeout as e:
                self.logger.warning(f"Ollama timeout on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(10)  # Wait 10 seconds before retry
                    continue
            except requests.exceptions.ConnectionError as e:
                self.logger.error(f"Ollama connection error: {e}")
                break  # Don't retry connection errors
            except Exception as e:
                self.logger.error(f"Ollama generation failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # Wait 5 seconds before retry
                    continue
                    
        self.logger.error("All Ollama generation attempts failed")
        return None
    
    async def generate_video_script(self, topic: str, research_data: Dict, 
                                  target_audience: str = "young_investors", 
                                  tone: str = "engaging") -> Dict:
        """Generate video script from research data using Ollama"""
        
        # Build context from research data
        context_parts = []
        if research_data.get('news_items'):
            context_parts.append(f"Recent news: {research_data['news_items'][:3]}")
        if research_data.get('trends'):
            context_parts.append(f"Current trends: {research_data['trends'][:3]}")
        if research_data.get('academic_insights'):
            context_parts.append(f"Research insights: {research_data['academic_insights'][:2]}")
            
        context = " | ".join(context_parts)
        
        prompt = f"""Create an engaging 60-second video script about {topic} for {target_audience}.
        
Context from research: {context}
        
Tone: {tone}
        
Format the response as JSON with these fields:
        {{
            "hook": "Attention-grabbing opening (10-15 seconds)",
            "main_content": "Core message with key insights (35-40 seconds)",
            "call_to_action": "Clear CTA (5-10 seconds)",
            "visual_cues": ["List of visual suggestions for each section"]
        }}
        
Make it viral-worthy, data-driven, and actionable. Use the research context to add credibility."""
        
        response = await self.generate_content(prompt, max_tokens=800)
        
        if response:
            try:
                # Try to parse JSON response
                script_data = json.loads(response)
                return {
                    "status": "success",
                    "content": script_data,
                    "raw_response": response,
                    "research_context": context
                }
            except json.JSONDecodeError:
                # Fallback to text parsing
                return {
                    "status": "success", 
                    "content": {
                        "hook": response[:200],
                        "main_content": response[200:600] if len(response) > 200 else response,
                        "call_to_action": response[-100:] if len(response) > 100 else "Subscribe for more insights!",
                        "visual_cues": ["Professional graphics", "Data visualizations", "Engaging animations"]
                    },
                    "raw_response": response,
                    "research_context": context
                }
        else:
            return {
                "status": "error",
                "content": None,
                "error": "Failed to generate content with Ollama"
            }
    
    def check_health(self) -> bool:
        """Check if Ollama service is available"""
        try:
            # First check if basic service is running
            response = requests.get(f"{self.base_url}", timeout=10)
            if response.status_code == 200 and "Ollama is running" in response.text:
                self.logger.info("Ollama service is running")
                
                # Then check API endpoints
                version_response = requests.get(f"{self.base_url}/api/version", timeout=10)
                if version_response.status_code == 200:
                    self.logger.info(f"Ollama API accessible, version: {version_response.json().get('version', 'unknown')}")
                    return True
                else:
                    self.logger.warning("Ollama service running but API not accessible")
                    return False
            else:
                self.logger.error("Ollama service not responding correctly")
                return False
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Cannot connect to Ollama service: {e}")
            return False
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Ollama health check timeout: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Ollama health check failed: {e}")
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model.get("name", "") for model in models]
            return []
        except:
            return []