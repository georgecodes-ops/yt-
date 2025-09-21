import hashlib
import json
import os
from typing import Dict, List, Set
from datetime import datetime, timedelta
import logging

class ContentDeduplicationManager:
    """Prevents duplicate video content and ensures uniqueness"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.content_database = "content_history.json"
        self.similarity_threshold = 0.85
        self.content_history = self._load_content_history()
        
    def _load_content_history(self) -> Dict:
        """Load existing content history"""
        if os.path.exists(self.content_database):
            with open(self.content_database, 'r') as f:
                data = json.load(f)
                # Convert lists back to sets
                data["title_hashes"] = set(data.get("title_hashes", []))
                data["content_hashes"] = set(data.get("content_hashes", []))
                return data
        return {"videos": [], "title_hashes": set(), "content_hashes": set()}
    
    def _save_content_history(self):
        """Save content history to file"""
        # Convert sets to lists for JSON serialization
        save_data = {
            "videos": self.content_history["videos"],
            "title_hashes": list(self.content_history["title_hashes"]),
            "content_hashes": list(self.content_history["content_hashes"])
        }
        with open(self.content_database, 'w') as f:
            json.dump(save_data, f, indent=2)
    
    def check_duplicate(self, content: Dict) -> Dict:
        """Check if content is duplicate"""
        title = content.get('title', '')
        description = content.get('description', '')
        script = content.get('script', '')
        
        # Generate content hashes
        title_hash = hashlib.md5(title.lower().strip().encode()).hexdigest()
        content_text = f"{title} {description} {script}"
        content_hash = hashlib.md5(content_text.lower().strip().encode()).hexdigest()
        
        # Check for exact duplicates
        if title_hash in self.content_history["title_hashes"]:
            return {
                "is_duplicate": True,
                "duplicate_type": "exact_title",
                "reason": "Identical title found in history"
            }
        
        if content_hash in self.content_history["content_hashes"]:
            return {
                "is_duplicate": True,
                "duplicate_type": "exact_content",
                "reason": "Identical content found in history"
            }
        
        # Check for similar content
        similarity_check = self._check_content_similarity(content)
        if similarity_check["is_similar"]:
            return {
                "is_duplicate": True,
                "duplicate_type": "similar_content",
                "reason": f"Similar content found: {similarity_check['similarity_score']:.2f}",
                "similar_video": similarity_check["similar_video"]
            }
        
        return {"is_duplicate": False}
    
    def register_content(self, content: Dict) -> str:
        """Register new content to prevent future duplicates"""
        content_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        title = content.get('title', '')
        description = content.get('description', '')
        script = content.get('script', '')
        
        # Generate hashes
        title_hash = hashlib.md5(title.lower().strip().encode()).hexdigest()
        content_text = f"{title} {description} {script}"
        content_hash = hashlib.md5(content_text.lower().strip().encode()).hexdigest()
        
        # Store content record
        content_record = {
            "id": content_id,
            "title": title,
            "title_hash": title_hash,
            "content_hash": content_hash,
            "created_at": datetime.now().isoformat(),
            "topic": content.get('topic', ''),
            "format_type": content.get('format_type', 'unknown')
        }
        
        self.content_history["videos"].append(content_record)
        self.content_history["title_hashes"].add(title_hash)
        self.content_history["content_hashes"].add(content_hash)
        
        self._save_content_history()
        self.logger.info(f"Registered new content: {content_id}")
        
        return content_id
    
    def _check_content_similarity(self, new_content: Dict) -> Dict:
        """Check similarity with existing content"""
        new_title = new_content.get('title', '').lower()
        new_words = set(new_title.split())
        
        for video in self.content_history["videos"]:
            existing_title = video.get('title', '').lower()
            existing_words = set(existing_title.split())
            
            # Calculate Jaccard similarity
            if len(new_words) > 0 and len(existing_words) > 0:
                intersection = len(new_words.intersection(existing_words))
                union = len(new_words.union(existing_words))
                similarity = intersection / union if union > 0 else 0
                
                if similarity >= self.similarity_threshold:
                    return {
                        "is_similar": True,
                        "similarity_score": similarity,
                        "similar_video": video
                    }
        
        return {"is_similar": False}
    
    def cleanup_old_content(self, days_to_keep: int = 90):
        """Remove old content records to prevent database bloat"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        original_count = len(self.content_history["videos"])
        
        # Filter out old videos
        self.content_history["videos"] = [
            video for video in self.content_history["videos"]
            if datetime.fromisoformat(video["created_at"]) > cutoff_date
        ]
        
        # Rebuild hash sets
        self.content_history["title_hashes"] = {
            video["title_hash"] for video in self.content_history["videos"]
        }
        self.content_history["content_hashes"] = {
            video["content_hash"] for video in self.content_history["videos"]
        }
        
        removed_count = original_count - len(self.content_history["videos"])
        self.logger.info(f"Cleaned up {removed_count} old content records")
        
        self._save_content_history()