import logging
from typing import Any, Dict, Union

class SmartContentFixer:
    @staticmethod
    def safe_script_operation(script: Union[str, Dict], operation: str) -> Union[str, Dict]:
        """Safely perform operations on script regardless of type"""
        if isinstance(script, dict):
            # Extract text from dict
            script_text = script.get('script', '') or script.get('content', '') or str(script)
            
            # Perform operation on text
            if operation == "add_hooks":
                script_text = f"🔥 VIRAL: {script_text}\n\nDrop a comment if this helped!"
            elif operation == "pattern_interrupt":
                if "." in script_text:
                    script_text = script_text.replace(".", ". But here's the secret...", 1)
            
            # Return updated dict
            result = script.copy()
            if 'script' in result:
                result['script'] = script_text
            elif 'content' in result:
                result['content'] = script_text
            else:
                result['script'] = script_text
            return result
        else:
            # Handle as string
            script_text = script or ""
            if operation == "add_hooks":
                return f"🔥 VIRAL: {script_text}\n\nDrop a comment if this helped!"
            elif operation == "pattern_interrupt":
                if "." in script_text:
                    return script_text.replace(".", ". But here's the secret...", 1)
            return script_text
    
    @staticmethod
    def ensure_output_quality(content_data: Dict) -> Dict:
        """Ensure all content fields have meaningful values"""
        defaults = {
            'title': 'Engaging Content Title',
            'description': 'Compelling description that drives engagement',
            'script': 'High-quality script content',
            'tags': ['trending', 'viral', 'engaging'],
            'viral_score': 75.0
        }
        
        for key, default_value in defaults.items():
            if not content_data.get(key) or content_data[key] == "":
                content_data[key] = default_value
                logging.warning(f"Filled missing {key} with default value")
        
        return content_data