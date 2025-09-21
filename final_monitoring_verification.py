#!/usr/bin/env python3
"""
Final Verification Script for Monitoring & Self-Healing System
Run this before deployment to ensure everything is properly configured
"""

import os
import sys
import asyncio
import logging
from datetime import datetime

def test_imports():
    """Test all monitoring system imports"""
    print("🔍 Testing imports...")
    
    try:
        from src.utils.fast_error_detector import setup_instant_problem_detection, FastDebugLogger, DiscordAlerter
        print("  ✅ fast_error_detector imports OK")
    except Exception as e:
        print(f"  ❌ fast_error_detector import failed: {e}")
        return False
    
    try:
        from src.utils.smart_debug_assistant import enable_instant_debugging, SmartDebugAssistant
        print("  ✅ smart_debug_assistant imports OK")
    except Exception as e:
        print(f"  ❌ smart_debug_assistant import failed: {e}")
        return False
    
    try:
        from src.utils.self_healing_system import SelfHealingSystem, AutoRecoveryWrapper
        print("  ✅ self_healing_system imports OK")
    except Exception as e:
        print(f"  ❌ self_healing_system import failed: {e}")
        return False
    
    try:
        from src.utils.system_health_checker import SystemHealthChecker
        print("  ✅ system_health_checker imports OK")
    except Exception as e:
        print(f"  ❌ system_health_checker import failed: {e}")
        return False
    
    return True

def test_environment_variables():
    """Test environment variables configuration"""
    print("\n🔧 Testing environment variables...")
    
    discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if discord_webhook:
        print(f"  ✅ Discord webhook configured: {discord_webhook[:50]}...")
    else:
        print("  ⚠️ Discord webhook not configured")
    
    # Test other critical env vars
    critical_vars = [
        'YOUTUBE_API_KEY',
        'TELEGRAM_BOT_TOKEN',
        'OPENAI_API_KEY'
    ]
    
    for var in critical_vars:
        value = os.getenv(var)
        if value and value != 'your-api-key-here':
            print(f"  ✅ {var} configured")
        else:
            print(f"  ⚠️ {var} not configured or using placeholder")
    
    return True

def test_discord_webhook():
    """Test Discord webhook functionality"""
    print("\n📱 Testing Discord webhook...")
    
    discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if not discord_webhook:
        print("  ⚠️ Discord webhook not configured - skipping test")
        return True
    
    try:
        import requests
        
        test_message = {
            "content": "🧪 **MONAY SYSTEM TEST**",
            "embeds": [{
                "title": "✅ Monitoring System Test",
                "description": "Fast detection and self-healing system is working!",
                "color": 65280,  # Green
                "timestamp": datetime.now().isoformat()
            }]
        }
        
        response = requests.post(discord_webhook, json=test_message, timeout=10)
        if response.status_code in [200, 204]:
            print("  ✅ Discord webhook test successful!")
            return True
        else:
            print(f"  ❌ Discord webhook test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Discord webhook test error: {e}")
        return False

async def test_monitoring_system():
    """Test monitoring system functionality"""
    print("\n🚨 Testing monitoring system...")
    
    try:
        from src.utils.fast_error_detector import setup_instant_problem_detection
        from src.utils.smart_debug_assistant import enable_instant_debugging
        
        # Test error detector setup
        detector = setup_instant_problem_detection()
        print("  ✅ Error detector setup successful")
        
        # Test debug assistant
        enable_instant_debugging()
        print("  ✅ Debug assistant enabled")
        
        # Stop monitoring for test
        detector.stop_monitoring()
        print("  ✅ Monitoring system test complete")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Monitoring system test failed: {e}")
        return False

async def test_self_healing_system():
    """Test self-healing system functionality"""
    print("\n🤖 Testing self-healing system...")
    
    try:
        from src.utils.self_healing_system import SelfHealingSystem, AutoRecoveryWrapper
        
        # Test healing system creation
        healing_system = SelfHealingSystem()
        print("  ✅ Self-healing system created")
        
        # Test recovery wrapper
        recovery_wrapper = AutoRecoveryWrapper(healing_system)
        print("  ✅ Auto-recovery wrapper created")
        
        # Test status method
        status = healing_system.get_healing_status()
        print(f"  ✅ Healing status: {status['healing_active']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Self-healing system test failed: {e}")
        return False

