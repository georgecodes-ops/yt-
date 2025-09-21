#!/usr/bin/env python3
"""
🚀 COMPLETE STARTUP & TESTING SCRIPT
Tests everything and starts the system with proper YouTube token handling
"""

import sys
import os
import json
import subprocess
import webbrowser
import time
from pathlib import Path

class CompleteStartup:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent
        self.tests_passed = 0
        self.tests_total = 0
        self.has_youtube_tokens = False
        
    def log(self, message, status="INFO"):
        """Colored logging"""
        colors = {
            "PASS": "\033[92m✅",
            "FAIL": "\033[91m❌", 
            "INFO": "\033[94mℹ️",
            "WARN": "\033[93m⚠️",
            "START": "\033[96m🚀",
            "SETUP": "\033[95m🔧"
        }
        reset = "\033[0m"
        print(f"{colors.get(status, '')} {message}{reset}")
    
    def check_youtube_tokens(self):
        """Check if YouTube tokens exist and are valid"""
        self.log("Checking YouTube tokens...")
        
        token_files = [
            'youtube_tokens.json',
            'credentials.json',
            'client_secret_919510636273.json',
            'client_secret_919510636273-6irenq7b2tncl8r5pqajh8t8fp1n73.apps.googleusercontent.com.json'
        ]
        
        found_tokens = None
        for token_file in token_files:
            token_path = self.project_root / token_file
            if token_path.exists():
                try:
                    with open(token_path, 'r') as f:
                        token_data = json.load(f)
                    
                    # Check if it's valid YouTube tokens
                    if 'token' in str(token_data) or ('client_id' in token_data and 'client_secret' in token_data):
                        found_tokens = token_file
                        break
                except:
                    continue
        
        if found_tokens:
            self.log(f"YouTube tokens found: {found_tokens}", "PASS")
            self.has_youtube_tokens = True
            return True
        else:
            self.log("No valid YouTube tokens found", "FAIL")
            return False
    
    def setup_youtube_tokens(self):
        """Run YouTube token setup if needed"""
        self.log("Setting up YouTube tokens...", "SETUP")
        
        try:
            # Run the YouTube token setup script
            result = subprocess.run([
                sys.executable, 
                str(self.project_root / 'get_youtube_tokens.py')
            ], capture_output=True, text=True, cwd=str(self.project_root))
            
            if result.returncode == 0:
                self.log("YouTube tokens setup completed", "PASS")
                self.has_youtube_tokens = True
                return True
            else:
                self.log(f"YouTube setup failed: {result.stderr}", "FAIL")
                return False
        except Exception as e:
            self.log(f"Error setting up YouTube tokens: {e}", "FAIL")
            return False
    
    def test_deployment_fix(self):
        """Test the virtual environment fix"""
        try:
            sys.path.insert(0, str(self.project_root))
            from setup_system_deployment import SystemDeploymentSetup
            
            setup = SystemDeploymentSetup()
            result = setup.force_set_venv_results()
            
            if result:
                venv_keys = ["main_venv", "ai_venv", "video_venv", "wan_venv"]
                all_set = all(setup.results.get(key, False) for key in venv_keys)
                return all_set
            return False
        except Exception as e:
            self.log(f"Deployment fix test error: {e}", "WARN")
            return False
    
    def test_system_readiness(self):
        """Test overall system readiness"""
        try:
            # Check Python version
            if sys.version_info < (3, 8):
                self.log("Python 3.8+ required", "FAIL")
                return False
            
            # Check essential files
            essential_files = [
                'config.yaml',
                'requirements.txt',
                'src/enhanced_main.py'
            ]
            
            for file_path in essential_files:
                if not (self.project_root / file_path).exists():
                    self.log(f"Missing: {file_path}", "FAIL")
                    return False
            
            return True
        except Exception as e:
            self.log(f"System readiness test error: {e}", "WARN")
            return False
    
    def test_distribution_import(self):
        """Test distribution module imports"""
        try:
            sys.path.insert(0, str(self.project_root / 'src'))
            from distribution.enhanced_upload_manager import EnhancedUploadManager
            
            config = {'youtube': {'enabled': self.has_youtube_tokens}}
            upload_manager = EnhancedUploadManager(config)
            return True
        except Exception as e:
            self.log(f"Distribution import test error: {e}", "WARN")
            return False
    
    def test_youtube_api(self):
        """Test YouTube API connection"""
        if not self.has_youtube_tokens:
            self.log("Skipping YouTube API test (no tokens)", "WARN")
            return False
            
        try:
            sys.path.insert(0, str(self.project_root))
            from get_youtube_tokens import get_youtube_service
            
            youtube = get_youtube_service()
            if youtube:
                response = youtube.channels().list(part='snippet', mine=True).execute()
                return bool(response.get('items'))
            return False
        except Exception as e:
            self.log(f"YouTube API test error: {e}", "WARN")
            return False
    
    def install_requirements(self):
        """Install required packages"""
        self.log("Checking requirements...")
        
        try:
            # Check if requirements are already installed
            import google.auth
            import googleapiclient.discovery
            import yaml
            return True
        except ImportError:
            self.log("Installing requirements...", "SETUP")
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
                ], check=True)
                return True
            except subprocess.CalledProcessError:
                self.log("Failed to install requirements", "FAIL")
                return False
    
    def run_complete_test(self):
        """Run all tests with YouTube token handling"""
        print("🎯 COMPLETE STARTUP & TESTING")
        print("===============================")
        
        # Install requirements first
        if not self.install_requirements():
            return False
        
        # Check YouTube tokens
        if not self.check_youtube_tokens():
            setup_choice = input("\n🤖 YouTube tokens missing. Set up now? (y/n): ").strip().lower()
            if setup_choice == 'y':
                if not self.setup_youtube_tokens():
                    print("❌ Cannot proceed without YouTube tokens")
                    return False
            else:
                print("⚠️ Continuing without YouTube functionality")
        
        # Run comprehensive tests
        tests = [
            ("System Readiness", self.test_system_readiness),
            ("Deployment Fix", self.test_deployment_fix),
            ("Distribution Module", self.test_distribution_import),
        ]
        
        if self.has_youtube_tokens:
            tests.append(("YouTube API", self.test_youtube_api))
        
        for name, test_func in tests:
            self.tests_total += 1
            if test_func():
                self.tests_passed += 1
        
        # Summary
        print(f"\n📊 Results: {self.tests_passed}/{self.tests_total} tests passed")
        
        if self.tests_passed == self.tests_total:
            print("\n🎉 ALL TESTS PASSED! System is ready!")
            return True
        else:
            print(f"\n⚠️ {self.tests_total - self.tests_passed} tests failed")
            return False
    
    def start_system(self):
        """Start the complete system"""
        if not self.run_complete_test():
            print("\n❌ Cannot start system - tests failed")
            return False
        
        print("\n🚀 Starting the complete YouTube automation system...")
        
        # Start options
        print("\n📋 Choose startup method:")
        print("1. Foreground (see all logs)")
        print("2. Background (with log file)")
        print("3. Screen session (recommended for servers)")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        try:
            if choice == "1":
                # Foreground
                subprocess.run([sys.executable, "src/enhanced_main.py"])
            elif choice == "2":
                # Background
                subprocess.Popen([
                    sys.executable, "src/enhanced_main.py"
                ], stdout=open('system.log', 'w'), stderr=subprocess.STDOUT)
                print("✅ System started in background")
                print("📊 Monitor with: tail -f system.log")
            elif choice == "3":
                # Screen session (Unix-like systems)
                try:
                    subprocess.run(["screen", "-S", "youtube", "-dm", 
                                  sys.executable, "src/enhanced_main.py"])
                    print("✅ System started in screen session 'youtube'")
                    print("📊 Attach with: screen -r youtube")
                except FileNotFoundError:
                    print("⚠️ Screen not available, starting in background")
                    subprocess.Popen([
                        sys.executable, "src/enhanced_main.py"
                    ], stdout=open('system.log', 'w'), stderr=subprocess.STDOUT)
            else:
                print("❌ Invalid choice")
                return False
                
        except KeyboardInterrupt:
            print("\n🛑 System startup interrupted")
            return False
        
        return True

if __name__ == "__main__":
    startup = CompleteStartup()
    
    # Quick start option
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        startup.start_system()
    else:
        startup.run_complete_test()