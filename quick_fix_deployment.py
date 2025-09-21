#!/usr/bin/env python3
"""
🚀 Quick Fix Deployment Script
Applies all the fixes needed for test_everything.py to pass
"""

import os
import sys
import subprocess
from pathlib import Path

class QuickFixDeployment:
    def __init__(self):
        self.project_root = Path.cwd()
        
    def print_step(self, message: str, status: str = "INFO"):
        """Print formatted step"""
        icons = {"SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}
        print(f"{icons.get(status, 'ℹ️')} {message}")
    
    def run_command(self, cmd: list, timeout: int = 300):
        """Run command and return success status and output"""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def install_google_api_modules(self) -> bool:
        """Install Google API modules in all virtual environments"""
        self.print_step("Installing Google API Modules")
        
        google_packages = [
            "google-api-python-client",
            "google-auth", 
            "google-auth-oauthlib",
            "google-auth-httplib2"
        ]
        
        venvs_to_update = [
            ("/opt/monay/main_venv/bin/pip", "main_venv"),
            ("/opt/monay/ai_service_venv/bin/pip", "ai_service_venv"), 
            ("/opt/monay/video_service_venv/bin/pip", "video_service_venv"),
            ("/opt/monay/wan_venv/bin/pip", "wan_venv"),
            ("venv/bin/pip", "project_venv")  # Local project venv
        ]
        
        for pip_path, venv_name in venvs_to_update:
            if not os.path.exists(pip_path):
                self.print_step(f"Skipping {venv_name} - pip not found at {pip_path}", "WARNING")
                continue
                
            self.print_step(f"Installing Google API modules in {venv_name}...")
            
            for package in google_packages:
                success, output = self.run_command([pip_path, "install", package])
                if success:
                    self.print_step(f"✅ {package} installed in {venv_name}", "SUCCESS")
                else:
                    self.print_step(f"⚠️ Failed to install {package} in {venv_name}: {output}", "WARNING")
        
        return True

    def fix_wan_directory_structure(self) -> bool:
        """Fix WAN directory structure for tests"""
        self.print_step("Fixing WAN Directory Structure")
        
        wan_dir = self.project_root / "wan"
        src_wan_dir = self.project_root / "src" / "wan"
        
        # Create wan directory if it doesn't exist
        if not wan_dir.exists():
            wan_dir.mkdir(exist_ok=True)
            self.print_step("Created wan directory", "SUCCESS")
        
        # Copy video_generator.py if it exists in src/wan
        if src_wan_dir.exists() and (src_wan_dir / "video_generator.py").exists():
            import shutil
            shutil.copy2(src_wan_dir / "video_generator.py", wan_dir / "video_generator.py")
            self.print_step("Copied video_generator.py to wan directory", "SUCCESS")
        
        # Create __init__.py if it doesn't exist
        init_file = wan_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")
            self.print_step("Created wan/__init__.py", "SUCCESS")
            
        return True

    def copy_missing_files_to_server(self) -> bool:
        """Copy missing test files to server (instructions only)"""
        self.print_step("Files to copy to server:")
        
        files_to_copy = [
            "test_everything.py",
            "test_deployment.py", 
            "test_distribution_import.py",
            "test_fix_immediately.py",
            "test_wan_generation.py",
            "setup_system_deployment.py"  # Updated version
        ]
        
        for file_name in files_to_copy:
            if (self.project_root / file_name).exists():
                self.print_step(f"📤 Copy: {file_name}", "INFO")
                print(f"   scp \"{self.project_root / file_name}\" george@94.72.111.253:~/monay_restored/")
            else:
                self.print_step(f"❌ Missing: {file_name}", "WARNING")
        
        return True

    def run_fixes(self) -> bool:
        """Run all fixes"""
        self.print_step("🚀 Running Quick Deployment Fixes")
        
        fixes = [
            ("Installing Google API modules", self.install_google_api_modules),
            ("Fixing WAN directory structure", self.fix_wan_directory_structure),
            ("Listing files to copy to server", self.copy_missing_files_to_server)
        ]
        
        for fix_name, fix_func in fixes:
            self.print_step(f"Running: {fix_name}")
            if not fix_func():
                self.print_step(f"Failed: {fix_name}", "ERROR")
                return False
            self.print_step(f"Completed: {fix_name}", "SUCCESS")
        
        self.print_step("🎉 All fixes completed!", "SUCCESS")
        
        # Print server commands
        print("\n🖥️ Commands to run on server:")
        print("# Install Google modules in server venvs:")
        print("/opt/monay/main_venv/bin/pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2")
        print("/opt/monay/ai_service_venv/bin/pip install google-api-python-client google-auth")
        print("/opt/monay/video_service_venv/bin/pip install google-api-python-client google-auth")
        print("/opt/monay/wan_venv/bin/pip install google-api-python-client google-auth")
        
        print("\n# Fix WAN directory:")
        print("cd ~/monay_restored")
        print("mkdir -p wan")
        print("cp src/wan/video_generator.py wan/ 2>/dev/null || echo 'video_generator.py not found'")
        print("touch wan/__init__.py")
        
        print("\n# Test everything:")
        print("python3 test_everything.py")
        
        return True

if __name__ == "__main__":
    fixer = QuickFixDeployment()
    success = fixer.run_fixes()
    sys.exit(0 if success else 1)