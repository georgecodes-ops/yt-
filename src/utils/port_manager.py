
"""Port Management Utility"""
import socket
import os
from typing import Optional

class PortManager:
    def __init__(self):
        self.used_ports = set()
        
    def find_free_port(self, start_port: int = 8080, preferred_port: Optional[int] = None) -> int:
        """Find a free port, preferring the specified port if available"""
        if preferred_port and self.is_port_free(preferred_port):
            self.used_ports.add(preferred_port)
            return preferred_port
            
        for port in range(start_port, start_port + 100):
            if self.is_port_free(port):
                self.used_ports.add(port)
                return port
                
        raise RuntimeError(f"No free ports available starting from {start_port}")
        
    def is_port_free(self, port: int) -> bool:
        """Check if a port is free"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except OSError:
            return False
            
    def release_port(self, port: int):
        """Release a port from tracking"""
        self.used_ports.discard(port)
        
# Global instance
port_manager = PortManager()

# Environment-based port configuration (reads from existing .env)
DEFAULT_APP_PORT = int(os.getenv('APP_PORT', '8080'))
DEFAULT_DASHBOARD_PORT = int(os.getenv('DASHBOARD_PORT', '8501'))
DEFAULT_API_PORT = int(os.getenv('API_PORT', '8000'))
