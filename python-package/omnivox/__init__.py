"""
Omnivox API - Python library for interacting with Dawson College's Omnivox platform.

This library provides a simple interface to:
- Authenticate with Omnivox
- Access LEA (Learning Environment) - courses, documents, grades
- Access MIO (Internal Messaging) - messages, send messages, search users

Example:
    from omnivox import OmnivoxClient
    
    client = OmnivoxClient("student_id", "password")
    classes = client.lea.get_all_classes()
    messages = client.mio.get_messages()
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .client import OmnivoxClient
from .exceptions import (
    OmnivoxError,
    AuthenticationError,
    NetworkError,
    ParsingError,
)

__all__ = [
    "OmnivoxClient",
    "OmnivoxError",
    "AuthenticationError",
    "NetworkError",
    "ParsingError",
]
