"""Security utilities and best practices for the tutorial application.

This module provides security-related functionality including input sanitization,
security headers, rate limiting, and secret management.
"""

import hashlib
import logging
import os
import re
import time
from collections import defaultdict
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)

# Security constants
MAX_INPUT_LENGTH = 10000
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
RATE_LIMIT_REQUESTS = 100  # requests per window
RATE_LIMIT_WINDOW = 60  # seconds
ALLOWED_DOMAINS = {"nvidia.com", "developer.nvidia.com", "docs.nvidia.com", "forums.developer.nvidia.com"}

# Dangerous patterns to filter
DANGEROUS_PATTERNS = [
    r"<script[^>]*>.*?</script>",  # Script tags
    r"javascript:",  # JavaScript URLs
    r"data:",  # Data URLs (potential XSS)
    r"vbscript:",  # VBScript
    r"on\w+\s*=",  # Event handlers
    r"<iframe[^>]*>.*?</iframe>",  # Iframes
    r"<object[^>]*>.*?</object>",  # Object tags
    r"<embed[^>]*>.*?</embed>",  # Embed tags
]

# Rate limiting storage
_rate_limit_store: Dict[str, list] = defaultdict(list)


class SecurityError(Exception):
    """Custom exception for security violations."""


class InputSanitizer:
    """Handles input sanitization and validation."""

    @staticmethod
    def sanitize_text_input(text: str, max_length: int = MAX_INPUT_LENGTH) -> str:
        """Sanitize text input by removing dangerous content and limiting length.

        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized text

        Raises:
            SecurityError: If input contains dangerous patterns
        """
        if not isinstance(text, str):
            raise SecurityError("Input must be a string")

        # Check length
        if len(text) > max_length:
            logger.warning("Input length %s exceeds maximum %s", len(text), max_length)
            text = text[:max_length]

        # Remove null bytes and other control characters
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

        # Check for dangerous patterns
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
                logger.warning("Dangerous pattern detected in input: %s", pattern)
                raise SecurityError(f"Input contains dangerous content: {pattern}")

        return text.strip()

    @staticmethod
    def validate_file_upload(file_content: bytes, filename: str) -> bool:
        """Validate uploaded file content and filename.

        Args:
            file_content: File content as bytes
            filename: Original filename

        Returns:
            True if file is safe

        Raises:
            SecurityError: If file is unsafe
        """
        # Check file size
        if len(file_content) > MAX_FILE_SIZE:
            raise SecurityError(f"File size {len(file_content)} exceeds maximum {MAX_FILE_SIZE}")

        # Check filename for dangerous patterns
        if ".." in filename or "/" in filename or "\\" in filename:
            raise SecurityError("Invalid filename")

        # Check for executable content in first few bytes
        if len(file_content) > 4:
            # Check for common executable signatures
            signatures = [b"#!/", b"<?php", b"<%", b"<script"]
            for sig in signatures:
                if file_content.startswith(sig):
                    raise SecurityError("File contains executable content")

        return True

    @staticmethod
    def sanitize_url(url: str) -> str:
        """Sanitize and validate URLs.

        Args:
            url: URL to sanitize

        Returns:
            Sanitized URL

        Raises:
            SecurityError: If URL is unsafe
        """
        if not url:
            return url

        try:
            parsed = urlparse(url)
            if parsed.scheme not in ["http", "https"]:
                raise SecurityError("Only HTTP and HTTPS URLs are allowed")

            # Check domain against whitelist
            domain = parsed.netloc.lower()
            if not any(domain.endswith(allowed) for allowed in ALLOWED_DOMAINS):
                logger.warning("URL domain %s not in allowed list", domain)
                # Allow but log - don't block for tutorial purposes

            return url

        except (ValueError, TypeError) as e:
            raise SecurityError(f"Invalid URL: {e}")


