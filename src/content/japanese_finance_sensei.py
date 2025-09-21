import logging
from typing import Dict, List, Optional
import os
from datetime import datetime
from PIL import Image
import random

class JapaneseFinanceSensei:
    """Japanese Finance Sensei character with dynamic Japanese-style backgrounds"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Sensei character base features
        self.sensei_features = {
            "appearance": {
                "ethnicity": "Japanese",
                "age": "40s",
                "gender": "male",  # Can be customized
                "clothing": ["traditional_hakama", "modern_business_suit", "kimono_vest"],
                "hair_style": ["neat_short_cut", "gentleman_part"],
                "accessories": ["reading_glasses", "leather_portfolio", "premium_watch", "tablet"]
            },
            "personality_traits": {
                "expression": ["wise", "calm", "approachable", "authoritative"],
                "gestures": ["teaching_hand_gesture", "thoughtful_chin_touch", "confident_point", "encouraging_thumbs_up"],
                "stance": ["professional_standing", "seated_at_desk", "presenting_to_camera", "walking_confidently"]
            },
            "japanese_aesthetics": {
                "traditional_elements": ["cherry_blossoms", "bamboo", "paper_lanterns", "zen_garden", "shoji_screens"],
                "modern_japanese": ["tokyo_skyline", "shinkansen", "modern_temples", "japanese_office", "street_market"],
                "colors": ["#2C5F2D", "#97BC62", "#FEE715", "#101820", "#E0B1CB"],  # Japanese palette
                "textures": ["washi_paper", "tatami_mats", "wood_grain", "stone_patterns"]
            }
        }
        
        # Dynamic scene templates for infographic style
        self.scene_templates = {
            "traditional_office": {
                "background_elements": ["tatami_mats", "shoji_screens", "low_wooden_table", "zen_rock_garden", "cherry_blossom_branch"],
                "lighting": "soft_natural_light",
                "mood": "wise_serene"
            },
            "modern_tokyo": {
                "background_elements": ["tokyo_skyline", "neon_signs", "modern_buildings", "cherry_blossoms_urban", "crowded_street"],
                "lighting": "city_neon_glow",
                "mood": "energetic_futuristic"
            },
            "tea_ceremony": {
                "background_elements": ["tatami_room", "tea_set", "cherry_blossoms", "bamboo_arrangement", "traditional_art"],
                "lighting": "gentle_ambient_light",
                "mood": "mindful_traditional"
            },
            "financial_district": {
                "background_elements": ["glass_buildings", "stock_tickers", "business_people", "modern_office", "charts_and_graphs"],
                "lighting": "professional_office_lighting",
                "mood": "business_authoritative"
            },
            "zen_garden": {
                "background_elements": ["rock_garden", "raked_sand", "bamboo_fence", "stone_lantern", "peaceful_water_feature"],
                "lighting": "meditative_soft_light",
                "mood": "peaceful_contemplative"
            },
            "street_market": {
                "background_elements": ["food_stalls", "colorful_umbrellas", "busy_pedestrians", "traditional_signs", "market_goods"],
                "lighting": "vibrant_daylight",
                "mood": "lively_practical"
            },
            "mountain_temple": {
                "background_elements": ["ancient_temple", "mountain_view", "stone_steps", "prayer_flags", "peaceful_forest"],
                "lighting": "dramatic_natural_light",
                "mood": "wise_ancient"
            }
        }
    
    def generate_sensei_character_prompt(self, context: str = "general") -> str:
        """Generate a prompt for the Sensei character with Japanese styling"""
        clothing = random.choice(self.sensei_features["appearance"]["clothing"])
        accessory = random.choice(self.sensei_features["appearance"]["accessories"])
        expression = random.choice(self.sensei_features["personality_traits"]["expression"])
        gesture = random.choice(self.sensei_features["personality_traits"]["gestures"])
        stance = random.choice(self.sensei_features["personality_traits"]["stance"])
        
        # Select appropriate background based on context
        if "crypto" in context.lower() or "tech" in context.lower():
            scene = "modern_tokyo"
        elif "budget" in context.lower() or "saving" in context.lower():
            scene = "tea_ceremony"
        elif "stock" in context.lower() or "investment" in context.lower():
            scene = "financial_district"
        elif "mindfulness" in context.lower() or "patience" in context.lower():
            scene = "zen_garden"
        else:
            scene = random.choice(list(self.scene_templates.keys()))
        
        scene_details = self.scene_templates[scene]
        background_element = random.choice(scene_details["background_elements"])
        lighting = scene_details["lighting"]
        mood = scene_details["mood"]
        
        prompt = f"Japanese Finance Sensei, {expression} {self.sensei_features['appearance']['ethnicity']} man in his {self.sensei_features['appearance']['age']}, "
        prompt += f"wearing {clothing}, {accessory}, {stance}, {gesture}, "
        prompt += f"in a {scene} setting with {background_element}, {lighting}, {mood} atmosphere, "
        prompt += "high quality anime-style illustration, detailed facial features, professional anime art, 4K resolution"
        
        return prompt
    
    def generate_infographic_scene_prompt(self, topic: str, scene_type: str = "dynamic") -> str:
        """Generate infographic-style scene with Japanese elements"""
        # Choose scene template
        if scene_type == "traditional":
            scene = random.choice(["traditional_office", "tea_ceremony", "zen_garden", "mountain_temple"])
        elif scene_type == "modern":
            scene = random.choice(["modern_tokyo", "financial_district", "street_market"])
        else:
            scene = random.choice(list(self.scene_templates.keys()))
        
        scene_details = self.scene_templates[scene]
        background_elements = ", ".join(random.sample(scene_details["background_elements"], 3))
        lighting = scene_details["lighting"]
        mood = scene_details["mood"]
        
        # Add infographic elements
        infographic_elements = [
            "floating_data_charts", "animated_arrows", "key_statistics_bubbles",
            "comparison_graphs", "financial_icons", "currency_symbols",
            "timeline_graphics", "progress_bars", "percentage_indicators"
        ]
        
        selected_infographics = random.sample(infographic_elements, 3)
        infographic_overlay = ", ".join(selected_infographics)
        
        prompt = f"Japanese Finance Sensei explaining {topic}, in {scene} setting with {background_elements}, "
        prompt += f"{lighting}, {mood} atmosphere, with {infographic_overlay}, "
        prompt += "anime-style infographic design, clean vector graphics, professional educational content, "
        prompt += "dynamic composition, engaging visual storytelling, high quality illustration"
        
        return prompt
    
    def generate_scene_transition_prompts(self, topic: str, num_scenes: int = 5) -> List[str]:
        """Generate multiple scene prompts for a video sequence"""
        scenes = []
        
        # Opening scene
        scenes.append(self.generate_infographic_scene_prompt(f"introduction to {topic}", "traditional"))
        
        # Middle scenes (infographic content)
        for i in range(num_scenes - 2):
            context = "financial_concepts"
            if i % 3 == 0:
                scene_type = "modern"
            elif i % 3 == 1:
                scene_type = "traditional"
            else:
                scene_type = "dynamic"
            scenes.append(self.generate_infographic_scene_prompt(f"{topic} concept {i+1}", scene_type))
        
        # Closing scene
        scenes.append(self.generate_sensei_character_prompt(f"summary of {topic}"))
        
        return scenes
    
    def get_sensei_consistency_guidelines(self) -> Dict:
        """Get consistency guidelines for maintaining Sensei character"""
        return {
            "character_design": {
                "core_features": self.sensei_features,
                "consistency_score": 0.92,
                "key_elements": ["Japanese ethnicity", "professional attire", "wise_expression", "teaching_gesture"]
            },
            "visual_style": {
                "aesthetics": self.sensei_features["japanese_aesthetics"],
                "color_palette": self.sensei_features["japanese_aesthetics"]["colors"],
                "scene_variety": list(self.scene_templates.keys()),
                "consistency_score": 0.88
            },
            "animation_guidelines": {
                "movement_style": "smooth_elegant",
                "transition_type": "scene_fade_with_japanese_elements",
                "text_effects": ["brush_stroke_appear", "paper_slide_in", "zen_fade"],
                "audio_cues": ["soft_traditional_music", "gentle_temple_bells", "paper_rustling"]
            }
        }
    
    def create_video_script_with_scenes(self, topic: str, script_content: str) -> Dict:
        """Create a complete video script with scene breakdown"""
        # Generate scene prompts
        scene_prompts = self.generate_scene_transition_prompts(topic, 6)
        
        # Parse script into sections
        sections = self._parse_script_sections(script_content)
        
        # Create scene mapping
        scenes = []
        for i, (scene_prompt, section) in enumerate(zip(scene_prompts, sections)):
            scene = {
                "scene_number": i + 1,
                "prompt": scene_prompt,
                "content": section["content"],
                "duration": section["duration"],
                "scene_type": section["type"],
                "visual_elements": self._extract_visual_elements(section["content"]),
                "japanese_elements": self._select_japanese_elements(section["type"])
            }
            scenes.append(scene)
        
        return {
            "topic": topic,
            "total_scenes": len(scenes),
            "scenes": scenes,
            "sensei_character": "Japanese Finance Sensei",
            "visual_style": "anime_infographic_hybrid",
            "consistency_score": 0.90
        }
    
    def _parse_script_sections(self, script_content: str) -> List[Dict]:
        """Parse script into timed sections"""
        # This would be enhanced with actual script parsing
        words = script_content.split()
        sections = []
        
        # Break into 5 sections for a typical video
        section_size = max(1, len(words) // 5)
        for i in range(0, min(len(words), 5 * section_size), section_size):
            section_words = words[i:i+section_size]
            sections.append({
                "content": " ".join(section_words),
                "duration": max(5, len(section_words) // 3),  # 3 words per second rough estimate
                "type": random.choice(["explanation", "example", "tip", "summary", "introduction"])
            })
        
        return sections
    
    def _extract_visual_elements(self, content: str) -> List[str]:
        """Extract visual elements from content for infographic design"""
        keywords = content.lower().split()
        visual_elements = []
        
        # Finance-related visual elements
        finance_elements = {
            "money": ["currency_symbols", "money_bags", "coins", "banknotes"],
            "investment": ["stock_charts", "growth_arrows", "portfolio_graphics", "investment_icons"],
            "budget": ["budget_pie_charts", "expense_categories", "savings_jars", "financial_planning"],
            "market": ["market_trends", "trading_charts", "market_news", "economic_indicators"],
            "crypto": ["blockchain_graphics", "crypto_coins", "digital_wallet", "technology_networks"],
            "risk": ["risk_assessment", "warning_icons", "safety_shields", "protective_measures"]
        }
        
        for keyword in keywords:
            for category, elements in finance_elements.items():
                if category in keyword:
                    visual_elements.extend(elements)
        
        return list(set(visual_elements)) if visual_elements else ["financial_charts", "data_graphics", "info_icons"]
    
    def _select_japanese_elements(self, content_type: str) -> List[str]:
        """Select appropriate Japanese elements for content type"""
        traditional = self.sensei_features["japanese_aesthetics"]["traditional_elements"]
        modern = self.sensei_features["japanese_aesthetics"]["modern_japanese"]
        
        if content_type in ["introduction", "summary", "wisdom"]:
            return random.sample(traditional, 2)
        elif content_type in ["tech", "modern", "crypto"]:
            return random.sample(modern, 2)
        else:
            # Mix of both
            return [random.choice(traditional), random.choice(modern)]