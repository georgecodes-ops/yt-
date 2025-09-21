#!/bin/bash

# 🔧 Post-Deployment Environment Update Script
# Run this script AFTER setup_system_deployment.py completes
# Updates the .env file with production-optimized settings

set -e  # Exit on any error

echo "🔧 Post-Deployment Environment Configuration"
echo "============================================="
echo ""

# Check if we're running as the correct user
if [ "$EUID" -eq 0 ]; then
    echo "❌ ERROR: Do not run this script as root!"
    echo "   Run as the same user that ran setup_system_deployment.py"
    exit 1
fi

# Detect platform and set base path
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    BASE_PATH="C:/opt/monay"
    IS_WINDOWS=true
else
    BASE_PATH="/opt/monay"
    IS_WINDOWS=false
fi

# Check if deployment was completed
if [ ! -d "$BASE_PATH" ]; then
    echo "❌ ERROR: MonAY deployment directory not found at $BASE_PATH"
    echo "   Please run setup_system_deployment.py first"
    exit 1
fi

# Check if the main .env file exists
if [ ! -f "$BASE_PATH/.env" ]; then
    echo "❌ ERROR: Main .env file not found at $BASE_PATH/.env"
    echo "   Deployment may not have completed successfully"
    exit 1
fi

echo "✅ Deployment directory found"
echo "✅ Main .env file found"
echo ""

# Run the Python environment updater
echo "🔄 Running environment configuration update..."
echo ""

if [ -f "update_production_env.py" ]; then
    if [ "$IS_WINDOWS" = true ]; then
        python update_production_env.py
    else
        python3 update_production_env.py
    fi
    UPDATE_STATUS=$?
else
    echo "❌ ERROR: update_production_env.py not found in current directory"
    echo "   Please ensure you're running this script from the project root"
    exit 1
fi

if [ $UPDATE_STATUS -eq 0 ]; then
    echo ""
    echo "✅ Environment configuration updated successfully!"
    echo ""
    
    if [ "$IS_WINDOWS" = true ]; then
        # Windows: Check for startup script
        if [ -f "$BASE_PATH/start_monay.bat" ]; then
            echo "ℹ️  MonAY startup script ready"
            echo "📋 To start MonAY:"
            echo "   • Run: $BASE_PATH/start_monay.bat"
            echo "   • Or double-click the batch file"
            echo "   • Test health: curl http://localhost:8000/health"
        else
            echo "⚠️  WARNING: MonAY startup script not found"
            echo "   Expected at: $BASE_PATH/start_monay.bat"
        fi
    else
        # Linux: Check if systemd service exists
        if systemctl list-unit-files | grep -q "monay.service"; then
            echo "🔄 Restarting MonAY service..."
            if sudo systemctl restart monay; then
                echo "✅ Service restarted successfully"
                
                # Wait a moment for service to start
                sleep 3
                
                echo "📊 Service status:"
                sudo systemctl status monay --no-pager -l
                
                echo ""
                echo "📋 Useful commands:"
                echo "   • Check logs: journalctl -u monay -f"
                echo "   • Test health: curl http://localhost:8000/health"
                echo "   • Stop service: sudo systemctl stop monay"
                echo "   • Start service: sudo systemctl start monay"
            else
                echo "⚠️  WARNING: Failed to restart service automatically"
                echo "   Please restart manually: sudo systemctl restart monay"
            fi
        else
            echo "ℹ️  MonAY service not found in systemd"
            echo "   You may need to enable it manually or run the application directly"
        fi
    fi
    
    echo ""
    echo "🎉 Post-deployment configuration complete!"
    echo ""
    echo "📁 Key files updated:"
    echo "   • $BASE_PATH/.env (production settings)"
    echo "   • $BASE_PATH/.env.backup (original backup)"
    echo ""
    echo "🔧 Production optimizations applied:"
    echo "   • CPU-only mode enabled for WAN and Stable Diffusion"
    echo "   • Resource limits set (4GB RAM, 50% CPU)"
    echo "   • Extended timeouts for CPU processing"
    echo "   • Production paths configured"
    echo "   • Rate limiting optimized for server deployment"
    
else
    echo ""
    echo "❌ Environment configuration update failed!"
    echo "   Please check the error messages above and try again"
    exit 1
fi