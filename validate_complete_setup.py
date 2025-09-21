#!/usr/bin/env python3
"""
🔍 MonAY Complete System Validation
Quick validation script to ensure all components are working
"""

import os
import sys
import subprocess
import requests
import json
import time
from pathlib import Path
from typing import Dict, List

class SystemValidator:
    def __init__(self):
        self.project_root = Path.cwd()
        self.wan_venv_path = self.project_root / "wan_venv"
        self.main_venv_path = self.project_root / "venv"
        self.validation_results = {}
        
    def print_header(self, title: str):
        """Print formatted section header"""
        print(f"\n{'='*50}")
        print(f"🔍 {title}")
        print(f"{'='*50}")
        
    def print_result(self, test: str, passed: bool, details: str = ""):
        """Print test result"""
        icon = "✅" if passed else "❌"
        print(f"{icon} {test}")
        if details:
            print(f"   📝 {details}")
        self.validation_results[test] = {"passed": passed, "details": details}
        
    def get_venv_python(self, venv_path: Path) -> str:
        """Get Python executable path for virtual environment"""
        if os.name == 'nt':  # Windows
            return str(venv_path / "Scripts" / "python.exe")
        else:  # Unix/Linux/macOS
            return str(venv_path / "bin" / "python")
            
    def run_command(self, cmd: List[str], timeout: int = 30) -> tuple:
        """Run command and return success status and output"""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                cwd=self.project_root
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
            
    def validate_python_environments(self):
        """Validate Python virtual environments"""
        self.print_header("Python Environments")
        
        # Check main venv
        main_python = self.get_venv_python(self.main_venv_path)
        if Path(main_python).exists():
            success, stdout, stderr = self.run_command([main_python, "--version"])
            if success:
                self.print_result("Main Virtual Environment", True, stdout.strip())
            else:
                self.print_result("Main Virtual Environment", False, stderr)
        else:
            self.print_result("Main Virtual Environment", False, "Python executable not found")
            
        # Check WAN venv
        wan_python = self.get_venv_python(self.wan_venv_path)
        if Path(wan_python).exists():
            success, stdout, stderr = self.run_command([wan_python, "--version"])
            if success:
                self.print_result("WAN Virtual Environment", True, stdout.strip())
            else:
                self.print_result("WAN Virtual Environment", False, stderr)
        else:
            self.print_result("WAN Virtual Environment", False, "Python executable not found")
            
    def validate_stable_diffusion(self):
        """Validate Stable Diffusion installation"""
        self.print_header("Stable Diffusion")
        
        main_python = self.get_venv_python(self.main_venv_path)
        if not Path(main_python).exists():
            self.print_result("Stable Diffusion Dependencies", False, "Main venv not found")
            return
            
        # Test torch (CPU-focused for server deployment)
        success, stdout, stderr = self.run_command([
            main_python, "-c", 
            "import torch; print(f'PyTorch {torch.__version__} - CPU cores: {torch.get_num_threads()}')"
        ])
        if success:
            self.print_result("PyTorch", True, stdout.strip())
        else:
            self.print_result("PyTorch", False, stderr)
            
        # Test diffusers
        success, stdout, stderr = self.run_command([
            main_python, "-c", 
            "import diffusers; print(f'Diffusers {diffusers.__version__}')"
        ])
        if success:
            self.print_result("Diffusers", True, stdout.strip())
        else:
            self.print_result("Diffusers", False, stderr)
            
        # Test transformers
        success, stdout, stderr = self.run_command([
            main_python, "-c", 
            "import transformers; print(f'Transformers {transformers.__version__}')"
        ])
        if success:
            self.print_result("Transformers", True, stdout.strip())
        else:
            self.print_result("Transformers", False, stderr)
            
        # Test compatibility check function
        enhanced_main = self.project_root / "src" / "enhanced_main.py"
        if enhanced_main.exists():
            success, stdout, stderr = self.run_command([
                main_python, "-c", 
                "import sys; sys.path.append('src'); from enhanced_main import check_stable_diffusion_server_compatibility; result = check_stable_diffusion_server_compatibility(); print(f\"Compatibility: {result['overall_status']}\")"
            ])
            if success:
                self.print_result("Compatibility Check", True, stdout.strip())
            else:
                self.print_result("Compatibility Check", False, stderr)
        else:
            self.print_result("Compatibility Check", False, "enhanced_main.py not found")
            
    def validate_wan_environment(self):
        """Validate WAN environment"""
        self.print_header("WAN Environment")
        
        wan_python = self.get_venv_python(self.wan_venv_path)
        if not Path(wan_python).exists():
            self.print_result("WAN Environment", False, "WAN venv not found")
            return
            
        # Test WAN dependencies
        dependencies = [
            ("torch", "import torch; print(f'PyTorch {torch.__version__}')"),
            ("transformers", "import transformers; print(f'Transformers {transformers.__version__}')"),
            ("numpy", "import numpy; print(f'NumPy {numpy.__version__}')"),
            ("datasets", "import datasets; print(f'Datasets {datasets.__version__}')"),
            ("accelerate", "import accelerate; print(f'Accelerate {accelerate.__version__}')")
        ]
        
        for dep_name, test_code in dependencies:
            success, stdout, stderr = self.run_command([wan_python, "-c", test_code])
            if success:
                self.print_result(f"WAN {dep_name}", True, stdout.strip())
            else:
                self.print_result(f"WAN {dep_name}", False, stderr)
                
        # Test WAN video generator
        wan_generator = self.project_root / "src" / "wan" / "video_generator.py"
        if wan_generator.exists():
            self.print_result("WAN Video Generator", True, "File exists")
        else:
            self.print_result("WAN Video Generator", False, "video_generator.py not found")
            
    def validate_ollama(self):
        """Validate Ollama installation and service"""
        self.print_header("Ollama")
        
        # Check Ollama command
        success, stdout, stderr = self.run_command(["ollama", "--version"])
        if success:
            self.print_result("Ollama Installation", True, stdout.strip())
        else:
            self.print_result("Ollama Installation", False, "Ollama command not found")
            return
            
        # Check Ollama service
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_count = len(models)
                self.print_result("Ollama Service", True, f"Running with {model_count} models")
                
                # List models
                if models:
                    model_names = [m.get("name", "unknown") for m in models]
                    print(f"   📋 Models: {', '.join(model_names)}")
            else:
                self.print_result("Ollama Service", False, f"HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.print_result("Ollama Service", False, f"Connection failed: {e}")
            
    def validate_mistral(self):
        """Validate Mistral model"""
        self.print_header("Mistral Model")
        
        try:
            # Check if Mistral model is available
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                mistral_models = [m for m in models if "mistral" in m.get("name", "").lower()]
                
                if mistral_models:
                    model_name = mistral_models[0]["name"]
                    self.print_result("Mistral Model Available", True, model_name)
                    
                    # Test Mistral inference
                    test_response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": "mistral",
                            "prompt": "Hello, respond with just 'OK'",
                            "stream": False
                        },
                        timeout=30
                    )
                    
                    if test_response.status_code == 200:
                        result = test_response.json()
                        response_text = result.get("response", "").strip()
                        self.print_result("Mistral Inference", True, f"Response: {response_text[:50]}...")
                    else:
                        self.print_result("Mistral Inference", False, f"HTTP {test_response.status_code}")
                else:
                    self.print_result("Mistral Model Available", False, "No Mistral models found")
            else:
                self.print_result("Mistral Model Check", False, "Ollama service not responding")
        except requests.exceptions.RequestException as e:
            self.print_result("Mistral Model Check", False, f"Connection failed: {e}")
            
    def validate_startup_scripts(self):
        """Validate startup scripts"""
        self.print_header("Startup Scripts")
        
        scripts = [
            ("Complete System Startup", "start_monay_complete.py"),
            ("WAN Service Launcher", "start_wan_service.py"),
            ("System Setup Script", "setup_complete_system.py")
        ]
        
        for script_name, script_file in scripts:
            script_path = self.project_root / script_file
            if script_path.exists():
                self.print_result(script_name, True, f"{script_file} exists")
            else:
                self.print_result(script_name, False, f"{script_file} not found")
                
    def validate_configuration_files(self):
        """Validate configuration files"""
        self.print_header("Configuration Files")
        
        configs = [
            ("Requirements", "requirements.txt"),
            ("Environment", ".env"),
            ("Config YAML", "config.yaml"),
            ("WAN PyProject", "src/wan/pyproject.toml"),
            ("Enhanced Main", "src/enhanced_main.py"),
            ("Data Bridge", "data_bridge.py")
        ]
        
        for config_name, config_file in configs:
            config_path = self.project_root / config_file
            if config_path.exists():
                self.print_result(config_name, True, f"{config_file} exists")
            else:
                self.print_result(config_name, False, f"{config_file} not found")
                
    def generate_validation_report(self):
        """Generate final validation report"""
        self.print_header("Validation Summary")
        
        total_tests = len(self.validation_results)
        passed_tests = sum(1 for result in self.validation_results.values() if result["passed"])
        failed_tests = total_tests - passed_tests
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for test_name, result in self.validation_results.items():
                if not result["passed"]:
                    print(f"   • {test_name}: {result['details']}")
                    
        # Save detailed report
        report_file = self.project_root / "validation_report.json"
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "detailed_results": self.validation_results
            }, f, indent=2)
            
        print(f"\n📄 Detailed report saved: {report_file}")
        
        # Overall system status
        critical_components = [
            "Main Virtual Environment",
            "WAN Virtual Environment", 
            "PyTorch",
            "Ollama Installation",
            "Ollama Service"
        ]
        
        critical_passed = all(
            self.validation_results.get(comp, {}).get("passed", False) 
            for comp in critical_components
        )
        
        if critical_passed:
            print("\n🎉 System is ready for deployment!")
            print("\n📋 Quick Start:")
            print("   1. python start_monay_complete.py  # Full system")
            print("   2. python start_wan_service.py     # WAN only")
            return True
        else:
            print("\n⚠️ Critical components failed - system not ready")
            print("\n🔧 Run: python setup_complete_system.py")
            return False
            
    def run_validation(self):
        """Run complete validation"""
        print("🔍 MonAY Complete System Validation")
        print("=" * 50)
        
        validation_steps = [
            self.validate_python_environments,
            self.validate_stable_diffusion,
            self.validate_wan_environment,
            self.validate_ollama,
            self.validate_mistral,
            self.validate_startup_scripts,
            self.validate_configuration_files
        ]
        
        for step in validation_steps:
            try:
                step()
            except Exception as e:
                print(f"❌ Validation step failed: {e}")
                
        return self.generate_validation_report()

def main():
    validator = SystemValidator()
    success = validator.run_validation()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())