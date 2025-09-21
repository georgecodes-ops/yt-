import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List

class SimpleFileStorage:
    """Simple file-based storage for quick deployment"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.data_dir / "agents").mkdir(exist_ok=True)
        (self.data_dir / "videos").mkdir(exist_ok=True)
        (self.data_dir / "analytics").mkdir(exist_ok=True)
        (self.data_dir / "temp").mkdir(exist_ok=True)
    
    def save_agents(self, agents: Dict) -> bool:
        """Save agents to JSON file"""
        try:
            agents_file = self.data_dir / "agents" / "agents.json"
            with open(agents_file, 'w') as f:
                json.dump(agents, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving agents: {e}")
            return False
    
    def load_agents(self) -> Dict:
        """Load agents from JSON file"""
        try:
            agents_file = self.data_dir / "agents" / "agents.json"
            if agents_file.exists():
                with open(agents_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading agents: {e}")
            return {}
    
    def save_video_data(self, video_id: str, data: Dict) -> bool:
        """Save video data"""
        try:
            video_file = self.data_dir / "videos" / f"{video_id}.json"
            data['saved_at'] = datetime.now().isoformat()
            with open(video_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving video data: {e}")
            return False
    
    def get_temp_dir(self) -> str:
        """Get temporary directory for file processing"""
        return str(self.data_dir / "temp")