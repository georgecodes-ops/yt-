#!/usr/bin/env python3
"""
🚀 MonAY Complete System Startup Script
Starts all MonAY services and components
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from typing import List, Dict

class MonAYSystemStarter:
    def __init__(self):
        self.project_root = Path.cwd()
        self.processes: List[subprocess.Popen] = []
        self.services = {
            'main': {
                'script': 'src/enhanced_main.py',
                'port': 8000,
                'name': 'Main MonAY Service'
            },
            'ai_service': {
                'script': 'ai_service/main.py', 
                'port': 8001,
                'name': 'AI Service'
            },
            'video_service': {
                'script': 'video_service/main.py',
                'port': 8002, 
                'name': 'Video Service'
            }
        }
        
    def print_header(self, message: str):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"🚀 {message}")
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
        
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are available"""
        self.print_header("Checking Dependencies")
        
        # Check Python virtual environments
        venvs = ['venv', 'ai_service/venv', 'video_service/venv', 'wan_venv']
        for venv in venvs:
            venv_path = self.project_root / venv
            python_path = venv_path / 'Scripts' / 'python.exe'  # Windows
            if not python_path.exists():
                python_path = venv_path / 'bin' / 'python'  # Linux
                
            if python_path.exists():
                self.print_step(f"Virtual environment {venv}: OK", "SUCCESS")
            else:
                self.print_step(f"Virtual environment {venv}: MISSING", "ERROR")
                return False
                
        # Check configuration files
        config_files = ['.env', 'config.yaml', 'requirements.txt']
        for config_file in config_files:
            if (self.project_root / config_file).exists():
                self.print_step(f"Configuration {config_file}: OK", "SUCCESS")
            else:
                self.print_step(f"Configuration {config_file}: MISSING", "WARNING")
                
        return True
        
    def start_service(self, service_name: str, service_config: Dict) -> bool:
        """Start a specific service"""
        script_path = self.project_root / service_config['script']
        
        if not script_path.exists():
            self.print_step(f"Script {script_path} not found", "ERROR")
            return False
            
        # Determine Python executable
        if service_name == 'main':
            python_path = self.project_root / 'venv' / 'Scripts' / 'python.exe'
            if not python_path.exists():
                python_path = self.project_root / 'venv' / 'bin' / 'python'
        elif service_name in ['ai_service', 'video_service']:
            python_path = self.project_root / f'{service_name}' / 'venv' / 'Scripts' / 'python.exe'
            if not python_path.exists():
                python_path = self.project_root / f'{service_name}' / 'venv' / 'bin' / 'python'
        else:
            python_path = sys.executable
            
        if not python_path.exists():
            self.print_step(f"Python executable not found for {service_name}", "ERROR")
            return False
            
        try:
            self.print_step(f"Starting {service_config['name']}...", "INFO")
            
            # Start the service
            process = subprocess.Popen(
                [str(python_path), str(script_path)],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes.append(process)
            self.print_step(f"{service_config['name']} started (PID: {process.pid})", "SUCCESS")
            
            # Give service time to start
            time.sleep(2)
            
            # Check if process is still running
            if process.poll() is None:
                self.print_step(f"{service_config['name']} is running on port {service_config['port']}", "SUCCESS")
                return True
            else:
                stdout, stderr = process.communicate()
                self.print_step(f"{service_config['name']} failed to start: {stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.print_step(f"Failed to start {service_config['name']}: {e}", "ERROR")
            return False
            
    def start_all_services(self) -> bool:
        """Start all MonAY services"""
        self.print_header("Starting MonAY Services")
        
        success_count = 0
        for service_name, service_config in self.services.items():
            if self.start_service(service_name, service_config):
                success_count += 1
            time.sleep(1)  # Stagger service starts
            
        total_services = len(self.services)
        self.print_step(f"Started {success_count}/{total_services} services", 
                       "SUCCESS" if success_count == total_services else "WARNING")
        
        return success_count > 0
        
    def monitor_services(self):
        """Monitor running services"""
        self.print_header("Monitoring Services")
        self.print_step("Press Ctrl+C to stop all services", "INFO")
        
        try:
            while True:
                running_count = 0
                for i, process in enumerate(self.processes):
                    if process.poll() is None:
                        running_count += 1
                    else:
                        service_name = list(self.services.keys())[i]
                        self.print_step(f"Service {service_name} has stopped", "WARNING")
                        
                if running_count == 0:
                    self.print_step("All services have stopped", "WARNING")
                    break
                    
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.print_step("Shutdown signal received", "INFO")
            self.stop_all_services()
            
    def stop_all_services(self):
        """Stop all running services"""
        self.print_header("Stopping Services")
        
        for i, process in enumerate(self.processes):
            if process.poll() is None:
                service_name = list(self.services.keys())[i]
                self.print_step(f"Stopping {service_name}...", "INFO")
                
                try:
                    process.terminate()
                    process.wait(timeout=10)
                    self.print_step(f"{service_name} stopped", "SUCCESS")
                except subprocess.TimeoutExpired:
                    self.print_step(f"Force killing {service_name}...", "WARNING")
                    process.kill()
                    process.wait()
                except Exception as e:
                    self.print_step(f"Error stopping {service_name}: {e}", "ERROR")
                    
    def run(self) -> bool:
        """Run the complete startup sequence"""
        self.print_header("MonAY Complete System Startup")
        
        # Check dependencies
        if not self.check_dependencies():
            self.print_step("Dependency check failed", "ERROR")
            return False
            
        # Start services
        if not self.start_all_services():
            self.print_step("Failed to start services", "ERROR")
            return False
            
        # Monitor services
        self.monitor_services()
        
        return True
        
def main():
    starter = MonAYSystemStarter()
    
    # Set up signal handlers
    def signal_handler(signum, frame):
        print("\nShutdown signal received")
        starter.stop_all_services()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    success = starter.run()
    return 0 if success else 1
    
if __name__ == "__main__":
    sys.exit(main())