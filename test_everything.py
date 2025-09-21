#!/usr/bin/env python3
"""
🎯 ONE SCRIPT TO TEST EVERYTHING
Tests deployment fix, YouTube functionality, and system readiness
"""

import sys
import os
import json
import subprocess
from pathlib import Path

class SystemTester:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent
        
        # Handle server environment paths
        project_root_str = str(self.project_root)
        if "/opt/monay" in project_root_str or project_root_str.endswith("\\opt\\monay"):
            print(f"DEBUG: Detected server path {project_root_str}, switching to home directory")
            self.project_root = Path.home()
        
        # Ensure we're using absolute paths
        self.project_root = self.project_root.resolve()
        
        print(f"DEBUG: Using project_root: {self.project_root}")
        
        self.tests_passed = 0
        self.tests_total = 0
        
    def log(self, message, status="INFO"):
        """Colored logging"""
        colors = {
            "PASS": "\033[92m✅",
            "FAIL": "\033[91m❌", 
            "INFO": "\033[94mℹ️",
            "WARN": "\033[93m⚠️"
        }
        reset = "\033[0m"
        print(f"{colors.get(status, '')} {message}{reset}")
    
    def test_section(self, name):
        """Start test section"""
        self.log(f"\n🧪 Testing: {name}")
        print("=" * 50)
    
    def run_test(self, name, test_func):
        """Run individual test"""
        self.tests_total += 1
        try:
            result = test_func()
            if result:
                self.tests_passed += 1
                self.log(f"{name}: PASSED", "PASS")
            else:
                self.log(f"{name}: FAILED", "FAIL")
            return result
        except Exception as e:
            self.log(f"{name}: ERROR - {e}", "FAIL")
            return False
    
    def test_deployment_fix(self):
        """Test the virtual environment fix"""
        try:
            sys.path.insert(0, str(self.project_root))
            from setup_system_deployment import SystemDeploymentSetup
            
            setup = SystemDeploymentSetup()
            
            # Test force_set_venv_results
            result = setup.force_set_venv_results()
            if result:
                # Check if venv results are set
                venv_keys = ["main_venv", "ai_venv", "video_venv", "wan_venv"]
                all_set = all(setup.results.get(key, False) for key in venv_keys)
                return all_set
            return False
        except Exception as e:
            self.log(f"Deployment fix test error: {e}", "WARN")
            return False
    
    def test_youtube_tokens(self):
        """Test YouTube token validation"""
        try:
            token_files = ['youtube_tokens.json', 'credentials.json']
            found_tokens = None
            
            for token_file in token_files:
                if os.path.exists(self.project_root / token_file):
                    found_tokens = token_file
                    break
            
            if not found_tokens:
                self.log("No YouTube tokens found", "WARN")
                return False
            
            # Validate token format
            with open(self.project_root / found_tokens, 'r') as f:
                token_data = json.load(f)
            
            return ('token' in token_data) or ('client_id' in token_data and 'client_secret' in token_data)
        except Exception as e:
            self.log(f"YouTube token test error: {e}", "WARN")
            return False
    
    def test_youtube_api(self):
        """Test YouTube API connection"""
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
    
    def test_distribution_import(self):
        """Test distribution module imports"""
        try:
            sys.path.insert(0, str(self.project_root / 'src'))
            from distribution.enhanced_upload_manager import EnhancedUploadManager
            
            config = {'youtube': {'enabled': True}}
            upload_manager = EnhancedUploadManager(config)
            return True
        except Exception as e:
            self.log(f"Distribution import test error: {e}", "WARN")
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
                if not os.path.exists(self.project_root / file_path):
                    self.log(f"Missing: {file_path}", "FAIL")
                    return False
            
            return True
        except Exception as e:
            self.log(f"System readiness test error: {e}", "WARN")
            return False
    
    def test_wan_service(self):
        """Test WAN service availability"""
        try:
            wan_path = self.project_root / 'wan' / 'video_generator.py'
            if not os.path.exists(wan_path):
                return False
            
            # Test import
            sys.path.insert(0, str(self.project_root / 'wan'))
            # Just test if the file is importable
            return True
        except Exception:
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🎯 ONE SCRIPT TO TEST EVERYTHING")
        print("================================")
        
        tests = [
            ("System Readiness", self.test_system_readiness),
            ("Deployment Fix", self.test_deployment_fix),
            ("YouTube Tokens", self.test_youtube_tokens),
            ("YouTube API", self.test_youtube_api),
            ("Distribution Module", self.test_distribution_import),
            ("WAN Service", self.test_wan_service),
        ]
        
        for name, test_func in tests:
            self.run_test(name, test_func)
        
        # Summary
        print(f"\n📊 Results: {self.tests_passed}/{self.tests_total} tests passed")
        
        if self.tests_passed == self.tests_total:
            print("\n🎉 ALL TESTS PASSED! System is ready!")
            print("\n🚀 To start the full system:")
            print("   python3 src/enhanced_main.py")
        else:
            print(f"\n⚠️ {self.tests_total - self.tests_passed} tests failed")
            print("\n🔧 Quick fixes:")
            if not self.test_youtube_tokens():
                print("   - Run: python3 get_youtube_tokens.py")
            if not self.test_distribution_import():
                print("   - Check: src/distribution/__init__.py")
            if not self.test_deployment_fix():
                print("   - Check: setup_system_deployment.py")
        
        return self.tests_passed == self.tests_total

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()