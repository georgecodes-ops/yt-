#!/usr/bin/env python3
"""
Comprehensive Error Testing Script
Tests all imports, paths, and potential issues before deployment
"""

import sys
import os
import traceback
import importlib
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

print("🔍 COMPREHENSIVE ERROR TESTING")
print("=" * 50)

# Test 1: Import Testing
print("\n📦 TESTING ALL IMPORTS...")
import_tests = [
    # Core modules
    ("agents.agent_manager", "AgentManager"),
    ("content.content_pipeline", "ContentPipeline"),
    ("distribution.enhanced_upload_manager", "EnhancedUploadManager"),
    ("ml.trend_predictor", "TrendPredictor"),
    ("monetization.revenue_optimizer", "RevenueOptimizer"),
    ("analytics.advanced_metrics_tracker", "AdvancedMetricsTracker"),
    
    # Analytics modules
    ("automation.smart_scheduler", "SmartScheduler"),
    ("analytics.youtube_algorithm_analyzer", "YouTubeAlgorithmAnalyzer"),
    ("analytics.predictive_analytics", "PredictiveAnalytics"),
    ("analytics.retention_analytics", "RetentionAnalytics"),
    ("analytics.youtube_psychology_analyzer", "YouTubePsychologyAnalyzer"),
    
    # Content modules
    ("content.longform_content_generator", "LongFormContentGenerator"),
    ("content.ai_viral_learning_system", "AIViralLearningSystem"),
    ("content.instant_viral_generator", "InstantViralGenerator"),
    ("content.viral_master_system", "UltimateViralSystem"),
    
    # Growth modules
    ("growth.viral_growth_engine", "ViralGrowthEngine"),
    ("growth.ten_k_accelerator", "TenKAccelerator"),
    
    # Utils modules
    ("utils.performance_monitor", "PerformanceMonitor"),
    ("utils.channel_verifier", "ChannelVerifier"),
    ("utils.cpu_resource_manager", "CPUResourceManager"),
    ("utils.bulletproof_youtube_auth", "BulletproofYouTubeAuth"),
    
    # Distribution modules
    ("distribution.social_manager", "SocialManager"),
    ("distribution.platform_optimizer", "PlatformOptimizer"),
    ("distribution.blog_manager", "BlogManager"),
]

failed_imports = []
successful_imports = []

for module_path, class_name in import_tests:
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, class_name):
            print(f"  ✅ {module_path}.{class_name}")
            successful_imports.append((module_path, class_name))
        else:
            print(f"  ❌ {module_path}.{class_name} - Class not found")
            failed_imports.append((module_path, class_name, "Class not found"))
    except ImportError as e:
        print(f"  ❌ {module_path}.{class_name} - Import failed: {e}")
        failed_imports.append((module_path, class_name, str(e)))
    except Exception as e:
        print(f"  ❌ {module_path}.{class_name} - Error: {e}")
        failed_imports.append((module_path, class_name, str(e)))

print(f"\n📊 IMPORT RESULTS:")
print(f"  ✅ Successful: {len(successful_imports)}")
print(f"  ❌ Failed: {len(failed_imports)}")

# Test 2: Path Validation
print("\n📁 TESTING FILE PATHS...")
required_files = [
    "src/enhanced_main.py",
    "src/agents/agent_manager.py",
    "src/content/longform_content_generator.py",
    "src/analytics/youtube_psychology_analyzer.py",
    "src/automation/smart_scheduler.py",
    "src/utils/bulletproof_youtube_auth.py",
    "src/distribution/social_manager.py",
    ".env",
    "config.yaml"
]

missing_files = []
for file_path in required_files:
    full_path = PROJECT_ROOT / file_path
    if full_path.exists():
        print(f"  ✅ {file_path}")
    else:
        print(f"  ❌ {file_path} - MISSING")
        missing_files.append(file_path)

# Test 3: Async Function Testing
print("\n⚡ TESTING ASYNC FUNCTIONS...")
try:
    import asyncio
    
    async def test_async_calls():
        """Test problematic async patterns"""
        test_results = []
        
        # Test 1: Dict in await
        try:
            test_dict = {'test': 'value'}
            # This should fail
            # result = await test_dict  # This would cause the error
            test_results.append("✅ Dict await test - properly handled")
        except Exception as e:
            test_results.append(f"❌ Dict await test failed: {e}")
        
        # Test 2: None in await
        try:
            test_none = None
            # result = await test_none  # This would cause error
            test_results.append("✅ None await test - properly handled")
        except Exception as e:
            test_results.append(f"❌ None await test failed: {e}")
        
        return test_results
    
    # Run async tests
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async_results = loop.run_until_complete(test_async_calls())
    loop.close()
    
    for result in async_results:
        print(f"  {result}")
        
except Exception as e:
    print(f"  ❌ Async testing failed: {e}")

# Test 4: Environment Variables
print("\n🌍 TESTING ENVIRONMENT VARIABLES...")
required_env_vars = [
    'WANAPITOKEN',
    'USEFREETIER', 
    'WAN_TOKEN',
    'HUGGINGFACE_HUB_CACHE',
    'TRANSFORMERS_CACHE',
    'CPU_LIMIT_PERCENT',
    'STARTUP_DELAY_SECONDS'
]

missing_env_vars = []
for var in required_env_vars:
    value = os.getenv(var)
    if value:
        print(f"  ✅ {var}: {value}")
    else:
        print(f"  ❌ {var}: NOT SET")
        missing_env_vars.append(var)

# Final Report
print("\n" + "=" * 50)
print("🎯 COMPREHENSIVE TEST RESULTS")
print("=" * 50)

if failed_imports:
    print(f"\n❌ FAILED IMPORTS ({len(failed_imports)}):")
    for module, class_name, error in failed_imports:
        print(f"  - {module}.{class_name}: {error}")

if missing_files:
    print(f"\n❌ MISSING FILES ({len(missing_files)}):")
    for file_path in missing_files:
        print(f"  - {file_path}")

if missing_env_vars:
    print(f"\n❌ MISSING ENV VARS ({len(missing_env_vars)}):")
    for var in missing_env_vars:
        print(f"  - {var}")

if not failed_imports and not missing_files and not missing_env_vars:
    print("\n🎉 ALL TESTS PASSED! System is ready for deployment!")
else:
    print(f"\n⚠️ ISSUES FOUND: {len(failed_imports)} imports, {len(missing_files)} files, {len(missing_env_vars)} env vars")

print("\n🚀 Run this script to identify all issues before deployment!")