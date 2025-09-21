#!/bin/bash

# MonAY Deployment Validation Script
# This script validates that the deployment was successful

set -e

echo "======================================"
echo "MonAY Deployment Validation"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message"
            ;;
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message"
            ;;
    esac
}

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
    print_status "WARNING" "Running as root. Some checks may not reflect normal user experience."
fi

# 1. Check system directory
print_status "INFO" "Checking system directory..."

# Detect platform and set base path
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    BASE_PATH="C:/opt/monay"
    IS_WINDOWS=true
else
    BASE_PATH="/opt/monay"
    IS_WINDOWS=false
fi

if [ -d "$BASE_PATH" ]; then
    print_status "SUCCESS" "MonAY system directory exists at $BASE_PATH"
else
    print_status "ERROR" "MonAY system directory not found at $BASE_PATH"
    exit 1
fi

# 2. Check virtual environments
print_status "INFO" "Checking virtual environments..."
venvs=("venv" "ai_service/venv" "video_service/venv" "wan/venv")
for venv in "${venvs[@]}"; do
    if [ "$IS_WINDOWS" = true ]; then
        python_path="$BASE_PATH/$venv/Scripts/python.exe"
    else
        python_path="$BASE_PATH/$venv/bin/python"
    fi
    
    if [ -f "$python_path" ]; then
        version=$("$python_path" --version 2>&1)
        print_status "SUCCESS" "$venv: $version"
    else
        print_status "ERROR" "$venv: Python interpreter not found at $python_path"
    fi
done

# 3. Check configuration files
print_status "INFO" "Checking configuration files..."
config_files=(".env" "config.yaml" "requirements.txt")
for file in "${config_files[@]}"; do
    if [ -f "$BASE_PATH/$file" ]; then
        print_status "SUCCESS" "Configuration file $file exists"
    else
        print_status "WARNING" "Configuration file $file not found"
    fi
done

# 4. Check service
print_status "INFO" "Checking service..."
if [ "$IS_WINDOWS" = true ]; then
    # Windows: Check for batch file
    if [ -f "$BASE_PATH/start_monay.bat" ]; then
        print_status "SUCCESS" "MonAY startup script exists"
        print_status "INFO" "To start MonAY on Windows, run: $BASE_PATH/start_monay.bat"
    else
        print_status "ERROR" "MonAY startup script not found"
    fi
else
    # Linux: Check systemd service
    if systemctl is-enabled monay.service >/dev/null 2>&1; then
        print_status "SUCCESS" "MonAY service is enabled"
    else
        print_status "ERROR" "MonAY service is not enabled"
    fi
    
    if systemctl is-active monay.service >/dev/null 2>&1; then
        print_status "SUCCESS" "MonAY service is active"
    else
        print_status "WARNING" "MonAY service is not active"
        print_status "INFO" "Service status:"
        systemctl status monay.service --no-pager || true
    fi
fi

# 5. Check critical dependencies
print_status "INFO" "Checking critical dependencies..."
critical_packages=("torch" "transformers" "diffusers" "requests" "numpy")
if [ "$IS_WINDOWS" = true ]; then
    python_cmd="$BASE_PATH/venv/Scripts/python.exe"
else
    python_cmd="$BASE_PATH/venv/bin/python"
fi

for package in "${critical_packages[@]}"; do
    if "$python_cmd" -c "import $package" 2>/dev/null; then
        print_status "SUCCESS" "Package $package is available"
    else
        print_status "ERROR" "Package $package is not available"
    fi
done

# 6. Test API endpoints (if service is running)
print_status "INFO" "Testing API endpoints..."
endpoints=("http://localhost:8000/health" "http://localhost:8001/health" "http://localhost:8002/health")
for endpoint in "${endpoints[@]}"; do
    if curl -s --connect-timeout 5 "$endpoint" >/dev/null 2>&1; then
        print_status "SUCCESS" "$endpoint is responding"
    else
        print_status "WARNING" "$endpoint is not responding (service may not be running)"
    fi
done

# 7. Check logs for errors
print_status "INFO" "Checking recent service logs..."
if [ "$IS_WINDOWS" = true ]; then
    # Windows: Check log files if they exist
    if [ -f "$BASE_PATH/logs/enhanced_system.log" ]; then
        if tail -100 "$BASE_PATH/logs/enhanced_system.log" | grep -i error >/dev/null; then
            print_status "WARNING" "Errors found in log files"
            print_status "INFO" "Recent error logs:"
            tail -100 "$BASE_PATH/logs/enhanced_system.log" | grep -i error | tail -5
        else
            print_status "SUCCESS" "No recent errors in log files"
        fi
    else
        print_status "INFO" "Log files not found (service may not have started yet)"
    fi
else
    # Linux: Check systemd logs
    if journalctl -u monay.service --since "1 hour ago" --no-pager -q 2>/dev/null | grep -i error >/dev/null; then
        print_status "WARNING" "Errors found in service logs (last hour)"
        print_status "INFO" "Recent error logs:"
        journalctl -u monay.service --since "1 hour ago" --no-pager | grep -i error | tail -5
    else
        print_status "SUCCESS" "No recent errors in service logs"
    fi
fi

# 8. Check disk space
print_status "INFO" "Checking disk space..."
if [ "$IS_WINDOWS" = true ]; then
    # Windows: Check disk space for C: drive
    if command -v powershell >/dev/null 2>&1; then
        disk_usage=$(powershell -Command "(Get-WmiObject -Class Win32_LogicalDisk -Filter \"DeviceID='C:'\" | Select-Object -ExpandProperty Size) - (Get-WmiObject -Class Win32_LogicalDisk -Filter \"DeviceID='C:'\" | Select-Object -ExpandProperty FreeSpace)" 2>/dev/null || echo "unknown")
        if [ "$disk_usage" != "unknown" ]; then
            print_status "SUCCESS" "Disk space check completed"
        else
            print_status "INFO" "Could not determine disk usage on Windows"
        fi
    else
        print_status "INFO" "PowerShell not available for disk space check"
    fi
else
    # Linux: Check disk space
    disk_usage=$(df "$BASE_PATH" | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$disk_usage" -lt 90 ]; then
        print_status "SUCCESS" "Disk usage is acceptable ($disk_usage%)"
    else
        print_status "WARNING" "Disk usage is high ($disk_usage%)"
    fi
fi

# Summary
echo ""
print_status "INFO" "Validation complete!"
if [ "$IS_WINDOWS" = true ]; then
    print_status "INFO" "For detailed testing, run: python $BASE_PATH/test_deployment.py"
    print_status "INFO" "To start MonAY: $BASE_PATH/start_monay.bat"
    print_status "INFO" "To view logs: check $BASE_PATH/logs/ directory"
else
    print_status "INFO" "For detailed testing, run: python3 $BASE_PATH/test_deployment.py"
    print_status "INFO" "To view service logs: journalctl -u monay.service -f"
    print_status "INFO" "To restart service: sudo systemctl restart monay.service"
fi

echo "======================================"
echo "Deployment validation finished"
echo "======================================"