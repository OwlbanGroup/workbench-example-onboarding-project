"""
Backend API test module for tutorial app.
"""

import logging
import requests

BASE_URL = "http://localhost:8000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health", timeout=10)
    assert response.status_code == 200
    logger.info("Health check passed: %s", response.json())


def test_create_user():
    """Test create user endpoint."""
    user_data = {"name": "Test User", "email": "test@example.com", "progress": {}}
    response = requests.post(f"{BASE_URL}/users/testuser", json=user_data, timeout=10)
    assert response.status_code == 200
    logger.info("Create user passed: %s", response.json())


def test_get_user():
    """Test get user endpoint."""
    response = requests.get(f"{BASE_URL}/users/testuser", timeout=10)
    assert response.status_code == 200
    logger.info("Get user passed: %s", response.json())


def test_store_app_data():
    """Test store app data endpoint."""
    app_data = {"key": "testkey", "value": "testvalue"}
    response = requests.post(f"{BASE_URL}/data", json=app_data, timeout=10)
    assert response.status_code == 200
    logger.info("Store app data passed: %s", response.json())


def test_get_app_data():
    """Test get app data endpoint."""
    response = requests.get(f"{BASE_URL}/data/testkey", timeout=10)
    assert response.status_code == 200
    logger.info("Get app data passed: %s", response.json())


if __name__ == "__main__":
    test_health()
    test_create_user()
    test_get_user()
    test_store_app_data()
    test_get_app_data()
