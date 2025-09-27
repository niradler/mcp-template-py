"""Simple input validation utilities."""

import re
from typing import Any, Optional


def sanitize_string(
    text: str,
    max_length: Optional[int] = None,
    remove_html: bool = True,
    remove_control_chars: bool = True,
) -> str:
    """Sanitize string input by removing unwanted characters and limiting length."""
    if not isinstance(text, str):
        return str(text)

    sanitized = text

    # Remove HTML tags if requested
    if remove_html:
        sanitized = re.sub(r"<[^>]+>", "", sanitized)

    # Remove control characters if requested
    if remove_control_chars:
        sanitized = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", sanitized)

    # Trim whitespace
    sanitized = sanitized.strip()

    # Truncate if needed
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def safe_int(
    value: Any, default: int = 0, min_val: Optional[int] = None, max_val: Optional[int] = None
) -> int:
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
