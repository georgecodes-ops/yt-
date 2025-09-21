#!/usr/bin/env python3
"""
🔧 Post-Deployment Environment Configuration
Updates .env file for production deployment after setup_system_deployment.py runs
"""

import os
import shutil
from pathlib import Path
import getpass

class ProductionEnvUpdater:
    def __init__(self):
        import platform
        self.current_user = getpass.getuser()
        
        # Use platform-appropriate paths
        if platform.system() == 'Windows':
            base_path = "C:/opt/monay"
        else:
            base_path = "/opt/monay"
            
        self.system_env_path = Path(f"{base_path}/.env")
        self.backup_env_path = Path(f"{base_path}/.env.backup")
        
    def print_step(self, message: str, status: str = "INFO"):
        """Print formatted step message"""
        status_colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m", 
            "WARNING": "\033[93m",
            "ERROR": "\033[91m"
        }
        reset_color = "\033[0m"
        color = status_colors.get(status, "\033[94m")
        print(f"{color}[{status}]{reset_color} {message}")
    
    def backup_current_env(self) -> bool:
        """Backup current .env file"""
        try:
            if self.system_env_path.exists():
                shutil.copy2(self.system_env_path, self.backup_env_path)
                self.print_step(f"Backed up current .env to {self.backup_env_path}", "SUCCESS")
                return True
            else:
                self.print_step("No existing .env file found to backup", "WARNING")
                return True
        except Exception as e:
            self.print_step(f"Failed to backup .env file: {e}", "ERROR")
            return False
    
    def update_production_env(self) -> bool:
        """Update .env file for production deployment"""
        import platform
        
        # Use platform-appropriate paths
        if platform.system() == 'Windows':
            base_path = "C:/opt/monay"
        else:
            base_path = "/opt/monay"
            
        production_env_content = f"""# ESSENTIAL YOUTUBE CONFIGURATION
YOUTUBE_API_KEY=AIzaSyC0ZFRYFm_XfHfMkhvyT5UpGzUDzU8JrQI
YOUTUBE_CLIENT_ID=919510636273-6irenq7b2tncl8r8r5pqajh9t8fp1n73.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=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
YOUTUBE_CREDENTIALS_FILE={base_path}/credentials/credentials.json
YOUTUBE_TOKEN_FILE={base_path}/credentials/token.json

# ESSENTIAL TELEGRAM CONFIGURATION
TELEGRAM_BOT_TOKEN=7998208155:AAEV6jueiq0L0OXqh5aV84BjJLCdIvIrEAk
TELEGRAM_CHAT_ID=7178329784

# SYSTEM CONFIGURATION (Production Paths)
DATABASE_URL=sqlite:///{base_path}/data/monay.db
VIDEO_RETENTION_DAYS=7
LOG_DIRECTORY={base_path}/logs
DATA_DIRECTORY={base_path}/data
TEMP_DIRECTORY={base_path}/temp

# CONTENT SETTINGS (CPU-Optimized)
MAX_VIDEOS_PER_CYCLE=1
CONTENT_GENERATION_BATCH_SIZE=1
SHORTS_ONLY_MODE=false
LONG_FORM_ENABLED=true
SHORTS_TO_LONGFORM_RATIO=3:1

# AUTOMATION SETTINGS (CPU Server Optimized)
AUTOMATION_CYCLE_HOURS=8
MIN_WAIT_BETWEEN_CYCLES_HOURS=4
CPU_LIMIT_PERCENT=50
STARTUP_DELAY_SECONDS=10
GENERATION_TIMEOUT_SECONDS=3600

# LOGGING & MONITORING
TELEGRAM_NOTIFICATIONS_ENABLED=true
TELEGRAM_CRITICAL_ONLY=true
LOG_LEVEL=INFO
LOG_ROTATION_DAYS=30

# Quality Gates (CPU-Adjusted)
QUALITY_THRESHOLD=0.7
ALGORITHM_COMPATIBILITY=0.7
MAX_DAILY_VIDEOS=3

# YouTube API Settings (Rate Limited)
YOUTUBE_API_ENABLED=true
RATE_LIMIT_DELAY=120
MAX_CONCURRENT_UPLOADS=1
UPLOAD_RETRY_ATTEMPTS=3
UPLOAD_TIMEOUT_SECONDS=1800

# WAN (Video Generation) Configuration (Production)
WAN_TOKEN=local
WAN_API_URL=http://localhost:8000
WAN_LOCAL_MODE=true
WAN_VENV_PATH={base_path}/wan_venv
WAN_CPU_MODE=true
WAN_RESOLUTION=512x512
WAN_INFERENCE_STEPS=15
WAN_BATCH_SIZE=1

# Stable Diffusion Configuration (CPU-Only)
SD_CPU_MODE=true
SD_RESOLUTION=512x512
SD_INFERENCE_STEPS=20
SD_GUIDANCE_SCALE=7.0
SD_MODEL_PATH={base_path}/models/stable-diffusion
SD_VAE_PATH={base_path}/models/vae
SD_CACHE_DIR={base_path}/cache/sd

# Resource Management (Production Limits)
CPU_LIMIT=50%
MEMORY_LIMIT=4GB
MAX_WORKERS=2
THREAD_POOL_SIZE=4
PROCESS_TIMEOUT=7200

# Service Configuration
SERVICE_USER={self.current_user}
SERVICE_GROUP={self.current_user}
SERVICE_HOME=/opt/monay
PYTHON_PATH=/opt/monay/main_venv/bin/python
WAN_PYTHON_PATH=/opt/monay/wan_venv/bin/python
AI_PYTHON_PATH=/opt/monay/ai_service_venv/bin/python

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=false
SECRET_KEY=production_secret_key_change_this
SSL_VERIFY=true

# Monitoring & Health Checks
HEALTH_CHECK_INTERVAL=300
METRICS_ENABLED=true
PERFORMANCE_MONITORING=true
ERROR_REPORTING=true
"""
        
        try:
            with open(self.system_env_path, 'w') as f:
                f.write(production_env_content)
            
            # Set proper permissions
            os.chmod(self.system_env_path, 0o600)
            
            self.print_step(f"Updated production .env file at {self.system_env_path}", "SUCCESS")
            return True
            
        except Exception as e:
            self.print_step(f"Failed to update .env file: {e}", "ERROR")
            return False
    
    def verify_env_update(self) -> bool:
        """Verify the .env file was updated correctly"""
        try:
            if not self.system_env_path.exists():
                self.print_step("Production .env file not found", "ERROR")
                return False
            
            with open(self.system_env_path, 'r') as f:
                content = f.read()
            
            # Check for key production settings
            required_settings = [
                "WAN_CPU_MODE=true",
                "SD_CPU_MODE=true", 
                "CPU_LIMIT=50%",
                "MEMORY_LIMIT=4GB",
                "DATABASE_URL=sqlite:////opt/monay/data/monay.db",
                f"SERVICE_USER={self.current_user}"
            ]
            
            missing_settings = []
            for setting in required_settings:
                if setting not in content:
                    missing_settings.append(setting)
            
            if missing_settings:
                self.print_step(f"Missing required settings: {', '.join(missing_settings)}", "ERROR")
                return False
            
            self.print_step("Production .env file verification passed", "SUCCESS")
            return True
            
        except Exception as e:
            self.print_step(f"Failed to verify .env file: {e}", "ERROR")
            return False
    
    def run_update(self) -> bool:
        """Run the complete environment update process"""
        print("\n🔧 Updating Production Environment Configuration")
        print("=" * 50)
        
        steps = [
            ("Backing up current .env file", self.backup_current_env),
            ("Updating production .env file", self.update_production_env),
            ("Verifying .env file update", self.verify_env_update)
        ]
        
        for step_name, step_func in steps:
            self.print_step(f"Starting: {step_name}")
            if not step_func():
                self.print_step(f"Failed: {step_name}", "ERROR")
                return False
            self.print_step(f"Completed: {step_name}", "SUCCESS")
        
        print("\n✅ Production environment configuration updated successfully!")
        print("\n📋 Next steps:")
        print("   1. Restart the MonAY service: sudo systemctl restart monay")
        print("   2. Check service status: sudo systemctl status monay")
        print("   3. Monitor logs: journalctl -u monay -f")
        print("   4. Test API endpoints: curl http://localhost:8000/health")
        
        return True

if __name__ == "__main__":
    updater = ProductionEnvUpdater()
    success = updater.run_update()
    exit(0 if success else 1)