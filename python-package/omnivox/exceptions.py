"""Custom exceptions for Omnivox API."""


class OmnivoxError(Exception):
    """Base exception for all Omnivox-related errors."""
    pass


class AuthenticationError(OmnivoxError):
    """Raised when authentication fails."""
    pass


class NetworkError(OmnivoxError):
    """Raised when network requests fail."""
    pass


class ParsingError(OmnivoxError):
    """Raised when HTML parsing fails or returns unexpected data."""
    pass


class NotFoundError(OmnivoxError):
    """Raised when a requested resource is not found."""
    pass
