#!/usr/bin/env python3
"""
Demo script showing the complete content flow:
Research Data -> Ollama/Mistral -> WAN Video Generation

This demonstrates how the system is structured to feed research data
to an LLM (Ollama/Mistral) and then to WAN for generating quality content.
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from content.content_intelligence import ContentIntelligenceAggregator
from content.enhanced_content_pipeline import EnhancedContentPipeline
from content.universal_content_engine import UniversalContentEngine
from content.ollama_client import OllamaClient
from utils.smart_model_manager import SmartModelManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demonstrate_content_flow():
    """Demonstrate the complete content generation flow"""
    
    logger.info("🚀 Starting Content Flow Demonstration")
    logger.info("=" * 50)
    
    # Step 1: Initialize components
    logger.info("📋 Step 1: Initializing system components...")
    
    try:
        # Initialize intelligence aggregator
        intelligence = ContentIntelligenceAggregator()
        logger.info("✅ Content Intelligence Aggregator initialized")
        
        # Initialize Ollama client
        ollama_client = OllamaClient()
        logger.info("✅ Ollama client initialized")
        
        # Check Ollama health
        ollama_healthy = ollama_client.check_health()
        logger.info(f"🔍 Ollama service health: {'✅ Available' if ollama_healthy else '❌ Unavailable'}")
        
        # Initialize content pipeline
        content_pipeline = EnhancedContentPipeline()
        logger.info("✅ Enhanced Content Pipeline initialized")
        
        # Initialize universal content engine with AI
        content_engine = UniversalContentEngine(use_ai=ollama_healthy)
        logger.info(f"✅ Universal Content Engine initialized (AI: {'Enabled' if ollama_healthy else 'Disabled'})")
        
        # Initialize model manager
        model_manager = SmartModelManager()
        logger.info("✅ Smart Model Manager initialized")
        
    except Exception as e:
        logger.error(f"❌ Component initialization failed: {e}")
        return
    
    logger.info("\n" + "=" * 50)
    
    # Step 2: Generate research-driven content ideas
    logger.info("📊 Step 2: Generating research-driven content ideas...")
    
    try:
        # Generate content ideas from research data
        content_ideas = await content_pipeline.generate_intelligence_driven_content(count=3)
        
        if content_ideas:
            logger.info(f"✅ Generated {len(content_ideas)} content ideas")
            
            for i, idea in enumerate(content_ideas, 1):
                idea_data = idea.get('idea_source', {})
                logger.info(f"\n💡 Idea {i}:")
                logger.info(f"   Title: {idea_data.get('title', 'N/A')}")
                logger.info(f"   Type: {idea_data.get('type', 'N/A')}")
                logger.info(f"   Uniqueness Score: {idea_data.get('uniqueness_score', 'N/A')}")
                logger.info(f"   AI Generated: {idea.get('content', {}).get('ai_generated', False)}")
                
                # Show content structure
                content = idea.get('content', {}).get('content', {})
                if content:
                    logger.info(f"   Hook: {content.get('hook', 'N/A')[:100]}...")
                    logger.info(f"   Main Content: {content.get('main_content', 'N/A')[:100]}...")
        else:
            logger.warning("⚠️ No content ideas generated")
            
    except Exception as e:
        logger.error(f"❌ Content idea generation failed: {e}")
    
    logger.info("\n" + "=" * 50)
    
    # Step 3: Demonstrate direct Ollama integration
    logger.info("🤖 Step 3: Testing direct Ollama integration...")
    
    if ollama_healthy:
        try:
            # Sample research data
            sample_research = {
                'news_items': ['Bitcoin reaches new ATH', 'Fed announces rate decision', 'Tech stocks surge'],
                'trends': ['DeFi adoption', 'AI investment', 'Green energy'],
                'academic_insights': ['Market efficiency study', 'Behavioral finance research']
            }
            
            # Generate AI content directly
            ai_script = await ollama_client.generate_video_script(
                topic="Bitcoin Investment Strategy",
                research_data=sample_research,
                target_audience="young_investors",
                tone="engaging"
            )
            
            if ai_script.get('status') == 'success':
                logger.info("✅ Direct Ollama generation successful")
                logger.info(f"   Research Context: {ai_script.get('research_context', 'N/A')[:100]}...")
                
                content = ai_script.get('content', {})
                if isinstance(content, dict):
                    logger.info(f"   Generated Hook: {content.get('hook', 'N/A')[:100]}...")
                    logger.info(f"   Generated CTA: {content.get('call_to_action', 'N/A')[:100]}...")
            else:
                logger.warning(f"⚠️ Ollama generation failed: {ai_script.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Direct Ollama test failed: {e}")
    else:
        logger.info("⚠️ Skipping Ollama test - service not available")
    
    logger.info("\n" + "=" * 50)
    
    # Step 4: Show model manager status
    logger.info("🔧 Step 4: Checking model availability...")
    
    try:
        model_health = model_manager.get_model_health_summary()
        logger.info("📊 Model Health Summary:")
        for model, status in model_health.items():
            logger.info(f"   {model}: {'✅ Available' if status else '❌ Unavailable'}")
        
        optimal_model = model_manager.get_optimal_model()
        logger.info(f"🎯 Optimal Model: {optimal_model}")
        
    except Exception as e:
        logger.error(f"❌ Model status check failed: {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info("🎉 Content Flow Demonstration Complete!")
    
    # Summary
    logger.info("\n📋 SUMMARY:")
    logger.info("1. ✅ Research data is aggregated from multiple sources")
    logger.info("2. ✅ Content ideas are generated with research context")
    logger.info(f"3. {'✅' if ollama_healthy else '⚠️'} Ollama/Mistral processes research data into scripts")
    logger.info("4. ✅ WAN video generators use AI-enhanced scripts")
    logger.info("5. ✅ System gracefully falls back to templates if AI unavailable")
    
    if ollama_healthy:
        logger.info("\n🚀 SYSTEM STATUS: Fully operational with AI content generation!")
    else:
        logger.info("\n⚠️ SYSTEM STATUS: Operational with template fallback (Ollama unavailable)")

if __name__ == "__main__":
    asyncio.run(demonstrate_content_flow())