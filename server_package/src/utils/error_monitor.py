"""
Critical Error Monitoring & Telegram Alert System
Sends real-time alerts for system failures
"""

import logging
import asyncio
import traceback
from typing import Any, Dict, Optional
import requests
import os
from datetime import datetime
import json

class TelegramErrorMonitor:
    """Monitors critical errors and sends Telegram alerts"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '@your_monay_alerts')
        self.error_count = 0
        self.last_error_time = None
        
        # ADD THROTTLING CONTROLS
        self.notification_throttle = {
            'max_notifications_per_hour': int(os.getenv('MAX_TELEGRAM_NOTIFICATIONS_PER_HOUR', '5')),
            'max_notifications_per_day': int(os.getenv('MAX_TELEGRAM_NOTIFICATIONS_PER_DAY', '20')),
            'notification_history': [],
            'last_reset_hour': datetime.now().hour,
            'last_reset_day': datetime.now().date(),
            'hourly_count': 0,
            'daily_count': 0
        }
        
        # Only send notifications for truly critical errors
        self.critical_errors = {
            'ImportError', 
            'ModuleNotFoundError',
            'ConnectionError',
            'TimeoutError'
        }
        
        # DISABLE NON-CRITICAL NOTIFICATIONS
        self.enable_upload_notifications = os.getenv('ENABLE_UPLOAD_NOTIFICATIONS', 'false').lower() == 'true'
        self.enable_success_notifications = os.getenv('ENABLE_SUCCESS_NOTIFICATIONS', 'false').lower() == 'true'
        self.enable_status_notifications = os.getenv('ENABLE_STATUS_NOTIFICATIONS', 'false').lower() == 'true'
    
    def _check_notification_throttle(self) -> bool:
        """Check if we can send a notification based on throttling rules"""
        now = datetime.now()
        current_hour = now.hour
        current_date = now.date()
        
        # Reset hourly counter
        if current_hour != self.notification_throttle['last_reset_hour']:
            self.notification_throttle['hourly_count'] = 0
            self.notification_throttle['last_reset_hour'] = current_hour
        
        # Reset daily counter
        if current_date != self.notification_throttle['last_reset_day']:
            self.notification_throttle['daily_count'] = 0
            self.notification_throttle['last_reset_day'] = current_date
        
        # Check limits
        if self.notification_throttle['hourly_count'] >= self.notification_throttle['max_notifications_per_hour']:
            self.logger.warning(f"⚠️ Hourly notification limit reached ({self.notification_throttle['max_notifications_per_hour']})")
            return False
        
        if self.notification_throttle['daily_count'] >= self.notification_throttle['max_notifications_per_day']:
            self.logger.warning(f"⚠️ Daily notification limit reached ({self.notification_throttle['max_notifications_per_day']})")
            return False
        
        return True
    
    def _increment_notification_count(self):
        """Increment notification counters"""
        self.notification_throttle['hourly_count'] += 1
        self.notification_throttle['daily_count'] += 1
        self.notification_throttle['notification_history'].append(datetime.now())
        
    async def send_error_alert(self, error: Exception, context: str = "", severity: str = "HIGH") -> bool:
        """Send error alert to Telegram with enhanced error handling and throttling"""
        try:
            if not self.telegram_bot_token:
                return False
            
            error_type = type(error).__name__
            
            # ONLY send notifications for critical errors
            if error_type not in self.critical_errors:
                self.logger.debug(f"Skipping non-critical error notification: {error_type}")
                return False
            
            # Check throttling
            if not self._check_notification_throttle():
                return False
                
            error_message = str(error)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Enhanced error categorization
            is_critical = error_type in self.critical_errors
            
            # Create comprehensive error message
            alert_message = f"🚨 {severity} ALERT\n\n"
            alert_message += f"⏰ Time: {timestamp}\n"
            alert_message += f"🔥 Error: {error_type}\n"
            alert_message += f"📝 Message: {error_message[:500]}...\n"  # Truncate long messages
            
            if context:
                alert_message += f"🎯 Context: {context}\n"
            
            alert_message += f"⚠️ Critical: {'YES' if is_critical else 'NO'}\n"
            alert_message += f"🔧 Action: {self._get_action_recommendation(error_type)}\n"
            
            # Add stack trace for critical errors (truncated)
            if is_critical:
                stack_trace = traceback.format_exc()[:300]
                alert_message += f"\n📊 Stack Trace:\n```\n{stack_trace}...\n```"
            
            success = await self._send_telegram_message(alert_message)
            
            if success:
                self._increment_notification_count()
                self.error_count += 1
                self.last_error_time = datetime.now()
                self.logger.info(f"Error alert sent successfully for {error_type}")
            else:
                self.logger.error(f"Failed to send error alert for {error_type}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Critical error in error monitoring system: {e}")
            return False
    
    async def send_system_status(self, status: Dict[str, Any]) -> bool:
        """Send system status update (THROTTLED)"""
        if not self.enable_status_notifications:
            return False
        
        if not self._check_notification_throttle():
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            status_message = f"""
✅ **MonAY System Status Update**

