#!/usr/bin/env python3
"""
Simple data bridge between finance and core environments
"""
import json
import requests
from pathlib import Path

class DataBridge:
    def __init__(self):
        self.data_dir = Path("shared_data")
        self.data_dir.mkdir(exist_ok=True)
    
    def save_finance_data(self, data, filename):
        """Save finance data to shared directory"""
        filepath = self.data_dir / f"{filename}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved: {filepath}")
    
    def load_finance_data(self, filename):
        """Load finance data from shared directory"""
        filepath = self.data_dir / f"{filename}.json"
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def start_finance_service(self):
        """Start finance data collection service"""
        print("🚀 Starting finance service on port 8001...")
        # This would run in venv_finance
        pass
    
    def start_core_service(self):
        """Start core AI/video service"""
        print("🚀 Starting core service on port 8000...")
        # This would run in venv_core
        pass

if __name__ == "__main__":
    bridge = DataBridge()
    print("🌉 Data bridge initialized")