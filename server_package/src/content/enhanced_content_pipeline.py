import logging
from typing import List, Dict, Optional
from datetime import datetime
import asyncio

# Import existing content modules
from .content_pipeline import ContentPipeline
from .universal_content_engine import UniversalContentEngine
from .trending_tools import TrendingTools

# Import new intelligence modules
from .intelligence.content_intelligence import ContentIntelligenceAggregator

class EnhancedContentPipeline:
    """Enhanced content pipeline with intelligence-driven content generation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_pipeline = ContentPipeline()
        self.universal_engine = UniversalContentEngine()
        self.trending_tools = TrendingTools()
        self.intelligence_aggregator = ContentIntelligenceAggregator()
        
    async def generate_intelligence_driven_content(self, count: int = 10) -> List[Dict]:
        """Generate content based on intelligence from multiple sources"""
        self.logger.info("🚀 Generating intelligence-driven content...")
        
        # Get unique content ideas from intelligence aggregator
        content_ideas = self.intelligence_aggregator.generate_unique_content_ideas(48)  # Last 48 hours
        
        # Generate content for top ideas
        generated_content = []
        
        for i, idea in enumerate(content_ideas[:count]):
            try:
                self.logger.info(f"Generating content for idea {i+1}/{len(content_ideas[:count])}: {idea['title']}")
                
                # Create content based on idea type
                content = await self._generate_content_from_idea(idea)
                if content:
                    generated_content.append(content)
                    
                # Brief pause between generations
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error generating content for idea '{idea['title']}': {e}")
                continue
        
        self.logger.info(f"✅ Generated {len(generated_content)} intelligence-driven content pieces")
        return generated_content
    
    async def _generate_content_from_idea(self, idea: Dict) -> Optional[Dict]:
        """Generate content based on a specific idea"""
        try:
            # Determine content type based on idea
            if idea['type'] == 'contrarian':
                format_type = 'video_script_controversial'
                tone = 'thoughtful_challenging'
            elif idea['type'] == 'academic_insight':
                format_type = 'video_script_educational'
                tone = 'authoritative'
            elif idea['type'] == 'reddit_pain_point':
                format_type = 'video_script_helpful'
                tone = 'empathetic'
            else:
                format_type = 'video_script'
                tone = 'engaging'
            
            # Generate content using universal engine
            content_data = await self.universal_engine.generate_universal_content(
                topic=idea['title'],
                format_type=format_type,
                target_audience=idea['target_audience'],
                tone=tone,
                additional_context={
                    'keywords': idea['keywords'],
                    'description': idea['description'],
                    'uniqueness_score': idea['uniqueness_score']
                }
            )
            
            # Enhance with trending data
            trending_context = self.trending_tools.get_current_trends()
            if trending_context:
                # Add trending context to content
                content_data['trending_context'] = trending_context.get('top_trends', [])[:3]
            
            # Add intelligence metadata
            enhanced_content = {
                'content': content_data,
                'idea_source': idea,
                'generated_at': datetime.now().isoformat(),
                'content_id': f"intel_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(idea['title']) % 10000}",
                'estimated_video_length': idea['estimated_video_length'],
                'uniqueness_score': idea['uniqueness_score']
            }
            
            return enhanced_content
            
        except Exception as e:
            self.logger.error(f"Error generating content from idea: {e}")
            return None
    
    async def generate_cross_niche_content(self, niche_combinations: int = 5) -> List[Dict]:
        """Generate content from cross-niche combinations"""
        self.logger.info("🔄 Generating cross-niche content...")
        
        # Get cross-niche combinations
        cross_combinations = self.intelligence_aggregator.generate_cross_niche_combinations()
        
        generated_content = []
        for i, combination in enumerate(cross_combinations[:niche_combinations]):
            try:
                self.logger.info(f"Generating cross-niche content {i+1}/{len(cross_combinations[:niche_combinations])}")
                
                # Generate content for combination
                content = await self._generate_content_from_idea(combination)
                if content:
                    generated_content.append(content)
                    
            except Exception as e:
                self.logger.error(f"Error generating cross-niche content: {e}")
                continue
        
        self.logger.info(f"✅ Generated {len(generated_content)} cross-niche content pieces")
        return generated_content
    
    async def generate_historical_context_content(self, historical_items: int = 3) -> List[Dict]:
        """Generate content based on historical parallels"""
        self.logger.info("📚 Generating historical context content...")
        
        # Get historical parallels
        historical_parallels = self.intelligence_aggregator.find_historical_parallels()
        
        generated_content = []
        for i, parallel in enumerate(historical_parallels[:historical_items]):
            try:
                self.logger.info(f"Generating historical content {i+1}/{len(historical_parallels[:historical_items])}")
                
                # Create idea from historical parallel
                idea = {
                    'type': 'historical',
                    'title': parallel['content_opportunity'],
                    'description': f"Comparing {parallel['current_event']} with {parallel['historical_parallel']}",
                    'keywords': [parallel['current_event'], parallel['historical_parallel'], 'history'],
                    'sources': ['historical_analysis'],
                    'uniqueness_score': 0.9,
                    'content_potential': parallel['estimated_engagement'],
                    'estimated_video_length': '90-150 seconds',
                    'target_audience': 'history-interested investors'
                }
                
                # Generate content
                content = await self._generate_content_from_idea(idea)
                if content:
                    generated_content.append(content)
                    
            except Exception as e:
                self.logger.error(f"Error generating historical content: {e}")
                continue
        
        self.logger.info(f"✅ Generated {len(generated_content)} historical context content pieces")
        return generated_content
    
    async def get_comprehensive_content_plan(self, hours_back: int = 24) -> Dict:
        """Generate a comprehensive content plan using all intelligence sources"""
        self.logger.info("📋 Generating comprehensive content plan...")
        
        # Get intelligence report
        intelligence_report = self.intelligence_aggregator.get_comprehensive_intelligence_report(hours_back)
        
        # Generate content based on different intelligence sources
        content_plan = {
            'timestamp': datetime.now().isoformat(),
            'report_period_hours': hours_back,
            'intelligence_driven_content': await self.generate_intelligence_driven_content(15),
            'cross_niche_content': await self.generate_cross_niche_content(5),
            'historical_content': await self.generate_historical_context_content(3),
            'trending_content': [],  # Traditional trending content
            'intelligence_insights': intelligence_report
        }
        
        # Add traditional trending content
        try:
            trending_topics = self.trending_tools.get_current_trends()
            if trending_topics:
                for topic in trending_topics.get('top_trends', [])[:5]:
                    idea = {
                        'type': 'trending',
                        'title': f"Latest Trend: {topic}",
                        'description': f"What everyone is talking about: {topic}",
                        'keywords': [topic],
                        'sources': ['trending_tools'],
                        'uniqueness_score': 0.5,  # Lower uniqueness for pure trending
                        'content_potential': 'high',
                        'estimated_video_length': '60-90 seconds',
                        'target_audience': 'trend-aware investors'
                    }
                    
                    content = await self._generate_content_from_idea(idea)
                    if content:
                        content_plan['trending_content'].append(content)
        except Exception as e:
            self.logger.error(f"Error generating trending content: {e}")
        
        self.logger.info("✅ Comprehensive content plan generated")
        return content_plan
    
    async def generate_unique_video_scripts(self, count: int = 10) -> List[Dict]:
        """Generate unique video scripts with high differentiation"""
        self.logger.info(f"🎬 Generating {count} unique video scripts...")
        
        # Get comprehensive content plan
        content_plan = await self.get_comprehensive_content_plan(48)
        
        # Combine all content types
        all_content = []
        all_content.extend(content_plan.get('intelligence_driven_content', []))
        all_content.extend(content_plan.get('cross_niche_content', []))
        all_content.extend(content_plan.get('historical_content', []))
        all_content.extend(content_plan.get('trending_content', []))
        
        # Sort by uniqueness score
        all_content.sort(key=lambda x: x.get('uniqueness_score', 0), reverse=True)
        
        # Return top 'count' unique scripts
        unique_scripts = all_content[:count]
        
        self.logger.info(f"✅ Generated {len(unique_scripts)} unique video scripts")
        return unique_scripts

if __name__ == "__main__":
    import asyncio
    
    # Test the enhanced content pipeline
    async def test_pipeline():
        pipeline = EnhancedContentPipeline()
        
        # Generate comprehensive content plan
        print("Generating comprehensive content plan...")
        content_plan = await pipeline.get_comprehensive_content_plan(24)
        
        print(f"\nContent Plan Summary:")
        print(f"- Intelligence-driven content: {len(content_plan.get('intelligence_driven_content', []))}")
        print(f"- Cross-niche content: {len(content_plan.get('cross_niche_content', []))}")
        print(f"- Historical content: {len(content_plan.get('historical_content', []))}")
        print(f"- Trending content: {len(content_plan.get('trending_content', []))}")
        
        # Generate unique video scripts
        print("\nGenerating unique video scripts...")
        scripts = await pipeline.generate_unique_video_scripts(5)
        
        print(f"\nGenerated {len(scripts)} unique video scripts:")
        for i, script in enumerate(scripts, 1):
            content_data = script.get('content', {})
            idea_source = script.get('idea_source', {})
            print(f"{i}. {idea_source.get('title', 'Untitled')}")
            print(f"   Type: {idea_source.get('type', 'unknown')}")
            print(f"   Uniqueness Score: {script.get('uniqueness_score', 0):.2f}")
            print(f"   Keywords: {', '.join(idea_source.get('keywords', []))}")
            print()
    
    # Run the test
    asyncio.run(test_pipeline())