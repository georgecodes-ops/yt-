import json
import requests
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime, timedelta
import os
from dataclasses import dataclass

@dataclass
class ModelPerformance:
    model_name: str
    success_rate: float
    avg_response_time: float
    error_count: int
    last_used: datetime
    cost_per_request: float
    quality_score: float

class AdaptiveModelManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.performance_data = {}
        self.model_configs = self._load_model_configs()
        self.fallback_order = []
        self._update_fallback_order()
        
    def _load_model_configs(self) -> Dict[str, Dict]:
        """Load model configurations dynamically"""
        return {
            'wan_mistral': {
                'enabled': True,
                'models': ['microsoft/DialoGPT-large', 'EleutherAI/gpt-neo-2.7B'],
                'api_key': os.getenv('WAN_API_TOKEN'),
                'endpoint': 'wan://local/',
                'max_tokens': 2000,
                'cost_per_1k_tokens': 0.0,
                'quality_tier': 3
            },
            'ollama': {
                'enabled': True,
                'models': ['mistral'],
                'endpoint': 'http://localhost:11434/api/generate',
                'max_tokens': 4000,
                'cost_per_1k_tokens': 0.0,
                'quality_tier': 2
            }
        }
    
    def get_best_model(self, task_type: str = 'general', budget_limit: float = None) -> str:
        """Get the best performing model for a specific task"""
        try:
            # Filter available models
            available_models = self._get_available_models()
            
            if not available_models:
                return self._get_emergency_fallback()
            
            # Apply budget filter if specified
            if budget_limit:
                available_models = [m for m in available_models 
                                  if self.model_configs[m]['cost_per_1k_tokens'] <= budget_limit]
            
            # Get task-specific preferences
            task_weights = self._get_task_weights(task_type)
            
            # Score models based on performance and task requirements
            model_scores = {}
            for model in available_models:
                score = self._calculate_model_score(model, task_weights)
                model_scores[model] = score
            
            # Return best scoring model
            if model_scores:
                best_model = max(model_scores, key=lambda k: model_scores[k])
                self.logger.info(f"Selected model {best_model} for task {task_type}")
                return best_model
            
            return self._get_emergency_fallback()
            
        except Exception as e:
            self.logger.error(f"Error selecting model: {e}")
            return self._get_emergency_fallback()
    
    def _get_available_models(self) -> List[str]:
        """Get list of enabled models"""
        available = []
        for model_name, config in self.model_configs.items():
            if config.get('enabled', False):
                available.append(model_name)
        return available
    
    def _get_task_weights(self, task_type: str) -> Dict[str, float]:
        """Get scoring weights for different task types"""
        task_weights = {
            'content_generation': {
                'quality_score': 0.4,
                'success_rate': 0.3,
                'response_time': 0.2,
                'cost': 0.1
            },
            'analysis': {
                'quality_score': 0.5,
                'success_rate': 0.3,
                'response_time': 0.1,
                'cost': 0.1
            },
            'quick_tasks': {
                'response_time': 0.4,
                'success_rate': 0.3,
                'cost': 0.2,
                'quality_score': 0.1
            },
            'budget_conscious': {
                'cost': 0.5,
                'success_rate': 0.3,
                'quality_score': 0.1,
                'response_time': 0.1
            }
        }
        return task_weights.get(task_type, task_weights['content_generation'])
    
    def _calculate_model_score(self, model_name: str, weights: Dict[str, float]) -> float:
        """Calculate weighted score for a model"""
        perf = self.performance_data.get(model_name)
        config = self.model_configs[model_name]
        
        if not perf:
            # New model - use config-based scoring
            return self._score_new_model(config, weights)
        
        # Calculate weighted score
        score = 0
        score += weights.get('quality_score', 0) * perf.quality_score
        score += weights.get('success_rate', 0) * perf.success_rate
        score += weights.get('response_time', 0) * (1 / max(perf.avg_response_time, 0.1))  # Inverse for time
        score += weights.get('cost', 0) * (1 / max(perf.cost_per_request, 0.001))  # Inverse for cost
        
        return score
    
    def _score_new_model(self, config: Dict, weights: Dict[str, float]) -> float:
        """Score a model that hasn't been used yet"""
        # Base scoring on configuration
        quality_tier_score = {1: 0.9, 2: 0.7, 3: 0.5}.get(config['quality_tier'], 0.5)
        cost_score = 1 / max(config['cost_per_1k_tokens'], 0.001)
        
        score = 0
        score += weights.get('quality_score', 0) * quality_tier_score
        score += weights.get('success_rate', 0) * 0.8  # Assume 80% success for new models
        score += weights.get('response_time', 0) * 0.5  # Neutral response time score
        score += weights.get('cost', 0) * min(cost_score / 100, 1.0)  # Normalize cost score
        
        return score
    
    def record_model_performance(self, model_name: str, success: bool, 
                               response_time: float, cost: float, quality_score: float = 0.8):
        """Record performance metrics for a model"""
        if model_name not in self.performance_data:
            self.performance_data[model_name] = ModelPerformance(
                model_name=model_name,
                success_rate=0.0,
                avg_response_time=0.0,
                error_count=0,
                last_used=datetime.now(),
                cost_per_request=0.0,
                quality_score=0.0
            )
        
        perf = self.performance_data[model_name]
        
        # Update metrics with exponential moving average
        alpha = 0.1  # Learning rate
        
        if success:
            perf.success_rate = (1 - alpha) * perf.success_rate + alpha * 1.0
            perf.quality_score = (1 - alpha) * perf.quality_score + alpha * quality_score
        else:
            perf.success_rate = (1 - alpha) * perf.success_rate + alpha * 0.0
            perf.error_count += 1
        
        perf.avg_response_time = (1 - alpha) * perf.avg_response_time + alpha * response_time
        perf.cost_per_request = (1 - alpha) * perf.cost_per_request + alpha * cost
        perf.last_used = datetime.now()
        
        # Update fallback order based on new performance
        self._update_fallback_order()
    
    def _update_fallback_order(self):
        """Update the fallback order based on current performance"""
        available_models = self._get_available_models()
        
        # Sort by overall performance score
        model_scores = []
        for model in available_models:
            weights = {'quality_score': 0.3, 'success_rate': 0.4, 'response_time': 0.2, 'cost': 0.1}
            score = self._calculate_model_score(model, weights)
            model_scores.append((model, score))
        
        # Sort by score (descending)
        model_scores.sort(key=lambda x: x[1], reverse=True)
        self.fallback_order = [model for model, score in model_scores]
    
    def get_fallback_models(self, exclude: List[str] = None) -> List[str]:
        """Get ordered list of fallback models"""
        exclude = exclude or []
        return [model for model in self.fallback_order if model not in exclude]
    
    def _get_emergency_fallback(self) -> str:
        """Get emergency fallback when no models are available"""
        # Return the first available model or a default
        available = self._get_available_models()
        if available:
            return available[0]
        
        # If no models are enabled, return a default that can work offline
        return 'wan_mistral'
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current status of all models"""
        status = {
            'available_models': self._get_available_models(),
            'fallback_order': self.fallback_order,
            'performance_data': {}
        }
        
        for model_name, perf in self.performance_data.items():
            status['performance_data'][model_name] = {
                'success_rate': perf.success_rate,
                'avg_response_time': perf.avg_response_time,
                'error_count': perf.error_count,
                'quality_score': perf.quality_score,
                'last_used': perf.last_used.isoformat()
            }
        
        return status
