#!/usr/bin/env python3
"""
🔍 MonAY Post-Deployment Validation Suite
Comprehensive testing to ensure all components work correctly after deployment fix
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
import importlib.util

class PostDeploymentValidator:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.is_windows = platform.system() == "Windows"
        self.is_linux = platform.system() == "Linux"
        self.results = {}
        
        # Platform-specific paths
        if self.is_linux:
            self.system_venv_path = Path("/opt/monay/venv")
            self.ai_venv_path = Path("/opt/monay/ai_service_venv")
            self.video_venv_path = Path("/opt/monay/video_service_venv")
            self.wan_venv_path = Path("/opt/monay/wan_venv")
            self.base_dir = "/opt/monay"
        else:
            self.system_venv_path = Path("C:/opt/monay/main_venv")
            self.ai_venv_path = Path("C:/opt/monay/ai_service_venv")
            self.video_venv_path = Path("C:/opt/monay/video_service_venv")
            self.wan_venv_path = Path("C:/opt/monay/wan_venv")
            self.base_dir = "C:/opt/monay"
    
    def print_header(self, message):
        print(f"\n{'='*60}")
        print(f"🔍 {message}")
        print(f"{'='*60}")
    
    def print_step(self, message, status="INFO"):
        icons = {"SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}
        print(f"{icons.get(status, 'ℹ️')} {message}")
    
    def run_command(self, cmd, cwd=None):
        """Execute command and return success status"""
        try:
            result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def validate_virtual_environments(self):
        """Test all virtual environments are functional"""
        self.print_header("Validating Virtual Environments")
        
        venvs = {
            "main_venv": self.system_venv_path,
            "ai_service_venv": self.ai_venv_path,
            "video_service_venv": self.video_venv_path,
            "wan_venv": self.wan_venv_path
        }
        
        all_good = True
        for name, path in venvs.items():
            # Check if directory exists
            if not path.exists():
                self.print_step(f"{name}: Directory not found at {path}", "ERROR")
                all_good = False
                continue
            
            # Check Python executable
            if self.is_windows:
                python_exe = path / "Scripts" / "python.exe"
                pip_exe = path / "Scripts" / "pip.exe"
            else:
                python_exe = path / "bin" / "python"
                pip_exe = path / "bin" / "pip"
            
            if not python_exe.exists():
                self.print_step(f"{name}: Python executable not found", "ERROR")
                all_good = False
                continue
            
            if not pip_exe.exists():
                self.print_step(f"{name}: pip executable not found", "ERROR")
                all_good = False
                continue
            
            # Test Python can run
            success, stdout, stderr = self.run_command([str(python_exe), "--version"])
            if success:
                self.print_step(f"{name}: Python {stdout.strip()}", "SUCCESS")
            else:
                self.print_step(f"{name}: Python execution failed", "ERROR")
                all_good = False
            
            # Test pip can run
            success, stdout, stderr = self.run_command([str(pip_exe), "--version"])
            if success:
                self.print_step(f"{name}: pip functional", "SUCCESS")
            else:
                self.print_step(f"{name}: pip execution failed", "ERROR")
                all_good = False
        
        self.results["virtual_environments"] = all_good
        return all_good
    
    def validate_core_imports(self):
        """Test core module imports work"""
        self.print_header("Validating Core Module Imports")
        
        # Test distribution module
        src_path = Path(self.base_dir) / "src"
        if not src_path.exists():
            self.print_step(f"Source directory not found: {src_path}", "ERROR")
            return False
        
        # Test imports using main Python
        main_python = self.system_venv_path
        if self.is_windows:
            main_python = main_python / "Scripts" / "python.exe"
        else:
            main_python = main_python / "bin" / "python"
        
        test_script = f"""
import sys
sys.path.insert(0, '{src_path}')

try:
    from distribution import EnhancedUploadManager, BlogManager, PODManager
    print("DISTRIBUTION_IMPORTS: SUCCESS")
except ImportError as e:
    print(f"DISTRIBUTION_IMPORTS: FAILED - {{e}}")
    sys.exit(1)

try:
    import torch
    print(f"TORCH_VERSION: {{torch.__version__}}")
except ImportError as e:
    print(f"TORCH: FAILED - {{e}}")
    sys.exit(1)

try:
    import transformers
    print(f"TRANSFORMERS_VERSION: {{transformers.__version__}}")
except ImportError as e:
    print(f"TRANSFORMERS: FAILED - {{e}}")
    sys.exit(1)