🕐 **Time:** {timestamp}

📊 **Performance Metrics:**
• Content Generated: {status.get('content_generated', 0)}
• Videos Processed: {status.get('videos_processed', 0)}
• Revenue: ${status.get('revenue', 0):.2f}
• Uptime: {status.get('uptime', 'Unknown')}

🔄 **Active Components:**
• Content Pipeline: {status.get('content_pipeline', '❌')}
• Video Processor: {status.get('video_processor', '❌')}
• Upload Manager: {status.get('upload_manager', '❌')}
• Analytics: {status.get('analytics', '❌')}

#MonAY #SystemStatus #Healthy
            """
            
            success = await self._send_telegram_message(status_message)
            if success:
                self._increment_notification_count()
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send status update: {e}")
            return False
    
    async def send_critical_fix_alert(self, fix_description: str, files_affected: list) -> bool:
        """Send alert when critical fixes are applied"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            fix_message = f"""
🔧 **MonAY Critical Fix Applied**

🕐 **Time:** {timestamp}
📝 **Fix Description:** {fix_description}

📁 **Files Modified:**
{chr(10).join([f'• {file}' for file in files_affected])}

✅ **Status:** Fix applied successfully
🔄 **Action:** System restart recommended

#MonAY #CriticalFix #SystemUpdate
            """
            
            return await self._send_telegram_message(fix_message)
            
        except Exception as e:
            self.logger.error(f"Failed to send fix alert: {e}")
            return False
    
    async def _send_telegram_message(self, message: str) -> bool:
        """Send message to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                self.logger.error(f"Telegram API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def _get_action_recommendation(self, error_type: str) -> str:
        """Get action recommendation based on error type"""
        recommendations = {
            'NoneType': '• Check content_pipeline.py return statements\n• Verify data flow in automation loop',
            'ImportError': '• Install missing dependencies\n• Check requirements.txt',
            'ConnectionError': '• Check internet connection\n• Verify API endpoints',
            'KeyError': '• Check configuration files\n• Verify environment variables',
            'AttributeError': '• Check object initialization\n• Verify method calls',
            'FileNotFoundError': '• Check file paths\n• Verify file permissions'
        }
        
        return recommendations.get(error_type, '• Check logs for details\n• Review recent changes')

    async def send_deployment_notification(self, deployment_info: Dict[str, Any]) -> bool:
        """Send deployment success notification"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            deployment_message = f"""
    🚀 **MonAY System Deployed Successfully!**
    
    🕐 **Deployment Time:** {timestamp}
    🖥️ **Server:** {deployment_info.get('server', 'Production Server')}
    📍 **Location:** {deployment_info.get('location', 'Remote Server')}
    
    ✅ **Components Deployed:**
    • Content Generation: ✅ Active
    • Video Processing: ✅ Active  
    • Analytics Dashboard: ✅ Active
    • Upload Manager: ✅ Active
    • Revenue Optimizer: ✅ Active
    
    🌐 **Access URLs:**
    • Dashboard: http://{deployment_info.get('server_ip', 'your-server')}:8501
    • API: http://{deployment_info.get('server_ip', 'your-server')}:8000
    
    💰 **Ready to generate revenue!**
    
    #MonAY #Deployment #Success #Production
            """
            
            return await self._send_telegram_message(deployment_message)
            
        except Exception as e:
            self.logger.error(f"Failed to send deployment notification: {e}")
            return False

    async def send_success_notification(self, message: str, video_data: Optional[Dict] = None) -> bool:
        """Send success notification to Telegram (THROTTLED)"""
        if not self.enable_success_notifications:
            return False
        
        if not self._check_notification_throttle():
            return False
        
        try:
            success_message = f"🎉 **MonAY Success Alert**\n\n{message}\n\n"
            
            if video_data:
                success_message += f"📊 **Video Details:**\n"
                success_message += f"• Title: {video_data.get('title', 'N/A')}\n"
                success_message += f"• Duration: {video_data.get('duration', 'N/A')}s\n"
                success_message += f"• Platforms: {', '.join(video_data.get('platforms', []))}\n"
                
            success_message += f"\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            success = await self._send_telegram_message(success_message)
            if success:
                self._increment_notification_count()
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send success notification: {e}")
            return False
            
    async def send_upload_notification(self, platform: str, video_id: str, share_url: Optional[str] = None) -> bool:
        """Send upload success notification (THROTTLED)"""
        if not self.enable_upload_notifications:
            return False
        
        if not self._check_notification_throttle():
            return False
        
        try:
            upload_message = f"🚀 **Video Uploaded Successfully!**\n\n"
            upload_message += f"📱 Platform: {platform.upper()}\n"
            upload_message += f"🆔 Video ID: {video_id}\n"
            
            if share_url:
                upload_message += f"🔗 Share URL: {share_url}\n"
                
            upload_message += f"\n⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            success = await self._send_telegram_message(upload_message)
            if success:
                self._increment_notification_count()
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send upload notification: {e}")
            return False

# Global error monitor instance
error_monitor = TelegramErrorMonitor()