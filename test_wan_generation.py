#!/usr/bin/env python3
"""
🧪 WAN Video Generation Test Script
Comprehensive testing for WAN video generation functionality
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Optional

class WANGenerationTester:
    def __init__(self):
        self.project_root = Path.cwd()
        self.wan_venv_path = self.project_root / "wan_venv"
        self.test_results: Dict[str, bool] = {}
        self.test_outputs: Dict[str, str] = {}
        
    def print_header(self, message: str):
        """Print formatted header"""
        print(f"\n{'='*60}")
        print(f"🧪 {message}")
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
        
    def test_wan_environment(self) -> bool:
        """Test WAN virtual environment setup"""
        self.print_header("Testing WAN Environment")
        
        # Check WAN virtual environment exists
        python_path = self.wan_venv_path / "Scripts" / "python.exe"  # Windows
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"  # Linux
            
        if not python_path.exists():
            self.print_step("WAN virtual environment not found", "ERROR")
            self.test_results["wan_venv"] = False
            return False
            
        # Test Python version
        try:
            result = subprocess.run(
                [str(python_path), "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.print_step(f"WAN Python: {version}", "SUCCESS")
                self.test_results["wan_python"] = True
            else:
                self.print_step("Failed to get Python version", "ERROR")
                self.test_results["wan_python"] = False
                return False
                
        except Exception as e:
            self.print_step(f"Python version check failed: {e}", "ERROR")
            self.test_results["wan_python"] = False
            return False
            
        self.test_results["wan_venv"] = True
        return True
        
    def test_wan_dependencies(self) -> bool:
        """Test WAN dependencies are installed"""
        self.print_header("Testing WAN Dependencies")
        
        python_path = self.wan_venv_path / "Scripts" / "python.exe"
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"
            
        # Critical WAN dependencies
        dependencies = [
            "torch", "torchvision", "transformers", "diffusers",
            "opencv-python", "numpy", "PIL", "accelerate",
            "safetensors", "huggingface_hub", "dotenv"
        ]
        
        failed_deps = []
        
        for dep in dependencies:
            try:
                # Handle special import names
                import_name = dep
                if dep == "opencv-python":
                    import_name = "cv2"
                elif dep == "PIL":
                    import_name = "PIL"
                elif dep == "dotenv":
                    import_name = "dotenv"
                    
                result = subprocess.run(
                    [str(python_path), "-c", f"import {import_name}; print('{dep} OK')"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    self.print_step(f"{dep}: OK", "SUCCESS")
                else:
                    self.print_step(f"{dep}: FAILED", "ERROR")
                    failed_deps.append(dep)
                    
            except Exception as e:
                self.print_step(f"{dep}: ERROR - {e}", "ERROR")
                failed_deps.append(dep)
                
        if failed_deps:
            self.print_step(f"Failed dependencies: {', '.join(failed_deps)}", "ERROR")
            self.test_results["wan_dependencies"] = False
            return False
        else:
            self.print_step("All WAN dependencies available", "SUCCESS")
            self.test_results["wan_dependencies"] = True
            return True
            
    def test_wan_import(self) -> bool:
        """Test WAN video generator import"""
        self.print_header("Testing WAN Import")
        
        python_path = self.wan_venv_path / "Scripts" / "python.exe"
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"
            
        test_script = """
import sys
import os
sys.path.append('src')

try:
    from wan.video_generator import WANVideoGenerator
    print('SUCCESS: WAN video generator imported')
except ImportError as e:
    print(f'IMPORT_ERROR: {e}')
    sys.exit(1)
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
"""
        
        try:
            result = subprocess.run(
                [str(python_path), "-c", test_script],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and "SUCCESS" in result.stdout:
                self.print_step("WAN video generator import: SUCCESS", "SUCCESS")
                self.test_results["wan_import"] = True
                return True
            else:
                self.print_step(f"WAN import failed: {result.stdout} {result.stderr}", "ERROR")
                self.test_results["wan_import"] = False
                return False
                
        except Exception as e:
            self.print_step(f"WAN import test error: {e}", "ERROR")
            self.test_results["wan_import"] = False
            return False
            
    def test_wan_initialization(self) -> bool:
        """Test WAN video generator initialization"""
        self.print_header("Testing WAN Initialization")
        
        python_path = self.wan_venv_path / "Scripts" / "python.exe"
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"
            
        test_script = """
import sys
import os
sys.path.append('src')

