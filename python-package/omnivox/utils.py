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
    
    TypeScript reference: 
    const removeWhiteSpace = new RegExp(" {2,}|" + String.fromCharCode(160) + "{2,}", "gm");
    return str.replace(removeWhiteSpace, '\n');
    
    This replaces 2+ spaces OR 2+ non-breaking spaces (char 160) with newline.
    
    Args:
        text: Text to clean
        
    Returns:
        Text with normalized whitespace
        
    Reference: archive/omnivox-crawler/src/utils/HTMLDecoder.ts
    """
    # String.fromCharCode(160) is non-breaking space (\xa0)
    # Replace 2+ regular spaces OR 2+ non-breaking spaces with newline
    pattern = re.compile(r' {2,}|\xa0{2,}', re.MULTILINE)
    return pattern.sub('\n', text)


def extract_k_token(html: str) -> Optional[str]:
    """
    Extract the 'k' authentication token from Omnivox login page HTML.
    
    This matches the TypeScript logic exactly:
    const init = answer.search("value=\"6") + "value=.".length;
    const k = answer.substring(init, init + 18);
    
    Args:
        html: HTML content of login page
        
    Returns:
        The k token if found, None otherwise
        
    Reference: archive/omnivox-crawler/src/modules/Login.ts
    """
    # Find the position of 'value="6' and add the length of 'value="' (7 chars)
    init = html.find('value="6')
    if init != -1:
        init += len('value="')
        k_token = html[init:init + 18]
        # Verify it's actually 18 characters
        if len(k_token) == 18:
            return k_token
    
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
