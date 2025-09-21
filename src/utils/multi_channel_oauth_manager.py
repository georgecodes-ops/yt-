from typing import Dict

class MultiChannelOAuthManager:
    def __init__(self):
        self.channel_tokens = {}
        self.channel_configs = {}
    
    def setup_new_channel(self, channel_name: str, niche: str) -> Dict:
        """Setup OAuth for new channel"""
        
        print(f"🔧 Setting up OAuth for {channel_name} ({niche})...")
        
        # Generate unique token filename
        token_filename = f"youtube_tokens_{channel_name.lower().replace(' ', '_')}.json"
        
        setup_instructions = {
            "step_1": "Create YouTube channel manually in YouTube Studio",
            "step_2": f"Run: python src/get_youtube_tokens.py --output {token_filename}",
            "step_3": "Select the new channel during OAuth flow",
            "step_4": f"Update config.yaml with new channel entry",
            "token_file": token_filename,
            "niche": niche
        }
        
        return setup_instructions
    
    def validate_channel_separation(self) -> bool:
        """Ensure each channel has separate OAuth tokens"""
        
        token_files = []
        for channel_id, config in self.channel_configs.items():
            if config["token_file"] in token_files:
                print(f"❌ Duplicate token file detected for {channel_id}")
                return False
            token_files.append(config["token_file"])
        
        print("✅ All channels have separate OAuth tokens")
        return True