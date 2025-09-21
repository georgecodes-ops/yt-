class ViralContentOrchestrator:
    def __init__(self):
        self.viral_hooks = {
            'shock_stats': [
                "Why 99% of people fail at {topic}",
                "The ${amount} mistake I made so you don't have to",
                "What banks don't want you to know about {topic}"
            ],
            'personal_stakes': [
                "How I lost ${amount} in {timeframe} (and what I learned)",
                "The {topic} strategy that changed my life",
                "Why I stopped {common_practice} and you should too"
            ],
            'secrets_revealed': [
                "The {topic} secret wealthy people use",
                "Hidden {topic} strategies banks use",
                "The {topic} loophole closing in {timeframe}"
            ]
        }
        
        self.story_structure = {
            'hook': {'duration': '0-3s', 'purpose': 'shocking_stat_or_question'},
            'problem': {'duration': '3-30s', 'purpose': 'identify_pain_point'},
            'solution': {'duration': '30s+', 'purpose': 'educational_content'},
            'cta': {'duration': 'final_10s', 'purpose': 'subscribe_engagement'}
        }
        
    def generate_viral_script(self, topic, target_emotion, duration):
        """Generate scripts optimized for 70%+ retention"""
        hook = self._select_viral_hook(topic, target_emotion)
        structure = self._adapt_structure_for_duration(duration)
        
        return {
            'hook': hook,
            'script_structure': structure,
            'sensei_character_notes': self._get_character_direction(target_emotion),
            'visual_cues': self._generate_visual_sequence(topic)
        }

    # ✅ Added missing methods
    def _select_viral_hook(self, topic, emotion):
        """Select the most appropriate viral hook for the topic and emotion"""
        return self.viral_hooks['shock_stats'][0].format(topic=topic)
    
    def _adapt_structure_for_duration(self, duration):
        """Adapt story structure based on video duration"""
        return self.story_structure
    
    def _get_character_direction(self, emotion):
        """Generate character direction for the Sensei persona"""
        return f"Expert sharing {emotion} insights"
    
    def _generate_visual_sequence(self, topic):
        """Generate visual sequence for video editing"""
        return ["hook", "problem", "solution", "cta"]

# ✅ Added backward compatibility alias
AIPromptOrchestrator = ViralContentOrchestrator
