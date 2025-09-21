
"""Data Validation Utilities"""
import json
import logging
import os  # ADD THIS LINE
from typing import Any, Dict, Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def safe_json_load(data: Union[str, Dict]) -> Dict:
        """Safely load JSON data with error handling"""
        if isinstance(data, dict):
            return data
            
        if isinstance(data, str):
            try:
                return json.loads(data)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON data: {e}")
                return {}
                
        logger.warning(f"Unexpected data type for JSON: {type(data)}")
        return {}
        
    @staticmethod
    def safe_json_dump(data: Any, indent: int = 2) -> str:
        """Safely dump data to JSON string"""
        try:
            return json.dumps(data, indent=indent, default=str, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            logger.error(f"Failed to serialize data to JSON: {e}")
            return '{}'
            
    @staticmethod
    def validate_content_data(content_data: Dict) -> Dict:
        """Validate and sanitize content data"""
        required_fields = ['title', 'script', 'topic']
        validated = {}
        
        for field in required_fields:
            if field in content_data and content_data[field]:
                validated[field] = str(content_data[field]).strip()
            else:
                logger.warning(f"Missing or empty required field: {field}")
                validated[field] = f"Default {field}"
                
        # Optional fields with defaults
        validated['description'] = content_data.get('description', '')
        validated['tags'] = content_data.get('tags', [])
        validated['format_type'] = content_data.get('format_type', 'general')
        
        return validated
        
    @staticmethod
    def validate_file_path(file_path: Union[str, Path]) -> Optional[Path]:
        """Validate file path exists and is accessible with enhanced error handling"""
        if not file_path:
            logger.error("File path is None or empty")
            return None
            
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                # Check if file is readable
                if os.access(path, os.R_OK):
                    return path
                else:
                    logger.error(f"File exists but is not readable: {file_path}")
                    return None
            else:
                logger.error(f"File does not exist or is not a file: {file_path}")
                return None
        except (OSError, PermissionError) as e:
            logger.error(f"Permission error accessing file {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error validating file path {file_path}: {e}")
            return None
    
    @staticmethod
    def safe_dict_get(data: Dict, key: str, default: Any = None, required: bool = False) -> Any:
        """Safely get value from dictionary with validation"""
        try:
            if not isinstance(data, dict):
                if required:
                    raise ValueError(f"Expected dict, got {type(data)}")
                return default
            
            if key in data:
                value = data[key]
                if value is not None:
                    return value
                elif required:
                    raise ValueError(f"Required key '{key}' has None value")
                else:
                    return default
            elif required:
                raise KeyError(f"Required key '{key}' not found in data")
            else:
                return default
        except Exception as e:
            logger.error(f"Error getting key '{key}' from data: {e}")
            if required:
                raise
            return default
            
# Global validator instance
validator = DataValidator()
