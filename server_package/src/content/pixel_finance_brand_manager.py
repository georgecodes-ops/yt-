from .brand_manager import BrandManager
from typing import Dict, List

class PixelFinanceBrandManager(BrandManager):
    """Specialized brand manager for Pixel Finance niche"""
    
    def __init__(self):
        super().__init__()
        self.niche_config = {
            "focus_areas": ["crypto", "stocks", "passive_income", "financial_freedom"],
            "content_pillars": [
                "Market Analysis",
                "Investment Strategies", 
                "Crypto Updates",
                "Financial Education"
            ],
            "viral_hooks": [
                "This ONE trick changed my portfolio",
                "Why 99% of investors fail at this",
                "The secret Wall Street doesn't want you to know",
                "How I made $X in Y days"
            ]
        }
    
    def generate_viral_title(self, topic: str) -> str:
        """Generate viral-optimized titles"""
        hooks = self.niche_config["viral_hooks"]
        import random
        hook = random.choice(hooks)
        return f"{hook} - {topic}"
    
    def get_content_pillars(self) -> List[str]:
        """Get content pillar topics"""
        return self.niche_config["content_pillars"]
    
    def generate_shorts_script(self, topic: str) -> str:
        """Generate YouTube Shorts script"""
        return f"""
        HOOK (0-3s): {topic} - You won't believe this!
        PROBLEM (3-15s): Most people struggle with {topic.lower()}
        SOLUTION (15-45s): Here's the exact strategy I use...
        CTA (45-60s): Follow for more finance tips! Comment your thoughts below.
        """
