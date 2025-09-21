@echo off
echo 🚀 Deploying updated files to server...

set SERVER=george@94.72.111.253
set LOCAL_DIR=C:\Users\gcall\OneDrive\Documents\monay_restored
set REMOTE_DIR=/opt/monay

echo 📦 Transferring setup_system_deployment.py...
scp "%LOCAL_DIR%\setup_system_deployment.py" "%SERVER%:%REMOTE_DIR%/"

echo 📦 Transferring YouTube token handling files...
scp "%LOCAL_DIR%\src\get_youtube_tokens.py" "%SERVER%:%REMOTE_DIR%/src/"
scp "%LOCAL_DIR%\src\enhanced_main.py" "%SERVER%:%REMOTE_DIR%/src/"

echo 📦 Transferring distribution package...
scp "%LOCAL_DIR%\src\distribution\__init__.py" "%SERVER%:%REMOTE_DIR%/src/distribution/"

echo 📦 Transferring YouTube credentials...
scp "%LOCAL_DIR%\youtube_tokens.json" "%SERVER%:%REMOTE_DIR/"

echo 📦 Transferring test script...
scp "%LOCAL_DIR%\test_distribution_import.py" "%SERVER%:%REMOTE_DIR/"

echo ✅ All updated files deployed successfully!
echo.
echo 🔄 Next steps:
echo 1. SSH to server: ssh george@94.72.111.253
echo 2. Navigate to directory: cd /opt/monay
echo 3. Run deployment: python3 setup_system_deployment.py
echo 4. Test distribution: python3 test_distribution_import.py

pause