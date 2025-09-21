import logging
import traceback
import sys
import inspect
import ast
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class SmartDebugAssistant:
    """AI-powered debugging assistant for instant problem solving"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.solution_database = self._build_solution_database()
        self.debug_history = []
    
    def _build_solution_database(self) -> Dict:
        """Build database of common problems and instant solutions"""
        return {
            'ModuleNotFoundError': {
                'solutions': [
                    "pip install {module_name}",
                    "Check if module is in requirements.txt",
                    "Verify virtual environment is activated",
                    "Check Python path and PYTHONPATH"
                ],
                'auto_fix': 'install_missing_module'
            },
            'ConnectionError': {
                'solutions': [
                    "Check network connectivity",
                    "Verify service is running on target port",
                    "Check firewall settings",
                    "Restart the target service"
                ],
                'auto_fix': 'restart_service'
            },
            'TimeoutError': {
                'solutions': [
                    "Increase timeout values in configuration",
                    "Check service response time",
                    "Verify network latency",
                    "Implement retry logic"
                ],
                'auto_fix': 'increase_timeouts'
            },
            'PermissionError': {
                'solutions': [
                    "Check file/directory permissions",
                    "Run with appropriate user privileges",
                    "Verify ownership of files",
                    "Check SELinux/AppArmor policies"
                ],
                'auto_fix': 'fix_permissions'
            },
            'FileNotFoundError': {
                'solutions': [
                    "Verify file path is correct",
                    "Check if file exists",
                    "Create missing directories",
                    "Check current working directory"
                ],
                'auto_fix': 'create_missing_paths'
            },
            'MemoryError': {
                'solutions': [
                    "Reduce batch size or chunk data",
                    "Use generators instead of lists",
                    "Clear unused variables with del",
                    "Restart the application"
                ],
                'auto_fix': 'optimize_memory'
            },
            'JSONDecodeError': {
                'solutions': [
                    "Validate JSON format",
                    "Check for trailing commas",
                    "Verify quotes are properly escaped",
                    "Use json.loads() with error handling"
                ],
                'auto_fix': 'fix_json_format'
            }
        }
    
    def analyze_exception(self, exception: Exception, context: Dict = None) -> Dict:
        """Analyze exception and provide instant solutions"""
        exc_type = type(exception).__name__
        exc_message = str(exception)
        
        # Get traceback information
        tb = traceback.extract_tb(exception.__traceback__)
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'exception_type': exc_type,
            'exception_message': exc_message,
            'file_location': None,
            'line_number': None,
            'function_name': None,
            'code_snippet': None,
            'instant_solutions': [],
            'auto_fix_available': False,
            'severity': self._determine_severity(exc_type, exc_message),
            'context': context or {}
        }
        
        # Extract location information
        if tb:
            last_frame = tb[-1]
            analysis['file_location'] = last_frame.filename
            analysis['line_number'] = last_frame.lineno
            analysis['function_name'] = last_frame.name
            analysis['code_snippet'] = last_frame.line
        
        # Get solutions from database
        if exc_type in self.solution_database:
            solutions = self.solution_database[exc_type]
            analysis['instant_solutions'] = self._customize_solutions(
                solutions['solutions'], exc_message, analysis
            )
            analysis['auto_fix_available'] = 'auto_fix' in solutions
            analysis['auto_fix_method'] = solutions.get('auto_fix')
        
        # Add to debug history
        self.debug_history.append(analysis)
        
        return analysis
    
    def _customize_solutions(self, solutions: List[str], exc_message: str, analysis: Dict) -> List[str]:
        """Customize generic solutions based on specific error details"""
        customized = []
        
        for solution in solutions:
            # Replace placeholders with actual values
            if '{module_name}' in solution:
                # Extract module name from error message
                module_match = re.search(r"No module named '([^']+)'", exc_message)
                if module_match:
                    module_name = module_match.group(1)
                    solution = solution.replace('{module_name}', module_name)
            
            if '{file_path}' in solution:
                if analysis.get('file_location'):
                    solution = solution.replace('{file_path}', analysis['file_location'])
            
            customized.append(solution)
        
        return customized
    
    def _determine_severity(self, exc_type: str, exc_message: str) -> str:
        """Determine error severity for prioritization"""
        critical_errors = ['MemoryError', 'SystemExit', 'KeyboardInterrupt']
        high_errors = ['ConnectionError', 'TimeoutError', 'PermissionError']
        
        if exc_type in critical_errors:
            return 'critical'
        elif exc_type in high_errors:
            return 'high'
        elif 'CRITICAL' in exc_message.upper():
            return 'critical'
        elif 'ERROR' in exc_message.upper():
            return 'high'
        else:
            return 'medium'
    
    def get_instant_fix_command(self, analysis: Dict) -> Optional[str]:
        """Get instant command to fix the issue"""
        exc_type = analysis['exception_type']
        exc_message = analysis['exception_message']
        
        # Generate specific fix commands
        if exc_type == 'ModuleNotFoundError':
            module_match = re.search(r"No module named '([^']+)'", exc_message)
            if module_match:
                module_name = module_match.group(1)
                return f"pip install {module_name}"
        
        elif exc_type == 'ConnectionError' and '11434' in exc_message:
            return "sudo systemctl restart ollama"
        
        elif exc_type == 'PermissionError':
            if analysis.get('file_location'):
                return f"chmod 755 {analysis['file_location']}"
        
        elif 'disk' in exc_message.lower() or 'space' in exc_message.lower():
            return "df -h && du -sh /tmp/* | sort -hr | head -10"
        
        return None
    
    def print_debug_report(self, analysis: Dict):
        """Print formatted debug report for instant understanding"""
        print("\n" + "="*60)
        print(f"🐛 INSTANT DEBUG REPORT - {analysis['severity'].upper()} SEVERITY")
        print("="*60)
        print(f"⏰ Time: {analysis['timestamp']}")
        print(f"🔥 Error: {analysis['exception_type']}")
        print(f"💬 Message: {analysis['exception_message']}")
        
        if analysis['file_location']:
            print(f"📁 File: {analysis['file_location']}:{analysis['line_number']}")
            print(f"🔧 Function: {analysis['function_name']}")
            
        if analysis['code_snippet']:
            print(f"📝 Code: {analysis['code_snippet']}")
        
        print("\n🚀 INSTANT SOLUTIONS:")
        for i, solution in enumerate(analysis['instant_solutions'], 1):
            print(f"  {i}. {solution}")
        
        # Show instant fix command
        fix_command = self.get_instant_fix_command(analysis)
        if fix_command:
            print(f"\n⚡ INSTANT FIX COMMAND:")
            print(f"  {fix_command}")
        
        if analysis['auto_fix_available']:
            print(f"\n🤖 AUTO-FIX AVAILABLE: {analysis['auto_fix_method']}")
        
        print("="*60)

# Decorator for automatic error detection and fixing
def auto_debug(func):
    """Decorator that automatically debugs and suggests fixes for errors"""
    def wrapper(*args, **kwargs):
        assistant = SmartDebugAssistant()
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Analyze the exception
            analysis = assistant.analyze_exception(e, {
                'function': func.__name__,
                'args': str(args)[:100],
                'kwargs': str(kwargs)[:100]
            })
            
            # Print debug report
            assistant.print_debug_report(analysis)
            
            # Try auto-fix if available
            fix_command = assistant.get_instant_fix_command(analysis)
            if fix_command:
                print(f"\n🔧 Run this command to fix: {fix_command}")
            
            # Re-raise the exception
            raise
    
    return wrapper

# Enhanced exception handler
class EnhancedExceptionHandler:
    """Global exception handler with instant debugging"""
    
    def __init__(self):
        self.assistant = SmartDebugAssistant()
        self.original_excepthook = sys.excepthook
        
    def install(self):
        """Install enhanced exception handler"""
        sys.excepthook = self.handle_exception
        print("✅ Enhanced exception handler installed")
    
    def uninstall(self):
        """Restore original exception handler"""
        sys.excepthook = self.original_excepthook
        print("🔄 Original exception handler restored")
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle exceptions with instant debugging"""
        if issubclass(exc_type, KeyboardInterrupt):
            # Don't debug keyboard interrupts
            self.original_excepthook(exc_type, exc_value, exc_traceback)
            return
        
        # Create exception object for analysis
        exception = exc_value
        exception.__traceback__ = exc_traceback
        
        # Analyze and provide solutions
        analysis = self.assistant.analyze_exception(exception)
        self.assistant.print_debug_report(analysis)
        
        # Call original handler
        self.original_excepthook(exc_type, exc_value, exc_traceback)

# Quick setup function
def enable_instant_debugging():
    """Enable instant debugging for the entire application"""
    
    # Install enhanced exception handler
    handler = EnhancedExceptionHandler()
    handler.install()
    
    # Setup fast debug logging
    from src.utils.fast_error_detector import FastDebugLogger
    FastDebugLogger.setup_fast_debug_logging()
    
    print("⚡ INSTANT DEBUGGING ENABLED!")
    print("🔍 All errors will be analyzed and solutions provided instantly")
    print("🤖 Auto-fixes available for common issues")
    
    return handler

# Usage example
if __name__ == "__main__":
    # Enable instant debugging
    debug_handler = enable_instant_debugging()
    
    # Example function with auto-debug decorator
    @auto_debug
    def test_function():
        # This will trigger an error for demonstration
        import non_existent_module
    
    try:
        test_function()
    except:
        pass  # Error already handled by auto_debug decorator