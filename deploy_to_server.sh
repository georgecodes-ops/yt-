#!/bin/bash

# MonAY Deployment Transfer Script
# This script transfers all updated files to the server in one command

set -e

echo "======================================"
echo "MonAY Server Deployment Transfer"
echo "======================================"

SERVER="george@94.72.111.253"
REMOTE_PATH="/home/george/monay_deployment"

echo "Creating remote directory..."
ssh $SERVER "mkdir -p $REMOTE_PATH"

echo "Transferring ALL project files..."
echo "This will transfer the complete MonAY project structure"

echo "Transferring core deployment files..."
scp setup_system_deployment.py $SERVER:$REMOTE_PATH/
scp setup_complete_system.py $SERVER:$REMOTE_PATH/
scp SYSTEM_DEPLOYMENT_GUIDE.md $SERVER:$REMOTE_PATH/
scp test_deployment.py $SERVER:$REMOTE_PATH/
scp validate_deployment.sh $SERVER:$REMOTE_PATH/
scp validate_complete_setup.py $SERVER:$REMOTE_PATH/
scp final_validation.py $SERVER:$REMOTE_PATH/

echo "Transferring requirements files..."
scp requirements.txt $SERVER:$REMOTE_PATH/
scp ai_service/requirements_ai.txt $SERVER:$REMOTE_PATH/ai_service_requirements.txt

echo "Transferring configuration files..."
scp config.yaml $SERVER:$REMOTE_PATH/
scp monay.service $SERVER:$REMOTE_PATH/
scp .env $SERVER:$REMOTE_PATH/env_template
scp .env.debug $SERVER:$REMOTE_PATH/env_debug_template

echo "Transferring complete source code structure..."
scp -r src $SERVER:$REMOTE_PATH/
scp -r ai_service $SERVER:$REMOTE_PATH/
scp -r video_service $SERVER:$REMOTE_PATH/
scp -r shared $SERVER:$REMOTE_PATH/
scp -r data $SERVER:$REMOTE_PATH/
scp -r server_package $SERVER:$REMOTE_PATH/

echo "Transferring utility scripts..."
scp get_youtube_tokens.py $SERVER:$REMOTE_PATH/
scp refresh_youtube_tokens.py $SERVER:$REMOTE_PATH/
scp data_bridge.py $SERVER:$REMOTE_PATH/

echo "Transferring log files and validation reports..."
if [ -f "debug.log" ]; then
    scp debug.log $SERVER:$REMOTE_PATH/
fi
if [ -f "enhanced_system.log" ]; then
    scp enhanced_system.log $SERVER:$REMOTE_PATH/
fi
if [ -f "validation_report.json" ]; then
    scp validation_report.json $SERVER:$REMOTE_PATH/
fi

echo "Transferring IDE configuration..."
if [ -d ".vscode" ]; then
    scp -r .vscode $SERVER:$REMOTE_PATH/
fi

echo "Transferring credentials (if exists)..."
if [ -f "client_secret_919510636273.json" ]; then
    scp client_secret_919510636273.json $SERVER:$REMOTE_PATH/
fi
if [ -f "youtube_tokens.json" ]; then
    scp youtube_tokens.json $SERVER:$REMOTE_PATH/
fi

echo "Setting permissions on remote server..."
ssh $SERVER "chmod +x $REMOTE_PATH/setup_system_deployment.py"
ssh $SERVER "chmod +x $REMOTE_PATH/validate_deployment.sh"
ssh $SERVER "chmod +x $REMOTE_PATH/test_deployment.py"

echo "======================================"
echo "Transfer Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Connect to server: ssh george@94.72.111.253"
echo "2. cd $REMOTE_PATH"
echo "3. sudo python3 setup_system_deployment.py"
echo "4. ./validate_deployment.sh"
echo ""
echo "Files transferred to: $SERVER:$REMOTE_PATH"
echo ""
echo "Starting SSH connection to server..."
ssh george@94.72.111.253