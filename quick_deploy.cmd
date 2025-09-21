@echo off
echo 🚀 Quick deployment to server...

set SERVER=george@94.72.111.253
set LOCAL_DIR=C:\Users\gcall\OneDrive\Documents\monay_restored

echo 📦 Deploying all updated files...
scp "%LOCAL_DIR%\setup_system_deployment.py" "%LOCAL_DIR%\src\get_youtube_tokens.py" "%LOCAL_DIR%\src\enhanced_main.py" "%LOCAL_DIR%\src\distribution\__init__.py" "%LOCAL_DIR%\youtube_tokens.json" "%LOCAL_DIR%\test_distribution_import.py" "%SERVER%:/opt/monay/"

echo ✅ Deployment complete!
echo 🔄 Connect to server: ssh george@94.72.111.253
echo 🔄 Run: cd /opt/monay && python3 setup_system_deployment.py