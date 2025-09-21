#!/bin/bash

# MonAY Updated Files Deployment Script
# This script transfers the files we just updated to the server

SERVER="george@94.72.111.253"
LOCAL_DIR="/c/Users/gcall/OneDrive/Documents/monay_restored"
REMOTE_DIR="/opt/monay"

# Files we updated
echo "🚀 Deploying updated files to server..."

# Core deployment files
echo "📦 Transferring setup_system_deployment.py..."
scp "$LOCAL_DIR/setup_system_deployment.py" "$SERVER:$REMOTE_DIR/"

# YouTube token handling files
echo "📦 Transferring get_youtube_tokens.py..."
scp "$LOCAL_DIR/src/get_youtube_tokens.py" "$SERVER:$REMOTE_DIR/src/"
scp "$LOCAL_DIR/src/enhanced_main.py" "$SERVER:$REMOTE_DIR/src/"

# Distribution package files
echo "📦 Transferring distribution package..."
scp "$LOCAL_DIR/src/distribution/__init__.py" "$SERVER:$REMOTE_DIR/src/distribution/"

# YouTube credentials
echo "📦 Transferring youtube_tokens.json..."
scp "$LOCAL_DIR/youtube_tokens.json" "$SERVER:$REMOTE_DIR/"

# Test script
echo "📦 Transferring test script..."
scp "$LOCAL_DIR/test_distribution_import.py" "$SERVER:$REMOTE_DIR/"

echo "✅ All updated files deployed successfully!"
echo ""
echo "🔄 Next steps:"
echo "1. SSH to server: ssh george@94.72.111.253"
echo "2. Navigate to directory: cd /opt/monay"
echo "3. Run deployment: python3 setup_system_deployment.py"
echo "4. Test distribution: python3 test_distribution_import.py"