import logging
from typing import Dict, List
import os

class AffiliateManager:
    """Manages affiliate marketing opportunities"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Your Amazon affiliate tag
        self.amazon_tag = os.getenv('AMAZON_AFFILIATE_TAG', 'your-amazon-tag-20')
        
        # Amazon product recommendations by topic
        self.amazon_products = {
            'investing': [
                {'title': 'The Intelligent Investor', 'asin': 'B000FC12C8'},
                {'title': 'Rich Dad Poor Dad', 'asin': 'B074VT5Z5M'},
                {'title': 'A Random Walk Down Wall Street', 'asin': 'B07L9W9QYJ'}
            ],
            'budgeting': [
                {'title': 'The Total Money Makeover', 'asin': 'B00DNX7YLM'},
                {'title': 'You Need a Budget', 'asin': 'B071LBGJB1'},
                {'title': 'The Automatic Millionaire', 'asin': 'B000FCJZ3G'}
            ],
            'trading': [
                {'title': 'Market Wizards', 'asin': 'B006X50OPW'},
                {'title': 'Trading for a Living', 'asin': 'B00DQUY8ZG'},
                {'title': 'Technical Analysis Explained', 'asin': 'B00B8QZPXY'}
            ],
            'crypto': [
                {'title': 'The Bitcoin Standard', 'asin': 'B078HJZQZX'},
                {'title': 'Mastering Bitcoin', 'asin': 'B071K7FCD4'},
                {'title': 'The Internet of Money', 'asin': 'B01L9WM0H8'}
            ],
            'business': [
                {'title': 'The Lean Startup', 'asin': 'B004J4XGN6'},
                {'title': 'Good to Great', 'asin': 'B0058DRUV6'},
                {'title': 'The E-Myth Revisited', 'asin': 'B000RO9VJK'}
            ]
        }
    
    async def initialize(self):
        """Initialize the AffiliateManager"""
        self.logger.info(f"Initializing AffiliateManager...")
        try:
            self.logger.info(f"AffiliateManager initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"AffiliateManager initialization failed: {e}")
            return False

    async def find_affiliate_opportunities(self, content: Dict) -> List[Dict]:
        """Find affiliate opportunities for content"""
        try:
            topic = content.get('topic', 'general').lower()
            opportunities = []
            
            # Find relevant Amazon products
            for category, products in self.amazon_products.items():
                if category in topic or any(keyword in topic for keyword in category.split()):
                    for product in products[:2]:  # Top 2 products per category
                        amazon_url = f"https://www.amazon.com/dp/{product['asin']}?tag={self.amazon_tag}"
                        opportunities.append({
                            'product': product['title'],
                            'link': amazon_url,
                            'commission': 0.04,  # Amazon's typical rate
                            'relevance': 0.8
                        })
            
            return opportunities
            
        except Exception as e:
            self.logger.error(f"Affiliate opportunity search failed: {e}")
            return []
    
    async def inject_affiliate_links_into_description(self, description: str, topic: str) -> str:
        """Inject Amazon affiliate links into video description"""
        try:
            opportunities = await self.find_affiliate_opportunities({'topic': topic})
            
            if not opportunities:
                return description
            
            # Add Amazon affiliate section to description
            affiliate_section = "\n\n📚 RECOMMENDED BOOKS & RESOURCES:\n"
            
            for opp in opportunities[:3]:  # Limit to top 3 most relevant
                affiliate_section += f"• {opp['product']}: {opp['link']}\n"
            
            affiliate_section += "\n⚠️ As an Amazon Associate, I earn from qualifying purchases at no extra cost to you.\n"
            
            return description + affiliate_section
            
        except Exception as e:
            self.logger.error(f"Affiliate link injection failed: {e}")
            return description
    
    async def get_affiliate_cta(self, topic: str) -> str:
        """Get call-to-action with affiliate links"""
        opportunities = await self.find_affiliate_opportunities({'topic': topic})
        
        if not opportunities:
            return "🔔 Subscribe for more finance tips!"
        
        return "📚 Check out the recommended books in the description - they're game changers!"
