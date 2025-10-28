"""Utility functions for HTML parsing and data manipulation."""

import re
from typing import Optional


def decode_html_entities(text: str) -> str:
    """
    Decode HTML entities and remove HTML tags.
    
    Args:
        text: HTML text to decode
        
    Returns:
        Decoded text without HTML tags
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Decode common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    
    return text


def remove_extra_whitespace(text: str) -> str:
    """
    Remove excessive whitespace from text.
    
    Args:
        text: Text to clean
        
    Returns:
        Text with normalized whitespace
    """
    # Replace multiple spaces with single space
    text = re.sub(r' {2,}', '\n', text)
    # Replace non-breaking spaces
    text = re.sub(r'\xa0{2,}', '\n', text)
    return text.strip()


def extract_k_token(html: str) -> Optional[str]:
    """
    Extract the 'k' authentication token from Omnivox login page HTML.
    
    Args:
        html: HTML content of login page
        
    Returns:
        The k token if found, None otherwise
    """
    # Look for value="6..." pattern
    match = re.search(r'value="(6[^"]{17})"', html)
    if match:
        return match.group(1)
    
    # Alternative: look for the token after "value="
    start = html.find('value="6')
    if start != -1:
        start += len('value="')
        return html[start:start + 18]
    
    return None


def parse_schedule(schedule_text: str) -> list[str]:
    """
    Parse schedule text into list of time slots.
    
    Args:
        schedule_text: Raw schedule text from Omnivox
        
    Returns:
        List of schedule strings
    """
    if not schedule_text:
        return []
    
    # Split by comma and clean each entry
    schedules = [s.strip() for s in schedule_text.split(',')]
    return [s for s in schedules if s]


def safe_int(value: str, default: int = 0) -> int:
    """
    Safely convert string to integer.
    
    Args:
        value: String value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value or default
    """
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return default


def safe_float(value: str, default: float = 0.0) -> float:
    """
    Safely convert string to float.
    
    Args:
        value: String value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return default
