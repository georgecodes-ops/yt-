import os
import logging
import time
from typing import Any, Callable

class ProductionErrorHandler:
    def __init__(self):
        self.setup_logging()
        self.setup_monitoring()
        self.retry_attempts = 3
        self.retry_delay = 2
    
    def setup_logging(self):
        """Setup production logging for Ubuntu server"""
        # Ensure log directory exists - create only if needed
        log_dir = "data/logs"
        os.makedirs(log_dir, exist_ok=True)

        # Use absolute paths for server compatibility
        log_file = os.path.join(log_dir, "errors.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Also log to console for systemd
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_monitoring(self):
        """Setup error monitoring"""
        self.error_counts = {}
        self.last_errors = []
    
    def handle_api_error(self, error: Exception, operation: str = "API call") -> bool:
        """Handle API errors with retries and logging"""
        self.logger.error(f"API Error in {operation}: {error}")
        
        # Track error frequency
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Store recent errors
        self.last_errors.append({
            'timestamp': time.time(),
            'operation': operation,
            'error': str(error),
            'type': error_type
        })
        
        # Keep only last 100 errors
        if len(self.last_errors) > 100:
            self.last_errors = self.last_errors[-100:]
        
        return True
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """Retry function with exponential backoff - Fixed return handling"""
        for attempt in range(self.retry_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    self.handle_api_error(e, func.__name__)
                    # Return safe fallback instead of raising
                    self.logger.error(f"All {self.retry_attempts} attempts failed")
                    return {
                        "success": False, 
                        "error": "Max retries exceeded", 
                        "fallback": True,
                        "function": func.__name__
                    }
                
                wait_time = self.retry_delay * (2 ** attempt)
                self.logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s")
                time.sleep(wait_time)