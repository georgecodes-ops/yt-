"""
Dependency Manager - Breaks circular imports with lazy loading
"""

import logging
from typing import Dict, Any, Optional
from functools import lru_cache

class DependencyManager:
    """Manages dependencies and breaks circular imports"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._instances = {}
        self._factories = {}
    
    def register_factory(self, name: str, factory_func):
        """Register a factory function for lazy loading"""
        self._factories[name] = factory_func
    
    @lru_cache(maxsize=None)
    def get_instance(self, name: str) -> Optional[Any]:
        """Get or create instance with caching"""
        if name in self._instances:
            return self._instances[name]
        
        if name in self._factories:
            try:
                instance = self._factories[name]()
                self._instances[name] = instance
                return instance
            except Exception as e:
                self.logger.error(f"Failed to create {name}: {e}")
                return None
        
        self.logger.warning(f"No factory registered for {name}")
        return None
    
    def clear_cache(self):
        """Clear all cached instances"""
        self._instances.clear()
        self.get_instance.cache_clear()

# Global dependency manager
dependency_manager = DependencyManager()

# Factory functions
def create_brand_manager():
    from content.brand_manager import BrandManager
    return BrandManager()

def create_finance_brand_manager():
    from content.finance_brand_manager import FinanceBrandManager
    return FinanceBrandManager()

def create_pixel_brand_manager():
    from content.pixel_finance_brand_manager import PixelFinanceBrandManager
    return PixelFinanceBrandManager()

def create_wan_video_generator():
    from content.wan_video_generator import WanVideoGenerator
    return WanVideoGenerator()

# Register factories
dependency_manager.register_factory('brand_manager', create_brand_manager)
dependency_manager.register_factory('finance_brand_manager', create_finance_brand_manager)
dependency_manager.register_factory('pixel_brand_manager', create_pixel_brand_manager)
dependency_manager.register_factory('wan_video_generator', create_wan_video_generator)