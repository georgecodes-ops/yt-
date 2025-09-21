#!/bin/bash
# 🚀 COMPLETE STARTUP SCRIPT FOR UBUNTU/LINUX
# Tests everything and starts the system with YouTube token handling

echo "🚀 COMPLETE STARTUP & TESTING SCRIPT"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_setup() {
    echo -e "${PURPLE}🔧 $1${NC}"
}

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    exit 1
fi

# Make the startup script executable
chmod +x complete_startup.py

# Run the complete startup process
print_info "Running complete startup and testing..."
python3 complete_startup.py

# Check if startup was successful
if [ $? -eq 0 ]; then
    print_status "Startup process completed successfully!"
    
    echo ""
    echo "📊 MONITORING OPTIONS:"
    echo "======================"
    echo "1. View real-time logs: tail -f system.log"
    echo "2. View enhanced logs: tail -f logs/enhanced_main.log"
    echo "3. Check system status: python3 complete_startup.py"
    echo ""
    echo "🎯 QUICK COMMANDS:"
    echo "=================="
    echo "• Start system: python3 complete_startup.py --quick"
    echo "• Test only: python3 complete_startup.py"
    echo "• Stop system: pkill -f enhanced_main.py"
    echo ""
    
    # Offer to start immediately
    read -p "🚀 Start the system now? (y/n): " start_choice
    if [[ $start_choice == [Yy]* ]]; then
        python3 complete_startup.py --quick
    fi
else
    print_error "Startup process failed. Check the output above."
    echo ""
    echo "🔧 COMMON FIXES:"
    echo "================"
    echo "• Install requirements: pip3 install -r requirements.txt"
    echo "• Set up YouTube tokens: python3 get_youtube_tokens.py"
    echo "• Check Python version: python3 --version"
    echo "• Fix deployment: python3 setup_system_deployment.py"
fi