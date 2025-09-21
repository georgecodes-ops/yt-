import logging
import os
import sys
from typing import Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

class SmartDebugAssistant:
    """Production-ready smart debugging assistant with Discord alerts"""
    
    def __init__(self, discord_webhook: str = None):
        self.discord_webhook = discord_webhook
        self.logger = logging.getLogger(__name__)
        
        if self.discord_webhook:
            self.logger.info("✅ Discord webhook configured")
        else:
            self.logger.warning("⚠️ No Discord webhook configured - using fallback logging only")
    
    def analyze_error(self, error_msg: str, traceback_info: str = "") -> dict:
        """Analyze error and send Discord alert immediately"""
        try:
            # Extract error information
            error_type = self._extract_error_type(error_msg)
            severity = self._assess_severity(error_type)
            suggestions = self._get_smart_suggestions({"error_type": error_type, "message": error_msg})
            
            analysis = {
                "error_type": error_type,
                "severity": severity,
                "message": error_msg,
                "suggestions": suggestions,
                "timestamp": datetime.now().isoformat()
            }
            
            # Log the error
            log_level = logging.ERROR if severity == "CRITICAL" else logging.WARNING
            self.logger.log(log_level, f"🚨 {severity} Error: {error_type} - {len(suggestions)} suggestions")
            
            # Send to Discord immediately
            self._send_discord_alert(analysis)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in analyze_error: {e}")
            return {"error": str(e)}
    
    def _send_discord_alert(self, analysis: dict):
        """Send Discord alert immediately - no queuing"""
        if not self.discord_webhook:
            return
            
        try:
            import requests
            
            # Create simple text message
            severity = analysis.get('severity', 'WARNING')
            error_type = analysis.get('error_type', 'Unknown')
            message = analysis.get('message', 'No details available')
            suggestions = analysis.get('suggestions', [])
            
            emoji_map = {
                "CRITICAL": "🚨",
                "WARNING": "⚠️",
                "INFO": "ℹ️"
            }
            
            emoji = emoji_map.get(severity, "⚠️")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create Discord message content
            content = f"{emoji} **MonAY {severity} ALERT** {emoji}\n\n"
            content += f"**Error Type:** {error_type}\n"
            content += f"**Details:** {message[:300]}\n"
            content += f"**Time:** {timestamp}\n"
            
            if suggestions:
                content += f"\n**Suggestions:**\n"
                for i, suggestion in enumerate(suggestions[:3], 1):
                    content += f"{i}. {suggestion}\n"
            
            content += f"\n**System:** MonAY Debug Assistant"
            
            # Send immediately
            response = requests.post(
                self.discord_webhook,
                json={"content": content},
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                self.logger.info(f"✅ Sent Discord alert: {response.status_code}")
            else:
                self.logger.error(f"❌ Discord webhook failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to send Discord alert: {e}")
    
    def _extract_error_type(self, error_msg: str) -> str:
        """Extract error type from error message"""
        error_types = ["ImportError", "ModuleNotFoundError", "FileNotFoundError", "ConnectionError", 
                      "NameError", "SyntaxError", "AttributeError", "KeyError", "ValueError"]
        
        for error_type in error_types:
            if error_type.lower() in error_msg.lower():
                return error_type
        return "Unknown"
    
    def _assess_severity(self, error_type: str) -> str:
        """Assess error severity"""
        critical_errors = ["ImportError", "ModuleNotFoundError", "SyntaxError", "NameError"]
        return "CRITICAL" if error_type in critical_errors else "WARNING"
    
    def _get_smart_suggestions(self, error_info: dict) -> list[str]:
        """Generate smart suggestions based on error type"""
        error_type = error_info.get("error_type", "").lower()
        message = error_info.get("message", "").lower()
        
        suggestions = []
        
        if "import" in error_type or "module" in error_type:
            suggestions.extend([
                "Check if the module is installed: pip list | grep module_name",
                "Install missing module: pip install module_name",
                "Check Python path and virtual environment",
                "Verify module spelling and case sensitivity"
            ])
        elif "file" in error_type:
            suggestions.extend([
                "Check if file exists: ls -la filename",
                "Verify file path and permissions",
                "Check working directory: pwd",
                "Create missing file or directory"
            ])
        elif "connection" in error_type:
            suggestions.extend([
                "Check network connectivity: ping target",
                "Verify service is running: systemctl status service",
                "Check firewall and port access",
                "Restart the target service",
                "Check system resources: free -h && df -h"
            ])
        else:
            suggestions.extend([
                "Check system logs: journalctl -u monay -n 50",
                "Restart the service: sudo systemctl restart monay",
                "Check system resources and dependencies",
                "Review recent code changes"
            ])
        
        return suggestions[:5]  # Return max 5 suggestions

def enable_instant_debugging(discord_webhook: str = None):
    """Enable instant debugging with Discord alerts"""
    assistant = SmartDebugAssistant(discord_webhook)
    logging.getLogger().info("🧠 Production-ready smart debugging assistant enabled")
    return assistant