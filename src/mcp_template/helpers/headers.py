"""Header and request utilities for MCP server."""

import base64
from typing import Dict, Optional, Tuple, Any
import json
import re

from .logging import get_logger

logger = get_logger(__name__)


def extract_header(headers: Dict[str, str], header_name: str, default: Optional[str] = None) -> Optional[str]:
    """Extract a header value by name (case-insensitive)."""
    # Normalize header name for case-insensitive lookup
    header_lower = header_name.lower()
    
    for key, value in headers.items():
        if key.lower() == header_lower:
            return value
    
    return default


def parse_authorization(auth_header: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Parse Authorization header and return (scheme, token)."""
    if not auth_header:
        return None, None
    
    parts = auth_header.strip().split(" ", 1)
    if len(parts) != 2:
        return None, None
    
    scheme, token = parts
    return scheme.lower(), token


def parse_bearer_token(auth_header: Optional[str]) -> Optional[str]:
    """Extract bearer token from Authorization header."""
    scheme, token = parse_authorization(auth_header)
    
    if scheme == "bearer":
        return token
    
    return None


def parse_basic_auth(auth_header: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Parse Basic authentication and return (username, password)."""
    scheme, token = parse_authorization(auth_header)
    
    if scheme != "basic" or not token:
        return None, None
    
    try:
        decoded = base64.b64decode(token).decode("utf-8")
        if ":" in decoded:
            username, password = decoded.split(":", 1)
            return username, password
    except Exception as e:
        logger.warning(f"Failed to parse basic auth: {e}")
    
    return None, None


def get_client_info(headers: Dict[str, str]) -> Dict[str, Any]:
    """Extract client information from headers."""
    return {
        "user_agent": extract_header(headers, "user-agent"),
        "client_ip": extract_header(headers, "x-forwarded-for") or extract_header(headers, "x-real-ip"),
        "host": extract_header(headers, "host"),
        "origin": extract_header(headers, "origin"),
        "referer": extract_header(headers, "referer"),
        "accept": extract_header(headers, "accept"),
        "accept_language": extract_header(headers, "accept-language"),
        "accept_encoding": extract_header(headers, "accept-encoding"),
    }


def parse_content_type(content_type: Optional[str]) -> Tuple[Optional[str], Dict[str, str]]:
    """Parse Content-Type header and return (media_type, parameters)."""
    if not content_type:
        return None, {}
    
    parts = content_type.split(";")
    media_type = parts[0].strip().lower()
    
    parameters = {}
    for part in parts[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            parameters[key.strip().lower()] = value.strip().strip('"')
    
    return media_type, parameters


def is_json_content_type(content_type: Optional[str]) -> bool:
    """Check if content type is JSON."""
    if not content_type:
        return False
    
    media_type, _ = parse_content_type(content_type)
    return media_type in ["application/json", "application/vnd.api+json", "text/json"]


def validate_json_payload(payload: str) -> bool:
    """Validate if payload is valid JSON."""
    try:
        json.loads(payload)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def sanitize_header_value(value: str) -> str:
    """Sanitize header value by removing control characters."""
    # Remove control characters except tab
    return re.sub(r'[\x00-\x08\x0A-\x1F\x7F]', '', value)


def extract_api_key(headers: Dict[str, str]) -> Optional[str]:
    """Extract API key from various common header formats."""
    # Try common API key headers
    api_key_headers = [
        "x-api-key",
        "apikey",
        "api-key",
        "x-apikey",
        "authorization",
    ]
    
    for header_name in api_key_headers:
        value = extract_header(headers, header_name)
        if value:
            # If it's an authorization header, try to extract the token
            if header_name == "authorization":
                bearer_token = parse_bearer_token(value)
                if bearer_token:
                    return bearer_token
            else:
                return value
    
    return None


def build_headers(**kwargs) -> Dict[str, str]:
    """Build headers dictionary, filtering out None values."""
    return {k: str(v) for k, v in kwargs.items() if v is not None}