print("ALL_CORE_IMPORTS: SUCCESS")
"""
        
        success, stdout, stderr = self.run_command([str(main_python), "-c", test_script])
        
        if success and "ALL_CORE_IMPORTS: SUCCESS" in stdout:
            self.print_step("Core imports validated successfully", "SUCCESS")
            self.results["core_imports"] = True
            return True
        else:
            self.print_step("Core imports validation failed", "ERROR")
            self.print_step(f"Details: {stdout} {stderr}", "WARNING")
            self.results["core_imports"] = False
            return False
    
    def validate_youtube_tokens(self):
        """Test YouTube tokens are accessible"""
        self.print_header("Validating YouTube Tokens")
        
        tokens_file = Path(self.base_dir) / "youtube_tokens.json"
        if not tokens_file.exists():
            self.print_step("youtube_tokens.json not found", "ERROR")
            self.results["youtube_tokens"] = False
            return False
        
        try:
            with open(tokens_file) as f:
                tokens = json.load(f)
            
            if "access_token" in tokens and "refresh_token" in tokens:
                self.print_step("YouTube tokens file is valid", "SUCCESS")
                self.results["youtube_tokens"] = True
                return True
            else:
                self.print_step("YouTube tokens missing required fields", "ERROR")
                self.results["youtube_tokens"] = False
                return False
        except Exception as e:
            self.print_step(f"Error reading YouTube tokens: {e}", "ERROR")
            self.results["youtube_tokens"] = False
            return False
    
    def validate_configuration_files(self):
        """Test configuration files are present"""
        self.print_header("Validating Configuration Files")
        
        config_files = [
            ".env",
            "config.yaml",
            "requirements.txt"
        ]
        
        all_good = True
        for config_file in config_files:
            file_path = Path(self.base_dir) / config_file
            if file_path.exists():
                self.print_step(f"{config_file}: Found", "SUCCESS")
            else:
                self.print_step(f"{config_file}: Missing", "ERROR")
                all_good = False
        
        self.results["configuration_files"] = all_good
        return all_good
    
    def validate_deployment_results(self):
        """Test deployment results file"""
        self.print_header("Validating Deployment Results")
        
        results_file = Path(self.base_dir) / "deployment_results.json"
        if not results_file.exists():
            self.print_step("deployment_results.json not found", "WARNING")
            return True  # Not critical
        
        try:
            with open(results_file) as f:
                results = json.load(f)
            
            critical_components = ["main_venv", "ai_venv", "video_venv", "wan_venv"]
            for component in critical_components:
                if results.get(component, False):
                    self.print_step(f"{component}: Deployment marked as SUCCESS", "SUCCESS")
                else:
                    self.print_step(f"{component}: Deployment marked as FAILED", "WARNING")
            
            return True
        except Exception as e:
            self.print_step(f"Error reading deployment results: {e}", "WARNING")
            return True
    
    def run_comprehensive_test(self):
        """Run comprehensive validation of all components"""
        self.print_header("🚀 MonAY Post-Deployment Validation")
        
        tests = [
            ("Virtual Environments", self.validate_virtual_environments),
            ("Core Imports", self.validate_core_imports),
            ("YouTube Tokens", self.validate_youtube_tokens),
            ("Configuration Files", self.validate_configuration_files),
            ("Deployment Results", self.validate_deployment_results)
        ]
        
        all_passed = True
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            if not test_func():
                self.print_step(f"{test_name}: FAILED", "ERROR")
                all_passed = False
            else:
                self.print_step(f"{test_name}: PASSED", "SUCCESS")
        
        # Summary
        self.print_header("Validation Summary")
        print("\n📊 Results:")
        for key, value in self.results.items():
            status = "✅ PASS" if value else "❌ FAIL"
            print(f"  {status} {key.replace('_', ' ').title()}")
        
        if all_passed:
            print("\n🎉 All validations passed! MonAY system is ready for use.")
            print("\n🚀 Next steps:")
            print("   1. Start the service: sudo systemctl start monay.service")
            print("   2. Check status: sudo systemctl status monay.service")
            print("   3. Monitor logs: sudo journalctl -u monay.service -f")
        else:
            print("\n⚠️  Some validations failed. Please review the errors above.")
        
        return all_passed

if __name__ == "__main__":
    validator = PostDeploymentValidator()
    success = validator.run_comprehensive_test()
    sys.exit(0 if success else 1)