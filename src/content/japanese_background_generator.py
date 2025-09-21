import logging
from typing import Dict, List, Optional
import random
import os
from datetime import datetime

class JapaneseBackgroundGenerator:
    """Dynamic generator for Japanese-style backgrounds with infographic elements"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Japanese background elements
        self.japanese_elements = {
            "traditional": {
                "nature": ["cherry_blossoms", "bamboo_forest", "maple_leaves", "mountain_views", "water_features"],
                "architecture": ["shoji_screens", "tatami_mats", "paper_lanterns", "torii_gates", "stone_lanterns"],
                "cultural": ["zen_rock_garden", "tea_ceremony_setup", "calligraphy_brush", "traditional_art", "koi_pond"],
                "colors": ["#FFD1DC", "#97BC62", "#2C5F2D", "#FEE715", "#101820"],  # Sakura, bamboo, traditional
                "textures": ["washi_paper", "tatami_texture", "wood_grain", "stone_patterns", "fabric_weave"]
            },
            "modern": {
                "urban": ["tokyo_skyline", "neon_signs", "shinkansen", "modern_buildings", "crowded_streets"],
                "technology": ["digital_displays", "holographic_interfaces", "futuristic_panels", "tech_screens", "data_streams"],
                "business": ["financial_district", "glass_towers", "business_people", "stock_tickers", "corporate_offices"],
                "colors": ["#00BCD4", "#2196F3", "#9C27B0", "#FF9800", "#4CAF50"],  # Modern, vibrant
                "textures": ["glass_reflection", "neon_glows", "digital_pixels", "metal_brushed", "concrete_smooth"]
            }
        }
        
        # Infographic elements that can be combined with Japanese backgrounds
        self.infographic_elements = {
            "charts": ["floating_pie_charts", "bar_graphs", "line_charts", "scatter_plots", "infographic_icons"],
            "data": ["percentage_bubbles", "statistic_cards", "progress_indicators", "comparison_arrows", "trend_lines"],
            "finance": ["currency_symbols", "investment_icons", "banking_graphics", "market_indicators", "risk_assessment"],
            "ui": ["interactive_buttons", "slide_controls", "notification_bubbles", "progress_bars", "menu_systems"]
        }
    
    def generate_background_prompt(self, scene_type: str = "mixed", topic: str = "finance") -> str:
        """Generate a prompt for Japanese-style background with infographic elements"""
        
        # Select elements based on scene type
        if scene_type == "traditional":
            elements = self.japanese_elements["traditional"]
            style = "traditional Japanese aesthetic"
        elif scene_type == "modern":
            elements = self.japanese_elements["modern"]
            style = "modern Japanese urban style"
        else:
            # Mixed traditional and modern
            nature_element = random.choice(self.japanese_elements["traditional"]["nature"])
            architecture_element = random.choice(self.japanese_elements["modern"]["urban"])
            cultural_element = random.choice(self.japanese_elements["traditional"]["cultural"])
            urban_element = random.choice(self.japanese_elements["modern"]["technology"])
            elements = {
                "combined": [nature_element, architecture_element, cultural_element, urban_element]
            }
            style = "fusion of traditional and modern Japanese elements"
        
        # Select infographic elements based on topic
        if "crypto" in topic.lower() or "tech" in topic.lower():
            infographic_type = "technology"
        elif "budget" in topic.lower() or "saving" in topic.lower():
            infographic_type = "finance"
        elif "market" in topic.lower() or "investment" in topic.lower():
            infographic_type = "charts"
        else:
            infographic_type = random.choice(list(self.infographic_elements.keys()))
        
        infographic_elements = random.sample(self.infographic_elements[infographic_type], 2)
        
        # Create prompt
        if scene_type in ["traditional", "modern"]:
            background_elements = random.sample(elements["nature"] + elements["architecture"] + elements["cultural"], 3)
        else:
            background_elements = elements["combined"]
        
        color_palette = random.sample(elements["colors"], 3)
        texture = random.choice(elements["textures"])
        
        prompt = f"Japanese {style} background with {', '.join(background_elements)}, "
        prompt += f"color palette of {', '.join(color_palette)}, {texture} texture, "
        prompt += f"combined with {', '.join(infographic_elements)} as floating infographic elements, "
        prompt += "professional anime-style illustration, clean design, cinematic composition, high detail, 4K quality"
        
        return prompt
    
    def generate_scene_sequence_prompts(self, topic: str, num_scenes: int = 5) -> List[str]:
        """Generate a sequence of background prompts for video scenes"""
        prompts = []
        
        # Ensure variety in scene types
        scene_types = ["traditional", "modern", "mixed"]
        
        for i in range(num_scenes):
            scene_type = scene_types[i % len(scene_types)]
            prompt = self.generate_background_prompt(scene_type, topic)
            prompts.append(prompt)
        
        return prompts
    
    def generate_transition_effect_prompt(self, from_scene: str, to_scene: str) -> str:
        """Generate prompt for transition effect between Japanese scenes"""
        transition_effects = [
            "dissolve_transition_with_cherry_blossom_petals",
            "slide_transition_with_paper_fan_effect",
            "fade_through_shoji_screen_pattern",
            "wipe_transition_with_zen_rock_garden_elements",
            "morph_transition_with_traditional_to_modern_style"
        ]
        
        effect = random.choice(transition_effects)
        prompt = f"Smooth {effect} from {from_scene} to {to_scene}, "
        prompt += "Japanese aesthetic transition, elegant animation, professional quality"
        
        return prompt
    
    def get_background_consistency_guidelines(self) -> Dict:
        """Get guidelines for maintaining background consistency"""
        return {
            "color_palettes": {
                "traditional": self.japanese_elements["traditional"]["colors"],
                "modern": self.japanese_elements["modern"]["colors"]
            },
            "element_combinations": {
                "allowed_combinations": [
                    "cherry_blossoms_with_floating_charts",
                    "bamboo_forest_with_digital_displays",
                    "tatami_mats_with_infographic_icons",
                    "tokyo_skyline_with_financial_graphs"
                ],
                "consistency_score": 0.90
            },
            "scene_variety": {
                "scene_types": ["traditional", "modern", "mixed"],
                "guaranteed_diversity": True,
                "visual_cohesion": "Japanese aesthetic throughout"
            }
        }
    
    def generate_thumbnail_background_prompt(self, topic: str) -> str:
        """Generate a Japanese-style thumbnail background"""
        # Combine striking traditional and modern elements
        traditional_element = random.choice(self.japanese_elements["traditional"]["nature"])
        modern_element = random.choice(self.japanese_elements["modern"]["urban"])
        color_accent = random.choice(self.japanese_elements["modern"]["colors"])
        
        # Add attention-grabbing infographic elements
        infographic_element = random.choice(self.infographic_elements["finance"] + self.infographic_elements["charts"])
        
        prompt = f"Japanese style YouTube thumbnail background with {traditional_element} and {modern_element}, "
        prompt += f"accented with {color_accent}, featuring {infographic_element}, "
        prompt += "bold composition, high contrast, eye-catching design, professional anime illustration style, 16:9 aspect ratio"
        
        return prompt
    
    def generate_character_background_prompt(self, character_context: str = "teaching") -> str:
        """Generate background appropriate for the Sensei character"""
        if character_context == "wisdom" or character_context == "traditional":
            scene_type = "traditional"
            main_element = random.choice(self.japanese_elements["traditional"]["cultural"])
            secondary_element = random.choice(self.japanese_elements["traditional"]["nature"])
        elif character_context == "modern" or character_context == "tech":
            scene_type = "modern"
            main_element = random.choice(self.japanese_elements["modern"]["business"])
            secondary_element = random.choice(self.japanese_elements["modern"]["urban"])
        else:
            scene_type = "mixed"
            main_element = random.choice(self.japanese_elements["traditional"]["cultural"])
            secondary_element = random.choice(self.japanese_elements["modern"]["business"])
        
        colors = self.japanese_elements[scene_type]["colors"] if scene_type in ["traditional", "modern"] else (
            self.japanese_elements["traditional"]["colors"] + self.japanese_elements["modern"]["colors"]
        )
        color_palette = random.sample(colors, 2)
        
        prompt = f"Japanese Finance Sensei background with {main_element} and {secondary_element}, "
        prompt += f"color scheme of {', '.join(color_palette)}, "
        prompt += "professional educational setting, anime illustration style, respectful atmosphere, high quality"
        
        return prompt