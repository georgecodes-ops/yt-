import logging
from typing import List, Dict
from datetime import datetime
import json
import time

# Import all intelligence collectors
from .rss_collector import RSSCollector
from .reddit_scraper import RedditScraper
from .google_trends import GoogleTrendsAnalyzer
from .economic_data import EconomicDataCollector
from .academic_research import AcademicResearchCollector
from .patent_data import PatentDataCollector

# Import free news aggregator
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'utils'))
from free_news_sources import FreeNewsAggregator

class ContentIntelligenceAggregator:
    """Aggregates intelligence from multiple sources to generate unique content ideas"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rss_collector = RSSCollector()
        self.reddit_scraper = RedditScraper()
        self.trends_analyzer = GoogleTrendsAnalyzer()
        self.economic_collector = EconomicDataCollector()
        self.academic_collector = AcademicResearchCollector()
        self.patent_collector = PatentDataCollector()
        self.news_aggregator = FreeNewsAggregator()
        
    def generate_unique_content_ideas(self, hours_back: int = 24) -> List[Dict]:
        """Generate unique content ideas by combining multiple intelligence sources"""
        all_ideas = []
        
        try:
            # 1. Free News API Analysis
            free_news = self.news_aggregator.get_free_finance_news()
            for news_item in free_news[:10]:  # Limit to top 10 news items
                idea = {
                    'type': 'breaking_news',
                    'title': f"Breaking: {news_item['title'][:50]}...",
                    'description': f"Latest news from {news_item['source']}: {news_item['title']}",
                    'keywords': [word for word in news_item['title'].split() if len(word) > 4][:5],
                    'sources': [news_item['source']],
                    'uniqueness_score': 0.7,
                    'content_potential': 'high',
                    'estimated_video_length': '45-75 seconds',
                    'target_audience': 'news-conscious investors',
                    'news_url': news_item['url']
                }
                all_ideas.append(idea)
                
        except Exception as e:
            self.logger.error(f"Error collecting free news intelligence: {e}")
            
        try:
            # 2. RSS Feed Analysis (backup)
            rss_topics = self.rss_collector.find_trending_topics(hours_back)
            for topic in rss_topics:
                idea = {
                    'type': 'rss_trend',
                    'title': f"Breaking: {topic['topic'].title()} Trending in Financial News",
                    'description': f"Latest developments in {topic['topic']} from top financial news sources",
                    'keywords': [topic['topic']],
                    'sources': topic['sources'],
                    'uniqueness_score': 0.6,
                    'content_potential': 'high' if topic['frequency'] > 5 else 'medium',
                    'estimated_video_length': '60-90 seconds',
                    'target_audience': 'news-conscious investors'
                }
                all_ideas.append(idea)
                
        except Exception as e:
            self.logger.error(f"Error collecting RSS intelligence: {e}")
        
        try:
            # 3. Reddit Pain Points
            pain_points = self.reddit_scraper.find_user_pain_points(hours_back)
            for point in pain_points:
                idea = {
                    'type': 'reddit_pain_point',
                    'title': f"Why {point['title'][:50]}... is Confusing Investors",
                    'description': f"Addressing common questions about {point['keywords'][0] if point['keywords'] else 'this topic'}",
                    'keywords': point['keywords'][:5],
                    'sources': [point['subreddit']],
                    'uniqueness_score': 0.8,
                    'content_potential': 'high',
                    'estimated_video_length': '45-75 seconds',
                    'target_audience': 'confused beginners'
                }
                all_ideas.append(idea)
                
        except Exception as e:
            self.logger.error(f"Error collecting Reddit intelligence: {e}")
        
        try:
            # 3. Contrarian Ideas
            contrarian_ideas = self.reddit_scraper.find_contrarian_ideas(hours_back)
            for idea_data in contrarian_ideas:
                idea = {
                    'type': 'contrarian',
                    'title': f"The Surprising Truth About {idea_data['title'][:40]}...",
                    'description': f"Challenging conventional wisdom about {idea_data['keywords'][0] if idea_data['keywords'] else 'this topic'}",
                    'keywords': idea_data['keywords'][:5],
                    'sources': [idea_data['subreddit']],
                    'uniqueness_score': 0.9,
                    'content_potential': 'very_high',
                    'estimated_video_length': '60-90 seconds',
                    'target_audience': 'skeptical investors'
                }
                all_ideas.append(idea)
                
        except Exception as e:
            self.logger.error(f"Error collecting contrarian intelligence: {e}")
        
        try:
            # 4. Academic Insights
            academic_insights = self.academic_collector.find_practical_insights(7)  # Weekly academic insights
            for insight in academic_insights[:10]:  # Limit to top 10
                idea = {
                    'type': 'academic_insight',
                    'title': f"What Research Reveals About {insight['title'][:40]}...",
                    'description': f"Science-backed insights on {insight['keywords'][0] if insight['keywords'] else 'this financial topic'}",
                    'keywords': insight['keywords'][:5],
                    'sources': [insight['source']],
                    'uniqueness_score': 0.85,
                    'content_potential': 'high',
                    'estimated_video_length': '75-120 seconds',
                    'target_audience': 'evidence-based investors'
                }
                all_ideas.append(idea)
                
        except Exception as e:
            self.logger.error(f"Error collecting academic intelligence: {e}")
        
        try:
            # 5. Patent-Based Innovation
            patent_opportunities = self.patent_collector.find_patent_based_content_opportunities()
            for opportunity in patent_opportunities[:8]:  # Limit to top 8
                idea = {
                    'type': 'innovation',
                    'title': f"How {opportunity['title'][:40]}...",
                    'description': opportunity['description'],
                    'keywords': opportunity['keywords'][:5],
                    'sources': ['patent_analysis'],
                    'uniqueness_score': 0.9,
                    'content_potential': opportunity['complexity'],
                    'estimated_video_length': '90-150 seconds',
                    'target_audience': 'tech-savvy investors'
                }
                all_ideas.append(idea)
                
        except Exception as e:
            self.logger.error(f"Error collecting patent intelligence: {e}")
        
        # Remove duplicates and sort by uniqueness score
        unique_ideas = self._remove_duplicate_ideas(all_ideas)
        unique_ideas.sort(key=lambda x: x['uniqueness_score'], reverse=True)
        
        self.logger.info(f"Generated {len(unique_ideas)} unique content ideas")
        return unique_ideas
    
    def _remove_duplicate_ideas(self, ideas: List[Dict]) -> List[Dict]:
        """Remove duplicate ideas based on title similarity"""
        unique_ideas = []
        seen_titles = set()
        
        for idea in ideas:
            # Create a simplified title for comparison
            title_key = ' '.join(idea['title'].lower().split()[:5])  # First 5 words
            if title_key not in seen_titles:
                unique_ideas.append(idea)
                seen_titles.add(title_key)
                
        return unique_ideas
    
    def find_historical_parallels(self) -> List[Dict]:
        """Find historical patterns that parallel current events"""
        # This would connect current trends with historical data
        historical_parallels = [
            {
                "current_event": "rising interest rates",
                "historical_parallel": "1980s Volcker disinflation",
                "content_opportunity": "Lessons from the 1980s: What Rising Rates Teach Us Today",
                "uniqueness_factor": "historical context",
                "estimated_engagement": "high"
            },
            {
                "current_event": "cryptocurrency regulation",
                "historical_parallel": "1930s banking regulation",
                "content_opportunity": "From Glass-Steagall to Crypto: How Financial Regulation Evolves",
                "uniqueness_factor": "regulatory evolution perspective",
                "estimated_engagement": "medium"
            },
            {
                "current_event": "inflation concerns",
                "historical_parallel": "1970s stagflation",
                "content_opportunity": "Stagflation Then vs Now: What's Different About Today's Inflation?",
                "uniqueness_factor": "economic cycle comparison",
                "estimated_engagement": "high"
            }
        ]
        
        return historical_parallels
    
    def generate_cross_niche_combinations(self) -> List[Dict]:
        """Generate content ideas by combining different niches"""
        # Common finance topics
        finance_topics = ['investing', 'retirement', 'budgeting', 'credit', 'insurance', 'taxes']
        
        # Cross-application domains
        cross_domains = [
            ('psychology', 'behavioral finance insights'),
            ('technology', 'fintech innovations'),
            ('history', 'historical financial lessons'),
            ('sports', 'performance and risk metaphors'),
            ('cooking', 'financial recipe analogies'),
            ('fitness', 'financial health comparisons'),
            ('gaming', 'strategy and risk management'),
            ('parenting', 'long-term financial planning'),
            ('travel', 'global financial perspectives'),
            ('gardening', 'investment growth metaphors')
        ]
        
        combinations = []
        import random
        
        for topic in finance_topics[:4]:  # Limit to 4 main topics
            for domain, description in cross_domains[:3]:  # Limit to 3 domains each
                combination = {
                    'type': 'cross_niche',
                    'title': f"{topic.title()} Lessons from {domain.title()}: {random.choice(['Unexpected', 'Surprising', 'Powerful'])} Financial Insights",
                    'description': f"Applying {description} to {topic} for unique perspectives",
                    'keywords': [topic, domain, 'unique', 'insight'],
                    'uniqueness_score': 0.95,
                    'content_potential': 'high',
                    'estimated_video_length': '60-120 seconds',
                    'target_audience': 'curious investors'
                }
                combinations.append(combination)
                
        return combinations
    
    def get_comprehensive_intelligence_report(self, hours_back: int = 24) -> Dict:
        """Generate a comprehensive intelligence report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'period_hours': hours_back,
            'content_ideas': self.generate_unique_content_ideas(hours_back),
            'historical_parallels': self.find_historical_parallels(),
            'cross_niche_combinations': self.generate_cross_niche_combinations(),
            'economic_indicators': {},
            'trending_keywords': [],
            'content_opportunities': []
        }
        
        try:
            # Add economic data
            report['economic_indicators'] = self.economic_collector.collect_fred_indicators()
        except Exception as e:
            self.logger.error(f"Error collecting economic indicators: {e}")
        
        try:
            # Add trending keywords
            rss_topics = self.rss_collector.find_trending_topics(hours_back)
            report['trending_keywords'] = [topic['topic'] for topic in rss_topics[:20]]
        except Exception as e:
            self.logger.error(f"Error collecting trending keywords: {e}")
        
        try:
            # Add content opportunities from all sources
            opportunities = []
            
            # Search gaps
            search_gaps = self.trends_analyzer.find_search_gaps()
            for gap in search_gaps:
                opportunities.append({
                    'type': 'search_gap',
                    'opportunity': gap['opportunity'],
                    'potential': gap['potential'],
                    'source': gap['source']
                })
            
            # Innovation gaps
            innovation_gaps = self.patent_collector.find_innovation_gaps()
            for gap in innovation_gaps:
                opportunities.append({
                    'type': 'innovation_gap',
                    'opportunity': gap['opportunity'],
                    'potential': gap['potential'],
                    'source': gap['source']
                })
            
            # Research gaps
            research_gaps = self.academic_collector.find_research_gaps()
            for gap in research_gaps:
                opportunities.append({
                    'type': 'research_gap',
                    'opportunity': gap['opportunity'],
                    'potential': gap['potential'],
                    'source': gap['source']
                })
            
            report['content_opportunities'] = opportunities
            
        except Exception as e:
            self.logger.error(f"Error collecting content opportunities: {e}")
        
        return report

if __name__ == "__main__":
    # Test the content intelligence aggregator
    aggregator = ContentIntelligenceAggregator()
    
    # Generate unique content ideas
    ideas = aggregator.generate_unique_content_ideas(48)  # Last 48 hours
    print(f"Generated {len(ideas)} unique content ideas:")
    
    # Show top 5 ideas by uniqueness score
    top_ideas = sorted(ideas, key=lambda x: x['uniqueness_score'], reverse=True)[:5]
    for i, idea in enumerate(top_ideas, 1):
        print(f"{i}. {idea['title']} (uniqueness: {idea['uniqueness_score']:.2f})")
        print(f"   Type: {idea['type']} | Potential: {idea['content_potential']}")
        print(f"   Keywords: {', '.join(idea['keywords'])}")
        print()
    
    print("="*50)
    
    # Generate comprehensive report
    report = aggregator.get_comprehensive_intelligence_report(24)
    print(f"Comprehensive report generated with {len(report['content_ideas'])} content ideas")
    print(f"Trending keywords: {len(report['trending_keywords'])}")
    print(f"Content opportunities: {len(report['content_opportunities'])}")