import os

class SmartCompetitorManager:
    def __init__(self):
        # Load static competitors from .env
        self.static_competitors = os.getenv('COMPETITOR_CHANNELS', '').split(',')
        
        # Dynamic discovery settings
        self.auto_discover = os.getenv('AUTO_DISCOVER_COMPETITORS', 'true').lower() == 'true'
        self.niche_keywords = os.getenv('YOUR_NICHE_KEYWORDS', '').split(',')
        self.min_subscribers = int(os.getenv('MIN_COMPETITOR_SUBSCRIBERS', '10000'))
        
        self.competitor_discovery = CompetitorDiscovery()
        self.dynamic_competitors = []
    
    async def update_competitor_list(self):
        """Automatically update competitor list"""
        if self.auto_discover:
            # Find new competitors dynamically
            keyword_competitors = await self.competitor_discovery.find_competitors_by_keywords(self.niche_keywords)
            trending_competitors = await self.competitor_discovery.find_trending_competitors(self.niche_keywords[0])
            
            # Combine and deduplicate
            all_competitors = list(set(self.static_competitors + keyword_competitors + trending_competitors))
            
            # Filter by criteria
            self.dynamic_competitors = await self.filter_competitors(all_competitors)
            
            self.logger.info(f"Updated competitor list: {len(self.dynamic_competitors)} channels")
    
    async def get_all_competitors(self):
        """Get combined static + dynamic competitor list"""
        return list(set(self.static_competitors + self.dynamic_competitors))