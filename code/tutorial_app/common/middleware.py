"""Middleware functions for Streamlit app: authentication, logging, and input sanitization."""

import logging
from typing import Callable

import httpx
import streamlit as st

from .security import InputSanitizer, initialize_security


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def initialize_app_middleware() -> None:
    """Initialize security and logging for the app."""
    initialize_security()
    logger.info("Middleware initialized: security and logging set up.")


def auth_middleware(func: Callable) -> Callable:
    """Authentication middleware decorator for Streamlit pages."""

    def wrapper(*args, **kwargs):
        # Simple session-based auth (in production, use JWT or similar)
        if "user_id" not in st.session_state:
            st.session_state.user_id = st.secrets.get("default_user_id", "anonymous")
            logger.info("New session for user: %s", st.session_state.user_id)

        # Sanitize inputs if any are passed (for pages that accept inputs)
        if kwargs:
            sanitizer = InputSanitizer()
            sanitized_kwargs = {k: sanitizer.sanitize(v) if isinstance(v, str) else v for k, v in kwargs.items()}
            kwargs = sanitized_kwargs

        logger.info("Executing page with user: %s", st.session_state.user_id)
        return func(*args, **kwargs)

    return wrapper


def logging_middleware(func: Callable) -> Callable:
    """Logging middleware to log page access and errors."""

    def wrapper(*args, **kwargs):
        try:
            logger.info("Page accessed: %s by user %s", func.__name__, st.session_state.get("user_id", "anonymous"))
            result = func(*args, **kwargs)
            logger.info("Page %s completed successfully", func.__name__)
            return result
        except Exception as e:
            logger.error("Error in page %s: %s", func.__name__, str(e))
            st.error(f"An error occurred: {str(e)}")
            raise

    return wrapper


def request_middleware(func: Callable) -> Callable:
    """Middleware for handling API requests to backend."""

    backend_url = "http://localhost:8000"  # Adjust for production

    def wrapper(*args, **kwargs):
        # Ensure backend is reachable
        try:
            with httpx.Client(base_url=backend_url, timeout=5.0) as client:
                response = client.get("/health")
                if response.status_code != 200:
                    logger.warning("Backend health check failed")
                    st.warning("Backend service may be unavailable.")
        except httpx.RequestError as e:
            logger.error("Backend connection error: %s", e)
            st.warning("Unable to connect to backend service.")

        return func(*args, **kwargs)

    return wrapper


# Global middleware setup (call at app start)
def setup_middleware(app_func: Callable) -> Callable:
    """Setup all middleware for the main app."""
    initialize_app_middleware()

    @logging_middleware
    @request_middleware
    @auth_middleware
    def wrapped_app(*args, **kwargs):
        return app_func(*args, **kwargs)

    return wrapped_app
