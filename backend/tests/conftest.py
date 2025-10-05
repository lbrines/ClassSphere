"""
Test configuration and fixtures for ClassSphere tests.
"""
import asyncio
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.app.main import create_app
from src.app.services.auth_service import AuthService
from src.app.services.oauth_service import OAuthService
from src.app.services.mock_service import MockService


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_service():
    """Create auth service for testing."""
    return AuthService()


@pytest.fixture
def oauth_service():
    """Create OAuth service for testing."""
    return OAuthService()


@pytest.fixture
def mock_service():
    """Create mock service for testing."""
    return MockService()


@pytest.fixture
def mock_user_data():
    """Mock user data for testing."""
    return {
        "id": "test-user-001",
        "email": "test@classsphere.edu",
        "name": "Test User",
        "role": "student",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def mock_google_user_info():
    """Mock Google user info for testing."""
    return {
        "id": "google-123456789",
        "email": "test@gmail.com",
        "verified_email": True,
        "name": "Test Google User",
        "given_name": "Test",
        "family_name": "User",
        "picture": "https://example.com/photo.jpg",
        "locale": "en"
    }


@pytest.fixture
def mock_google_oauth_response():
    """Mock Google OAuth response for testing."""
    return {
        "access_token": "mock-access-token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_token": "mock-refresh-token",
        "scope": "openid email profile"
    }


@pytest.fixture
def mock_jwt_token():
    """Mock JWT token for testing."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0LXVzZXItMDAxIiwiZW1haWwiOiJ0ZXN0QGNsYXNzc3BoZXJlLmVkdSIsInJvbGUiOiJzdHVkZW50IiwiZXhwIjo5OTk5OTk5OTk5fQ.test-signature"


@pytest.fixture
def mock_redis_unavailable():
    """Mock Redis unavailable scenario."""
    with patch('src.app.services.mock_service.MockService.redis_available', False):
        yield