class RateLimiter:
    """Handles rate limiting for API calls and user actions."""

    @staticmethod
    def check_rate_limit(identifier: str, requests: int = RATE_LIMIT_REQUESTS, window: int = RATE_LIMIT_WINDOW) -> bool:
        """Check if request is within rate limits.

        Args:
            identifier: Unique identifier for the client/user
            requests: Maximum requests allowed in window
            window: Time window in seconds

        Returns:
            True if request is allowed, False if rate limited
        """
        current_time = time.time()

        # Clean old entries
        _rate_limit_store[identifier] = [
            timestamp for timestamp in _rate_limit_store[identifier] if current_time - timestamp < window
        ]

        # Check if under limit
        if len(_rate_limit_store[identifier]) < requests:
            _rate_limit_store[identifier].append(current_time)
            return True

        logger.warning("Rate limit exceeded for %s", identifier)
        return False

    @staticmethod
    def get_remaining_requests(identifier: str) -> int:
        """Get remaining requests for an identifier.

        Args:
            identifier: Unique identifier

        Returns:
            Number of remaining requests
        """
        current_time = time.time()
        _rate_limit_store[identifier] = [
            timestamp for timestamp in _rate_limit_store[identifier] if current_time - timestamp < RATE_LIMIT_WINDOW
        ]

        return max(0, RATE_LIMIT_REQUESTS - len(_rate_limit_store[identifier]))


class SecretManager:
    """Handles secure storage and retrieval of secrets."""

    @staticmethod
    def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret from environment variables.

        Args:
            key: Secret key
            default: Default value if not found

        Returns:
            Secret value or default
        """
        # Check environment variables
        value = os.environ.get(key)
        if value:
            return value

        # Check Streamlit secrets (if available)
        try:
            if hasattr(st, "secrets") and key in st.secrets:
                return st.secrets[key]
        except (AttributeError, FileNotFoundError):
            pass  # Streamlit secrets not available

        return default

    @staticmethod
    def hash_sensitive_data(data: str, salt: Optional[str] = None) -> str:
        """Hash sensitive data for logging/storage.

        Args:
            data: Data to hash
            salt: Optional salt

        Returns:
            Hashed data
        """
        if salt:
            data = salt + data

        return hashlib.sha256(data.encode()).hexdigest()


class SecurityHeaders:
    """Manages security headers for Streamlit applications."""

    @staticmethod
    def apply_security_headers() -> None:
        """Apply security headers to the Streamlit application.

        Note: Streamlit has limited support for custom headers.
        This method provides guidance for manual configuration.
        """
        # These would be set in the web server/reverse proxy
        security_headers = {
            # Content Security Policy
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self'; "
                "connect-src 'self' https://*.nvidia.com; "
                "frame-ancestors 'none';"
            ),
            # Prevent clickjacking
            "X-Frame-Options": "DENY",
            # Prevent MIME type sniffing
            "X-Content-Type-Options": "nosniff",
            # Enable XSS protection
            "X-XSS-Protection": "1; mode=block",
            # Referrer policy
            "Referrer-Policy": "strict-origin-when-cross-origin",
            # HSTS (if HTTPS is enabled)
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        }

        # Log security headers for manual configuration
        logger.info("Security headers should be configured in web server:")
        for header, value in security_headers.items():
            logger.info("  %s: %s", header, value)

    @staticmethod
    def validate_request_origin(request_headers: Dict[str, str]) -> bool:
        """Validate request origin for CORS-like protection.

        Args:
            request_headers: Request headers

        Returns:
            True if origin is allowed
        """
        origin = request_headers.get("Origin", "").lower()

        if not origin:
            return True  # Allow requests without Origin header

        try:
            parsed = urlparse(origin)
            domain = parsed.netloc

            return any(domain.endswith(allowed) for allowed in ALLOWED_DOMAINS)
        except (ValueError, TypeError):
            return False


def initialize_security() -> None:
    """Initialize security measures for the application."""
    logger.info("Initializing security measures...")

    # Apply security headers
    SecurityHeaders.apply_security_headers()

    # Log security status
    logger.info("Security initialization complete")


# Utility functions for common security checks
def secure_file_operation(filepath: str, operation: str = "read") -> bool:
    """Check if file operation is secure.

    Args:
        filepath: File path to check
        operation: Operation type ('read', 'write', 'execute')

    Returns:
        True if operation is allowed
    """
    # Prevent directory traversal
    if ".." in filepath or not filepath.startswith("/"):
        return False

    # Check file permissions (basic check)
    if operation == "execute":
        # Don't allow execution of files
        return False

    return True


def audit_log(action: str, user_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> None:
    """Log security-related actions for audit purposes.

    Args:
        action: Action performed
        user_id: User identifier (if available)
        details: Additional details
    """
    log_entry = {
        "timestamp": time.time(),
        "action": action,
        "user_id": user_id or "anonymous",
        "details": details or {},
    }

    logger.info("SECURITY AUDIT: %s", log_entry)
