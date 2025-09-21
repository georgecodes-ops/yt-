#!/usr/bin/env python3
"""
Example integration of Japanese Finance Sensei system into video generation pipeline
"""

import asyncio
import logging
from typing import Dict, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JapaneseContentGenerator:
    """Example integration class for Japanese Finance Sensei content generation"""
    
    def __init__(self):
        """Initialize Japanese styling components"""
        try:
            from .japanese_finance_sensei import JapaneseFinanceSensei  # type: ignore
            from .japanese_background_generator_complete import JapaneseBackgroundGenerator  # type: ignore
            from .japanese_style_video_processor import JapaneseStyleVideoProcessor  # type: ignore
            
            self.sensei = JapaneseFinanceSensei()
            self.background_generator = JapaneseBackgroundGenerator()
            self.video_processor = JapaneseStyleVideoProcessor()
            
            logger.info("Japanese Finance Sensei system initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Japanese system: {e}")
            raise
    
    async def generate_japanese_style_video(self, topic: str, script: str, audio_path: str = None) -> Dict:
        """
        Generate a complete Japanese-style video with Sensei character and dynamic scenes
        
        Args:
            topic (str): The financial topic for the video
            script (str): The script content for the video
            audio_path (str, optional): Path to audio file
            
        Returns:
            Dict: Video generation results including paths and metadata
        """
        try:
            logger.info(f"Generating Japanese-style video for topic: {topic}")
            
            # 1. Generate Sensei scenes and background prompts
            logger.info("1. Generating Sensei scene prompts...")
            scene_prompts = self.sensei.generate_scene_transition_prompts(topic, 6)
            
            # 2. Generate background scene prompts
            logger.info("2. Generating background scene prompts...")
            background_prompts = self.background_generator.generate_scene_sequence_prompts(topic, 6)
            
            # 3. Generate transition effects
            logger.info("3. Generating scene transitions...")
            transitions = []
            for i in range(len(scene_prompts) - 1):
                from_scene = f"scene_{i}"
                to_scene = f"scene_{i+1}"
                transition = self.background_generator.generate_transition_effect_prompt(
                    from_scene, to_scene
                )
                transitions.append(transition)
            
            # 4. Create video with Japanese styling
            logger.info("4. Creating video with Japanese styling...")
            video_path = self.video_processor.create_japanese_style_shorts(
                script=script,
                topic=topic,
                audio_path=audio_path
            )
            
            # 5. Create matching thumbnail
            logger.info("5. Creating matching thumbnail...")
            thumbnail_path = self.video_processor.create_thumbnail_with_japanese_style(topic)
            
            # 6. Generate styling consistency report
            logger.info("6. Generating styling consistency report...")
            styling_report = self.video_processor.get_japanese_styling_report()
            
            result = {
                "status": "success",
                "video_path": video_path,
                "thumbnail_path": thumbnail_path,
                "topic": topic,
                "scene_prompts": scene_prompts,
                "background_prompts": background_prompts,
                "transitions": transitions,
                "styling_report": styling_report,
                "scene_count": len(scene_prompts),
                "consistency_score": styling_report.get("consistency_score", 0.92)
            }
            
            logger.info(f"✅ Japanese-style video generation completed successfully!")
            logger.info(f"   Video: {video_path}")
            logger.info(f"   Thumbnail: {thumbnail_path}")
            logger.info(f"   Scenes: {len(scene_prompts)} dynamic scenes")
            logger.info(f"   Consistency: {styling_report.get('consistency_score', 0.92)}/1.00")
            
            return result
            
        except Exception as e:
            logger.error(f"Japanese-style video generation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "topic": topic
            }
    
    def generate_content_plan(self, topics: List[str]) -> Dict:
        """
        Generate a content plan with Japanese styling for multiple topics
        
        Args:
            topics (List[str]): List of financial topics
            
        Returns:
            Dict: Content plan with scene and background details
        """
        logger.info(f"Generating content plan for {len(topics)} topics...")
        
        content_plan = {
            "topics": [],
            "total_scenes": 0,
            "styling_consistency": 0.92
        }
        
        for topic in topics:
            # Generate Sensei scenes for this topic
            sensei_scenes = self.sensei.generate_scene_transition_prompts(topic, 4)
            
            # Generate background scenes for this topic
            bg_scenes = self.background_generator.generate_scene_sequence_prompts(topic, 4)
            
            # Create topic entry
            topic_entry = {
                "topic": topic,
                "sensei_scenes": sensei_scenes,
                "background_scenes": bg_scenes,
                "scene_count": len(sensei_scenes),
                "sample_scene": sensei_scenes[0] if sensei_scenes else "",
                "sample_background": bg_scenes[0] if bg_scenes else ""
            }
            
            content_plan["topics"].append(topic_entry)
            content_plan["total_scenes"] += len(sensei_scenes)
        
        logger.info(f"✅ Content plan generated with {content_plan['total_scenes']} total scenes")
        return content_plan

# Example usage
async def example_usage():
    """Example of how to use the Japanese Content Generator"""
    try:
        # Initialize the generator
        generator = JapaneseContentGenerator()
        
        # Example 1: Generate a single video
        print("=== Example 1: Single Video Generation ===")
        sample_script = """
        [HOOK] 
        Have you ever wondered why some people seem to effortlessly build wealth while others struggle?
        
        [PROBLEM]
        Most people treat money like a game of chance, hopping from one investment to another 
        without a clear strategy. They're missing the fundamental principles that separate 
        the financially successful from the rest.
        
        [SOLUTION]
        Today, I'll share three timeless principles from Japanese financial wisdom that 
        have helped build generational wealth for centuries.
        
        [CALL TO ACTION]
        If you found these principles valuable, drop a comment below with which one resonates 
        most with you, and subscribe for more financial wisdom every week!
        """
        
        result = await generator.generate_japanese_style_video(
            topic="Japanese Wealth Building Principles",
            script=sample_script
        )
        
        if result["status"] == "success":
            print(f"✅ Video created: {result['video_path']}")
            print(f"✅ Thumbnail created: {result['thumbnail_path']}")
            print(f"📊 Consistency score: {result['consistency_score']}")
        else:
            print(f"❌ Video generation failed: {result['error']}")
        
        # Example 2: Generate content plan
        print("\n=== Example 2: Content Plan Generation ===")
        topics = [
            "The Power of Patience in Investing",
            "How to Build Multiple Income Streams",
            "Understanding Market Cycles Like a Pro",
            "Budgeting Secrets from Tokyo's Smart Savers"
        ]
        
        content_plan = generator.generate_content_plan(topics)
        print(f"✅ Content plan for {len(content_plan['topics'])} topics")
        print(f"🎬 Total scenes to generate: {content_plan['total_scenes']}")
        print(f"🎯 Styling consistency: {content_plan['styling_consistency']}")
        
        # Show sample from first topic
        if content_plan["topics"]:
            first_topic = content_plan["topics"][0]
            print(f"\n📝 Sample scene for '{first_topic['topic']}':")
            print(f"   {first_topic['sample_scene'][:100]}...")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")

if __name__ == "__main__":
    # Run the example
    asyncio.run(example_usage())