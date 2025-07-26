"""
Custom exceptions for the EnableAI SDK
"""


class EnableAIError(Exception):
    """Base exception for EnableAI SDK"""
    pass


class AuthenticationError(EnableAIError):
    """Authentication failed"""
    pass


class ValidationError(EnableAIError):
    """Request validation failed"""
    pass


class RateLimitError(EnableAIError):
    """Rate limit exceeded"""
    pass 