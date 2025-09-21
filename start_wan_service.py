#!/usr/bin/env python3
"""
🎬 WAN Video Generation Service Starter
Starts the WAN video generation service for MonAY
"""

import os
import sys
import subprocess
import time
import signal
import json
from pathlib import Path
from typing import Optional

class WANServiceStarter:
    def __init__(self):
        self.project_root = Path.cwd()
        self.wan_venv_path = self.project_root / "wan_venv"
        self.wan_config_path = self.project_root / "src" / "wan" / "wan_config.json"
        self.process: Optional[subprocess.Popen] = None
        
    def print_header(self, message: str):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"🎬 {message}")
        print(f"{'='*60}")
        
    def print_step(self, message: str, status: str = "INFO"):
        """Print formatted step"""
        colors = {
            "SUCCESS": "\033[92m",  # Green
            "ERROR": "\033[91m",    # Red
            "WARNING": "\033[93m",  # Yellow
            "INFO": "\033[94m",     # Blue
            "RESET": "\033[0m"      # Reset
        }
        
        color = colors.get(status, colors["INFO"])
        reset = colors["RESET"]
        print(f"{color}[{status}]{reset} {message}")
        
    def check_wan_environment(self) -> bool:
        """Check if WAN environment is properly set up"""
        self.print_header("Checking WAN Environment")
        
        # Check WAN virtual environment
        python_path = self.wan_venv_path / "Scripts" / "python.exe"  # Windows
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"  # Linux
            
        if not python_path.exists():
            self.print_step("WAN virtual environment not found", "ERROR")
            self.print_step(f"Expected at: {self.wan_venv_path}", "INFO")
            return False
            
        self.print_step("WAN virtual environment: OK", "SUCCESS")
        
        # Check WAN video generator module
        wan_generator_path = self.project_root / "src" / "wan" / "video_generator.py"
        if not wan_generator_path.exists():
            self.print_step("WAN video generator not found", "ERROR")
            return False
            
        self.print_step("WAN video generator: OK", "SUCCESS")
        
        # Check WAN configuration
        if self.wan_config_path.exists():
            self.print_step("WAN configuration: OK", "SUCCESS")
        else:
            self.print_step("WAN configuration not found, will create default", "WARNING")
            self.create_default_wan_config()
            
        return True
        
    def create_default_wan_config(self):
        """Create default WAN configuration"""
        default_config = {
            "model_path": "./models/wan_model",
            "output_dir": "./data/videos/wan_output",
            "max_duration": 60,
            "resolution": "1920x1080",
            "fps": 30,
            "quality": "high",
            "use_gpu": True,
            "batch_size": 1,
            "temp_dir": "./data/temp/wan"
        }
        
        try:
            self.wan_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.wan_config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            self.print_step("Default WAN configuration created", "SUCCESS")
        except Exception as e:
            self.print_step(f"Failed to create WAN config: {e}", "ERROR")
            
    def test_wan_import(self) -> bool:
        """Test if WAN can be imported"""
        self.print_step("Testing WAN import...", "INFO")
        
        python_path = self.wan_venv_path / "Scripts" / "python.exe"
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"
            
        try:
            # Test basic imports
            test_script = """
import sys
sys.path.append('src')
try:
    from wan.video_generator import WANVideoGenerator
    print('WAN import: SUCCESS')
except ImportError as e:
    print(f'WAN import failed: {e}')
    sys.exit(1)
"""
            
            result = subprocess.run(
                [str(python_path), "-c", test_script],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.print_step("WAN import test: PASSED", "SUCCESS")
                return True
            else:
                self.print_step(f"WAN import test failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.print_step(f"WAN import test error: {e}", "ERROR")
            return False
            
    def start_wan_service(self) -> bool:
        """Start the WAN video generation service"""
        self.print_header("Starting WAN Service")
        
        python_path = self.wan_venv_path / "Scripts" / "python.exe"
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"
            
        # Create a simple WAN service script
        service_script = """
import sys
import time
sys.path.append('src')

from wan.video_generator import WANVideoGenerator

print("🎬 WAN Video Generation Service Started")
print("Listening for video generation requests...")

# Initialize WAN generator
try:
    generator = WANVideoGenerator()
    print("✅ WAN Generator initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize WAN Generator: {e}")
    sys.exit(1)

# Keep service running
try:
    while True:
        print("🔄 WAN Service heartbeat - Ready for requests")
        time.sleep(30)
except KeyboardInterrupt:
    print("\n🛑 WAN Service shutting down...")
    print("✅ WAN Service stopped")
"""
        
        try:
            self.print_step("Starting WAN video generation service...", "INFO")
            
            self.process = subprocess.Popen(
                [str(python_path), "-c", service_script],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give service time to start
            time.sleep(3)
            
            # Check if process is still running
            if self.process.poll() is None:
                self.print_step(f"WAN Service started (PID: {self.process.pid})", "SUCCESS")
                return True
            else:
                stdout, stderr = self.process.communicate()
                self.print_step(f"WAN Service failed to start: {stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.print_step(f"Failed to start WAN service: {e}", "ERROR")
            return False
            
    def monitor_service(self):
        """Monitor the WAN service"""
        self.print_header("Monitoring WAN Service")
        self.print_step("Press Ctrl+C to stop the service", "INFO")
        
        try:
            while True:
                if self.process and self.process.poll() is None:
                    # Service is running
                    time.sleep(5)
                else:
                    self.print_step("WAN Service has stopped", "WARNING")
                    break
                    
        except KeyboardInterrupt:
            self.print_step("Shutdown signal received", "INFO")
            self.stop_service()
            
    def stop_service(self):
        """Stop the WAN service"""
        if self.process and self.process.poll() is None:
            self.print_step("Stopping WAN service...", "INFO")
            
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
                self.print_step("WAN service stopped", "SUCCESS")
            except subprocess.TimeoutExpired:
                self.print_step("Force killing WAN service...", "WARNING")
                self.process.kill()
                self.process.wait()
            except Exception as e:
                self.print_step(f"Error stopping WAN service: {e}", "ERROR")
                
    def run(self) -> bool:
        """Run the WAN service startup sequence"""
        self.print_header("WAN Video Generation Service")
        
        # Check environment
        if not self.check_wan_environment():
            self.print_step("WAN environment check failed", "ERROR")
            return False
            
        # Test imports
        if not self.test_wan_import():
            self.print_step("WAN import test failed", "ERROR")
            return False
            
        # Start service
        if not self.start_wan_service():
            self.print_step("Failed to start WAN service", "ERROR")
            return False
            
        # Monitor service
        self.monitor_service()
        
        return True
        
def main():
    starter = WANServiceStarter()
    
    # Set up signal handlers
    def signal_handler(signum, frame):
        print("\nShutdown signal received")
        starter.stop_service()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    success = starter.run()
    return 0 if success else 1
    
if __name__ == "__main__":
    sys.exit(main())