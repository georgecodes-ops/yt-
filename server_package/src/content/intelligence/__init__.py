"""
Content Intelligence Module
==========================

This module provides intelligence gathering and analysis capabilities
for generating unique financial content by collecting data from multiple
free sources including RSS feeds, Reddit, Google Trends, economic data,
academic research, and patent information.

Modules:
- rss_collector: Collects news from financial RSS feeds
- reddit_scraper: Scrapes Reddit for user discussions and pain points
- google_trends: Analyzes search trends and patterns
- economic_data: Collects economic indicators and data
- academic_research: Gathers academic papers and research
- patent_data: Analyzes financial technology patents
- content_intelligence: Main aggregator that combines all sources

Usage:
    from content.intelligence import ContentIntelligenceAggregator
    
    aggregator = ContentIntelligenceAggregator()
    ideas = aggregator.generate_unique_content_ideas(hours_back=24)
"""

from .content_intelligence import ContentIntelligenceAggregator
from .rss_collector import RSSCollector
from .reddit_scraper import RedditScraper
from .google_trends import GoogleTrendsAnalyzer
from .economic_data import EconomicDataCollector
from .academic_research import AcademicResearchCollector
from .patent_data import PatentDataCollector

__all__ = [
    'ContentIntelligenceAggregator',
    'RSSCollector', 
    'RedditScraper',
    'GoogleTrendsAnalyzer',
    'EconomicDataCollector',
    'AcademicResearchCollector',
    'PatentDataCollector'
]