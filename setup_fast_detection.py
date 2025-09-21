#!/usr/bin/env python3
"""
Quick setup script for Fast Error Detection System
Run this once to enable instant problem detection and auto-fixing
"""

import os
import sys
import logging
from datetime import datetime

def setup_fast_detection_system():
    """Setup the complete fast detection system"""
    
    print("🚀 Setting up Fast Error Detection System...")
    print("=" * 50)
    
    # 1. Setup enhanced logging
    print("📝 1. Setting up enhanced logging...")
    setup_enhanced_logging()
    
    # 2. Create monitoring directories
    print("📁 2. Creating monitoring directories...")
    create_monitoring_dirs()
    
    # 3. Setup auto-start integration
    print("🔧 3. Setting up auto-start integration...")
    integrate_with_main_system()
    
    # 4. Create quick start script
    print("⚡ 4. Creating quick start script...")
    create_quick_start_script()
    
    print("\n✅ FAST DETECTION SYSTEM READY!")
    print("🎯 To start monitoring: python start_monitoring.py")
    print("🔧 Auto-fixes enabled for common issues")
    print("📊 Real-time alerts will show in console")
    print("💾 All alerts saved to daily JSON files")

def setup_enhanced_logging():
    """Setup enhanced logging configuration"""
    
    # Create logging config
    logging_config = '''
import logging
import sys
from datetime import datetime

# Enhanced logging setup
def setup_fast_logging():
    """Setup fast debugging logging"""
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(name)20s | %(funcName)15s:%(lineno)3d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(simple_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Debug file handler (ALL logs)
    debug_handler = logging.FileHandler('fast_debug.log')
    debug_handler.setFormatter(detailed_formatter)
    debug_handler.setLevel(logging.DEBUG)
    
    # Error-only handler (quick error review)
    error_handler = logging.FileHandler('errors_only.log')
    error_handler.setFormatter(detailed_formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Add new handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(debug_handler)
    root_logger.addHandler(error_handler)
    
    print("✅ Enhanced logging configured")
    return root_logger

# Auto-setup when imported
setup_fast_logging()
'''
    
    with open('src/utils/fast_logging_config.py', 'w') as f:
        f.write(logging_config)
    
    print("  ✅ Enhanced logging config created")

def create_monitoring_dirs():
    """Create necessary directories for monitoring"""
    
    dirs = [
        'monitoring',
        'monitoring/alerts',
        'monitoring/reports',
        'monitoring/auto_fixes'
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"  📁 Created: {directory}")

def integrate_with_main_system():
    """Integrate monitoring with main system startup"""
    
    integration_code = '''
# Add this to your main startup file (enhanced_main.py)

# Import fast detection system
try:
    from src.utils.fast_error_detector import setup_instant_problem_detection
    from src.utils.smart_debug_assistant import enable_instant_debugging
    from src.utils.fast_logging_config import setup_fast_logging
    
    # Enable instant debugging
    print("🚨 Enabling fast error detection...")
    
    # Setup logging
    setup_fast_logging()
    
    # Setup error detection
    detector = setup_instant_problem_detection()
    debug_handler = enable_instant_debugging()
    
    print("✅ Fast detection system active!")
    
except Exception as e:
    print(f"⚠️ Fast detection setup failed: {e}")
    print("📝 System will continue with basic logging")
'''
    
    with open('monitoring/integration_code.py', 'w') as f:
        f.write(integration_code)
    
    print("  🔧 Integration code created in monitoring/integration_code.py")

def create_quick_start_script():
    """Create quick start script for monitoring"""
    
    start_script = '''#!/usr/bin/env python3
"""
Quick start script for Fast Error Detection System
"""

import asyncio
import os
import sys

# Add src to path
sys.path.append('src')

async def main():
    """Start the fast detection system"""
    
    print("🚨 Starting Fast Error Detection System...")
    print("=" * 50)
    
    try:
        # Import and setup
        from src.utils.fast_error_detector import setup_instant_problem_detection, AutoFixer
        from src.utils.smart_debug_assistant import enable_instant_debugging
        
        # Enable instant debugging
        debug_handler = enable_instant_debugging()
        
        # Setup error detection with auto-fixing
        detector = setup_instant_problem_detection()
        auto_fixer = AutoFixer()
        
        print("✅ All systems active!")
        print("🔍 Monitoring logs in real-time...")
        print("🤖 Auto-fixes enabled")
        print("📊 Press Ctrl+C to stop")
        print("-" * 50)
        
        # Keep running and show status
        while True:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            # Show error summary
            summary = detector.get_error_summary()
            if summary['errors_last_hour'] > 0:
                print(f"📊 Errors in last hour: {summary['errors_last_hour']}")
                print(f"🔥 Most common: {summary['most_common_errors'][:3]}")
    
    except KeyboardInterrupt:
        print("\\n🛑 Stopping monitoring system...")
        if 'detector' in locals():
            detector.stop_monitoring()
        print("✅ Monitoring stopped")
    
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("📝 Check that all files are in place")

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    with open('start_monitoring.py', 'w') as f:
        f.write(start_script)
    
    print("  ⚡ Quick start script created: start_monitoring.py")

def create_slack_setup():
    """Create Slack integration setup"""
    
    slack_setup = '''
# Slack Integration Setup
# 
# 1. Go to your Slack workspace
# 2. Create a new app: https://api.slack.com/apps
# 3. Enable Incoming Webhooks
# 4. Create webhook for your channel
# 5. Copy webhook URL
# 6. Set environment variable:
#    export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
# 
# Then restart the monitoring system to enable Slack alerts

# Test Slack integration:
import os
import requests

def test_slack_alert():
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL not set")
        return
    
    test_message = {
        "text": "🚨 MONAY System Test Alert",
        "attachments": [{
            "color": "good",
            "text": "Fast detection system is working! ✅"
        }]
    }
    
    try:
        response = requests.post(webhook_url, json=test_message)
        if response.status_code == 200:
            print("✅ Slack integration working!")
        else:
            print(f"❌ Slack test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Slack test error: {e}")

if __name__ == "__main__":
    test_slack_alert()
'''
    
    with open('monitoring/slack_setup.py', 'w') as f:
        f.write(slack_setup)
    
    print("  📱 Slack setup guide created: monitoring/slack_setup.py")

if __name__ == "__main__":
    setup_fast_detection_system()
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("1. Run: python start_monitoring.py")
    print("2. Optional: Setup Slack alerts (see monitoring/slack_setup.py)")
    print("3. Your system will now auto-detect and fix issues!")
    print("=" * 50)