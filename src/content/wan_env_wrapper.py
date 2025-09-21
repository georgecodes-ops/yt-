#!/usr/bin/env python3
"""
WAN Environment Wrapper
Provides interface to WAN functionality running in separate environment
"""

import subprocess
import json
import os
import logging
from typing import Dict, Any

class WANEnvironmentWrapper:
    """Wrapper for WAN functionality in separate environment"""
    
    def __init__(self):
        # Get the absolute path to the project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        # Check for system-level deployment first (platform-aware)
        import platform
        is_windows = platform.system() == 'Windows'
        if is_windows:
            system_wan_path = 'C:/opt/monay/wan_venv/Scripts/python.exe'
        else:
            system_wan_path = '/opt/monay/wan_venv/bin/python'
        local_wan_path = os.path.join(project_root, 'wan_venv', 'Scripts', 'python.exe')  # Windows
        local_wan_path_unix = os.path.join(project_root, 'wan_venv', 'bin', 'python')  # Unix
        
        # Priority: system > local Windows > local Unix
        if os.path.exists(system_wan_path):
            self.python_path = system_wan_path
            print(f"✅ Using system WAN environment: {self.python_path}")
        elif os.path.exists(local_wan_path):
            self.python_path = local_wan_path
            print(f"✅ Using local WAN environment (Windows): {self.python_path}")
        elif os.path.exists(local_wan_path_unix):
            self.python_path = local_wan_path_unix
            print(f"✅ Using local WAN environment (Unix): {self.python_path}")
        else:
            # Fallback to main environment
            main_python = os.path.join(project_root, 'venv', 'Scripts', 'python.exe')
            if os.path.exists(main_python):
                self.python_path = main_python
                print(f"⚠️ Using main environment as fallback: {self.python_path}")
            else:
                raise FileNotFoundError(f"No suitable Python environment found. Checked: {[system_wan_path, local_wan_path, local_wan_path_unix, main_python]}")
        
        print(f"Debug - Project root: {project_root}")
        print(f"Debug - Selected Python path: {self.python_path}")
        print("✅ WAN environment wrapper initialized successfully")
    
    def run_wan_command(self, wan_script: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run a WAN command in the separate environment"""
        try:
            # Prepare command
            cmd = [self.python_path, '-c', wan_script]
            if data:
                cmd.append(json.dumps(data))
            
            print(f"🚀 Running WAN command...")
            
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=300  # 5 minute timeout
            )
            
            # Parse result
            if result.stdout.strip():
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    return {"output": result.stdout}
            else:
                return {"status": "success", "output": "No output"}
                
        except subprocess.TimeoutExpired:
            raise Exception("WAN command timed out")
        except subprocess.CalledProcessError as e:
            raise Exception(f"WAN command failed: {e.stderr}")
        except Exception as e:
            raise Exception(f"WAN command error: {str(e)}")

# Test when run directly
if __name__ == "__main__":
    try:
        wrapper = WANEnvironmentWrapper()
        print("✅ WAN environment wrapper ready")
    except Exception as e:
        print(f"❌ WAN environment wrapper failed: {e}")
        import traceback
        traceback.print_exc()