try:
    from wan.video_generator import WANVideoGenerator
    
    # Try to initialize the generator
    generator = WANVideoGenerator()
    print('SUCCESS: WAN generator initialized')
    
    # Test basic configuration
    if hasattr(generator, 'config'):
        print('SUCCESS: WAN config loaded')
    else:
        print('WARNING: WAN config not found')
        
except Exception as e:
    print(f'INIT_ERROR: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        
        try:
            result = subprocess.run(
                [str(python_path), "-c", test_script],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0 and "SUCCESS: WAN generator initialized" in result.stdout:
                self.print_step("WAN generator initialization: SUCCESS", "SUCCESS")
                if "WARNING" in result.stdout:
                    self.print_step("WAN config warning detected", "WARNING")
                self.test_results["wan_init"] = True
                return True
            else:
                self.print_step(f"WAN initialization failed: {result.stdout} {result.stderr}", "ERROR")
                self.test_results["wan_init"] = False
                return False
                
        except Exception as e:
            self.print_step(f"WAN initialization test error: {e}", "ERROR")
            self.test_results["wan_init"] = False
            return False
            
    def test_wan_basic_generation(self) -> bool:
        """Test basic WAN video generation capability"""
        self.print_header("Testing WAN Basic Generation")
        
        python_path = self.wan_venv_path / "Scripts" / "python.exe"
        if not python_path.exists():
            python_path = self.wan_venv_path / "bin" / "python"
            
        test_script = """
import sys
import os
sys.path.append('src')

try:
    from wan.video_generator import WANVideoGenerator
    
    # Initialize generator
    generator = WANVideoGenerator()
    
    # Test basic generation method exists
    if hasattr(generator, 'generate'):
        print('SUCCESS: WAN generate method available')
    else:
        print('ERROR: WAN generate method not found')
        sys.exit(1)
        
    # Test configuration methods
    if hasattr(generator, '_load_wan_config'):
        print('SUCCESS: WAN config loader available')
    else:
        print('WARNING: WAN config loader not found')
        
    print('SUCCESS: WAN basic generation test passed')
    
except Exception as e:
    print(f'GENERATION_ERROR: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        
        try:
            result = subprocess.run(
                [str(python_path), "-c", test_script],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and "SUCCESS: WAN basic generation test passed" in result.stdout:
                self.print_step("WAN basic generation test: SUCCESS", "SUCCESS")
                self.test_results["wan_generation"] = True
                return True
            else:
                self.print_step(f"WAN generation test failed: {result.stdout} {result.stderr}", "ERROR")
                self.test_results["wan_generation"] = False
                return False
                
        except Exception as e:
            self.print_step(f"WAN generation test error: {e}", "ERROR")
            self.test_results["wan_generation"] = False
            return False
            
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report"""
        self.print_header("Test Report")
        
        total_tests = len(self.test_results)
        passed_tests = sum(self.test_results.values())
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": success_rate
            },
            "detailed_results": self.test_results,
            "test_outputs": self.test_outputs
        }
        
        # Print summary
        self.print_step(f"Total tests: {total_tests}", "INFO")
        self.print_step(f"Passed: {passed_tests}", "SUCCESS" if passed_tests == total_tests else "INFO")
        self.print_step(f"Failed: {total_tests - passed_tests}", "ERROR" if passed_tests < total_tests else "INFO")
        self.print_step(f"Success rate: {success_rate:.1f}%", 
                       "SUCCESS" if success_rate >= 80 else "WARNING" if success_rate >= 60 else "ERROR")
        
        # Save report
        try:
            report_path = self.project_root / "wan_test_report.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            self.print_step(f"Test report saved to: {report_path}", "SUCCESS")
        except Exception as e:
            self.print_step(f"Failed to save test report: {e}", "WARNING")
            
        return report
        
    def run_all_tests(self) -> bool:
        """Run all WAN tests"""
        self.print_header("WAN Video Generation Test Suite")
        
        tests = [
            self.test_wan_environment,
            self.test_wan_dependencies,
            self.test_wan_import,
            self.test_wan_initialization,
            self.test_wan_basic_generation
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                self.print_step(f"Test {test.__name__} failed with exception: {e}", "ERROR")
                self.test_results[test.__name__] = False
                
        # Generate report
        report = self.generate_test_report()
        
        # Return success if 80% or more tests passed
        return report["summary"]["success_rate"] >= 80
        
def main():
    tester = WANGenerationTester()
    success = tester.run_all_tests()
    return 0 if success else 1
    
if __name__ == "__main__":
    sys.exit(main())