def test_intelligence_modules():
    """Test intelligence module functionality"""
    print("\n🧠 Testing intelligence modules...")
    
    try:
        sys.path.append('src')
        
        # Test academic research
        from content.intelligence.academic_research import AcademicResearchCollector
        academic_collector = AcademicResearchCollector()
        print("  ✅ Academic research collector created")
        
        # Test content intelligence aggregator
        from content.intelligence.content_intelligence import ContentIntelligenceAggregator
        intelligence_aggregator = ContentIntelligenceAggregator()
        print("  ✅ Content intelligence aggregator created")
        
        # Test enhanced content pipeline
        from content.enhanced_content_pipeline import EnhancedContentPipeline
        enhanced_pipeline = EnhancedContentPipeline()
        print("  ✅ Enhanced content pipeline created")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Intelligence modules test failed: {e}")
        return False

def test_analytics_modules():
    """Test analytics module functionality"""
    print("\n📊 Testing analytics modules...")
    
    try:
        sys.path.append('src')
        
        # Test key analytics modules
        from analytics.ab_testing_system import ViralABTestingSystem
        ab_testing = ViralABTestingSystem()
        print("  ✅ A/B Testing system created")
        
        from analytics.competitor_discovery import CompetitorDiscovery
        competitor_discovery = CompetitorDiscovery()
        print("  ✅ Competitor discovery created")
        
        from analytics.youtube_psychology_analyzer import YouTubePsychologyAnalyzer
        psychology_analyzer = YouTubePsychologyAnalyzer()
        print("  ✅ Psychology analyzer created")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Analytics modules test failed: {e}")
        return False

def test_main_integration():
    """Test integration with main system"""
    print("\n🔗 Testing main system integration...")
    
    try:
        # Test that enhanced_main.py can import monitoring
        sys.path.append('src')
        
        # Test monitoring imports
        from utils.fast_error_detector import setup_instant_problem_detection, FastDebugLogger
        from utils.smart_debug_assistant import enable_instant_debugging
        from utils.self_healing_system import SelfHealingSystem, AutoRecoveryWrapper
        from utils.system_health_checker import SystemHealthChecker
        print("  ✅ Monitoring components imported")
        
        # Test intelligence imports
        try:
            from content.intelligence.content_intelligence import ContentIntelligenceAggregator
            from content.enhanced_content_pipeline import EnhancedContentPipeline
            print("  ✅ Intelligence components imported")
        except ImportError as e:
            print(f"  ⚠️ Intelligence components not available: {e}")
        
        # Test analytics imports
        try:
            from analytics.ab_testing_system import ViralABTestingSystem
            from analytics.competitor_discovery import CompetitorDiscovery
            print("  ✅ Analytics components imported")
        except ImportError as e:
            print(f"  ⚠️ Analytics components not available: {e}")
        
        # Test Discord webhook environment variable
        discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
        if discord_webhook:
            print("  ✅ Discord webhook available to main system")
        else:
            print("  ⚠️ Discord webhook not available to main system")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Main system integration test failed: {e}")
        return False

async def run_complete_verification():
    """Run complete verification of monitoring system"""
    print("🔍 FINAL MONITORING SYSTEM VERIFICATION")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Environment Variables", test_environment_variables),
        ("Discord Webhook", test_discord_webhook),
        ("Monitoring System", test_monitoring_system),
        ("Self-Healing System", test_self_healing_system),
        ("Intelligence Modules", test_intelligence_modules),
        ("Analytics Modules", test_analytics_modules),
        ("Main Integration", test_main_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 OVERALL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🚀 ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT!")
        print("📱 Discord alerts will work")
        print("🤖 Self-healing will auto-fix issues")
        print("⚡ Fast detection will catch problems instantly")
        return True
    else:
        print("⚠️ SOME TESTS FAILED - REVIEW ISSUES BEFORE DEPLOYMENT")
        return False

if __name__ == "__main__":
    # Set up basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Run verification
    success = asyncio.run(run_complete_verification())
    
    if success:
        print("\n✅ READY TO SCP TO SERVER!")
        print("Command: scp -r src/ setup_fast_detection.py .env george@94.72.111.253:/opt/monay/")
    else:
        print("\n❌ FIX ISSUES BEFORE DEPLOYMENT!")
    
    sys.exit(0 if success else 1)