"""Input validation utilities for MCP server."""

import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from .logging import get_logger

logger = get_logger(__name__)


def validate_input(
    data: Any,
    required_fields: Optional[List[str]] = None,
    field_types: Optional[Dict[str, type]] = None,
    max_length: Optional[int] = None,
) -> bool:
    """Validate input data against requirements."""
    if data is None:
        return False
    
    # Check if it's a dictionary for field validation
    if isinstance(data, dict):
        # Check required fields
        if required_fields:
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Missing required field: {field}")
                    return False
        
        # Check field types
        if field_types:
            for field, expected_type in field_types.items():
                if field in data and not isinstance(data[field], expected_type):
                    logger.warning(f"Field {field} has wrong type: expected {expected_type}, got {type(data[field])}")
                    return False
    
    # Check string length
    if isinstance(data, str) and max_length and len(data) > max_length:
        logger.warning(f"Input too long: {len(data)} > {max_length}")
        return False
    
    return True


def sanitize_string(
    text: str,
    max_length: Optional[int] = None,
    remove_html: bool = True,
    remove_control_chars: bool = True,
) -> str:
    """Sanitize string input."""
    if not isinstance(text, str):
        return str(text)
    
    sanitized = text
    
    # Remove HTML tags if requested
    if remove_html:
        sanitized = re.sub(r'<[^>]+>', '', sanitized)
    
    # Remove control characters if requested
    if remove_control_chars:
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Truncate if needed
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_uri(uri: str) -> bool:
    """Validate URI format."""
    try:
        parsed = urlparse(uri)
        return bool(parsed.scheme and parsed.netloc or parsed.path)
    except Exception:
        return False


def validate_email(email: str) -> bool:
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_json_schema(data: Any, schema: Dict[str, Any]) -> bool:
    """Basic JSON schema validation."""
    try:
        if "type" in schema:
            expected_type = schema["type"]
            
            if expected_type == "string" and not isinstance(data, str):
                return False
            elif expected_type == "number" and not isinstance(data, (int, float)):
                return False
            elif expected_type == "integer" and not isinstance(data, int):
                return False
            elif expected_type == "boolean" and not isinstance(data, bool):
                return False
            elif expected_type == "array" and not isinstance(data, list):
                return False
            elif expected_type == "object" and not isinstance(data, dict):
                return False
        
        if "properties" in schema and isinstance(data, dict):
            for prop, prop_schema in schema["properties"].items():
                if prop in data:
                    if not validate_json_schema(data[prop], prop_schema):
                        return False
        
        if "required" in schema and isinstance(data, dict):
            for required_prop in schema["required"]:
                if required_prop not in data:
                    return False
        
        return True
    
    except Exception as e:
        logger.warning(f"Schema validation error: {e}")
        return False


def validate_tool_arguments(arguments: Dict[str, Any], tool_schema: Dict[str, Any]) -> bool:
    """Validate tool arguments against schema."""
    return validate_json_schema(arguments, tool_schema)


def safe_int(value: Any, default: int = 0, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """Safely convert value to integer with bounds checking."""
    try:
        result = int(value)
        
        if min_val is not None and result < min_val:
            return min_val
        
        if max_val is not None and result > max_val:
            return max_val
        
        return result
    
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0, min_val: Optional[float] = None, max_val: Optional[float] = None) -> float:
    """Safely convert value to float with bounds checking."""
    try:
        result = float(value)
        
        if min_val is not None and result < min_val:
            return min_val
        
        if max_val is not None and result > max_val:
            return max_val
        
        return result
    
    except (ValueError, TypeError):
        return default


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    return re.sub(r'\s+', ' ', text.strip())


def is_safe_filename(filename: str) -> bool:
    """Check if filename is safe (no directory traversal, etc.)."""
    # Check for directory traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    # Check for reserved names (Windows)
    reserved_names = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    if filename.upper() in reserved_names:
        return False
    
    # Check for invalid characters
    invalid_chars = '<>:"|?*\x00'
    if any(char in filename for char in invalid_chars):
        return False
    
    return True
