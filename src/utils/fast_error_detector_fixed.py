import logging
import threading
import time
import requests
import json
from datetime import datetime
from typing import Callable, Optional

class DiscordAlerter:
    """Send alerts to Discord webhook"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, title: str, message: str, color: int = 16711680):
        """Send alert to Discord"""
        try:
            payload = {
                "embeds": [{
                    "title": f"🚨 MONAY ALERT: {title}",
                    "description": message,
                    "color": color,
                    "timestamp": datetime.now().isoformat(),
                    "footer": {"text": "MonAY Fast Detection System"}
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            if response.status_code in [200, 204]:
                self.logger.info(f"✅ Discord alert sent: {title}")
            else:
                self.logger.error(f"❌ Discord alert failed: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Discord alert error: {e}")

class FastDebugLogger:
    """Ultra-fast debug logger with instant problem detection"""
    
    def __init__(self, alert_callback: Optional[Callable] = None):
        self.alert_callback = alert_callback
        self.error_count = 0
        self.last_error_time = None
        self.monitoring = True
        
    def log_error(self, error_msg: str, context: str = ""):
        """Log error with instant alerting"""
        self.error_count += 1
        self.last_error_time = datetime.now()
        
        full_message = f"{error_msg} | Context: {context}"
        logging.error(full_message)
        
        if self.alert_callback and self.monitoring:
            self.alert_callback("System Error", full_message)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False

def setup_instant_problem_detection(discord_webhook: str = None, slack_webhook: str = None) -> FastDebugLogger:
    """Setup instant problem detection with Discord/Slack alerts"""
    
    # Prioritize Discord over Slack
    webhook_url = discord_webhook or slack_webhook
    alert_callback = None
    
    if webhook_url:
        if discord_webhook:
            alerter = DiscordAlerter(webhook_url)
            alert_callback = alerter.send_alert
            logging.info("✅ Discord alerts configured")
        else:
            # Slack fallback (simplified)
            def slack_alert(title, message, color=None):
                try:
                    payload = {"text": f"🚨 {title}: {message}"}
                    requests.post(webhook_url, json=payload, timeout=10)
                except:
                    pass
            alert_callback = slack_alert
            logging.info("✅ Slack alerts configured")
    else:
        logging.warning("⚠️ No webhook configured - using console alerts only")
    
    return FastDebugLogger(alert_callback)

def enable_instant_debugging():
    """Enable instant debugging capabilities"""
    logging.info("🔍 Instant debugging enabled")