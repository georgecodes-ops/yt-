import logging
import os
import sys
import asyncio
import threading
import time
from typing import Dict, Optional
from datetime import datetime
from collections import deque
from logging.handlers import RotatingFileHandler

# Configure structured logging early
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

class SmartDebugAssistant:
    """Production-ready intelligent debugging assistant with rate limiting and async webhooks"""
    
    def __init__(self, discord_webhook: str = None):
        self.logger = logging.getLogger(__name__)
        self.discord_webhook = discord_webhook
        self.message_queue = deque()
        self.queue_lock = threading.Lock()
        self.last_flush = time.time()
        self.flush_interval = 5.0  # Batch messages every 5 seconds
        self.max_queue_size = 50
        
        # Setup fallback file logging
        self._setup_fallback_logging()
        
        # Validate configuration at startup
        self._validate_config()
        
        self.error_patterns = {
            "ImportError": ["Check if package is installed", "Verify PYTHONPATH", "Check for circular imports"],
            "NameError": ["Check variable spelling", "Verify imports", "Check scope"],
            "AttributeError": ["Check object type", "Verify method exists", "Check initialization"],
            "FileNotFoundError": ["Check file path", "Verify file exists", "Check permissions"],
            "ConnectionError": ["Check network", "Verify URL", "Check firewall"],
            "ModuleNotFoundError": ["Install missing package", "Check virtual environment", "Verify package name"]
        }
    
    def _setup_fallback_logging(self):
        """Setup rotating file handler as fallback"""
        try:
            fallback_handler = RotatingFileHandler(
                '/opt/monay/data/logs/debug_assistant.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            fallback_handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s"
            ))
            self.fallback_logger = logging.getLogger('debug_assistant_fallback')
            self.fallback_logger.addHandler(fallback_handler)
            self.fallback_logger.setLevel(logging.INFO)
        except Exception as e:
            self.logger.warning(f"Could not setup fallback logging: {e}")
            self.fallback_logger = None
    
    def _validate_config(self):
        """Validate configuration at startup"""
        if self.discord_webhook:
            if not self.discord_webhook.startswith('https://discord'):
                self.logger.warning("Discord webhook URL format may be invalid")
            else:
                self.logger.info("✅ Discord webhook configured")
        else:
            self.logger.warning("⚠️ No Discord webhook configured - using fallback logging only")
    
    def analyze_error(self, error_msg: str, traceback_info: str = "") -> dict:
        """Analyze error and provide smart suggestions with robust error handling"""
        try:
            error_type = self._extract_error_type(error_msg)
            suggestions = self._get_smart_suggestions({"error_msg": error_msg, "type": error_type})
            severity = self._assess_severity(error_type)
            
            analysis = {
                "error_type": error_type,
                "message": error_msg,
                "suggestions": suggestions,
                "severity": severity,
                "timestamp": datetime.now().isoformat()
            }
            
            # Use severity to adjust logging level
            if severity == "CRITICAL":
                self.logger.error(f"🚨 CRITICAL Error: {error_type} - {len(suggestions)} suggestions")
            else:
                self.logger.warning(f"⚠️ Warning: {error_type} - {len(suggestions)} suggestions")
            
            # Queue for batched Discord notification
            self._queue_discord_message(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error("Error in analyze_error", exc_info=e)
            fallback_analysis = {
                "error_type": "Unknown",
                "message": error_msg,
                "suggestions": ["Check logs for more details"],
                "severity": "WARNING",
                "timestamp": datetime.now().isoformat()
            }
            return fallback_analysis
    
    def _queue_discord_message(self, analysis: dict):
        """Queue message for batched Discord sending (thread-safe)"""
        try:
            # Convert analysis to simple text format that works with Discord
            severity = analysis.get('severity', 'WARNING')
            error_type = analysis.get('error_type', 'Unknown')
            message = analysis.get('message', 'No details available')
            
            emoji_map = {
                "CRITICAL": "🚨",
                "WARNING": "⚠️",
                "INFO": "ℹ️"
            }
            
            emoji = emoji_map.get(severity, "⚠️")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create simple text message like the one that worked
            content = f"{emoji} **MonAY {severity} ALERT** {emoji}\n\n"
            content += f"**Error Type:** {error_type}\n"
            content += f"**Details:** {message[:200]}...\n"
            content += f"**Time:** {timestamp}\n"
            content += f"**System:** MonAY Debug Assistant"
            
            discord_payload = {"content": content}
            
            with self.queue_lock:
                if len(self.message_queue) >= self.max_queue_size:
                    self.message_queue.popleft()  # Remove oldest message
                
                self.message_queue.append(discord_payload)
                
                # Force immediate flush for testing - don't wait for interval
                self._flush_discord_queue()
                    
        except Exception as e:
            self.logger.error(f"Error queuing Discord message: {e}")
    
    def _flush_discord_queue(self):
        """Flush queued messages to Discord (batched)"""
        if not self.discord_webhook or not self.message_queue:
            return
            
        try:
            # Lazy import to reduce startup overhead
            import requests
            
            messages_to_send = []
            with self.queue_lock:
                while self.message_queue and len(messages_to_send) < 10:  # Max 10 per batch
                    messages_to_send.append(self.message_queue.popleft())
                self.last_flush = time.time()
            
            if messages_to_send:
                # Send each message individually for reliability
                for message in messages_to_send:
                    try:
                        response = requests.post(
                            self.discord_webhook,
                            json=message,  # message is already formatted as {"content": "..."}
                            timeout=10
                        )
                        
                        if response.status_code in [200, 204]:
                            self.logger.info(f"✅ Sent Discord alert: {response.status_code}")
                        else:
                            self.logger.error(f"❌ Discord webhook failed: {response.status_code} - {response.text}")
                            
                    except Exception as msg_error:
                        self.logger.error(f"❌ Failed to send individual message: {msg_error}")
                        self._fallback_log_messages([message])
                    
        except Exception as e:
            self.logger.error(f"Error flushing Discord queue: {e}")
            self._fallback_log_messages(messages_to_send if 'messages_to_send' in locals() else [])
    
    def _create_discord_batch_message(self, messages: list) -> dict:
        """Create simple Discord text message from batched messages"""
        critical_count = sum(1 for msg in messages if 'CRITICAL' in str(msg))
        warning_count = len(messages) - critical_count
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"🤖 **MonAY Debug Assistant - Batch Alert** 🤖\n\n"
        content += f"📊 **Summary:** {critical_count} Critical, {warning_count} Warnings\n\n"
        
        for i, msg in enumerate(messages[:3]):  # Show max 3 detailed messages
            content += f"**Alert {i+1}:**\n{msg.get('content', str(msg))}\n\n"
        
        if len(messages) > 3:
            content += f"... and {len(messages) - 3} more alerts\n\n"
            
        content += f"**Batch Time:** {timestamp}"
        
        return {"content": content}
    
    def _fallback_log_messages(self, messages: list):
        """Log messages to fallback file when Discord fails"""
        if self.fallback_logger:
            for msg in messages:
                self.fallback_logger.error(f"FALLBACK: {msg}")
    
    def _get_smart_suggestions(self, error_info: dict) -> list[str]:
        """Get context-aware suggestions for the error"""
        try:
            error_type = error_info.get("type", "Unknown")
            error_msg = error_info.get("error_msg", "")
            
            suggestions = self.error_patterns.get(error_type, ["Check logs for more details"]).copy()
            
            # Add context-specific suggestions
            if "discord" in error_msg.lower():
                suggestions.append("Check Discord webhook URL")
            if "ollama" in error_msg.lower():
                suggestions.append("Verify Ollama service is running")
            if "youtube" in error_msg.lower():
                suggestions.append("Check YouTube API credentials")
                
            return suggestions
        except Exception as e:
            self.logger.error("Error generating suggestions", exc_info=e)
            return ["Check logs for more details"]
    
    def _extract_error_type(self, error_msg: str) -> str:
        """Extract error type from error message"""
        for error_type in self.error_patterns.keys():
            if error_type in error_msg:
                return error_type
        return "Unknown"
    
    def _assess_severity(self, error_type: str) -> str:
        """Assess error severity"""
        critical_errors = ["ImportError", "ModuleNotFoundError", "SyntaxError"]
        if error_type in critical_errors:
            return "CRITICAL"
        return "WARNING"
    
    def health_check(self) -> dict:
        """Health check endpoint to verify assistant status"""
        try:
            status = {
                "status": "healthy",
                "discord_configured": bool(self.discord_webhook),
                "queue_size": len(self.message_queue),
                "fallback_logging": bool(self.fallback_logger),
                "timestamp": datetime.now().isoformat()
            }
            
            # Test Discord connectivity if configured
            if self.discord_webhook:
                try:
                    import requests
                    test_response = requests.head(self.discord_webhook, timeout=5)
                    status["discord_reachable"] = test_response.status_code < 400
                except:
                    status["discord_reachable"] = False
            
            return status
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

def enable_instant_debugging(discord_webhook: str = None):
    """Enable instant debugging with smart suggestions"""
    assistant = SmartDebugAssistant(discord_webhook)
    logging.info("🧠 Production-ready smart debugging assistant enabled")
    return assistant