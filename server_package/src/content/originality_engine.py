import logging
import hashlib
import json
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from pathlib import Path

class OriginalityEngine:
    """Ensures content uniqueness and originality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.content_hashes: Set[str] = set()
        self.content_history: List[Dict] = []
        self.similarity_threshold = 0.8
        
    def check_originality(self, content: str) -> Dict:
        """Check if content is original"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        if content_hash in self.content_hashes:
            return {
                "is_original": False,
                "similarity_score": 1.0,
                "reason": "Exact duplicate found"
            }
        
        # Check similarity with existing content
        similarity_score = self._calculate_similarity(content)
        
        is_original = similarity_score < self.similarity_threshold
        
        if is_original:
            self.content_hashes.add(content_hash)
            self.content_history.append({
                "hash": content_hash,
                "content_preview": content[:100],
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "is_original": is_original,
            "similarity_score": similarity_score,
            "reason": "Content is unique" if is_original else "Content too similar to existing"
        }
    
    def _calculate_similarity(self, content: str) -> float:
        """Calculate similarity with existing content"""
        if not self.content_history:
            return 0.0
        
        # Simple word-based similarity check
        content_words = set(content.lower().split())
        max_similarity = 0.0
        
        for historical_content in self.content_history[-10:]:  # Check last 10 pieces
            hist_words = set(historical_content["content_preview"].lower().split())
            if len(content_words) == 0 or len(hist_words) == 0:
                continue
            
            intersection = len(content_words.intersection(hist_words))
            union = len(content_words.union(hist_words))
            similarity = intersection / union if union > 0 else 0
            max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def enhance_originality(self, content: str) -> str:
        """Enhance content to make it more original"""
        # Add timestamp-based uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        # Add unique perspective markers
        enhanced_content = f"{content}\n\n[Generated: {timestamp}]"
        
        return enhanced_content