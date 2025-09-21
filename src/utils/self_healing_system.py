import asyncio
import logging
import time
import subprocess
import os
import sys
import psutil
import requests
from typing import Dict, List, Callable
from datetime import datetime, timedelta
import threading
import json

class SelfHealingSystem:
    """Automatically detects issues and fixes them to keep functions working"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.healing_active = True
        self.healing_history = []
        self.service_monitors = {}
        
        # Auto-healing strategies
        self.healing_strategies = {
            'ollama_down': self._heal_ollama_service,
            'high_memory': self._heal_memory_issues,
            'disk_full': self._heal_disk_space,
            'api_timeout': self._heal_api_timeouts,
            'process_crash': self._heal_crashed_processes,
            'network_issues': self._heal_network_problems
        }
        
        # Service health thresholds
        self.health_thresholds = {
            'memory_percent': 90,
            'disk_percent': 95,
            'cpu_percent': 95,
            'response_time': 30,  # seconds
            'error_rate': 10      # errors per minute
        }
    
    async def start_self_healing(self):
        """Start the self-healing monitoring system"""
        self.logger.info("🔄 Starting self-healing system...")
        
        # Start continuous monitoring
        asyncio.create_task(self._monitor_system_health())
        asyncio.create_task(self._monitor_ollama_service())
        asyncio.create_task(self._monitor_content_generation())
        asyncio.create_task(self._monitor_video_processing())
        
        self.logger.info("✅ Self-healing system active - will auto-fix issues")
    
    async def _monitor_system_health(self):
        """Continuously monitor system health and auto-heal"""
        while self.healing_active:
            try:
                # Check memory usage
                memory = psutil.virtual_memory()
                if memory.percent > self.health_thresholds['memory_percent']:
                    await self._heal_memory_issues()
                
                # Check disk space
                disk = psutil.disk_usage('/')
                disk_percent = (disk.used / disk.total) * 100
                if disk_percent > self.health_thresholds['disk_percent']:
                    await self._heal_disk_space()
                
                # Check CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                if cpu_percent > self.health_thresholds['cpu_percent']:
                    await self._heal_cpu_overload()
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"System health monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def _monitor_ollama_service(self):
        """Monitor Ollama service and auto-restart if needed"""
        consecutive_failures = 0
        
        while self.healing_active:
            try:
                # Test Ollama health
                response = requests.get('http://localhost:11434/api/version', timeout=10)
                
                if response.status_code == 200:
                    consecutive_failures = 0
                    self.service_monitors['ollama'] = {
                        'status': 'healthy',
                        'last_check': datetime.now(),
                        'version': response.json().get('version', 'unknown')
                    }
                else:
                    consecutive_failures += 1
                    
            except Exception as e:
                consecutive_failures += 1
                self.logger.warning(f"Ollama health check failed: {e}")
            
            # Auto-heal if multiple failures
            if consecutive_failures >= 3:
                self.logger.warning("🔄 Ollama service failing - attempting auto-heal...")
                success = await self._heal_ollama_service()
                if success:
                    consecutive_failures = 0
                else:
                    consecutive_failures = 1  # Reset but keep monitoring
            
            await asyncio.sleep(60)  # Check every minute
    
    async def _monitor_content_generation(self):
        """Monitor content generation pipeline and auto-fix issues"""
        while self.healing_active:
            try:
                # Check if content generation is working
                from src.content.instant_viral_generator import InstantViralGenerator
                
                # Test basic functionality
                generator = InstantViralGenerator()
                topics = await generator.get_fresh_topics()
                
                if not topics or len(topics) == 0:
                    self.logger.warning("🔄 Content generation failing - attempting auto-heal...")
                    await self._heal_content_generation()
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                self.logger.error(f"Content generation monitoring error: {e}")
                await self._heal_content_generation()
                await asyncio.sleep(300)
    
    async def _monitor_video_processing(self):
        """Monitor video processing and auto-fix TTS/video issues"""
        while self.healing_active:
            try:
                # Test TTS generation
                from src.content.tts_generator import TTSGenerator
                
                tts = TTSGenerator()
                if tts.tts_engine == "none":
                    self.logger.warning("🔄 TTS engine not available - attempting auto-heal...")
                    await self._heal_tts_engine()
                
                await asyncio.sleep(600)  # Check every 10 minutes
                
            except Exception as e:
                self.logger.error(f"Video processing monitoring error: {e}")
                await asyncio.sleep(600)
    
    async def _heal_ollama_service(self) -> bool:
        """Auto-heal Ollama service issues"""
        try:
            self.logger.info("🔧 Healing Ollama service...")
            
            # Try to restart Ollama service
            restart_commands = [
                ['sudo', 'systemctl', 'restart', 'ollama'],
                ['systemctl', '--user', 'restart', 'ollama'],
                ['pkill', '-f', 'ollama'],  # Force kill if needed
            ]
            
            for cmd in restart_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        self.logger.info(f"✅ Ollama restart successful with: {' '.join(cmd)}")
                        break
                except:
                    continue
            
            # Wait and test
            await asyncio.sleep(10)
            
            # Verify service is working
            response = requests.get('http://localhost:11434/api/version', timeout=15)
            if response.status_code == 200:
                self._log_healing_action('ollama_service', 'restart', True)
                self.logger.info("✅ Ollama service healed successfully")
                return True
            
            self._log_healing_action('ollama_service', 'restart', False)
            return False
            
        except Exception as e:
            self.logger.error(f"Ollama healing failed: {e}")
            self._log_healing_action('ollama_service', 'restart', False, str(e))
            return False
    
    async def _heal_memory_issues(self) -> bool:
        """Auto-heal memory issues"""
        try:
            self.logger.info("🔧 Healing memory issues...")
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Find and restart high-memory Python processes
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    if ('python' in proc.info['name'].lower() and 
                        proc.info['memory_percent'] > 50 and
                        proc.pid != os.getpid()):  # Don't kill ourselves
                        
                        self.logger.info(f"🔄 Restarting high-memory process: {proc.info['name']}")
                        proc.terminate()
                        
                except:
                    continue
            
            # Clear temp files
            await self._cleanup_temp_files()
            
            self._log_healing_action('memory', 'cleanup_and_restart', True)
            return True
            
        except Exception as e:
            self.logger.error(f"Memory healing failed: {e}")
            self._log_healing_action('memory', 'cleanup_and_restart', False, str(e))
            return False
    
    async def _heal_disk_space(self) -> bool:
        """Auto-heal disk space issues"""
        try:
            self.logger.info("🔧 Healing disk space issues...")
            
            freed_space = 0
            
            # Clean temp directories
            temp_dirs = ['outputs', 'data/temp', 'data/videos', '/tmp']
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        try:
                            if os.path.isfile(file_path):
                                # Remove files older than 2 hours
                                if time.time() - os.path.getmtime(file_path) > 7200:
                                    size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    freed_space += size
                        except:
                            continue
            
            # Clean large log files
            log_files = ['debug.log', 'enhanced_system.log', 'fast_debug.log']
            for log_file in log_files:
                if os.path.exists(log_file):
                    size = os.path.getsize(log_file)
                    if size > 100 * 1024 * 1024:  # > 100MB
                        # Keep last 1000 lines
                        with open(log_file, 'r') as f:
                            lines = f.readlines()
                        
                        with open(log_file, 'w') as f:
                            f.writelines(lines[-1000:])
                        
                        freed_space += size - os.path.getsize(log_file)
            
            freed_mb = freed_space / (1024 * 1024)
            self.logger.info(f"✅ Freed {freed_mb:.1f}MB of disk space")
            
            self._log_healing_action('disk_space', 'cleanup', True, f"Freed {freed_mb:.1f}MB")
            return freed_mb > 0
            
        except Exception as e:
            self.logger.error(f"Disk space healing failed: {e}")
            self._log_healing_action('disk_space', 'cleanup', False, str(e))
            return False
    
    async def _heal_content_generation(self) -> bool:
        """Auto-heal content generation issues"""
        try:
            self.logger.info("🔧 Healing content generation...")
            
            # Restart news aggregator
            try:
                from src.content.news_aggregator import NewsAggregator
                # Reinitialize news aggregator
                news_agg = NewsAggregator()
                await news_agg.initialize()
            except:
                pass
            
            # Test and fix viral growth engine
            try:
                from src.growth.viral_growth_engine import ViralGrowthEngine
                growth_engine = ViralGrowthEngine()
                await growth_engine.initialize()
            except:
                pass
            
            self._log_healing_action('content_generation', 'restart_components', True)
            return True
            
        except Exception as e:
            self.logger.error(f"Content generation healing failed: {e}")
            self._log_healing_action('content_generation', 'restart_components', False, str(e))
            return False
    
    async def _heal_tts_engine(self) -> bool:
        """Auto-heal TTS engine issues"""
        try:
            self.logger.info("🔧 Healing TTS engine...")
            
            # Try to install missing TTS packages
            tts_packages = ['gtts', 'edge-tts', 'pyttsx3']
            
            for package in tts_packages:
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'install', package],
                        capture_output=True, text=True, timeout=60
                    )
                    if result.returncode == 0:
                        self.logger.info(f"✅ Installed TTS package: {package}")
                        break
                except:
                    continue
            
            self._log_healing_action('tts_engine', 'install_packages', True)
            return True
            
        except Exception as e:
            self.logger.error(f"TTS healing failed: {e}")
            self._log_healing_action('tts_engine', 'install_packages', False, str(e))
            return False
    
    async def _heal_cpu_overload(self) -> bool:
        """Auto-heal CPU overload issues"""
        try:
            self.logger.info("🔧 Healing CPU overload...")
            
            # Find CPU-intensive processes and lower their priority
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if (proc.info['cpu_percent'] > 80 and 
                        'python' in proc.info['name'].lower() and
                        proc.pid != os.getpid()):
                        
                        # Lower process priority
                        process = psutil.Process(proc.pid)
                        process.nice(10)  # Lower priority
                        self.logger.info(f"🔄 Lowered priority for: {proc.info['name']}")
                        
                except:
                    continue
            
            self._log_healing_action('cpu_overload', 'lower_priority', True)
            return True
            
        except Exception as e:
            self.logger.error(f"CPU healing failed: {e}")
            return False
    
    async def _cleanup_temp_files(self) -> int:
        """Cleanup temporary files and return bytes freed"""
        freed_bytes = 0
        
        temp_patterns = [
            'outputs/*.tmp',
            'data/temp/*',
            '*.pyc',
            '__pycache__/*'
        ]
        
        for pattern in temp_patterns:
            try:
                import glob
                for file_path in glob.glob(pattern, recursive=True):
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        os.remove(file_path)
                        freed_bytes += size
            except:
                continue
        
        return freed_bytes
    
    def _log_healing_action(self, issue_type: str, action: str, success: bool, details: str = ""):
        """Log healing actions for tracking"""
        healing_record = {
            'timestamp': datetime.now().isoformat(),
            'issue_type': issue_type,
            'action': action,
            'success': success,
            'details': details
        }
        
        self.healing_history.append(healing_record)
        
        # Save to file
        try:
            healing_file = f"monitoring/healing_log_{datetime.now().strftime('%Y%m%d')}.json"
            
            if os.path.exists(healing_file):
                with open(healing_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            history.append(healing_record)
            
            with open(healing_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to log healing action: {e}")
    
    async def emergency_restart_all_services(self):
        """Emergency restart of all critical services"""
        self.logger.critical("🚨 EMERGENCY: Restarting all services...")
        
        services = ['ollama', 'monay']
        restart_success = []
        
        for service in services:
            try:
                result = subprocess.run(
                    ['sudo', 'systemctl', 'restart', service],
                    capture_output=True, text=True, timeout=30
                )
                restart_success.append(result.returncode == 0)
                
            except Exception as e:
                self.logger.error(f"Failed to restart {service}: {e}")
                restart_success.append(False)
        
        if any(restart_success):
            self.logger.info("✅ Emergency restart partially successful")
            return True
        else:
            self.logger.critical("❌ Emergency restart failed")
            return False
    
    def get_healing_status(self) -> Dict:
        """Get current healing system status"""
        recent_actions = [
            action for action in self.healing_history 
            if datetime.fromisoformat(action['timestamp']) > datetime.now() - timedelta(hours=1)
        ]
        
        return {
            'healing_active': self.healing_active,
            'total_healing_actions': len(self.healing_history),
            'recent_actions': len(recent_actions),
            'success_rate': sum(1 for a in recent_actions if a['success']) / max(len(recent_actions), 1),
            'service_status': self.service_monitors,
            'last_healing': self.healing_history[-1] if self.healing_history else None
        }

class AutoRecoveryWrapper:
    """Wrapper that adds auto-recovery to any function"""
    
    def __init__(self, healing_system: SelfHealingSystem):
        self.healing_system = healing_system
        self.logger = logging.getLogger(__name__)
    
    def auto_recover(self, max_retries: int = 3, recovery_delay: float = 5.0):
        """Decorator that adds auto-recovery to functions"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                        
                    except Exception as e:
                        last_exception = e
                        self.logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}): {e}")
                        
                        if attempt < max_retries:
                            # Try to heal the issue
                            await self._attempt_healing(e, func.__name__)
                            
                            # Wait before retry
                            await asyncio.sleep(recovery_delay)
                        else:
                            # Final attempt failed
                            self.logger.error(f"Function {func.__name__} failed after {max_retries} retries")
                            raise last_exception
                
                return None
            
            return wrapper
        return decorator
    
    async def _attempt_healing(self, exception: Exception, function_name: str):
        """Attempt to heal based on exception type"""
        exc_type = type(exception).__name__
        exc_message = str(exception)
        
        # Determine healing strategy
        if 'ollama' in exc_message.lower() or 'connection' in exc_message.lower():
            await self.healing_system._heal_ollama_service()
        elif 'memory' in exc_message.lower():
            await self.healing_system._heal_memory_issues()
        elif 'disk' in exc_message.lower() or 'space' in exc_message.lower():
            await self.healing_system._heal_disk_space()
        elif 'timeout' in exc_message.lower():
            # Generic timeout healing
            await asyncio.sleep(2)  # Brief pause
        
        self.logger.info(f"🔄 Attempted healing for {function_name} after {exc_type}")

