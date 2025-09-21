@echo off
REM 🔧 Post-Deployment Environment Update Script (Windows)
REM This is for local testing - the actual deployment uses the .sh version
REM Updates the .env file with production-optimized settings

setlocal enabledelayedexpansion

echo 🔧 Post-Deployment Environment Configuration (Windows Test)
echo ================================================================
echo.

REM Check if we're in the right directory
if not exist "update_production_env.py" (
    echo ❌ ERROR: update_production_env.py not found in current directory
    echo    Please ensure you're running this script from the project root
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found in current directory
    echo    This script updates the local .env for testing purposes
    pause
    exit /b 1
)

echo ✅ Found update_production_env.py
echo ✅ Found .env file
echo.

REM Create a local version of the updater for Windows testing
echo 🔄 Creating local environment updater for Windows testing...
echo.

(
echo #!/usr/bin/env python3
echo """
echo 🔧 Local Environment Configuration ^(Windows Test^\)
echo Updates .env file for local testing of production settings
echo """
echo.
echo import os
echo import shutil
echo from pathlib import Path
echo import getpass
echo.
echo class LocalEnvUpdater:
echo     def __init__^(self^\):
echo         self.current_user = getpass.getuser^(^\)
echo         self.local_env_path = Path^".env"^
echo         self.backup_env_path = Path^".env.backup"^
echo         
echo     def print_step^(self, message: str, status: str = "INFO"^\):
echo         """Print formatted step message"""
echo         status_colors = {
echo             "INFO": "\033[94m",
echo             "SUCCESS": "\033[92m", 
echo             "WARNING": "\033[93m",
echo             "ERROR": "\033[91m"
echo         }
echo         reset_color = "\033[0m"
echo         color = status_colors.get^(status, "\033[94m"^\)
echo         print^(f"{color}[{status}]{reset_color} {message}"^\)
echo     
echo     def backup_current_env^(self^\) -^> bool:
echo         """Backup current .env file"""
echo         try:
echo             if self.local_env_path.exists^(^\):
echo                 shutil.copy2^(self.local_env_path, self.backup_env_path^\)
echo                 self.print_step^(f"Backed up current .env to {self.backup_env_path}", "SUCCESS"^\)
echo                 return True
echo             else:
echo                 self.print_step^("No existing .env file found to backup", "WARNING"^\)
echo                 return True
echo         except Exception as e:
echo             self.print_step^(f"Failed to backup .env file: {e}", "ERROR"^\)
echo             return False
echo     
echo     def update_local_env^(self^\) -^> bool:
echo         """Update .env file for local testing"""
echo         local_env_content = f"""# LOCAL TESTING CONFIGURATION ^(Windows^\)
echo # This simulates production settings for local development
echo.
echo # ESSENTIAL YOUTUBE CONFIGURATION
echo YOUTUBE_API_KEY=AIzaSyC0ZFRYFm_XfHfMkhvyT5UpGzUDzU8JrQI
echo YOUTUBE_CLIENT_ID=919510636273-6irenq7b2tncl8r8r5pqajh9t8fp1n73.apps.googleusercontent.com
echo YOUTUBE_CLIENT_SECRET=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
echo YOUTUBE_CREDENTIALS_FILE=youtube_tokens.json
echo.
echo # ESSENTIAL TELEGRAM CONFIGURATION
echo TELEGRAM_BOT_TOKEN=7998208155:AAEV6jueiq0L0OXqh5aV84BjJLCdIvIrEAk
echo TELEGRAM_CHAT_ID=7178329784
echo.
echo # SYSTEM CONFIGURATION ^(Local Paths^\)
echo DATABASE_URL=sqlite:///monay.db
echo VIDEO_RETENTION_DAYS=7
echo LOG_DIRECTORY=./logs
echo DATA_DIRECTORY=./data
echo TEMP_DIRECTORY=./temp
echo.
echo # CONTENT SETTINGS ^(CPU-Optimized^\)
echo MAX_VIDEOS_PER_CYCLE=1
echo CONTENT_GENERATION_BATCH_SIZE=1
echo SHORTS_ONLY_MODE=false
echo LONG_FORM_ENABLED=true
echo SHORTS_TO_LONGFORM_RATIO=3:1
echo.
echo # AUTOMATION SETTINGS ^(CPU Server Optimized^\)
echo AUTOMATION_CYCLE_HOURS=8
echo MIN_WAIT_BETWEEN_CYCLES_HOURS=4
echo CPU_LIMIT_PERCENT=50
echo STARTUP_DELAY_SECONDS=10
echo GENERATION_TIMEOUT_SECONDS=3600
echo.
echo # LOGGING ^& MONITORING
echo TELEGRAM_NOTIFICATIONS_ENABLED=true
echo TELEGRAM_CRITICAL_ONLY=true
echo LOG_LEVEL=INFO
echo LOG_ROTATION_DAYS=30
echo.
echo # Quality Gates ^(CPU-Adjusted^\)
echo QUALITY_THRESHOLD=0.7
echo ALGORITHM_COMPATIBILITY=0.7
echo MAX_DAILY_VIDEOS=3
echo.
echo # YouTube API Settings ^(Rate Limited^\)
echo YOUTUBE_API_ENABLED=true
echo RATE_LIMIT_DELAY=120
echo MAX_CONCURRENT_UPLOADS=1
echo UPLOAD_RETRY_ATTEMPTS=3
echo UPLOAD_TIMEOUT_SECONDS=1800
echo.
echo # WAN ^(Video Generation^\) Configuration ^(Local^\)
echo WAN_TOKEN=local
echo WAN_API_URL=http://localhost:8000
echo WAN_LOCAL_MODE=true
echo WAN_VENV_PATH=./wan_venv
echo WAN_CPU_MODE=true
echo WAN_RESOLUTION=512x512
echo WAN_INFERENCE_STEPS=15
echo WAN_BATCH_SIZE=1
echo.
echo # Stable Diffusion Configuration ^(CPU-Only^\)
echo SD_CPU_MODE=true
echo SD_RESOLUTION=512x512
echo SD_INFERENCE_STEPS=20
echo SD_GUIDANCE_SCALE=7.0
echo SD_MODEL_PATH=./models/stable-diffusion
echo SD_VAE_PATH=./models/vae
echo SD_CACHE_DIR=./cache/sd
echo.
echo # Resource Management ^(Local Limits^\)
echo CPU_LIMIT=50%%
echo MEMORY_LIMIT=4GB
echo MAX_WORKERS=2
echo THREAD_POOL_SIZE=4
echo PROCESS_TIMEOUT=7200
echo.
echo # Service Configuration ^(Local^\)
echo SERVICE_USER={self.current_user}
echo SERVICE_GROUP={self.current_user}
echo SERVICE_HOME=.
echo PYTHON_PATH=./venv/Scripts/python.exe
echo WAN_PYTHON_PATH=./wan_venv/Scripts/python.exe
echo AI_PYTHON_PATH=./ai_service/venv/Scripts/python.exe
echo.
echo # Security Settings
echo ALLOWED_HOSTS=localhost,127.0.0.1
echo DEBUG=true
echo SECRET_KEY=local_development_key
echo SSL_VERIFY=true
echo.
echo # Monitoring ^& Health Checks
echo HEALTH_CHECK_INTERVAL=300
echo METRICS_ENABLED=true
echo PERFORMANCE_MONITORING=true
echo ERROR_REPORTING=true
echo """
echo         
echo         try:
echo             with open^(self.local_env_path, 'w'^\) as f:
echo                 f.write^(local_env_content^\)
echo             
echo             self.print_step^(f"Updated local .env file at {self.local_env_path}", "SUCCESS"^\)
echo             return True
echo             
echo         except Exception as e:
echo             self.print_step^(f"Failed to update .env file: {e}", "ERROR"^\)
echo             return False
echo     
echo     def run_update^(self^\) -^> bool:
echo         """Run the complete environment update process"""
echo         print^("\n🔧 Updating Local Environment Configuration ^(Windows Test^\)"^\)
echo         print^("=" * 60^\)
echo         
echo         steps = [
echo             ^("Backing up current .env file", self.backup_current_env^\),
echo             ^("Updating local .env file", self.update_local_env^\)
echo         ]
echo         
echo         for step_name, step_func in steps:
echo             self.print_step^(f"Starting: {step_name}"^\)
echo             if not step_func^(^\):
echo                 self.print_step^(f"Failed: {step_name}", "ERROR"^\)
echo                 return False
echo             self.print_step^(f"Completed: {step_name}", "SUCCESS"^\)
echo         
echo         print^("\n✅ Local environment configuration updated successfully!"^\)
echo         print^("\n📋 This is a LOCAL TEST configuration:"^\)
echo         print^("   • Uses local paths ^(./venv, ./data, etc.^\)"^\)
echo         print^("   • Enables CPU-only mode for testing"^\)
echo         print^("   • Sets development-friendly timeouts"^\)
echo         print^("   • For actual deployment, use the Linux version"^\)
echo         
echo         return True
echo.
echo if __name__ == "__main__":
echo     updater = LocalEnvUpdater^(^\)
echo     success = updater.run_update^(^\)
echo     exit^(0 if success else 1^\)
) > update_local_env.py

REM Run the local environment updater
echo 🔄 Running local environment configuration update...
echo.

python update_local_env.py
set UPDATE_STATUS=%ERRORLEVEL%

if %UPDATE_STATUS% equ 0 (
    echo.
    echo ✅ Local environment configuration updated successfully!
    echo.
    echo 📁 Files updated:
    echo    • .env ^(local test settings^)
    echo    • .env.backup ^(original backup^)
    echo.
    echo 🔧 Local test optimizations applied:
    echo    • CPU-only mode enabled for WAN and Stable Diffusion
    echo    • Resource limits set for local testing
    echo    • Local paths configured ^(./venv, ./data, etc.^)
    echo    • Development-friendly settings
    echo.
    echo 📋 Next steps for local testing:
    echo    1. Test the application locally
    echo    2. Verify CPU-only mode works
    echo    3. Deploy to Ubuntu server using setup_system_deployment.py
    echo    4. Run update_env_after_deployment.sh on the server
    echo.
) else (
    echo.
    echo ❌ Local environment configuration update failed!
    echo    Please check the error messages above and try again
    pause
    exit /b 1
)

REM Clean up temporary file
if exist "update_local_env.py" del "update_local_env.py"

echo 🎉 Local environment update complete!
pause