from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.content.ai_image_generator import AIImageGenerator
from src.content.ai_prompt_orchestrator import AIPromptOrchestrator
from src.ml.adaptive_model_manager import AdaptiveModelManager
from shared.api_client import APIClient
from shared.config import Config

app = FastAPI(title="AI Service", version="1.0.0")

class ImageGenerationRequest(BaseModel):
    prompt: str
    style: str = "cinematic"
    width: int = 512
    height: int = 512
    negative_prompt: str = ""

class ContentAnalysisRequest(BaseModel):
    content: str
    content_type: str = "text"

# Initialize AI components
ai_image_gen = AIImageGenerator()
ai_orchestrator = AIPromptOrchestrator()
model_manager = AdaptiveModelManager()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai"}

@app.post("/generate_image")
async def generate_image(request: ImageGenerationRequest):
    try:
        result = ai_image_gen.generate(
            prompt=request.prompt,
            style=request.style,
            width=request.width,
            height=request.height,
            negative_prompt=request.negative_prompt
        )
        return {"success": True, "image_url": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze_content")
async def analyze_content(request: ContentAnalysisRequest):
    try:
        analysis = ai_orchestrator.analyze_content(
            content=request.content,
            content_type=request.content_type
        )
        return {"success": True, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_trends")
async def predict_trends(content: str):
    try:
        prediction = model_manager.predict_trends(content)
        return {"success": True, "prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)