# Integration with main system
def integrate_self_healing_with_main():
    """Integrate self-healing with main system components"""
    
    integration_code = '''
# Add to enhanced_main.py or main startup file

import asyncio
from src.utils.self_healing_system import SelfHealingSystem, AutoRecoveryWrapper

# Initialize self-healing system
healing_system = SelfHealingSystem()
recovery_wrapper = AutoRecoveryWrapper(healing_system)

# Start self-healing in background
asyncio.create_task(healing_system.start_self_healing())

# Wrap critical functions with auto-recovery
@recovery_wrapper.auto_recover(max_retries=3, recovery_delay=5.0)
async def generate_content_with_recovery(*args, **kwargs):
    """Content generation with auto-recovery"""
    # Your existing content generation code here
    pass

@recovery_wrapper.auto_recover(max_retries=2, recovery_delay=10.0)
async def process_video_with_recovery(*args, **kwargs):
    """Video processing with auto-recovery"""
    # Your existing video processing code here
    pass

# Use these wrapped functions instead of original ones
'''
    
    with open('monitoring/self_healing_integration.py', 'w') as f:
        f.write(integration_code)
    
    print("🔧 Self-healing integration code created")

# Quick setup function
async def setup_complete_self_healing():
    """Setup complete self-healing system"""
    
    print("🔄 Setting up complete self-healing system...")
    
    # Create healing system
    healing_system = SelfHealingSystem()
    
    # Start self-healing
    await healing_system.start_self_healing()
    
    # Create recovery wrapper
    recovery_wrapper = AutoRecoveryWrapper(healing_system)
    
    print("✅ Self-healing system fully active!")
    print("🤖 Functions will auto-recover from failures")
    print("🔄 Services will auto-restart when needed")
    print("💾 Memory and disk will auto-cleanup")
    
    return healing_system, recovery_wrapper

# Usage example
if __name__ == "__main__":
    async def main():
        healing_system, recovery_wrapper = await setup_complete_self_healing()
        
        # Keep running and show status
        while True:
            await asyncio.sleep(60)
            status = healing_system.get_healing_status()
            print(f"🔄 Healing Status: {status['recent_actions']} actions in last hour")
    
    asyncio.run(main())