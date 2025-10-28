"""Tests for utility functions."""

import unittest
from omnivox.utils import (
    decode_html_entities,
    remove_extra_whitespace,
    extract_k_token,
    parse_schedule,
    safe_int,
    safe_float
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_decode_html_entities(self):
        """Test HTML entity decoding."""
        text = "Hello&nbsp;World&amp;Test"
        result = decode_html_entities(text)
        self.assertEqual(result, "Hello World&Test")
    
    def test_decode_html_entities_with_tags(self):
        """Test HTML entity decoding with tags."""
        text = "<p>Hello&nbsp;World</p>"
        result = decode_html_entities(text)
        self.assertEqual(result, "Hello World")
    
    def test_remove_extra_whitespace(self):
        """Test whitespace removal."""
        text = "Hello     World"
        result = remove_extra_whitespace(text)
        self.assertEqual(result, "Hello\nWorld")
    
    def test_extract_k_token(self):
        """Test k token extraction."""
        html = '<input name="k" value="6123456789012345678">'
        result = extract_k_token(html)
        self.assertEqual(result, "6123456789012345678")
    
    def test_extract_k_token_not_found(self):
        """Test k token extraction when not found."""
        html = '<input name="other" value="12345">'
        result = extract_k_token(html)
        self.assertIsNone(result)
    
    def test_parse_schedule(self):
        """Test schedule parsing."""
        schedule_text = "Mon 10:00-12:00, Wed 14:00-16:00"
        result = parse_schedule(schedule_text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Mon 10:00-12:00")
        self.assertEqual(result[1], "Wed 14:00-16:00")
    
    def test_parse_schedule_empty(self):
        """Test parsing empty schedule."""
        result = parse_schedule("")
        self.assertEqual(result, [])
    
    def test_safe_int(self):
        """Test safe integer conversion."""
        self.assertEqual(safe_int("123"), 123)
        self.assertEqual(safe_int("  456  "), 456)
        self.assertEqual(safe_int("invalid"), 0)
        self.assertEqual(safe_int("invalid", -1), -1)
    
    def test_safe_float(self):
        """Test safe float conversion."""
        self.assertEqual(safe_float("12.5"), 12.5)
        self.assertEqual(safe_float("  45.67  "), 45.67)
        self.assertEqual(safe_float("invalid"), 0.0)
        self.assertEqual(safe_float("invalid", -1.0), -1.0)


if __name__ == '__main__':
    unittest.main()
