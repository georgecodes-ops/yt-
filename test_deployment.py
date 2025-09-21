#!/usr/bin/env python3
"""
MonAY Deployment Test Script

This script tests the complete deployment flow to ensure all components
work correctly before production deployment.
"""

import subprocess
import sys
import time
from pathlib import Path
import json
import requests
from setup_system_deployment import MonAYSystemDeployment

class DeploymentTester:
    def __init__(self):
        self.test_results = {}
        self.deployment = MonAYSystemDeployment()
    
    def print_test_header(self, message: str):
        """Print a formatted test header"""
        print(f"\n{'='*60}")
        print(f" {message}")
        print(f"{'='*60}")
    
    def print_test_step(self, message: str, status: str = "INFO"):
        """Print a formatted test step"""
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
    
    def test_virtual_environments(self) -> bool:
        """Test all virtual environments are working"""
        import platform
        self.print_test_header("Testing Virtual Environments")
        
        # Use platform-appropriate paths
        if platform.system() == 'Windows':
            base_path = "C:/opt/monay"
        else:
            base_path = "/opt/monay"
            
        venvs = {
            "main": f"{base_path}/venv",
            "ai_service": f"{base_path}/ai_service/venv",
            "video_service": f"{base_path}/video_service/venv",
            "wan": f"{base_path}/wan/venv"
        }
        
        all_passed = True
        for name, path in venvs.items():
            python_path = f"{path}/bin/python"
            try:
                result = subprocess.run([python_path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.print_test_step(f"{name} venv: {result.stdout.strip()}", "SUCCESS")
                    self.test_results[f"venv_{name}"] = True
                else:
                    self.print_test_step(f"{name} venv failed: {result.stderr}", "ERROR")
                    self.test_results[f"venv_{name}"] = False
                    all_passed = False
            except Exception as e:
                self.print_test_step(f"{name} venv error: {e}", "ERROR")
                self.test_results[f"venv_{name}"] = False
                all_passed = False
        
        return all_passed
    
    def test_dependencies(self) -> bool:
        """Test critical dependencies are installed"""
        self.print_test_header("Testing Dependencies")
        
        main_python = "/opt/monay/venv/bin/python"
        critical_packages = [
            "torch", "transformers", "diffusers", "requests", 
            "numpy", "fastapi", "uvicorn", "pydantic"
        ]
        
        all_passed = True
        for package in critical_packages:
            try:
                result = subprocess.run(
                    [main_python, "-c", f"import {package}; print('{package} imported successfully')"],
                    capture_output=True, text=True, timeout=30
                )
                if result.returncode == 0:
                    self.print_test_step(f"{package}: OK", "SUCCESS")
                    self.test_results[f"dep_{package}"] = True
                else:
                    self.print_test_step(f"{package}: FAILED - {result.stderr}", "ERROR")
                    self.test_results[f"dep_{package}"] = False
                    all_passed = False
            except Exception as e:
                self.print_test_step(f"{package}: ERROR - {e}", "ERROR")
                self.test_results[f"dep_{package}"] = False
                all_passed = False
        
        return all_passed
    
    def test_service_status(self) -> bool:
        """Test systemd service status"""
        self.print_test_header("Testing Service Status")
        
        try:
            # Check if service is enabled
            result = subprocess.run(["systemctl", "is-enabled", "monay.service"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_test_step(f"Service enabled: {result.stdout.strip()}", "SUCCESS")
                self.test_results["service_enabled"] = True
            else:
                self.print_test_step(f"Service not enabled: {result.stderr}", "ERROR")
                self.test_results["service_enabled"] = False
                return False
            
            # Check if service is active
            result = subprocess.run(["systemctl", "is-active", "monay.service"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_test_step(f"Service active: {result.stdout.strip()}", "SUCCESS")
                self.test_results["service_active"] = True
            else:
                self.print_test_step(f"Service not active: {result.stderr}", "WARNING")
                self.test_results["service_active"] = False
            
            # Get service status
            result = subprocess.run(["systemctl", "status", "monay.service", "--no-pager"],
                                  capture_output=True, text=True)
            self.print_test_step("Service status output:", "INFO")
            print(result.stdout)
            
            return True
            
        except Exception as e:
            self.print_test_step(f"Service status check failed: {e}", "ERROR")
            self.test_results["service_status"] = False
            return False
    
    def test_api_endpoints(self) -> bool:
        """Test API endpoints are responding"""
        self.print_test_header("Testing API Endpoints")
        
        # Wait for service to be ready
        self.print_test_step("Waiting for service to be ready...", "INFO")
        time.sleep(10)
        
        endpoints = [
            ("http://localhost:8000/health", "Main API Health"),
            ("http://localhost:8001/health", "AI Service Health"),
            ("http://localhost:8002/health", "Video Service Health")
        ]
        
        all_passed = True
        for url, name in endpoints:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.print_test_step(f"{name}: OK (Status: {response.status_code})", "SUCCESS")
                    self.test_results[f"api_{name.lower().replace(' ', '_')}"] = True
                else:
                    self.print_test_step(f"{name}: FAILED (Status: {response.status_code})", "ERROR")
                    self.test_results[f"api_{name.lower().replace(' ', '_')}"] = False
                    all_passed = False
            except requests.exceptions.RequestException as e:
                self.print_test_step(f"{name}: ERROR - {e}", "ERROR")
                self.test_results[f"api_{name.lower().replace(' ', '_')}"] = False
                all_passed = False
        
        return all_passed
    
    def test_configuration_files(self) -> bool:
        """Test configuration files are present and valid"""
        import platform
        self.print_test_header("Testing Configuration Files")
        
        # Use platform-appropriate paths
        if platform.system() == 'Windows':
            base_path = "C:/opt/monay"
            service_path = "C:/opt/monay/monay.service"  # Windows service location
        else:
            base_path = "/opt/monay"
            service_path = "/etc/systemd/system/monay.service"  # Linux systemd location
            
        config_files = [
            f"{base_path}/.env",
            f"{base_path}/config.yaml",
            f"{base_path}/requirements.txt",
            service_path
        ]
        
        all_passed = True
        for config_file in config_files:
            if Path(config_file).exists():
                self.print_test_step(f"{config_file}: EXISTS", "SUCCESS")
                self.test_results[f"config_{Path(config_file).name}"] = True
            else:
                self.print_test_step(f"{config_file}: MISSING", "ERROR")
                self.test_results[f"config_{Path(config_file).name}"] = False
                all_passed = False
        
        return all_passed
    
    def run_full_test_suite(self) -> bool:
        """Run the complete test suite"""
        self.print_test_header("MonAY Deployment Test Suite")
        
        tests = [
            ("Configuration Files", self.test_configuration_files),
            ("Virtual Environments", self.test_virtual_environments),
            ("Dependencies", self.test_dependencies),
            ("Service Status", self.test_service_status),
            ("API Endpoints", self.test_api_endpoints)
        ]
        
        all_tests_passed = True
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    self.print_test_step(f"{test_name}: PASSED", "SUCCESS")
                else:
                    self.print_test_step(f"{test_name}: FAILED", "ERROR")
                    all_tests_passed = False
            except Exception as e:
                self.print_test_step(f"{test_name}: ERROR - {e}", "ERROR")
                all_tests_passed = False
        
        # Print summary
        self.print_test_header("Test Summary")
        if all_tests_passed:
            self.print_test_step("ALL TESTS PASSED - Deployment is ready!", "SUCCESS")
        else:
            self.print_test_step("SOME TESTS FAILED - Check errors above", "ERROR")
        
        # Save test results
        with open("/tmp/monay_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        return all_tests_passed

if __name__ == "__main__":
    tester = DeploymentTester()
    success = tester.run_full_test_suite()
    sys.exit(0 if success else 1)