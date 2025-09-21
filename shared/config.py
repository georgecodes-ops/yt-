import os
from pathlib import Path

class Config:
    # Service URLs
    AI_SERVICE_URL = "http://localhost:8000"
    VIDEO_SERVICE_URL = "http://localhost:8501"
    
    # Directory paths
    BASE_DIR = Path(__file__).parent.parent
    AI_SERVICE_DIR = BASE_DIR / "ai_service"
    VIDEO_SERVICE_DIR = BASE_DIR / "video_service"
    SHARED_DIR = BASE_DIR / "shared"
    
    # Environment
    ENV = os.getenv("ENV", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Timeouts
    AI_SERVICE_TIMEOUT = 300  # 5 minutes for heavy AI operations
    VIDEO_SERVICE_TIMEOUT = 600  # 10 minutes for video processing