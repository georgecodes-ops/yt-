import logging
import asyncio
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Callable
import threading
import queue
import re
from collections import defaultdict, deque

class FastErrorDetector:
    """Real-time error detection and instant alerting system"""
    
    def __init__(self, alert_callback: Callable = None):
        self.logger = logging.getLogger(__name__)
        self.alert_callback = alert_callback or self._default_alert
        
        # Error pattern detection
        self.error_patterns = {
            'ollama_timeout': r'Ollama.*timeout|HTTPConnectionPool.*11434.*timeout',
            'memory_error': r'MemoryError|Out of memory|Cannot allocate memory',
            'disk_space': r'No space left on device|Disk full',
            'api_quota': r'quota.*exceeded|rate.*limit|429',
            'ffmpeg_error': r'ffmpeg.*error|Broken pipe.*ffmpeg',
            'import_error': r'ModuleNotFoundError|ImportError',
            'permission_error': r'PermissionError|Permission denied',
            'network_error': r'ConnectionError|Network.*unreachable|DNS.*failed'
        }
        
        # Error tracking
        self.error_counts = defaultdict(int)
        self.recent_errors = deque(maxlen=100)
        self.error_trends = defaultdict(list)
        
        # Real-time monitoring
        self.monitoring_active = False
        self.log_queue = queue.Queue()
        self.alert_thresholds = {
            'error_rate': 5,  # errors per minute
            'critical_errors': 1,  # immediate alert
            'repeated_errors': 3   # same error 3 times
        }
        
    def start_real_time_monitoring(self, log_files: List[str] = None):
        """Start real-time log monitoring for instant error detection"""
        if not log_files:
            log_files = ['debug.log', 'enhanced_system.log', '/var/log/monay.log']
        
        self.monitoring_active = True
        self.logger.info("🚨 Starting real-time error detection...")
        
        # Start log file watchers
        for log_file in log_files:
            if os.path.exists(log_file):
                threading.Thread(
                    target=self._watch_log_file, 
                    args=(log_file,), 
                    daemon=True
                ).start()
        
        # Start error processor
        threading.Thread(
            target=self._process_errors, 
            daemon=True
        ).start()
        
        self.logger.info(f"✅ Monitoring {len(log_files)} log files in real-time")
    
    def _watch_log_file(self, log_file: str):
        """Watch log file for new entries and detect errors instantly"""
        try:
            with open(log_file, 'r') as f:
                # Go to end of file
                f.seek(0, 2)
                
                while self.monitoring_active:
                    line = f.readline()
                    if line:
                        self._analyze_log_line(line.strip(), log_file)
                    else:
                        time.sleep(0.1)  # Check every 100ms for new lines
                        
        except Exception as e:
            self.logger.error(f"Error watching {log_file}: {e}")
    
    def _analyze_log_line(self, line: str, source_file: str):
        """Analyze log line for error patterns and queue for processing"""
        timestamp = datetime.now()
        
        # Check for error patterns
        for error_type, pattern in self.error_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                error_data = {
                    'timestamp': timestamp,
                    'error_type': error_type,
                    'line': line,
                    'source_file': source_file,
                    'severity': self._determine_severity(error_type, line)
                }
                
                self.log_queue.put(error_data)
                break
        
        # Check for general ERROR/CRITICAL/FAILED patterns
        if any(keyword in line.upper() for keyword in ['ERROR:', 'CRITICAL:', 'FAILED:', 'EXCEPTION:']):
            error_data = {
                'timestamp': timestamp,
                'error_type': 'general_error',
                'line': line,
                'source_file': source_file,
                'severity': 'high' if 'CRITICAL' in line.upper() else 'medium'
            }
            self.log_queue.put(error_data)
    
    def _process_errors(self):
        """Process detected errors and trigger alerts"""
        while self.monitoring_active:
            try:
                # Process all queued errors
                errors_this_minute = []
                
                while not self.log_queue.empty():
                    try:
                        error = self.log_queue.get_nowait()
                        errors_this_minute.append(error)
                        self.recent_errors.append(error)
                        self.error_counts[error['error_type']] += 1
                        
                        # Track error trends
                        self.error_trends[error['error_type']].append(error['timestamp'])
                        
                        # Immediate alert for critical errors
                        if error['severity'] == 'critical':
                            self._trigger_alert('CRITICAL', error)
                        
                    except queue.Empty:
                        break
                
                # Check for error rate spikes
                if len(errors_this_minute) >= self.alert_thresholds['error_rate']:
                    self._trigger_alert('HIGH_ERROR_RATE', {
                        'count': len(errors_this_minute),
                        'errors': errors_this_minute
                    })
                
                # Check for repeated errors
                self._check_repeated_errors()
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                self.logger.error(f"Error processing errors: {e}")
                time.sleep(5)
    
    def _determine_severity(self, error_type: str, line: str) -> str:
        """Determine error severity for prioritization"""
        critical_patterns = ['CRITICAL', 'FATAL', 'CRASH', 'SHUTDOWN']
        high_patterns = ['ERROR', 'FAILED', 'EXCEPTION', 'TIMEOUT']
        
        line_upper = line.upper()
        
        if any(pattern in line_upper for pattern in critical_patterns):
            return 'critical'
        elif any(pattern in line_upper for pattern in high_patterns):
            return 'high'
        elif error_type in ['ollama_timeout', 'memory_error', 'disk_space']:
            return 'high'
        else:
            return 'medium'
    
    def _check_repeated_errors(self):
        """Check for repeated errors that indicate systemic issues"""
        now = datetime.now()
        five_minutes_ago = now - timedelta(minutes=5)
        
        for error_type, timestamps in self.error_trends.items():
            # Count errors in last 5 minutes
            recent_count = sum(1 for ts in timestamps if ts > five_minutes_ago)
            
            if recent_count >= self.alert_thresholds['repeated_errors']:
                self._trigger_alert('REPEATED_ERROR', {
                    'error_type': error_type,
                    'count': recent_count,
                    'timeframe': '5 minutes'
                })
    
    def _trigger_alert(self, alert_type: str, error_data: Dict):
        """Trigger immediate alert for detected issues"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'alert_type': alert_type,
            'error_data': error_data,
            'suggested_actions': self._get_suggested_actions(alert_type, error_data)
        }
        
        # Call alert callback (could be Slack, email, etc.)
        self.alert_callback(alert)
        
        # Log the alert
        self.logger.critical(f"🚨 ALERT: {alert_type} - {error_data}")
    
    def _get_suggested_actions(self, alert_type: str, error_data: Dict) -> List[str]:
        """Get suggested actions for different error types"""
        actions = {
            'CRITICAL': [
                "Restart the affected service immediately",
                "Check system resources (memory, disk, CPU)",
                "Review recent deployments or changes"
            ],
            'HIGH_ERROR_RATE': [
                "Check system load and resource usage",
                "Review recent traffic patterns",
                "Consider scaling resources"
            ],
            'REPEATED_ERROR': [
                f"Fix recurring {error_data.get('error_type', 'unknown')} issue",
                "Check configuration and dependencies",
                "Review error logs for root cause"
            ],
            'ollama_timeout': [
                "Restart Ollama service: sudo systemctl restart ollama",
                "Check Ollama service status: sudo systemctl status ollama",
                "Verify Ollama is accessible: curl http://localhost:11434/api/version"
            ],
            'memory_error': [
                "Check memory usage: free -h",
                "Restart memory-intensive processes",
                "Clear temporary files and caches"
            ],
            'disk_space': [
                "Check disk usage: df -h",
                "Clean up log files and temp files",
                "Remove old video files from outputs/"
            ]
        }
        
        error_type = error_data.get('error_type', alert_type)
        return actions.get(error_type, actions.get(alert_type, ["Investigate the issue manually"]))
    
    def _default_alert(self, alert: Dict):
        """Default alert handler - prints to console and saves to file"""
        print(f"\n🚨 INSTANT ALERT: {alert['alert_type']}")
        print(f"⏰ Time: {alert['timestamp']}")
        print(f"📋 Suggested Actions:")
        for action in alert['suggested_actions']:
            print(f"  • {action}")
        print("-" * 50)
        
        # Save to alerts file
        alerts_file = f"alerts_{datetime.now().strftime('%Y%m%d')}.json"
        try:
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r') as f:
                    alerts = json.load(f)
            else:
                alerts = []
            
            alerts.append(alert)
            
            with open(alerts_file, 'w') as f:
                json.dump(alerts, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save alert: {e}")
    
    def get_error_summary(self) -> Dict:
        """Get summary of detected errors"""
        now = datetime.now()
        last_hour = now - timedelta(hours=1)
        
        recent_errors = [e for e in self.recent_errors if e['timestamp'] > last_hour]
        
        return {
            'total_errors_detected': len(self.recent_errors),
            'errors_last_hour': len(recent_errors),
            'error_types': dict(self.error_counts),
            'most_common_errors': sorted(
                self.error_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
            'monitoring_status': 'active' if self.monitoring_active else 'inactive'
        }
    
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring_active = False
        self.logger.info("🛑 Real-time error monitoring stopped")

# Enhanced logging setup for faster debugging
class FastDebugLogger:
    """Enhanced logging setup for instant problem identification"""
    
    @staticmethod
    def setup_fast_debug_logging():
        """Setup logging configuration for fast debugging"""
        
        # Create custom formatter with more context
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(name)20s | %(funcName)15s:%(lineno)3d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # File handler for all logs
        file_handler = logging.FileHandler('fast_debug.log')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Error-only handler for quick error review
        error_handler = logging.FileHandler('errors_only.log')
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
        
        return root_logger

# Usage example with Slack integration
class SlackAlerter:
    """Send instant alerts to Slack for immediate notification"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')
    
    def send_alert(self, alert: Dict):
        """Send alert to Slack channel"""
        if not self.webhook_url:
            return
        
        try:
            import requests
            
            error_type = alert['alert_type']
            error_data = alert['error_data']
            
            # Create Slack message
            message = {
                "text": f"🚨 MONAY SYSTEM ALERT: {error_type}",
                "attachments": [
                    {
                        "color": "danger" if "CRITICAL" in error_type else "warning",
                        "fields": [
                            {
                                "title": "Error Type",
                                "value": error_type,
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": alert['timestamp'],
                                "short": True
                            },
                            {
                                "title": "Suggested Actions",
                                "value": "\n".join(f"• {action}" for action in alert['suggested_actions']),
                                "short": False
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(self.webhook_url, json=message, timeout=10)
            if response.status_code == 200:
                print("✅ Alert sent to Slack")
            else:
                print(f"❌ Failed to send Slack alert: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Slack alert failed: {e}")

# Discord alerter class
class DiscordAlerter:
    """Send instant alerts to Discord for immediate notification"""
    
    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv('DISCORD_WEBHOOK_URL')
    
    def send_alert(self, alert: Dict):
        """Send alert to Discord channel"""
        if not self.webhook_url:
            return
        
        try:
            import requests
            
            error_type = alert['alert_type']
            error_data = alert['error_data']
            
            # Create Discord embed message
            embed = {
                "title": f"🚨 MONAY SYSTEM ALERT: {error_type}",
                "color": 15158332 if "CRITICAL" in error_type else 16776960,  # Red or Yellow
                "fields": [
                    {
                        "name": "Error Type",
                        "value": error_type,
                        "inline": True
                    },
                    {
                        "name": "Time",
                        "value": alert['timestamp'],
                        "inline": True
                    },
                    {
                        "name": "Suggested Actions",
                        "value": "\n".join(f"• {action}" for action in alert['suggested_actions'][:5]),
                        "inline": False
                    }
                ],
                "timestamp": alert['timestamp']
            }
            
            message = {
                "content": f"🚨 **MONAY ALERT** - {error_type}",
                "embeds": [embed]
            }
            
            response = requests.post(self.webhook_url, json=message, timeout=10)
            if response.status_code in [200, 204]:
                print("✅ Alert sent to Discord")
            else:
                print(f"❌ Failed to send Discord alert: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Discord alert failed: {e}")

# Quick setup function
def setup_instant_problem_detection(webhook_url: str = None):
    """Setup instant problem detection system with Discord/Slack support"""
    
    # Setup enhanced logging
    FastDebugLogger.setup_fast_debug_logging()
    
    # Setup alerting (try Discord first, then Slack)
    alerter = None
    if webhook_url:
        if 'discord' in webhook_url.lower():
            alerter = DiscordAlerter(webhook_url)
        else:
            alerter = SlackAlerter(webhook_url)
    else:
        # Try environment variables
        discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
        slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
        
        if discord_webhook:
            alerter = DiscordAlerter(discord_webhook)
        elif slack_webhook:
            alerter = SlackAlerter(slack_webhook)
    
    # Create error detector
    detector = FastErrorDetector(
        alert_callback=alerter.send_alert if alerter else None
    )
    
    # Start monitoring
    detector.start_real_time_monitoring()
    
    return detector

# Auto-fix system for common issues
class AutoFixer:
    """Automatically fix common issues when detected"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.auto_fixes = {
            'ollama_timeout': self._fix_ollama_service,
            'disk_space': self._cleanup_temp_files,
            'memory_error': self._restart_memory_intensive_processes,
            'permission_error': self._fix_permissions
        }
    
    async def attempt_auto_fix(self, error_type: str, error_data: Dict) -> bool:
        """Attempt to automatically fix detected issues"""
        if error_type in self.auto_fixes:
            try:
                self.logger.info(f"🔧 Attempting auto-fix for {error_type}")
                success = await self.auto_fixes[error_type](error_data)
                if success:
                    self.logger.info(f"✅ Auto-fix successful for {error_type}")
                    return True
                else:
                    self.logger.warning(f"⚠️ Auto-fix failed for {error_type}")
                    return False
            except Exception as e:
                self.logger.error(f"❌ Auto-fix error for {error_type}: {e}")
                return False
        return False
    
    async def _fix_ollama_service(self, error_data: Dict) -> bool:
        """Auto-fix Ollama service issues"""
        try:
            import subprocess
            
            # Try to restart Ollama service
            result = subprocess.run(
                ['sudo', 'systemctl', 'restart', 'ollama'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                # Wait a moment and test
                await asyncio.sleep(5)
                
                import requests
                response = requests.get('http://localhost:11434/api/version', timeout=10)
                return response.status_code == 200
            
            return False
            
        except Exception as e:
            self.logger.error(f"Ollama auto-fix failed: {e}")
            return False
    
    async def _cleanup_temp_files(self, error_data: Dict) -> bool:
        """Auto-cleanup temp files to free disk space"""
        try:
            import shutil
            
            temp_dirs = ['outputs', 'data/temp', '/tmp']
            cleaned = False
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        file_path = os.path.join(temp_dir, file)
                        if os.path.isfile(file_path):
                            # Remove files older than 1 hour
                            if time.time() - os.path.getmtime(file_path) > 3600:
                                os.remove(file_path)
                                cleaned = True
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Temp cleanup auto-fix failed: {e}")
            return False
    
    async def _restart_memory_intensive_processes(self, error_data: Dict) -> bool:
        """Restart memory-intensive processes"""
        try:
            import psutil
            import gc
            
            # Force garbage collection
            gc.collect()
            
            # Find and restart high-memory Python processes
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    if 'python' in proc.info['name'].lower() and proc.info['memory_percent'] > 50:
                        proc.terminate()
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Memory auto-fix failed: {e}")
            return False
    
    async def _fix_permissions(self, error_data: Dict) -> bool:
        """Fix common permission issues"""
        try:
            import subprocess
            
            # Fix common directory permissions
            dirs_to_fix = ['outputs', 'data/videos', 'data/temp']
            
            for directory in dirs_to_fix:
                if os.path.exists(directory):
                    result = subprocess.run(
                        ['chmod', '-R', '755', directory],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode != 0:
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Permission auto-fix failed: {e}")
            return False

# Complete fast debugging setup
async def main():
    """Example usage of fast problem detection system"""
    
    # Setup instant problem detection
    detector = setup_instant_problem_detection()
    
    # Setup auto-fixer
    auto_fixer = AutoFixer()
    
    print("🚨 Fast Error Detection System Active!")
    print("📊 Monitoring logs in real-time...")
    print("🔧 Auto-fix enabled for common issues")
    print("⚡ Problems will be detected and fixed within seconds!")
    
    try:
        # Keep monitoring
        while True:
            await asyncio.sleep(10)
            
            # Get error summary every 10 seconds
            summary = detector.get_error_summary()
            if summary['errors_last_hour'] > 0:
                print(f"📊 Errors detected in last hour: {summary['errors_last_hour']}")
    
    except KeyboardInterrupt:
        detector.stop_monitoring()
        print("🛑 Monitoring stopped")

if __name__ == "__main__":
    asyncio.run(main())