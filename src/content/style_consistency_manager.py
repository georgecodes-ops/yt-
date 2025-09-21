import logging
from typing import Dict, List, Optional
import os
from PIL import Image
import numpy as np

class StyleConsistencyManager:
    """Manages visual consistency using reference images"""
    
    def __init__(self, reference_image_dir: str = "."):
        self.logger = logging.getLogger(__name__)
        self.reference_image_dir = reference_image_dir
        self.reference_images = self._load_reference_images()
        self.style_features = self._extract_style_features()
    
    def _load_reference_images(self) -> List[str]:
        """Load reference images from directory"""
        reference_images = []
        try:
            for filename in os.listdir(self.reference_image_dir):
                if filename.startswith("Lucid_Origin") and filename.endswith(('.jpg', '.png', '.jpeg')):
                    reference_images.append(os.path.join(self.reference_image_dir, filename))
            self.logger.info(f"Loaded {len(reference_images)} reference images")
        except Exception as e:
            self.logger.error(f"Failed to load reference images: {e}")
        return reference_images
    
    def _extract_style_features(self) -> Dict:
        """Extract key style features from reference images"""
        # This would typically use computer vision to extract:
        # - Color palette
        # - Composition patterns
        # - Visual motifs
        # - Character positions
        # For now, we'll use simulated features based on your images
        
        return {
            "color_palette": {
                "primary": ["#00FFFF", "#FF00FF", "#FFFF00"],  # Neon colors from your theme
                "background": "#0A0A0A",  # Dark backgrounds
                "accent": "#FFFFFF"  # Bright accents
            },
            "composition": {
                "focal_point": "center",
                "aspect_ratio": "16:9",
                "typical_elements": ["geometric_shapes", "neon_outlines", "cinematic_lighting"]
            },
            "character_style": {
                "pose": "professional_standing",
                "expression": "confident",
                "clothing": "modern_business_attire",
                "accessories": ["tablet", "charts", "glasses"]
            },
            "visual_effects": {
                "lighting": "dramatic_contrast",
                "textures": ["smooth_gradients", "sharp_lines"],
                "mood": "cinematic_professional"
            }
        }
    
    def apply_style_consistency(self, prompt: str) -> str:
        """Apply reference style to generation prompt"""
        # Add style guidance based on reference images
        style_guidance = f"""
        Style reference: Cinematic professional look with neon accents,
        Color palette: {', '.join(self.style_features['color_palette']['primary'])},
        Composition: {self.style_features['composition']['focal_point']} focus,
        Character style: {self.style_features['character_style']['pose']} pose,
        Visual effects: {self.style_features['visual_effects']['lighting']} lighting,
        Overall mood: {self.style_features['visual_effects']['mood']}
        """
        
        return f"{prompt}, {style_guidance}"
    
    def get_brand_consistent_thumbnail_prompt(self, topic: str) -> str:
        """Generate brand-consistent thumbnail prompt"""
        base_prompt = f"Professional finance thumbnail, {topic}"
        return self.apply_style_consistency(base_prompt)
    
    def get_brand_consistent_character_prompt(self, character_type: str = "finance_expert") -> str:
        """Generate brand-consistent character prompt using reference style"""
        character_prompts = {
            "finance_expert": "Professional financial advisor, modern business attire, confident expression",
            "crypto_trader": "Modern crypto trader, tech-forward appearance, analytical expression",
            "budget_coach": "Friendly budget coach, approachable appearance, encouraging expression"
        }
        
        base_prompt = character_prompts.get(character_type, character_prompts["finance_expert"])
        return self.apply_style_consistency(base_prompt)
    
    def validate_reference_images(self) -> bool:
        """Validate that reference images are available and readable"""
        if not self.reference_images:
            self.logger.warning("No reference images found")
            return False
        
        all_valid = True
        for img_path in self.reference_images:
            try:
                with Image.open(img_path) as img:
                    img.verify()
            except Exception as e:
                self.logger.error(f"Invalid reference image {img_path}: {e}")
                all_valid = False
        
        return all_valid
    
    def get_reference_image_paths(self) -> List[str]:
        """Get paths to all reference images"""
        return self.reference_images
    
    def get_style_features(self) -> Dict:
        """Get extracted style features"""
        return self.style_features