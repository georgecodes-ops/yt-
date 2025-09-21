import requests
import feedparser
from datetime import datetime, timedelta
import logging
from typing import List, Dict
import time
import re

class AcademicResearchCollector:
    """Collects academic research papers for unique content insights"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Academic sources with RSS feeds or APIs
        self.sources = {
            'arxiv': {
                'url': 'http://export.arxiv.org/api/query',
                'categories': ['q-fin.GN', 'q-fin.CP', 'q-fin.EC', 'q-fin.PM', 'q-fin.PR', 'q-fin.RM', 'q-fin.ST', 'econ.GN', 'econ.TH']
            },
            'ssrn': {
                'url': 'https://papers.ssrn.com/sol3/DisplayAbstractSearch.cfm',
                'rss_base': 'https://www.ssrn.com/abstract.cfm?abstr_id='
            },
            'nber': {
                'url': 'https://www.nber.org/papers.xml',
                'description': 'National Bureau of Economic Research'
            }
        }
        
    def collect_finance_papers(self, days_back: int = 7) -> List[Dict]:
        """Collect recent finance and economics research papers"""
        all_papers = []
        
        # Collect from arXiv (quantitative finance and economics)
        try:
            arxiv_papers = self._collect_arxiv_papers(days_back)
            all_papers.extend(arxiv_papers)
            self.logger.info(f"Collected {len(arxiv_papers)} papers from arXiv")
        except Exception as e:
            self.logger.error(f"Error collecting arXiv papers: {e}")
        
        # Collect from NBER (National Bureau of Economic Research)
        try:
            nber_papers = self._collect_nber_papers(days_back)
            all_papers.extend(nber_papers)
            self.logger.info(f"Collected {len(nber_papers)} papers from NBER")
        except Exception as e:
            self.logger.error(f"Error collecting NBER papers: {e}")
            
        return all_papers
    
    def _collect_arxiv_papers(self, days_back: int = 7) -> List[Dict]:
        """Collect papers from arXiv quantitative finance and economics categories"""
        papers = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for category in self.sources['arxiv']['categories']:
            try:
                # arXiv API search
                search_query = f"cat:{category}"
                params = {
                    'search_query': search_query,
                    'max_results': 10,  # Limit results
                    'sortBy': 'submittedDate',
                    'sortOrder': 'descending'
                }
                
                # Note: In production, you'd make actual API calls
                # response = requests.get(self.sources['arxiv']['url'], params=params)
                # feed = feedparser.parse(response.text)
                
                # For now, simulate with sample papers
                sample_papers = self._simulate_arxiv_papers(category)
                papers.extend(sample_papers)
                
                time.sleep(1)  # Be respectful to arXiv servers
                
            except Exception as e:
                self.logger.error(f"Error collecting arXiv papers for {category}: {e}")
                
        return papers
    
    def _simulate_arxiv_papers(self, category: str) -> List[Dict]:
        """Simulate arXiv papers for demonstration"""
        import random
        
        # Sample paper titles and abstracts
        sample_titles = [
            f"Behavioral Biases in {category} Investment Decisions",
            f"Machine Learning Approaches to {category} Risk Assessment",
            f"Economic Impact of {category} Regulatory Changes",
            f"Network Analysis of {category} Market Dynamics",
            f"Cryptocurrency and {category} Portfolio Diversification"
        ]
        
        sample_abstracts = [
            "This paper examines the behavioral patterns of investors in quantitative finance markets and identifies systematic biases that affect decision-making processes.",
            "We apply advanced machine learning techniques to predict risk factors in financial markets using comprehensive datasets spanning multiple economic cycles.",
            "This study analyzes the effects of recent regulatory changes on market efficiency and investor behavior in the financial sector.",
            "Using network theory, we model the interconnectedness of financial institutions and identify systemic risk factors in modern markets.",
            "We investigate the role of cryptocurrency assets in portfolio diversification and their impact on traditional investment strategies."
        ]
        
        papers = []
        for i in range(3):  # 3 papers per category
            paper = {
                'title': random.choice(sample_titles),
                'abstract': random.choice(sample_abstracts),
                'authors': [f"Author {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])}", 
                           f"Author {random.choice(['Davis', 'Miller', 'Wilson', 'Moore', 'Taylor'])}"],
                'category': category,
                'published': (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat(),
                'source': 'arXiv',
                'keywords': self._extract_keywords(random.choice(sample_abstracts)),
                'paper_id': f"arxiv-{category}-{random.randint(1000, 9999)}",
                'interestingness_score': random.uniform(0.6, 0.9)
            }
            papers.append(paper)
            
        return papers
    
    def _collect_nber_papers(self, days_back: int = 7) -> List[Dict]:
        """Collect papers from NBER"""
        # Simulate NBER papers
        import random
        
        sample_titles = [
            "The Impact of Financial Literacy on Household Wealth Accumulation",
            "Behavioral Finance and Market Anomalies: New Evidence",
            "Cryptocurrency Adoption and Traditional Banking",
            "Economic Inequality and Financial Decision Making",
            "The Role of Technology in Financial Inclusion"
        ]
        
        sample_abstracts = [
            "This paper uses longitudinal data to examine how financial literacy affects long-term wealth building strategies across different demographic groups.",
            "We document new market anomalies that cannot be explained by traditional finance theories, suggesting the importance of behavioral factors.",
            "Our analysis shows how cryptocurrency adoption is changing the competitive landscape for traditional banking institutions and financial services.",
            "Using survey data, we explore the relationship between economic inequality and financial decision-making patterns across income groups.",
            "This research examines how digital financial technologies are expanding access to financial services in underserved communities."
        ]
        
        papers = []
        for i in range(5):
            paper = {
                'title': random.choice(sample_titles),
                'abstract': random.choice(sample_abstracts),
                'authors': [f"Researcher {random.choice(['Anderson', 'Thomas', 'Jackson', 'White', 'Harris'])}"],
                'published': (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat(),
                'source': 'NBER',
                'keywords': self._extract_keywords(random.choice(sample_abstracts)),
                'paper_id': f"nber-{random.randint(10000, 99999)}",
                'interestingness_score': random.uniform(0.7, 0.95)
            }
            papers.append(paper)
            
        return papers
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from academic text"""
        # Simple keyword extraction for academic content
        common_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 
            'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 
            'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'paper', 'study',
            'research', 'analysis', 'findings', 'results', 'data', 'methodology', 'conclusion', 'abstract',
            'introduction', 'literature', 'review', 'framework', 'model', 'approach', 'evidence', 'significant',
            'statistical', 'economic', 'finance', 'financial', 'market', 'markets', 'investment', 'investor',
            'portfolio', 'risk', 'return', 'asset', 'pricing', 'behavioral', 'theory', 'empirical', 'quantitative'
        }
        
        # Clean and extract words
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        keywords = [word for word in words if word not in common_words]
        return list(set(keywords))[:15]  # Return unique keywords, limit to 15
    
    def find_practical_insights(self, days_back: int = 7) -> List[Dict]:
        """Extract practical insights from academic research"""
        papers = self.collect_finance_papers(days_back)
        
        insights = []
        for paper in papers:
            # Look for practical implications in papers
            practical_insights = self._extract_practical_insights(paper)
            insights.extend(practical_insights)
            
        # Sort by interestingness score
        insights.sort(key=lambda x: x.get('interestingness_score', 0), reverse=True)
        return insights[:20]  # Return top 20 insights
    
    def _extract_practical_insights(self, paper: Dict) -> List[Dict]:
        """Extract practical insights from a research paper"""
        insights = []
        
        # Keywords that suggest practical applications
        practical_indicators = [
            'recommendation', 'suggestion', 'strategy', 'approach', 'method', 'technique', 
            'framework', 'model', 'implementation', 'application', 'practical', 'real-world',
            'policy', 'implication', 'guidance', 'advice', 'solution', 'improvement'
        ]
        
        abstract = paper.get('abstract', '').lower()
        title = paper.get('title', '').lower()
        
        # Check for practical content
        has_practical_content = any(indicator in abstract or indicator in title 
                                 for indicator in practical_indicators)
        
        if has_practical_content or paper.get('interestingness_score', 0) > 0.8:
            insight = {
                'title': paper['title'],
                'summary': paper['abstract'][:200] + '...' if len(paper['abstract']) > 200 else paper['abstract'],
                'source': paper['source'],
                'authors': paper['authors'],
                'keywords': paper['keywords'],
                'paper_id': paper['paper_id'],
                'interestingness_score': paper.get('interestingness_score', 0.5),
                'type': 'academic_insight'
            }
            insights.append(insight)
            
        return insights
    
    def find_research_gaps(self) -> List[Dict]:
        """Identify gaps in current research that represent content opportunities"""
        # Simulate research gap identification
        research_gaps = [
            {
                "opportunity": "Behavioral finance for gig economy workers",
                "reasoning": "Limited research on financial decision-making in non-traditional employment",
                "difficulty": "medium",
                "potential": "high",
                "source": "literature_review"
            },
            {
                "opportunity": "Cryptocurrency adoption among young investors",
                "reasoning": "Growing demographic with unique risk preferences",
                "difficulty": "low",
                "potential": "very_high",
                "source": "market_analysis"
            },
            {
                "opportunity": "Financial literacy in digital-first communities",
                "reasoning": "New financial behaviors emerge in digitally-native populations",
                "difficulty": "medium",
                "potential": "growing",
                "source": "trend_analysis"
            },
            {
                "opportunity": "AI-driven personal finance decision making",
                "reasoning": "Intersection of technology adoption and financial behavior",
                "difficulty": "high",
                "potential": "high",
                "source": "technology_trend"
            },
            {
                "opportunity": "Environmental, Social, Governance (ESG) investing psychology",
                "reasoning": "Values-based investing with limited behavioral research",
                "difficulty": "medium",
                "potential": "growing",
                "source": "market_gap"
            }
        ]
        
        return research_gaps

if __name__ == "__main__":
    # Test the academic research collector
    collector = AcademicResearchCollector()
    
    # Collect recent papers
    papers = collector.collect_finance_papers(7)
    print(f"Collected {len(papers)} academic papers:")
    for paper in papers[:3]:
        print(f"- {paper['title']} ({paper['source']})")
    
    print("\n" + "="*50 + "\n")
    
    # Find practical insights
    insights = collector.find_practical_insights(7)
    print(f"Found {len(insights)} practical insights:")
    for insight in insights[:3]:
        print(f"- {insight['title']} (score: {insight['interestingness_score']:.2f})")