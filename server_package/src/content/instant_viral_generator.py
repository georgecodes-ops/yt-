import logging
from typing import Dict, List, Optional
from datetime import datetime
import random

class InstantViralGenerator:
    """Generates viral content instantly based on trending topics"""
    
    def __init__(self, brand_manager=None):
        self.logger = logging.getLogger(__name__)
        self.brand_manager = brand_manager
        
        self.viral_formulas = {
            "curiosity_gap": "You won't believe what happens when {topic}",
            "social_proof": "99% of people don't know this {topic} secret",
            "urgency": "This {topic} trick is going viral (try before it's banned)",
            "controversy": "Why {topic} is actually bad for you",
            "transformation": "How {topic} changed my life in 30 days"
        }
        
        self.trending_topics = [
            "AI investing", "crypto trading", "passive income", 
            "stock market", "financial freedom", "side hustles"
        ]
    
    def generate_viral_title(self, topic: Optional[str] = None) -> str:
        """Generate viral title using proven formulas"""
        if not topic:
            topic = random.choice(self.trending_topics)
            
        formula_key = random.choice(list(self.viral_formulas.keys()))
        formula = self.viral_formulas[formula_key]
        
        return formula.format(topic=topic)
    
    def create_viral_shorts_package(self, topic: Optional[str] = None) -> Dict:
        """Create complete viral Shorts package"""
        if not topic:
            topic = random.choice(self.trending_topics)
            
        title = self.generate_viral_title(topic)
        
        script = f"""
        HOOK (0-3s): {title}
        
        PROBLEM (3-15s): Most people are doing {topic} completely wrong...
        
        SOLUTION (15-45s): Here's the exact method that actually works:
        Step 1: [Specific action]
        Step 2: [Specific action] 
        Step 3: [Specific action]
        
        PROOF (45-55s): I've used this to [specific result]
        
        CTA (55-60s): Follow for more! Comment 'YES' if you want the full guide!
        """
        
        thumbnail_text = f"{topic.upper()} SECRET REVEALED"
        
        description = f"""
        {title}
        
        In this video, I reveal the exact {topic} strategy that changed everything.
        
        TIMESTAMPS:
        0:00 - The Problem
        0:15 - The Solution
        0:45 - Proof It Works
        
        FOLLOW FOR MORE:
        - Daily finance tips
        - Investment strategies
        - Wealth building secrets
        
        #shorts #{topic.replace(' ', '')} #investing #money #wealth
        """
        
        return {
            "title": title,
            "script": script,
            "thumbnail_text": thumbnail_text,
            "description": description,
            "topic": topic,
            "viral_score": random.randint(7, 10),
            "created_at": datetime.now().isoformat()
        }
    
    def generate_content_series(self, main_topic: str, count: int = 7) -> List[Dict]:
        """Generate a series of viral content for a week"""
        series = []
        
        for i in range(count):
            # Vary the topic slightly for each video
            variations = [
                f"{main_topic} for beginners",
                f"advanced {main_topic}",
                f"{main_topic} mistakes",
                f"{main_topic} secrets",
                f"{main_topic} strategy",
                f"{main_topic} tips",
                f"{main_topic} guide"
            ]
            
            topic_variation = variations[i % len(variations)]
            package = self.create_viral_shorts_package(topic_variation)
            package["series_position"] = i + 1
            package["series_total"] = count
            
            series.append(package)
            
        return series
