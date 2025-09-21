#!/usr/bin/env python3
"""
Enhanced MonAY - Fully Integrated YouTube Automation System
Includes ALL components: Smart Scheduling, Viral Optimization, Advanced Analytics, etc.
With Warm-up Sequence and Hardcoded Hugging Face Configuration
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

try:
    import wikipedia  # type: ignore
except ImportError:
    wikipedia = None
    print("⚠️ wikipedia module not found - some features may be limited")

try:
    import mediapipe as mp  # type: ignore
except ImportError:
    mp = None
    print("⚠️ mediapipe not found - video processing features may be limited")

# Explicitly load the project-root .env and override any existing vars
PROJECT_ROOT = Path(__file__).resolve().parents[1]
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path, override=True)



# YouTube Token Validation System
def validate_youtube_tokens():
    """Comprehensive YouTube token validation"""
    print("\n🔍 Validating YouTube API Configuration...")
    
    # Check for token file
    token_files = ['youtube_tokens.json', 'tokens.json', 'credentials.json']
    token_file_found = None
    
    for token_file in token_files:
        if os.path.exists(token_file):
            token_file_found = token_file
            print(f"✅ Token file found: {token_file}")
            break
    
    if not token_file_found:
        print("❌ No YouTube token file found!")
        print("📋 Expected files: youtube_tokens.json, tokens.json, or credentials.json")
        return False
    
    # Validate token file content
    try:
        with open(token_file_found, 'r') as f:
            token_data = json.load(f)
        
        required_fields = ['client_id', 'client_secret']
        optional_fields = ['refresh_token', 'access_token', 'token_uri']
        
        missing_fields = []
        for field in required_fields:
            if field not in token_data or not token_data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Missing required fields in {token_file_found}: {missing_fields}")
            return False
        
        print(f"✅ Token file validation passed: {token_file_found}")
        
        # Check environment variables
        env_vars = {
            'YOUTUBE_CLIENT_ID': os.getenv('YOUTUBE_CLIENT_ID'),
            'YOUTUBE_CLIENT_SECRET': os.getenv('YOUTUBE_CLIENT_SECRET')
        }
        
        for var_name, var_value in env_vars.items():
            if var_value:
                print(f"✅ Environment variable set: {var_name}")
            else:
                print(f"⚠️ Environment variable not set: {var_name}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {token_file_found}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading {token_file_found}: {e}")
        return False

def test_youtube_upload_readiness():
    """Test YouTube upload functionality early in startup"""
    print("\n🚀 Testing YouTube Upload Readiness...")
    print("=" * 50)
    
    try:
        # Test 1: Import YouTube service
        print("1. Testing YouTube service import...")
        try:
            from get_youtube_tokens import get_youtube_service, validate_youtube_tokens as validate_tokens
            print("   ✅ YouTube service imported successfully")
        except ImportError as e:
            print(f"   ❌ Import failed: {e}")
            print("   💡 Check get_youtube_tokens.py file")
            return False
        
        # Test 2: Validate tokens
        print("2. Validating YouTube tokens...")
        try:
            if validate_tokens():
                print("   ✅ YouTube tokens are valid")
            else:
                print("   ❌ YouTube tokens validation failed")
                print("   💡 Run: python get_youtube_tokens.py")
                return False
        except Exception as e:
            print(f"   ❌ Token validation error: {e}")
            return False
        
        # Test 3: Create YouTube service
        print("3. Creating YouTube service...")
        try:
            youtube = get_youtube_service()
            if youtube:
                print("   ✅ YouTube service created successfully")
            else:
                print("   ❌ Failed to create YouTube service")
                return False
        except Exception as e:
            print(f"   ❌ Service creation error: {e}")
            return False
        
        # Test 4: Test API connection
        print("4. Testing YouTube API connection...")
        try:
            response = youtube.channels().list(
                part='snippet',
                mine=True
            ).execute()
            
            if response.get('items'):
                channel_title = response['items'][0]['snippet']['title']
                print(f"   ✅ Connected to channel: {channel_title}")
            else:
                print("   ❌ No channel found")
                return False
        except Exception as e:
            print(f"   ❌ API connection error: {e}")
            if 'invalid_grant' in str(e):
                print("   💡 Tokens expired - run: python get_youtube_tokens.py")
            else:
                print("   💡 Check API quotas and permissions")
            return False
        
        # Test 5: Import upload manager
        print("5. Testing upload manager import...")
        try:
            from distribution.enhanced_upload_manager import EnhancedUploadManager
            print("   ✅ Upload manager imported successfully")
        except ImportError as e:
            print(f"   ❌ Upload manager import failed: {e}")
            return False
        
        # Test 6: Initialize upload manager
        print("6. Initializing upload manager...")
        try:
            config = {'youtube': {'enabled': True}}
            upload_manager = EnhancedUploadManager(config)
            print("   ✅ Upload manager initialized successfully")
        except Exception as e:
            print(f"   ❌ Upload manager initialization failed: {e}")
            return False
        
        print("\n🎉 YouTube Upload Readiness Test PASSED!")
        print("✅ All upload functionality is ready")
        return True
        
    except Exception as e:
        print(f"\n❌ YouTube Upload Readiness Test FAILED: {e}")
        return False

# Run YouTube token validation
youtube_tokens_valid = validate_youtube_tokens()
if not youtube_tokens_valid:
    print("\n⚠️ WARNING: YouTube tokens not properly configured!")
    print("🔧 System will continue but YouTube uploads may fail.")
    print("📖 Please run: python src/get_youtube_tokens.py")

# Run YouTube upload readiness test
youtube_upload_ready = test_youtube_upload_readiness()
if youtube_upload_ready:
    print("\n✅ YouTube upload functionality verified and ready!")
else:
    print("\n⚠️ WARNING: YouTube upload functionality not ready!")
    print("🔧 System will continue but uploads may fail.")
    print("📖 Fix issues above or run: python quick_youtube_test.py")

# Debug: ensure correct token
print("DEBUG WAN_TOKEN:", repr(os.getenv("WAN_TOKEN")))
print("DEBUG PROJECT_ROOT:", PROJECT_ROOT)

import sys
import time
import logging
import asyncio
import requests
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Dict
import signal

# WAN 2.2 Configuration
os.environ.setdefault("WAN_VERSION", "2.2")
os.environ.setdefault("WAN_DEVICE", "auto")
os.environ.setdefault("WAN_PRECISION", "fp16")
os.environ.setdefault('RETRY_DELAY', '2')

# Add src to path
sys.path.append(str(Path(__file__).parent))

# Core Components
from agents.agent_manager import AgentManager
from content.content_pipeline import ContentPipeline
from distribution.enhanced_upload_manager import EnhancedUploadManager as UploadManager
from ml.trend_predictor import TrendPredictor
from monetization.revenue_optimizer import RevenueOptimizer
from analytics.advanced_metrics_tracker import AdvancedMetricsTracker
from dashboard.streamlit_app import DashboardManager

# NEW: Advanced Components Integration
from automation.smart_scheduler import SmartScheduler
from automation.daily_optimizer import DailyOptimizer
from analytics.youtube_algorithm_analyzer import YouTubeAlgorithmAnalyzer
from analytics.predictive_analytics import PredictiveAnalytics
from analytics.retention_analytics import RetentionAnalytics
from growth.viral_growth_engine import ViralGrowthEngine
from growth.ten_k_accelerator import TenKAccelerator
from content.youtube_retention_system import YouTubeRetentionSystem
from content.algorithm_optimizer import AlgorithmOptimizer
from content.viral_optimization import ViralOptimizer
from content.quality_enhancer import VideoQualityEnhancer
from content.viral_master_system import UltimateViralSystem, ViralMonetizationIntegrator
from content.instant_viral_generator import InstantViralGenerator
from content.ai_viral_learning_system import AIViralLearningSystem
from content.ai_prompt_orchestrator import AIPromptOrchestrator
from content.brand_manager import BrandManager
from distribution.platform_optimizer import PlatformOptimizer
from distribution.social_manager import SocialManager
from monetization.smart_ad_optimizer import SmartAdOptimizer
from monetization.affiliate_manager import AffiliateManager
from monetization.email_automation import EmailAutomation
from utils.performance_monitor import PerformanceMonitor
from utils.auto_policy_checker import EnhancedPolicyWatcher
from utils.channel_verifier import ChannelVerifier
from utils.content_deduplication import ContentDeduplicationManager
from ml.enhanced_learning_system import EnhancedLearningSystem
from utils.cpu_resource_manager import CPUResourceManager

# MONEY-MAKING MODULES - Direct imports
from content.original_finance_generator import OriginalFinanceGenerator
from content.human_touch_enhancer import HumanTouchEnhancer
from content.ai_data_interpreter import AIDataInterpreter
from content.ai_refinement_system import AIRefinementSystem
from content.blog_generator import BlogGenerator
from content.dynamic_keyword_engine import DynamicKeywordEngine
from content.enhanced_finance_producer import EnhancedFinanceProducer
from content.finance_brand_manager import FinanceBrandManager
from content.ai_image_generator import AIImageGenerator



from content.kdp_generator import KDPGenerator
from content.originality_engine import OriginalityEngine
from content.text_branding import TextBranding
from content.unified_pixel_finance_brand import PixelFinanceBrand
from content.universal_content_engine import UniversalContentEngine

from content.pixel_finance_brand_manager import PixelFinanceBrandManager
from content.trending_tools import TrendingTools
from content.tts_generator import TTSGenerator
from content.video_processor import VideoProcessor

# DISTRIBUTION & MONETIZATION
from distribution.enhanced_upload_manager import EnhancedUploadManager
from distribution.blog_manager import BlogManager
from distribution.pod_manager import PODManager
from monetization.course_creator import CourseCreator
from monetization.lead_magnet_generator import LeadMagnetGenerator
from monetization.membership_manager import MembershipManager


# ANALYTICS & GROWTH
from analytics.ab_testing_system import ViralABTestingSystem
from analytics.ad_performance import AdPerformanceAnalytics
from analytics.competitor_discovery import CompetitorDiscovery
from analytics.competitor_insights import CompetitorInsights
from analytics.competitor_monitor import CompetitorMonitor
from analytics.daily_metrics_dashboard import DailyMetricsDashboard
from analytics.engagement_metrics import EngagementMetrics
from analytics.enhanced_competitor_discovery import EnhancedCompetitorDiscovery
from analytics.smart_competitor_manager import SmartCompetitorManager
from analytics.smart_trend_detector import SmartTrendDetector
from analytics.youtube_psychology_analyzer import YouTubePsychologyAnalyzer

# Additional import error handling for missing modules
try:
    from utils.smart_model_manager import SmartModelManager  # type: ignore
    from utils.data_validator import DataValidator  # type: ignore
    from utils.browser_manager import BrowserManager  # type: ignore
except ImportError as e:
    logging.warning(f"Import warning for utils modules: {e}")
    class SmartModelManager: pass  # type: ignore
    class DataValidator: pass  # type: ignore
    class BrowserManager: pass  # type: ignore

try:
    from automation.cpu_queue_manager import CPUQueueManager  # type: ignore
    from automation.night_processor import NightProcessor  # type: ignore
except ImportError as e:
    logging.warning(f"Import warning for automation modules: {e}")
    class CPUQueueManager: pass  # type: ignore
    class NightProcessor: pass  # type: ignore

# Resource management settings
os.environ.setdefault('CPU_LIMIT_PERCENT', '70')  # Lower default limit
os.environ.setdefault('STARTUP_DELAY_SECONDS', '3')  # Delay between component batches
os.environ.setdefault('CPU_CHECK_INTERVAL', '2')  # CPU check frequency

# Performance tuning based on server capacity
os.environ.setdefault('CONTENT_BATCH_SIZE', '3')  # Videos per batch
os.environ.setdefault('CONCURRENT_UPLOADS', '2')  # Parallel uploads
os.environ.setdefault('TREND_CHECK_INTERVAL', '1800')  # 30 minutes
os.environ.setdefault('VIRAL_MODE_THRESHOLD', '0.8')  # Trigger viral mode

class EnhancedMonAYOrchestrator:
    """Fully Enhanced YouTube Automation System with ALL Components and Resource Management"""
    
    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # Resource management settings
        self.cpu_limit = int(os.getenv('CPU_LIMIT_PERCENT', '70'))
        self.startup_delay = int(os.getenv('STARTUP_DELAY_SECONDS', '3'))
        self.cpu_check_interval = int(os.getenv('CPU_CHECK_INTERVAL', '2'))
        
        # Daily counter management
        self._today_video_count = 0
        self._last_reset_date = datetime.now().date()
        self.daily_upload_count = 0
        self.daily_revenue_count = 0
        
        # Initialize CPU resource manager
        self.cpu_manager = CPUResourceManager()
        
        self.logger.info(f"🔧 Resource settings: CPU limit {self.cpu_limit}%, startup delay {self.startup_delay}s")
        
        # Initialize component placeholders
        self._init_component_placeholders()
    
    def _reset_daily_counters(self):
        """Reset daily counters if it's a new day"""
        current_date = datetime.now().date()
        if not hasattr(self, '_last_reset_date') or current_date != self._last_reset_date:
            self._today_video_count = 0
            self._last_reset_date = current_date
            self.logger.info("🔄 Daily counters reset for new day")
    
    async def detect_channel_age_weeks(self) -> int:
        """Detect channel age in weeks for warmup scheduling"""
        try:
            # Try to get channel creation date from YouTube API
            if hasattr(self, 'channel_verifier') and self.channel_verifier:
                channel_info = self.channel_verifier.verify_connected_channel()
                if channel_info and 'snippet' in channel_info:
                    published_at = channel_info['snippet'].get('publishedAt')
                    if published_at:
                        from datetime import datetime
                        import dateutil.parser
                        creation_date = dateutil.parser.parse(published_at)
                        age_days = (datetime.now(creation_date.tzinfo) - creation_date).days
                        age_weeks = max(1, age_days // 7)  # At least 1 week
                        self.logger.info(f"📅 Channel age detected: {age_weeks} weeks ({age_days} days)")
                        return age_weeks
            
            # Fallback: check for stored channel age or use environment variable
            import os
            stored_age = os.getenv('CHANNEL_AGE_WEEKS')
            if stored_age:
                age_weeks = int(stored_age)
                self.logger.info(f"📅 Using stored channel age: {age_weeks} weeks")
                return age_weeks
            
            # Default to week 1 for new channels (conservative approach)
            self.logger.warning("⚠️ Could not detect channel age, defaulting to week 1 (warmup mode)")
            return 1
            
        except Exception as e:
            self.logger.error(f"❌ Channel age detection failed: {e}")
            return 1  # Safe default
        
    def _init_component_placeholders(self):
        """Initialize all component placeholders to None for progressive loading"""
        # Core Components
        self.agent_manager = None
        self.content_pipeline = None
        self.upload_manager = None
        self.trend_predictor = None
        self.revenue_optimizer = None
        self.metrics_tracker = None
        self.dashboard_manager = None
        
        # Advanced Automation
        self.smart_scheduler = None
        self.daily_optimizer = None
        
        # Advanced Analytics
        self.algorithm_analyzer = None
        self.predictive_analytics = None
        self.retention_analytics = None
        
        # Growth & Viral Systems
        self.viral_growth_engine = None
        self.ten_k_accelerator = None
        
        # Advanced Content Systems
        self.retention_system = None
        self.algorithm_optimizer = None
        self.viral_optimizer = None
        self.quality_enhancer = None
        
        # Advanced Viral Systems
        self.viral_master_system = None
        self.viral_monetization = None
        self.neon_finance_ai = None
        self.instant_viral_generator = None
        self.ai_viral_learning = None
        
        # Enhanced Distribution
        self.platform_optimizer = None
        self.social_manager = None
        
        # Advanced Monetization
        self.smart_ad_optimizer = None
        self.affiliate_manager = None
        self.email_automation = None
        
        # System Monitoring
        self.performance_monitor = None
        self.policy_checker = None
        
        # Content Generation Tools
        self.tts_generator = None
        self.channel_verifier = None
        
        # AI Prompt Orchestrator
        self.ai_prompt_orchestrator = None
        
        # Brand Manager
        self.brand_manager = None
        
        # Content Deduplication and Enhanced Learning
        self.deduplication_manager = None
        self.enhanced_learning = None
        
        # Original Finance Generator
        self.original_finance_generator = None
    
    async def check_component_availability(self) -> Dict[str, bool]:
        """Check which components are actually available vs fallbacks"""
        availability = {
            'core_components': True,
            'content_modules': hasattr(self.content_pipeline, 'generate_content'),
            'upload_manager': hasattr(self.upload_manager, 'upload_video'),
            'analytics': hasattr(self.metrics_tracker, 'track_performance'),
            'monetization': hasattr(self.revenue_optimizer, 'optimize_revenue'),
            'viral_systems': hasattr(self.viral_growth_engine, 'accelerate_growth')
        }
        
        missing_components = [k for k, v in availability.items() if not v]
        if missing_components:
            self.logger.warning(f"⚠️ Missing components: {missing_components}")
        
        return availability
        
    def setup_logging(self):
        """Setup comprehensive logging with rotation"""
        from logging.handlers import RotatingFileHandler
        
        # Create rotating file handler (10MB max, keep 5 backups)
        file_handler = RotatingFileHandler(
            'enhanced_system.log', 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                file_handler,
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Add error tracking
        self.error_count = 0
        self.last_error_time = None

    async def check_cpu_usage(self) -> bool:
        """Check if CPU usage is within acceptable limits"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > self.cpu_limit:
                self.logger.warning(f"⚠️ High CPU usage: {cpu_percent:.1f}% (limit: {self.cpu_limit}%)")
                return False
            return True
        except Exception as e:
            self.logger.warning(f"⚠️ Could not check CPU usage: {e}")
            return True

    async def wait_for_cpu_cooldown(self, max_wait: int = 30):
        """Wait for CPU usage to drop below limit"""
        wait_time = 0
        while wait_time < max_wait:
            if await self.check_cpu_usage():
                return
            self.logger.info(f"🔄 Waiting for CPU cooldown... ({wait_time}s/{max_wait}s)")
            await asyncio.sleep(self.cpu_check_interval)
            wait_time += self.cpu_check_interval
        
        self.logger.warning(f"⚠️ CPU cooldown timeout after {max_wait}s, continuing anyway")

    async def safe_execute_with_logging(self, func, *args, **kwargs):
        """Execute function with comprehensive error logging"""
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except Exception as e:
            self.error_count += 1
            self.last_error_time = datetime.now()
            self.logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            return None

    async def progressive_delay(self, step_name: str):
        """Progressive delay with CPU monitoring"""
        self.logger.info(f"⏳ Pausing {self.startup_delay}s after {step_name}...")
        await asyncio.sleep(self.startup_delay)
        await self.wait_for_cpu_cooldown()
    
    async def run_system_warm_up(self):
        """Resource-aware system warm-up with progressive loading"""
        self.logger.info("🔥 Starting Resource-Aware MonAY System Warm-up...")
        
        try:
            # 1. Initial Resource Check
            self.logger.info("📊 Initial resource assessment...")
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            disk = psutil.disk_usage('.')
            
            self.logger.info(f"💾 Memory: {memory.percent:.1f}% used ({memory.available // (1024**3)} GB available)")
            self.logger.info(f"🖥️ CPU: {cpu_percent:.1f}% usage")
            self.logger.info(f"💽 Disk: {disk.percent:.1f}% used ({disk.free // (1024**3)} GB free)")
            
            # Resource warnings
            if memory.percent > 85:
                self.logger.warning("⚠️ High memory usage detected - proceeding with caution")
            if cpu_percent > self.cpu_limit:
                self.logger.warning(f"⚠️ High CPU usage detected - waiting for cooldown")
                await self.wait_for_cpu_cooldown()
            
            await self.progressive_delay("initial resource check")
            
            # 2. API Connectivity Tests (lightweight)
            self.logger.info("📡 Testing API connectivity...")
            
            # Test Hugging Face API
            try:
                wan_token = (
                    os.getenv('WAN_TOKEN')
                    or os.getenv('WAN_API_TOKEN')
                    or os.getenv('HF_TOKEN')
                )
                # Use v2 endpoint for auth, and allow redirects
                wan_test_url = "https://wan.co/api/whoami-v2"
                headers = {"Authorization": f"Bearer {wan_token}"} if wan_token and wan_token != 'wan_free_tier' else {}
                response = requests.get(wan_test_url, headers=headers, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    self.logger.info("✅ Hugging Face API: Connected")
                else:
                    self.logger.warning(f"⚠️ Hugging Face API: Status {response.status_code}")
            except Exception as e:
                self.logger.warning(f"⚠️ Hugging Face API: {e}")
            
            # Test YouTube API
            try:
                if os.path.exists('youtube_tokens.json'):
                    self.logger.info("✅ YouTube tokens: Found")
                else:
                    self.logger.warning("⚠️ YouTube tokens: Not found")
            except Exception as e:
                self.logger.warning(f"⚠️ YouTube tokens: {e}")
            
            await self.progressive_delay("API connectivity tests")
            
            # 3. File System Tests
            self.logger.info("📁 Testing file system...")
            
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            test_file = data_dir / 'warmup_test.txt'
            
            try:
                test_file.write_text('warmup test')
                content = test_file.read_text()
                test_file.unlink()
                self.logger.info("✅ File system: Read/Write OK")
            except Exception as e:
                self.logger.error(f"❌ File system: {e}")
            
            await self.progressive_delay("file system tests")
            
            # 4. Directory Structure Check
            self.logger.info("🔧 Checking directory structure...")
            
            required_dirs = ['src', 'src/content', 'src/analytics', 'src/distribution']
            for dir_path in required_dirs:
                if Path(dir_path).exists():
                    self.logger.info(f"✅ Directory: {dir_path}")
                else:
                    self.logger.warning(f"⚠️ Directory missing: {dir_path}")
            
            await self.progressive_delay("directory structure check")
            
            # 5. Environment Variables Check
            self.logger.info("🌍 Checking environment variables...")
            
            env_vars = {
    'WAN_API_TOKEN': os.getenv('WAN_API_TOKEN', 'Not set'),
    'WAN_TOKEN': os.getenv('WAN_TOKEN', 'Not set'),
    'USE_FREE_TIER': os.getenv('USE_FREE_TIER', 'Not set'),
    'CPU_LIMIT_PERCENT': os.getenv('CPU_LIMIT_PERCENT', 'Not set')
}
            
            for var, value in env_vars.items():
                if value != 'Not set':
                    self.logger.info(f"✅ {var}: Configured")
                else:
                    self.logger.warning(f"⚠️ {var}: Not set")
            
            self.logger.info("🚀 Resource-aware warm-up completed successfully!")
            self.logger.info("" + "="*50)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Warm-up failed: {e}")
            return False

    async def initialize_component_batch(self, batch_name: str, components: List[tuple]) -> int:
        """Initialize a batch of components with enhanced error handling"""
        initialized_count = 0
        failed_components = []
        
        self.logger.info(f"🔄 Initializing {batch_name} batch ({len(components)} components)")
        
        for component_name, component_class in components:
            try:
                # Check CPU before each component
                if not await self.check_cpu_usage():
                    await self.wait_for_cpu_cooldown()
                
                self.logger.info(f"   ⚡ Initializing {component_name}...")
                
                # Special handling for components that need config
                if component_name == 'upload_manager':
                    # Create config for EnhancedUploadManager
                    upload_config = {
                        'auto_retry': True,
                        'max_retries': 3,
                        'platforms': ['youtube', 'blog', 'pod', 'social'],
                        'youtube_enabled': True,
                        'blog_enabled': True,
                        'pod_enabled': True,
                        'social_enabled': True
                    }
                    component_instance = component_class(upload_config)
                else:
                    # Enhanced component initialization with timeout
                    component_instance = component_class()
                
                # Initialize with timeout if method exists
                if hasattr(component_instance, 'initialize'):
                    try:
                        await asyncio.wait_for(
                            component_instance.initialize(), 
                            timeout=30.0  # 30 second timeout
                        )
                    except asyncio.TimeoutError:
                        self.logger.error(f"   ❌ {component_name} initialization timed out")
                        failed_components.append(component_name)
                        continue
                
                # Store component
                setattr(self, component_name.lower().replace(' ', '_'), component_instance)
                initialized_count += 1
                
                self.logger.info(f"   ✅ {component_name} initialized successfully")
                
                # Progressive delay between components
                await self.progressive_delay(f"{batch_name}_{component_name}")
                
            except ImportError as e:
                self.logger.warning(f"   ⚠️ {component_name} not available: {e}")
                failed_components.append(component_name)
                # Create a placeholder/fallback
                setattr(self, component_name.lower().replace(' ', '_'), None)
                
            except Exception as e:
                self.logger.error(f"   ❌ Failed to initialize {component_name}: {e}")
                failed_components.append(component_name)
                # Create a placeholder
                setattr(self, component_name.lower().replace(' ', '_'), None)
        
        if failed_components:
            self.logger.warning(f"Failed components in {batch_name}: {failed_components}")
        
        self.logger.info(f"✅ {batch_name} batch complete: {initialized_count}/{len(components)} successful")
        return initialized_count
    
    async def initialize_system(self):
        """Initialize ALL system components with progressive resource-aware loading"""
        self.logger.info("🚀 Starting Resource-Aware System Initialization...")
        
        # Run warm-up sequence first
        if not await self.run_system_warm_up():
            self.logger.error("❌ Warm-up failed, but continuing with initialization...")
        
        try:
            # Optimize system for long-running tasks
            await self.cpu_manager.optimize_for_long_running()
            
            # Get optimal settings
            optimal_settings = self.cpu_manager.get_optimal_settings()
            self.logger.info(f"🔧 Using CPU-optimized settings: {optimal_settings}")
            
            total_initialized = 0
            
            # Batch 1: Core Essential Components
            core_components = [
                ('agent_manager', AgentManager),
                ('content_pipeline', ContentPipeline),
                ('upload_manager', UploadManager),
            ]
            total_initialized += await self.initialize_component_batch("Core Components", core_components)
            await self.progressive_delay("core components")
            
            # Batch 2: Analytics and Prediction
            analytics_components = [
                ('trend_predictor', TrendPredictor),
                ('metrics_tracker', AdvancedMetricsTracker),
                ('algorithm_analyzer', YouTubeAlgorithmAnalyzer),
            ]
            total_initialized += await self.initialize_component_batch("Analytics Components", analytics_components)
            await self.progressive_delay("analytics components")
            
            # Batch 3: Automation and Optimization
            automation_components = [
                ('smart_scheduler', SmartScheduler),
                ('daily_optimizer', DailyOptimizer),
                ('revenue_optimizer', RevenueOptimizer),
            ]
            total_initialized += await self.initialize_component_batch("Automation Components", automation_components)
            await self.progressive_delay("automation components")
            
            # Batch 4: Content Generation Systems
            content_components = [
                ('retention_system', YouTubeRetentionSystem),
                ('algorithm_optimizer', AlgorithmOptimizer),
                ('viral_optimizer', ViralOptimizer),
                ('quality_enhancer', VideoQualityEnhancer),
                ('brand_manager', BrandManager),
                ('original_finance_generator', OriginalFinanceGenerator),
                ('ai_image_generator', AIImageGenerator),
                ('tts_generator', TTSGenerator),
            ]
            total_initialized += await self.initialize_component_batch("Content Components", content_components)
            await self.progressive_delay("content components")
            
            # Batch 5: Advanced Viral Systems
            viral_components = [
                ('viral_master_system', UltimateViralSystem),
                ('viral_monetization', ViralMonetizationIntegrator),
                ('instant_viral_generator', InstantViralGenerator),
            ]
            total_initialized += await self.initialize_component_batch("Viral Components", viral_components)
            await self.progressive_delay("viral components")
            
            # Batch 6: AI and Learning Systems
            ai_components = [
                ('ai_viral_learning', AIViralLearningSystem),
                ('ai_prompt_orchestrator', AIPromptOrchestrator),
            ]
            total_initialized += await self.initialize_component_batch("AI Components", ai_components)
            await self.progressive_delay("AI components")
            
            # Batch 7: Distribution and Social
            distribution_components = [
                ('platform_optimizer', PlatformOptimizer),
                ('social_manager', SocialManager),
            ]
            total_initialized += await self.initialize_component_batch("Distribution Components", distribution_components)
            await self.progressive_delay("distribution components")
            
            # Batch 8: Advanced Analytics
            advanced_analytics_components = [
                ('predictive_analytics', PredictiveAnalytics),
                ('retention_analytics', RetentionAnalytics),
            ]
            total_initialized += await self.initialize_component_batch("Advanced Analytics", advanced_analytics_components)
            await self.progressive_delay("advanced analytics")
            
            # Batch 9: Growth and Monetization
            growth_components = [
                ('viral_growth_engine', ViralGrowthEngine),
                ('ten_k_accelerator', TenKAccelerator),
                ('smart_ad_optimizer', SmartAdOptimizer),
                ('affiliate_manager', AffiliateManager),
                ('email_automation', EmailAutomation),
            ]
            total_initialized += await self.initialize_component_batch("Growth & Monetization", growth_components)
            await self.progressive_delay("growth components")
            
            # Batch 10: Content Management and Learning
            content_management_components = [
                ('deduplication_manager', ContentDeduplicationManager),
                ('enhanced_learning', EnhancedLearningSystem),
            ]
            total_initialized += await self.initialize_component_batch("Content Management", content_management_components)
            await self.progressive_delay("content management")
            
            # Batch 11: System Monitoring (Last)
            monitoring_components = [
                ('performance_monitor', PerformanceMonitor),
                ('policy_checker', EnhancedPolicyWatcher),
                ('channel_verifier', ChannelVerifier),
                ('dashboard_manager', DashboardManager),
            ]
            total_initialized += await self.initialize_component_batch("Monitoring Components", monitoring_components)
            
            # Connect orchestrator to video generator
            try:
                if self.content_pipeline is not None:
                    if hasattr(self.content_pipeline, 'pro_video_generator') and self.content_pipeline.pro_video_generator:
                        self.content_pipeline.pro_video_generator.set_orchestrator(self)
                        self.logger.info("✅ Orchestrator connected to video generator")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not connect orchestrator: {e}")
            
            self.logger.info(f"🚀 Resource-aware initialization completed! {total_initialized} components initialized")
            
            # Final resource check
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            self.logger.info(f"📊 Final resource usage - Memory: {memory.percent:.1f}%, CPU: {cpu_percent:.1f}%")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Resource-aware system initialization failed: {e}")
            return False
    
    async def enhanced_automation_loop(self):
        """FULLY ENHANCED automation loop with ALL features and resource monitoring"""
        while self.running:
            try:
                cycle_start = datetime.now()
                self.logger.info("🔄 Starting ENHANCED automation cycle...")
                
                # Check resources before starting cycle
                if not await self.check_cpu_usage():
                    self.logger.warning("⚠️ High CPU usage detected, waiting before cycle")
                    await self.wait_for_cpu_cooldown()
                
                # 1. ENHANCED TREND ANALYSIS
                trends = await self.get_enhanced_trends()
                
                # 2. VIRAL CONTENT GENERATION with AI Enhancement
                content_batch = await self.generate_viral_content(trends)
                
                # 3. ALGORITHM OPTIMIZATION
                optimized_content = await self.optimize_for_algorithm(content_batch) # type: ignore
                
                # 4. QUALITY ENHANCEMENT
                enhanced_content = await self.enhance_content_quality(optimized_content) # type: ignore
                
                # 5. SMART SCHEDULING (Prime Time)
                scheduled_uploads = await self.schedule_prime_time_uploads(enhanced_content) # type: ignore
                
                # 6. MULTI-PLATFORM DISTRIBUTION
                distribution_results = await self.distribute_across_platforms(scheduled_uploads) # type: ignore
                
                # 7. VIRAL GROWTH ACCELERATION
                growth_results = await self.accelerate_viral_growth(distribution_results) # type: ignore
                
                # 8. ADVANCED MONETIZATION
                monetization_results = await self.optimize_advanced_monetization(growth_results) # type: ignore
                
                # 9. PREDICTIVE ANALYTICS
                predictions = await self.run_predictive_analytics(monetization_results) # type: ignore
                
                # 10. DAILY OPTIMIZATIONS
                daily_optimizations = await self.run_daily_optimizations() # type: ignore
                
                # 11. PERFORMANCE MONITORING
                performance_metrics = await self.monitor_system_performance() # type: ignore
                
                # 12. DASHBOARD UPDATE with ALL metrics
                await self.update_enhanced_dashboard({ # type: ignore
                    'trends': trends,
                    'content': enhanced_content,
                    'uploads': scheduled_uploads,
                    'distribution': distribution_results,
                    'growth': growth_results,
                    'monetization': monetization_results,
                    'predictions': predictions,
                    'optimizations': daily_optimizations,
                    'performance': performance_metrics
                })
                
                cycle_duration = (datetime.now() - cycle_start).total_seconds()
                self.logger.info(f"✅ Enhanced cycle completed in {cycle_duration:.2f}s")
                
                # Smart wait time based on performance and CPU usage
                wait_time = await self.calculate_optimal_wait_time(cycle_duration) # type: ignore
                
                # Additional wait if CPU is high
                if not await self.check_cpu_usage():
                    wait_time = max(wait_time, 600)  # At least 10 minutes if CPU is high
                    self.logger.info(f"⏳ Extended wait time due to high CPU usage: {wait_time}s")
                
                await asyncio.sleep(wait_time)
                
            except Exception as e:
                self.logger.error(f"❌ Enhanced automation cycle failed: {e}")
                await asyncio.sleep(300)  # 5 min wait on error
    
    async def get_enhanced_trends(self) -> List[Dict]:
        """Get trends with advanced analysis"""
        try:
            # Basic trends
            if self.trend_predictor is not None and hasattr(self.trend_predictor, 'get_trending_topics'):
                basic_trends = self.safe_execute_with_logging(self.trend_predictor.get_trending_topics) or []
            else:
                basic_trends = []
                self.logger.warning("Trend predictor not available, using empty trends")
            
            # Enhanced with viral potential analysis
            enhanced_trends = []
            for trend in basic_trends:
                viral_result = {'viral_scores': {}, 'high_potential_trends': []}
                if self.viral_growth_engine is not None and hasattr(self.viral_growth_engine, 'analyze_viral_potential'):
                    viral_result = self.safe_execute_with_logging(self.viral_growth_engine.analyze_viral_potential, trend) or {'viral_scores': {}, 'high_potential_trends': []}
                else:
                    self.logger.warning("Viral growth engine not available")
                
                algorithm_result = {'algorithm_fit_score': 0.5}
                if self.algorithm_analyzer is not None and hasattr(self.algorithm_analyzer, 'analyze_trend_algorithm_fit'):
                    algorithm_result = self.safe_execute_with_logging(self.algorithm_analyzer.analyze_trend_algorithm_fit, trend, content_data=trend) or {'algorithm_fit_score': 0.5}
                else:
                    self.logger.warning("Algorithm analyzer not available")
                
                # Extract numeric scores from the dictionaries
                viral_score = 0.5  # Default fallback
                if isinstance(viral_result, dict):
                    # Get the average viral score from viral_scores dict, or use a default
                    viral_scores = viral_result.get('viral_scores', {})
                    if viral_scores:
                        viral_score = sum(viral_scores.values()) / len(viral_scores)
                    elif viral_result.get('high_potential_trends'):
                        # Use the first high potential trend's score
                        viral_score = viral_result['high_potential_trends'][0].get('viral_score', 0.5)
                
                algorithm_score = 0.5  # Default fallback
                if isinstance(algorithm_result, dict):
                    algorithm_score = algorithm_result.get('algorithm_fit_score', 0.5)
                
                enhanced_trends.append({
                    'topic': trend,
                    'viral_score': viral_score,
                    'algorithm_score': algorithm_score,
                    'combined_score': (viral_score + algorithm_score) / 2
                })
            
            # Sort by combined score
            enhanced_trends.sort(key=lambda x: x['combined_score'], reverse=True)
            return enhanced_trends[:5]  # Top 5
            
        except Exception as e:
            self.logger.error(f"Enhanced trend analysis failed: {e}")
            return [{'topic': 'AI automation', 'viral_score': 0.8, 'algorithm_score': 0.7, 'combined_score': 0.75}]
    
    async def generate_viral_content(self, trends: List[Dict]) -> List[Dict]:
        """Generate viral content using PRO models with daily limits and Shorts classification"""
        self.logger.info("🎬 Generating VIRAL content with pro models...")
        
        try:
            # Reset daily counters if new day
            self._reset_daily_counters()
            
            # Detect channel age for warmup scheduling
            channel_age_weeks = await self.detect_channel_age_weeks()
            
            # Check if we've already hit today's limit
            if hasattr(self, 'smart_scheduler') and self.smart_scheduler:
                self.logger.info("📋 Checking smart scheduler for daily limits...")
                daily_schedule = await self.smart_scheduler.get_viral_schedule(channel_age_weeks)
                max_daily_videos = len(daily_schedule.get('shorts', []))
                
                # Check how many videos we've already created today
                today_videos = getattr(self, '_today_video_count', 0)
                
                self.logger.info(f"📊 Daily video status: {today_videos}/{max_daily_videos} videos created today")
                self.logger.info(f"📋 Daily schedule: {daily_schedule}")
                self.logger.info(f"📅 Channel age: {channel_age_weeks} weeks")
                
                if today_videos >= max_daily_videos:
                    self.logger.info(f"📊 Daily limit reached: {today_videos}/{max_daily_videos} videos")
                    return []
                
                # Limit to remaining videos for today
                remaining_videos = max_daily_videos - today_videos
                video_count = min(len(trends), remaining_videos, 3)  # Max 3 per cycle
                self.logger.info(f"🎯 Planning to generate {video_count} videos (remaining: {remaining_videos})")
            else:
                self.logger.warning("⚠️ Smart scheduler not available, using fallback limits")
                # Implement basic warmup schedule as fallback
                if channel_age_weeks <= 1:
                    max_daily_videos = 1
                elif channel_age_weeks <= 2:
                    max_daily_videos = 2
                else:
                    max_daily_videos = 3
                
                today_videos = getattr(self, '_today_video_count', 0)
                remaining_videos = max_daily_videos - today_videos
                video_count = min(len(trends), remaining_videos, 3)
                self.logger.info(f"📊 Fallback warmup: Week {channel_age_weeks}, max daily: {max_daily_videos}, remaining: {remaining_videos}")
            
            if video_count <= 0:
                self.logger.info("⏸️ No videos to generate - daily limit reached or no trends available")
                self.logger.info(f"🔍 Debug info - trends count: {len(trends)}, video_count: {video_count}")
                return []
            
            # Generate content with CPU resource management
            content_batch = []
            
            for trend in trends[:video_count]:  # Limit concurrent generation
                    try:
                        # Execute with resource limits
                        if self.cpu_manager is not None:
                            content = await self.cpu_manager.execute_with_limits( # type: ignore
                                self._create_single_viral_content,
                                f"content_generation_{trend.get('topic', 'unknown')}",
                                trend=trend
                            )
                        else:
                            # Fallback: create content directly without CPU manager
                            content = await self._create_single_viral_content(trend)
                            self.logger.warning("CPU manager not available, using direct generation")
                        
                        if content:
                            content_batch.append(content)
                            
                    except Exception as e:
                        self.logger.error(f"Content generation failed for {trend}: {e}")
            
            # Check for duplicates and filter content
            filtered_content_batch = []
            for content in content_batch:
                # Check for duplicates before processing
                if self.deduplication_manager:
                    duplicate_check = self.deduplication_manager.check_duplicate(content)
                    
                    if duplicate_check["is_duplicate"]:
                        self.logger.warning(f"Duplicate content detected: {duplicate_check['reason']}")
                        # Skip this content
                        continue
                    
                    # Register content to prevent future duplicates
                    content_id = self.deduplication_manager.register_content(content)
                    content['content_id'] = content_id
                
                filtered_content_batch.append(content)
            
            content_batch = filtered_content_batch
            
            # Ensure each video is properly marked as a Short
            for content in content_batch:
                content.update({
                    'format_type': 'short',
                    'is_youtube_short': True,
                    'vertical_format': True,
                    'aspect_ratio': '9:16',
                    'duration': min(content.get('duration', 60), 60),  # Max 60 seconds
                    'shorts_optimized': True,
                    'platform_format': 'youtube_shorts'
                })
                
                # Add #Shorts hashtag if not present
                tags = content.get('tags', [])
                if 'Shorts' not in tags and 'shorts' not in tags:
                    tags.append('Shorts')
                content['tags'] = tags
                
                # Ensure title indicates it's a Short
                title = content.get('title', '')
                if not any(indicator in title.lower() for indicator in ['#shorts', 'in 60 seconds', 'quick']):
                    content['title'] = f"{title} #Shorts"
            
            # Track today's video count
            if not hasattr(self, '_today_video_count'):
                self._today_video_count = 0
            self._today_video_count += len(content_batch)
            
            self.logger.info(f"✅ Generated {len(content_batch)} YouTube Shorts ({self._today_video_count} total today)")
            
            # Additional debug logging
            if len(content_batch) == 0:
                self.logger.warning("⚠️ No content was generated despite passing initial checks")
                self.logger.info(f"🔍 Debug - trends: {len(trends)}, video_count: {video_count}")
                self.logger.info(f"🔍 Debug - filtered_content_batch length: {len(filtered_content_batch)}")
            
            return content_batch
            
        except Exception as e:
            self.logger.error(f"Viral content generation failed: {e}")
            return []
    
    async def _create_single_viral_content(self, trend: Dict) -> Dict:
        """Create single piece of viral content with CPU optimization"""
        try:
            # Generate script
            if self.instant_viral_generator is not None:
                script = await self.instant_viral_generator.create_viral_shorts_package( # type: ignore
                    trend.get('topic')
                )
            else:
                script = {'script': 'Fallback script content'}
                self.logger.warning("Instant viral generator not available, using fallback script")
            
            # Generate audio with CPU limits
            if self.tts_generator is not None: # type: ignore
                audio_path = await self.tts_generator.generate_audio( # type: ignore
                    script['script']
                )
            else:
                audio_path = 'fallback_audio.mp3'
                self.logger.warning("TTS generator not available, using fallback audio")
            
            # Generate video with CPU limits
            if self.video_processor is not None:
                video_path = self.video_processor.create_shorts_video(
                    script['script'],
                    audio_path,
                    background_type="finance_charts"
                )
            else:
                video_path = 'fallback_video.mp4'
                self.logger.warning("Video processor not available, using fallback video")
            
            return {
                'script': script,
                'audio_path': audio_path,
                'video_path': video_path,
                'trend': trend,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Single content creation failed: {e}")
            return {
                'script': {'script': 'Error: Content generation failed'},
                'audio_path': 'error_audio.mp3',
                'video_path': 'error_video.mp4',
                'trend': trend,
                'created_at': datetime.now().isoformat(),
                'error': str(e)
            }
    
    async def optimize_for_algorithm(self, content_batch: List[Dict]) -> List[Dict]:
        """Optimize content for YouTube algorithm"""
        optimized_content = []
        
        for content in content_batch:
            try:
                # Algorithm optimization
                algorithm_optimized = {}
                if self.algorithm_optimizer is not None:
                    algorithm_optimized = await self.algorithm_optimizer.optimize_content_for_algorithm(content)
                else:
                    self.logger.warning("Algorithm optimizer not available")
                
                # Algorithm analysis
                algorithm_analysis = {}
                if self.algorithm_analyzer is not None:
                    algorithm_analysis = await self.algorithm_analyzer.analyze_algorithm_performance(content)
                else:
                    self.logger.warning("Algorithm analyzer not available")
                
                optimized_content.append({
                    **content,
                    'algorithm_optimization': algorithm_optimized,
                    'algorithm_analysis': algorithm_analysis
                })
                
            except Exception as e:
                self.logger.error(f"Algorithm optimization failed: {e}")
                optimized_content.append(content)
        
        return optimized_content
    
    async def enhance_content_quality(self, content_batch: List[Dict]) -> List[Dict]:
        """Enhance content quality"""
        enhanced_content = []
        
        for content in content_batch:
            try:
                # Quality enhancement
                quality_enhanced = {}
                if self.quality_enhancer is not None:
                    quality_enhanced = await self.quality_enhancer.enhance_content_quality(content)
                else:
                    self.logger.warning("Quality enhancer not available")
                
                # Policy compliance check
                policy_check = {}
                if self.policy_checker is not None:
                    policy_check = await self.policy_checker.check_content_compliance(content)
                else:
                    self.logger.warning("Policy checker not available")
                
                enhanced_content.append({
                    **content,
                    'quality_enhancement': quality_enhanced,
                    'policy_compliance': policy_check
                })
                
            except Exception as e:
                self.logger.error(f"Quality enhancement failed: {e}")
                enhanced_content.append(content)
        
        return enhanced_content
    
    async def schedule_prime_time_uploads(self, content_batch: List[Dict]) -> List[Dict]:
        """Schedule uploads for prime time using smart scheduler"""
        scheduled_uploads = []
        
        for content in content_batch:
            try:
                # Get available agent
                agent = None
                if self.agent_manager is not None:
                    agent = self.agent_manager.get_next_available_agent()
                if not agent:
                    self.logger.warning("No available agents for upload")
                    continue
                
                # Calculate optimal upload time
                current_week = (datetime.now() - self.system_start_date).days // 7
                optimal_time = datetime.now() + timedelta(hours=1)  # Fallback
                if self.smart_scheduler is not None:
                    optimal_time = await self.smart_scheduler.predict_optimal_time(content, current_week)
                else:
                    self.logger.warning("Smart scheduler not available, using fallback time")

                # Schedule upload for optimal time (not immediate!)
                upload_task = None
                if self.upload_manager is not None:
                    upload_task = await self.upload_manager.schedule_upload_for_time(agent, content, optimal_time)
                else:
                    self.logger.warning("Upload manager not available")
                
                scheduled_uploads.append({
                    'content': content,
                    'agent': agent,
                    'upload_task': upload_task,
                    'scheduled_time': optimal_time
                })
                
                self.logger.info(f"📅 Scheduled upload for {optimal_time}: {content.get('id', 'unknown')}")
                
            except Exception as e:
                self.logger.error(f"Prime time scheduling failed: {e}")
        
        return scheduled_uploads
    
    async def distribute_across_platforms(self, scheduled_uploads: List[Dict]) -> List[Dict]:
        """Distribute content across multiple platforms"""
        distribution_results = []
        
        for upload_data in scheduled_uploads:
            try:
                content = upload_data['content']
                
                # Platform optimization
                platform_optimized = {}
                if self.platform_optimizer is not None:
                    platform_optimized = await self.platform_optimizer.optimize_for_platforms(content, ["youtube", "tiktok", "instagram", "x"])
                else:
                    self.logger.warning("Platform optimizer not available")
                
                # Social media distribution
                social_results = {}
                if self.social_manager is not None:
                    social_results = await self.social_manager.distribute_to_social_media(content)
                else:
                    self.logger.warning("Social manager not available")
                
                # Blog distribution
                blog_result = await self.trigger_enhanced_autoblog(content)
                
                # POD distribution
                pod_result = await self.trigger_enhanced_pod(content)
                
                distribution_results.append({
                    **upload_data,
                    'platform_optimization': platform_optimized,
                    'social_distribution': social_results,
                    'blog_distribution': blog_result,
                    'pod_distribution': pod_result
                })
                
            except Exception as e:
                self.logger.error(f"Multi-platform distribution failed: {e}")
                distribution_results.append(upload_data)
        
        return distribution_results
    
    async def accelerate_viral_growth(self, distribution_results: List[Dict]) -> List[Dict]:
        """Apply viral growth acceleration strategies"""
        growth_results = []
        
        for result in distribution_results:
            try:
                content = result['content']
                
                # Viral growth strategies
                viral_strategies = {}
                if self.viral_growth_engine is not None:
                    viral_strategies = await self.viral_growth_engine.implement_viral_strategies(content)
                else:
                    self.logger.warning("Viral growth engine not available")
                
                # 10K subscriber acceleration
                acceleration_plan = {}
                if self.ten_k_accelerator is not None:
                    acceleration_plan = await self.ten_k_accelerator.create_acceleration_plan(content)
                else:
                    self.logger.warning("10K accelerator not available")
                
                growth_results.append({
                    **result,
                    'viral_strategies': viral_strategies,
                    'acceleration_plan': acceleration_plan
                })
                
            except Exception as e:
                self.logger.error(f"Viral growth acceleration failed: {e}")
                growth_results.append(result)
        
        return growth_results
    
    async def optimize_advanced_monetization(self, growth_results: List[Dict]) -> List[Dict]:
        """Apply advanced monetization strategies"""
        monetization_results = []
        
        for result in growth_results:
            try:
                content = result['content']
                
                # Smart ad optimization
                ad_optimization = {}
                if self.smart_ad_optimizer is not None:
                    ad_optimization = await self.smart_ad_optimizer.optimize_ad_placement(content)
                else:
                    self.logger.warning("Smart ad optimizer not available")
                
                # Affiliate marketing
                affiliate_opportunities = {}
                if self.affiliate_manager is not None:
                    affiliate_opportunities = await self.affiliate_manager.find_affiliate_opportunities(content)
                else:
                    self.logger.warning("Affiliate manager not available")
                
                # Email automation
                email_campaign = {}
                if self.email_automation is not None:
                    email_campaign = await self.email_automation.create_content_campaign(content)
                else:
                    self.logger.warning("Email automation not available")
                
                # Revenue optimization
                revenue_optimization = {}
                if self.revenue_optimizer is not None:
                    revenue_optimization = await self.revenue_optimizer.optimize_revenue({
                        'content': content,
                        'ad_optimization': ad_optimization,
                        'affiliate_opportunities': affiliate_opportunities
                    })
                else:
                    self.logger.warning("Revenue optimizer not available")
                
                monetization_results.append({
                    **result,
                    'ad_optimization': ad_optimization,
                    'affiliate_opportunities': affiliate_opportunities,
                    'email_campaign': email_campaign,
                    'revenue_optimization': revenue_optimization
                })
                
            except Exception as e:
                self.logger.error(f"Advanced monetization failed: {e}")
                monetization_results.append(result)
        
        return monetization_results
    
    async def run_predictive_analytics(self, monetization_results: List[Dict]) -> Dict:
        """Run predictive analytics on all content"""
        try:
            # Predict performance - handle both sync and async methods
            try:
                performance_predictions = await self.predictive_analytics.predict_content_performance(monetization_results)
            except TypeError:
                # Fallback for non-async method
                performance_predictions = self.predictive_analytics.predict_content_performance(monetization_results)
            
            # Retention predictions - handle both sync and async methods
            try:
                retention_predictions = await self.retention_analytics.predict_retention_metrics(monetization_results)
            except (TypeError, AttributeError):
                # Fallback implementation
                retention_predictions = {'status': 'fallback', 'predictions': []}
            
            return {
                'performance_predictions': performance_predictions,
                'retention_predictions': retention_predictions,
                'generated_at': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Predictive analytics failed: {e}")
            return {'status': 'failed', 'error': str(e)}


    async def run_daily_optimizations(self) -> Dict:
        """Run comprehensive daily optimizations"""
        try:
            # Ensure the method exists and is callable
            if hasattr(self.daily_optimizer, 'run_daily_optimizations'):
                result = self.daily_optimizer.run_daily_optimizations()
                # Handle both sync and async returns
                if hasattr(result, '__await__'):
                    return await result
                else:
                    return result
            else:
                # Fallback implementation
                return {
                    'status': 'fallback',
                    'optimizations_applied': 0,
                    'message': 'Daily optimizer method not available'
                }
        except Exception as e:
            self.logger.error(f"Daily optimizations failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    async def monitor_system_performance(self) -> Dict:
        """Monitor system performance"""
        try:
            return await self.performance_monitor.monitor_automation_cycle()
        except Exception as e:
            self.logger.error(f"Performance monitoring failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    async def update_enhanced_dashboard(self, all_metrics: Dict):
        """Update dashboard with all enhanced metrics"""
        try:
            # Check if dashboard_manager has the method, if not create a basic implementation
            if hasattr(self.dashboard_manager, 'update_enhanced_metrics'):
                await self.dashboard_manager.update_enhanced_metrics(all_metrics)
            else:
                # Basic dashboard update
                self.logger.info(f"📊 Dashboard updated with {len(all_metrics)} metric categories")
            
            # Check if metrics_tracker has the method
            if hasattr(self.metrics_tracker, 'track_enhanced_metrics'):
                await self.metrics_tracker.track_enhanced_metrics(all_metrics)
            else:
                # Basic metrics tracking
                self.logger.info(f"📈 Metrics tracked: {list(all_metrics.keys())}")
                
        except Exception as e:
            self.logger.error(f"Enhanced dashboard update failed: {e}")

    async def calculate_optimal_wait_time(self, cycle_duration: float) -> int:
        """Calculate optimal wait time between cycles with daily limits"""
        # Respect minimum interval from environment
        min_interval = int(os.getenv('MIN_UPLOAD_INTERVAL_HOURS', '6')) * 3600  # Convert to seconds
        
        # Adaptive wait time based on performance
        if cycle_duration < 60:  # Fast cycle
            base_wait = 1800  # 30 minutes minimum
        elif cycle_duration < 120:  # Normal cycle
            base_wait = 3600  # 1 hour
        else:  # Slow cycle
            base_wait = 7200  # 2 hours
        
        # Use the longer of base wait or minimum interval
        return max(base_wait, min_interval)
    
    async def generate_viral_content_now(self, urgency: str = 'maximum'):
        """Generate viral content using the master system"""
        self.logger.info(f"🚀 GENERATING VIRAL CONTENT - Urgency: {urgency}")
        
        try:
            # Use the viral master system
            viral_result = await self.content_pipeline.generate_ultimate_viral_content(urgency)
            
            if viral_result:
                self.logger.info(f"✅ Viral content generated!")
                self.logger.info(f"📊 Viral Score: {viral_result.get('viral_score', 0)}")
                self.logger.info(f"💰 Revenue Potential: ${viral_result.get('revenue_potential', 0):,.0f}")
                
                return viral_result
            else:
                self.logger.error("❌ Viral content generation failed")
                return {
                    'viral_score': 0,
                    'revenue_potential': 0,
                    'error': 'Viral content generation failed',
                    'status': 'failed'
                }
                
        except Exception as e:
            self.logger.error(f"Viral content generation error: {e}")
            return {
                'viral_score': 0,
                'revenue_potential': 0,
                'error': str(e),
                'status': 'error'
            }
    
    async def run_viral_mode(self):
        """Run the system in viral content generation mode"""
        self.logger.info("🔥 STARTING VIRAL MODE - Maximum Engagement Focus")
        
        while self.running:
            try:
                # Generate viral content every 2 hours
                viral_result = await self.generate_viral_content_now('maximum')
                
                if viral_result:
                    # Upload immediately for maximum viral potential
                    await self.upload_manager.upload_video_immediately(viral_result)
                
                # Wait 2 hours before next viral content
                await asyncio.sleep(7200)  # 2 hours
                
            except Exception as e:
                self.logger.error(f"Viral mode error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def trigger_enhanced_autoblog(self, content: Dict) -> Dict:
        """Enhanced autoblog with SEO optimization"""
        try:
            from distribution.blog_manager import BlogManager
            blog_manager = BlogManager()
            return await blog_manager.create_seo_optimized_blog(content)
        except Exception as e:
            self.logger.error(f"Enhanced autoblog failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    async def trigger_enhanced_pod(self, content: Dict) -> Dict:
        """Enhanced POD with design optimization"""
        try:
            from distribution.pod_manager import PODManager
            pod_manager = PODManager()
            return await pod_manager.create_optimized_pod_products(content)
        except Exception as e:
            self.logger.error(f"Enhanced POD failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def verify_channel_connection(self):
        """Verify which YouTube channel we're connected to before starting"""
        print("🔍 Verifying YouTube channel connection...")
        
        try:
            channel_info = self.channel_verifier.verify_connected_channel()
            
            if channel_info:
                channel_title = channel_info.get('snippet', {}).get('title', 'Unknown')
                channel_id = channel_info.get('id', 'Unknown')
                
                print(f"✅ Connected to: {channel_title} (ID: {channel_id})")
                
                # Store channel info for later use
                self.verified_channel_id = channel_id
                self.verified_channel_title = channel_title
                
                # Update agent manager with verified channel info (if available)
                if hasattr(self, 'agent_manager') and self.agent_manager:
                    self.agent_manager.update_channel_info(channel_id, channel_title)
                else:
                    self.logger.info("📝 Channel info stored for later agent manager update")
                    
                return True
            else:
                print("❌ Channel verification failed!")
                return False
        except Exception as e:
            self.logger.error(f"Channel verification error: {e}")
            print(f"❌ Channel verification failed: {e}")
            return False
    
    async def start(self):
        """Start the enhanced automation system with warm-up"""
        self.logger.info("🚀 Starting Enhanced MonAY YouTube Automation System...")
        
        # Initialize channel verifier first for early verification
        try:
            self.channel_verifier = ChannelVerifier()
            self.logger.info("✅ Channel verifier initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not initialize channel verifier: {e}")
            self.channel_verifier = None
        
        # Verify channel connection if verifier is available
        if self.channel_verifier and not self.verify_channel_connection():
            self.logger.warning("⚠️  Starting without verified channel connection")
        
        # Initialize the rest of the system
        if not await self.initialize_system():
            self.logger.error("❌ System initialization failed")
            return
        
        self.running = True
        
        # Start enhanced automation loop
        automation_task = asyncio.create_task(self.enhanced_automation_loop())
        
        # Start dashboard
        dashboard_task = asyncio.create_task(self.dashboard_manager.start_dashboard())
        
        try:
            await asyncio.gather(automation_task, dashboard_task)
        except KeyboardInterrupt:
            await self.shutdown()
        
        self.logger.info("✅ Enhanced system shutdown completed")
    
    async def shutdown(self):
        """Enhanced shutdown with state preservation"""
        self.logger.info("🛑 Initiating graceful shutdown...")
        self.running = False
        
        # Save current state
        try:
            state = {
                'last_cycle_time': datetime.now().isoformat(),
                'daily_counters': {
                    'content_generated': getattr(self, '_today_video_count', 0),
                    'uploads_completed': getattr(self, 'daily_upload_count', 0),
                    'revenue_optimized': getattr(self, 'daily_revenue_count', 0)
                },
                'error_count': getattr(self, 'error_count', 0),
                'component_status': await self.check_component_availability()
            }
            
            with open('system_state.json', 'w') as f:
                json.dump(state, f, indent=2)
            
            self.logger.info("💾 System state saved")
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
        
        try:
            # Cancel all running tasks
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
            if tasks:
                self.logger.info(f"🔄 Cancelling {len(tasks)} running tasks...")
                for task in tasks:
                    task.cancel()
                
                # Wait for tasks to complete cancellation
                await asyncio.gather(*tasks, return_exceptions=True)
            
            # Shutdown components gracefully
            if hasattr(self, 'dashboard_manager'):
                await self.dashboard_manager.shutdown()
            
            if hasattr(self, 'upload_manager'):
                await self.upload_manager.shutdown()
                
            self.logger.info("✅ Shutdown complete")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
    
    async def generate_weekly_content_schedule(self, trends: List[Dict]) -> List[Dict]:
        """Generate weekly content schedule with 2 long-form videos + shorts"""
        try:
            all_content = []
            
            # Generate 2 long-form videos per week
            for i in range(2):
                if i < len(trends):
                    trend = trends[i]
                    topic = trend.get('topic', f'trending topic {i+1}')
                else:
                    topic = f'finance education topic {i+1}'
                
                long_form_content = {
                    'id': f"longform_{datetime.now().strftime('%Y%m%d')}_{i}",
                    'topic': topic,
                    'type': 'long_form',
                    'title': f"Complete Guide to {topic}",
                    'description': f"Comprehensive tutorial about {topic}. Everything you need to know!",
                    'duration': 600,  # 10 minutes
                    'tags': [topic, 'tutorial', 'guide', 'finance', 'education'],
                    'content_type': 'educational',
                    'schedule_day': f'day_{i+1}',
                    'priority': 'high',
                    'viral_potential': trend.get('viral_score', 0.7) if i < len(trends) else 0.6
                }
                all_content.append(long_form_content)
            
            # Generate 5 shorts per week
            for i in range(5):
                if i < len(trends):
                    trend = trends[i]
                    topic = trend.get('topic', f'trending topic {i+1}')
                else:
                    topic = f'finance tip {i+1}'
                
                short_content = {
                    'id': f"short_{datetime.now().strftime('%Y%m%d')}_{i}",
                    'topic': topic,
                    'type': 'short',
                    'title': f"{topic} in 60 Seconds!",
                    'description': f"Quick tip about {topic}. #Shorts #Finance",
                    'duration': 60,  # 1 minute
                    'tags': [topic, 'shorts', 'quick', 'finance', 'tips'],
                    'content_type': 'educational',
                    'schedule_day': f'day_{i+1}',
                    'priority': 'medium',
                    'viral_potential': trend.get('viral_score', 0.8) if i < len(trends) else 0.7
                }
                all_content.append(short_content)
            
            self.logger.info(f"✅ Generated weekly schedule: {len(all_content)} content pieces")
            return all_content
            
        except Exception as e:
            self.logger.error(f"Weekly content schedule generation failed: {e}")
            # Return fallback content
            return [{
                'id': f"fallback_{datetime.now().strftime('%Y%m%d')}",
                'topic': 'financial education',
                'type': 'long_form',
                'title': 'Essential Financial Tips for Success',
                'description': 'Learn the fundamentals of financial success.',
                'duration': 300,
                'tags': ['finance', 'education', 'success'],
                'content_type': 'educational',
                'schedule_day': 'day_1',
                'priority': 'high',
                'viral_potential': 0.6
            }]
    
    async def generate_original_finance_content(self, niche: str = None) -> Dict:
        """Generate original finance content with AI visuals"""
        if not self.original_finance_generator:
            return {'status': 'error', 'message': 'Original finance generator not available'}
        
        try:
            # Generate content with AI visuals
            content_package = await self.original_finance_generator.generate_complete_content_package(niche)
            
            self.logger.info(f"Generated original finance content with AI visuals: {content_package['topic']}")
            return content_package
            
        except Exception as e:
            self.logger.error(f"Original finance content generation failed: {e}")
            return {'status': 'error', 'message': str(e)}

async def main():
    """Main entry point for the enhanced MonAY system"""
    orchestrator = None
    
    def signal_handler(signum, frame):
        print("\n🛑 Shutdown signal received...")
        if orchestrator:
            asyncio.create_task(orchestrator.shutdown())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        orchestrator = EnhancedMonAYOrchestrator()
        await orchestrator.start()
    except KeyboardInterrupt:
        print("\n🛑 Keyboard interrupt received")
        if orchestrator:
            await orchestrator.shutdown()
    except Exception as e:
        print(f"Fatal startup error: {e}")
        sys.exit(1)
    finally:
        print("\nShutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Application stopped")
    except Exception as e:
        print(f"Fatal startup error: {e}")
        sys.exit(1)