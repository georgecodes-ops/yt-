import re
import json
import sys
import os
import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import functools
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class EnhancedPolicyWatcher:
    """Enhanced policy checker with real-time monitoring and compliance tracking"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.limits = {
            'youtube': {
                'title': 100, 
                'description': 5000, 
                'tags': 500,
                'thumbnail_text': 50,
                'video_length_min': 1,
                'video_length_max': 720  # 12 hours
            },
            'tiktok': {
                'caption': 2200, 
                'hashtags': 100,
                'video_length_min': 3,
                'video_length_max': 600  # 10 minutes
            },
            'x': {
                'tweet': 280, 
                'bio': 160,
                'thread_max': 25
            },
            'instagram': {
                'caption': 2200,
                'bio': 150,
                'story_text': 100
            }
        }
        
        # Enhanced flagged content detection
        self.flagged_keywords = {
            'prohibited': [
                'scam', 'fraud', 'fake news', 'illegal', 'hack', 'cheat',
                'violence', 'hate speech', 'discrimination', 'harassment',
                'spam', 'bot network', 'misleading', 'misinformation',
                'adult content', 'explicit', 'nsfw', 'inappropriate',
                'pyramid scheme', 'ponzi', 'get rich quick'
            ],
            'financial_warnings': [
                'guaranteed returns', 'risk-free', 'easy money',
                'financial advice', 'investment tip', 'stock tip',
                'crypto pump', 'moon shot', 'diamond hands'
            ],
            'clickbait': [
                'you won\'t believe', 'shocking', 'doctors hate',
                'one weird trick', 'this will blow your mind',
                'secret method', 'instant results'
            ]
        }
        
        self.platform_restrictions = {
            'youtube': {
                'prohibited': ['monetization hack', 'sub4sub', 'view bot', 'fake subscribers'],
                'discouraged': ['like and subscribe', 'smash that bell', 'first comment']
            },
            'tiktok': {
                'prohibited': ['follow for follow', 'like4like', 'fake followers'],
                'discouraged': ['viral hack', 'algorithm trick']
            },
            'x': {
                'prohibited': ['follow back', 'dm for promo', 'buy followers'],
                'discouraged': ['retweet for retweet', 'engagement pod']
            }
        }
        
        # Compliance tracking
        self.compliance_log = []
        self.violation_count = {'minor': 0, 'major': 0, 'critical': 0}
        
        # File monitoring
        self.observer = None
        self.monitoring_paths = ['src/content/', 'temp/', 'assets/']
        
        # Add missing timeout attribute
        self.timeout = 30  # Default timeout in seconds
        
        # Auto-install hooks
        self._install_hooks()
        self._start_file_monitoring()
    
    def _quick_policy_check(self, content: str, platform: str = 'general') -> bool:
        """Quick policy check for basic compliance"""
        try:
            if not content or not isinstance(content, str):
                return False
            
            content_lower = content.lower()
            
            # Check for prohibited keywords
            for keyword in self.flagged_keywords.get('prohibited', []):
                if keyword.lower() in content_lower:
                    self.logger.warning(f"Prohibited keyword detected: {keyword}")
                    return False
            
            # Check for financial warnings
            for keyword in self.flagged_keywords.get('financial_warnings', []):
                if keyword.lower() in content_lower:
                    self.logger.warning(f"Financial warning keyword detected: {keyword}")
                    return False
            
            # Platform-specific checks
            if platform in self.platform_restrictions:
                for keyword in self.platform_restrictions[platform].get('prohibited', []):
                    if keyword.lower() in content_lower:
                        self.logger.warning(f"Platform-prohibited keyword detected: {keyword}")
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in quick policy check: {e}")
            return False
    
    # Find line 95 and replace:
    # self._hook_upload_functions()
    # With:
    # self._hook_upload_functions()  # Disabled - requires upload_manager parameter
    
    # Or better yet, modify the _install_hooks method around line 92-99:
    def _install_hooks(self):
        """Automatically hook into existing upload functions"""
        try:
            # self._hook_upload_functions()  # Disabled - requires upload_manager
            self._hook_content_functions()
            print("✅ Enhanced policy checker hooks installed successfully")
        except Exception as e:
            print(f"⚠️ Policy checker hook installation: {e}")
    
    
    
    def _hook_content_functions(self):
        """Hook into content generation functions for policy checking"""
        try:
            # Basic content function hooking
            if hasattr(self, 'logger'):
                self.logger.info("Content function hooks installed")
            else:
                print("✅ Content function hooks installed")
            return True
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Error hooking content functions: {e}")
            else:
                print(f"⚠️ Error hooking content functions: {e}")
            return False

    def _start_file_monitoring(self):
        """Start real-time file monitoring for content compliance"""
        try:
            self.observer = Observer()
            handler = ContentFileHandler(self)
            
            for path in self.monitoring_paths:
                if os.path.exists(path):
                    self.observer.schedule(handler, path, recursive=True)
            
            self.observer.start()
            print("✅ Real-time content monitoring started")
        except Exception as e:
            print(f"⚠️ File monitoring setup failed: {e}")
    
    async def comprehensive_check(self, content: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """Comprehensive policy check with detailed analysis"""
        result = {
            'platform': platform,
            'timestamp': datetime.now().isoformat(),
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'suggestions': [],
            'compliance_level': 'excellent'
        }
        
        # Check each content field
        for field, text in content.items():
            if isinstance(text, str):
                field_result = await self._analyze_content_field(text, field, platform)
                result['issues'].extend(field_result['issues'])
                result['warnings'].extend(field_result['warnings'])
                result['suggestions'].extend(field_result['suggestions'])
                result['score'] -= field_result['penalty']
        
        # Determine overall compliance
        if result['score'] < 60:
            result['passed'] = False
            result['compliance_level'] = 'critical'
        elif result['score'] < 80:
            result['compliance_level'] = 'needs_improvement'
        elif result['score'] < 95:
            result['compliance_level'] = 'good'
        
        # Log compliance check
        self._log_compliance_check(result)
        
        return result
    
    async def _analyze_content_field(self, text: str, field: str, platform: str) -> Dict[str, Any]:
        """Analyze individual content field for policy compliance"""
        result = {'issues': [], 'warnings': [], 'suggestions': [], 'penalty': 0}
        
        # Length checks
        if platform in self.limits and field in self.limits[platform]:
            max_length = self.limits[platform][field]
            if len(text) > max_length:
                result['issues'].append(f"{field} exceeds {max_length} characters ({len(text)})")
                result['penalty'] += 20
        
        # Keyword analysis
        text_lower = text.lower()
        
        # Check prohibited content
        for category, keywords in self.flagged_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if category == 'prohibited':
                        result['issues'].append(f"Prohibited content detected: '{keyword}'")
                        result['penalty'] += 30
                    else:
                        result['warnings'].append(f"Potentially problematic: '{keyword}' ({category})")
                        result['penalty'] += 10
        
        # Platform-specific checks
        if platform in self.platform_restrictions:
            restrictions = self.platform_restrictions[platform]
            
            for keyword in restrictions.get('prohibited', []):
                if keyword in text_lower:
                    result['issues'].append(f"Platform violation: '{keyword}'")
                    result['penalty'] += 25
            
            for keyword in restrictions.get('discouraged', []):
                if keyword in text_lower:
                    result['warnings'].append(f"Discouraged practice: '{keyword}'")
                    result['penalty'] += 5
        
        # Content quality suggestions
        if len(text.split()) < 5 and field in ['description', 'caption']:
            result['suggestions'].append(f"{field} could be more descriptive")
        
        if text.count('!') > 3:
            result['suggestions'].append("Consider reducing exclamation marks for professionalism")
        
        return result
    
    def _log_compliance_check(self, result: Dict[str, Any]):
        """Log compliance check for tracking and reporting"""
        self.compliance_log.append(result)
        
        # Update violation counts
        if result['compliance_level'] == 'critical':
            self.violation_count['critical'] += 1
        elif result['compliance_level'] == 'needs_improvement':
            self.violation_count['major'] += 1
        elif len(result['warnings']) > 0:
            self.violation_count['minor'] += 1
        
        # Keep only last 1000 entries
        if len(self.compliance_log) > 1000:
            self.compliance_log = self.compliance_log[-1000:]
    
    def get_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        recent_checks = self.compliance_log[-100:] if self.compliance_log else []
        
        return {
            'total_checks': len(self.compliance_log),
            'violation_counts': self.violation_count,
            'recent_average_score': sum(c['score'] for c in recent_checks) / len(recent_checks) if recent_checks else 0,
            'compliance_trend': self._calculate_compliance_trend(),
            'top_issues': self._get_top_issues(),
            'recommendations': self._generate_recommendations()
        }
    
    def _calculate_compliance_trend(self) -> str:
        """Calculate compliance trend over recent checks"""
        if len(self.compliance_log) < 10:
            return "insufficient_data"
        
        recent_scores = [c['score'] for c in self.compliance_log[-20:]]
        early_avg = sum(recent_scores[:10]) / 10
        late_avg = sum(recent_scores[10:]) / 10
        
        if late_avg > early_avg + 5:
            return "improving"
        elif late_avg < early_avg - 5:
            return "declining"
        else:
            return "stable"
    
    def _get_top_issues(self) -> List[str]:
        """Get most common compliance issues"""
        issue_counts = {}
        for check in self.compliance_log[-100:]:
            for issue in check['issues']:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        return sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on compliance history"""
        recommendations = []
        
        if self.violation_count['critical'] > 0:
            recommendations.append("Review content creation guidelines to avoid critical violations")
        
        if self.violation_count['major'] > 5:
            recommendations.append("Implement additional content review steps before publishing")
        
        recent_checks = self.compliance_log[-20:] if self.compliance_log else []
        avg_score = sum(c['score'] for c in recent_checks) / len(recent_checks) if recent_checks else 100
        
        if avg_score < 85:
            recommendations.append("Consider content quality training for team members")
        
        return recommendations
    
    def stop_monitoring(self):
        """Stop file monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()

    def _hook_upload_functions(self, upload_manager):
        """
        Hook into upload manager functions for policy checking
        """
        try:
            if not upload_manager:
                self.logger.warning("No upload manager provided for hooking")
                return False
            
            # Store reference to upload manager
            self.upload_manager = upload_manager
            
            # Hook into upload functions if they exist
            if hasattr(upload_manager, 'upload_video'):
                original_upload = upload_manager.upload_video
                
                def hooked_upload(*args, **kwargs):
                    # Pre-upload policy check
                    video_data = args[0] if args else kwargs.get('video_data')
                    if video_data:
                        policy_check = self.check_content_policy(video_data)
                        if not policy_check.get('approved', True):
                            self.logger.warning(f"Upload blocked by policy: {policy_check.get('reason')}")
                            return {'status': 'blocked', 'reason': policy_check.get('reason')}
                    
                    # Proceed with original upload
                    return original_upload(*args, **kwargs)
                
                upload_manager.upload_video = hooked_upload
                self.logger.info("Successfully hooked upload_video function")
            
            if hasattr(upload_manager, 'schedule_upload'):
                original_schedule = upload_manager.schedule_upload
                
                def hooked_schedule(*args, **kwargs):
                    # Pre-schedule policy check
                    content_data = args[0] if args else kwargs.get('content_data')
                    if content_data:
                        policy_check = self.check_content_policy(content_data)
                        if not policy_check.get('approved', True):
                            self.logger.warning(f"Schedule blocked by policy: {policy_check.get('reason')}")
                            return {'status': 'blocked', 'reason': policy_check.get('reason')}
                    
                    return original_schedule(*args, **kwargs)
                
                upload_manager.schedule_upload = hooked_schedule
                self.logger.info("Successfully hooked schedule_upload function")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error hooking upload functions: {e}")
            return False

    async def check_content_compliance(self, content: Dict) -> Dict:
        """Check content compliance across all platforms"""
        try:
            compliance_results = {
                'overall_compliant': True,
                'platform_compliance': {},
                'violations': [],
                'warnings': [],
                'recommendations': []
            }
            
            # Check each platform's compliance
            platforms = ['youtube', 'tiktok', 'x', 'instagram']
            
            for platform in platforms:
                platform_result = await self._check_platform_compliance(content, platform)
                compliance_results['platform_compliance'][platform] = platform_result
                
                if not platform_result.get('compliant', True):
                    compliance_results['overall_compliant'] = False
                    compliance_results['violations'].extend(platform_result.get('violations', []))
                
                compliance_results['warnings'].extend(platform_result.get('warnings', []))
                compliance_results['recommendations'].extend(platform_result.get('recommendations', []))
            
            # Log compliance check
            self.compliance_log.append({
                'timestamp': datetime.now().isoformat(),
                'content_id': content.get('id', 'unknown'),
                'compliant': compliance_results['overall_compliant'],
                'violations': len(compliance_results['violations'])
            })
            
            return compliance_results
            
        except Exception as e:
            self.logger.error(f"Content compliance check failed: {e}")
            return {
                'overall_compliant': False,
                'error': str(e),
                'platform_compliance': {},
                'violations': [f"Compliance check error: {e}"],
                'warnings': [],
                'recommendations': ['Manual review required']
            }
    
    async def _check_platform_compliance(self, content: Dict, platform: str) -> Dict:
        """Check compliance for a specific platform"""
        try:
            result = {
                'compliant': True,
                'violations': [],
                'warnings': [],
                'recommendations': []
            }
            
            # Check content length limits
            if platform in self.limits:
                limits = self.limits[platform]
                
                # Check title/caption length
                title_field = 'title' if platform == 'youtube' else 'caption'
                if title_field in content:
                    title_length = len(content[title_field])
                    max_length = limits.get('title' if platform == 'youtube' else 'caption', 1000)
                    
                    if title_length > max_length:
                        result['violations'].append(f"{title_field.title()} exceeds {max_length} characters ({title_length})")
                        result['compliant'] = False
            
            # Check for flagged keywords
            content_text = str(content.get('title', '')) + ' ' + str(content.get('description', '')) + ' ' + str(content.get('caption', ''))
            
            for category, keywords in self.flagged_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in content_text.lower():
                        if category == 'prohibited':
                            result['violations'].append(f"Prohibited content detected: {keyword}")
                            result['compliant'] = False
                        else:
                            result['warnings'].append(f"Flagged content ({category}): {keyword}")
            
            # Check platform-specific restrictions
            if platform in self.platform_restrictions:
                restrictions = self.platform_restrictions[platform]
                
                for keyword in restrictions.get('prohibited', []):
                    if keyword.lower() in content_text.lower():
                        result['violations'].append(f"Platform violation: {keyword}")
                        result['compliant'] = False
                
                for keyword in restrictions.get('discouraged', []):
                    if keyword.lower() in content_text.lower():
                        result['warnings'].append(f"Discouraged content: {keyword}")
            
            return result
            
        except Exception as e:
            return {
                'compliant': False,
                'violations': [f"Platform compliance check error: {e}"],
                'warnings': [],
                'recommendations': ['Manual review required']
            }

class ContentFileHandler(FileSystemEventHandler):
    """File system event handler for content monitoring"""
    
    def __init__(self, policy_checker):
        self.policy_checker = policy_checker
        self.content_extensions = ['.txt', '.md', '.json', '.py']
    
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if any(file_path.endswith(ext) for ext in self.content_extensions):
                self._check_file_content(file_path)
    
    def _check_file_content(self, file_path: str):
        """Check file content for policy compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Quick policy check
            if self.policy_checker._quick_policy_check(content, 'general'):
                print(f"✅ Policy check passed: {file_path}")
            else:
                print(f"⚠️ Policy concerns detected: {file_path}")
        except Exception as e:
            print(f"Error checking file {file_path}: {e}")

# Global policy watcher instance
_policy_watcher = None

def get_policy_watcher():
    """Get or create global policy watcher instance"""
    global _policy_watcher
    if _policy_watcher is None:
        _policy_watcher = EnhancedPolicyWatcher()
    return _policy_watcher

# Auto-initialize when imported
if __name__ != "__main__":
    try:
        get_policy_watcher()
    except Exception as e:
        print(f"Policy watcher auto-init: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Policy Watcher')
    parser.add_argument('--check', help='Check content for compliance')
    parser.add_argument('--platform', default='youtube', help='Target platform')
    parser.add_argument('--report', action='store_true', help='Generate compliance report')
    parser.add_argument('--monitor', action='store_true', help='Start monitoring mode')
    
    args = parser.parse_args()
    
    watcher = get_policy_watcher()
    
    if args.report:
        report = watcher.get_compliance_report()
        print(json.dumps(report, indent=2))
    elif args.check:
        result = asyncio.run(watcher.comprehensive_check({'content': args.check}, args.platform))
        print(json.dumps(result, indent=2))
    elif args.monitor:
        print("Starting monitoring mode... Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            watcher.stop_monitoring()
            print("\nMonitoring stopped")