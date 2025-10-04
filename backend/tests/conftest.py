"""
Pytest configuration and fixtures for ClassSphere TDD

CRITICAL OBJECTIVES:
- Configure timeouts for different test types
- Set up AsyncMock fixtures
- Configure test environment

DEPENDENCIES:
- pytest-asyncio
- pytest-mock
- pytest-cov
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import AsyncGenerator, Generator
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# BEGINNING: Critical fixtures for core functionality
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_redis() -> AsyncMock:
    """Mock Redis client with proper async methods"""
    mock = AsyncMock()
    mock.ping = AsyncMock(return_value=True)
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock(return_value=True)
    mock.delete = AsyncMock(return_value=1)
    mock.exists = AsyncMock(return_value=False)
    mock.close = AsyncMock()
    mock.aclose = AsyncMock()
    return mock

@pytest.fixture
def mock_httpx_client() -> AsyncMock:
    """Mock httpx client for API calls"""
    mock = AsyncMock()
    mock.get = AsyncMock()
    mock.post = AsyncMock()
    mock.put = AsyncMock()
    mock.delete = AsyncMock()
    mock.aclose = AsyncMock()
    return mock

# MIDDLE: Detailed implementation fixtures
@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "id": "test_user_123",
        "email": "test@classsphere.com",
        "role": "teacher",
        "name": "Test User",
        "is_active": True
    }

@pytest.fixture
def mock_jwt_token():
    """Mock JWT token for testing"""
    return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfMTIzIiwiZXhwIjoxNzM4NDQ0MDAwfQ.test_signature"

@pytest.fixture
def mock_google_oauth_response():
    """Mock Google OAuth response"""
    return {
        "access_token": "mock_access_token",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_token": "mock_refresh_token",
        "scope": "openid email profile"
    }

# END: Verification and next steps
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Set test environment variables
    os.environ["TESTING"] = "true"
    os.environ["REDIS_URL"] = "redis://localhost:6379/1"
    os.environ["SECRET_KEY"] = "test_secret_key_for_testing_only"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    
    yield
    
    # Cleanup after test
    if "TESTING" in os.environ:
        del os.environ["TESTING"]

# Timeout configurations
def pytest_configure(config):
    """Configure pytest with timeout settings"""
    config.addinivalue_line(
        "markers", "timeout_2s: Test with 2 second timeout (unit tests)"
    )
    config.addinivalue_line(
        "markers", "timeout_5s: Test with 5 second timeout (integration tests)"
    )
    config.addinivalue_line(
        "markers", "timeout_10s: Test with 10 second timeout (e2e tests)"
    )

# Async test timeout decorators
def timeout_2s(func):
    """Decorator for 2 second timeout (unit tests)"""
    return pytest.mark.asyncio(timeout=2.0)(func)

def timeout_5s(func):
    """Decorator for 5 second timeout (integration tests)"""
    return pytest.mark.asyncio(timeout=5.0)(func)

def timeout_10s(func):
    """Decorator for 10 second timeout (e2e tests)"""
    return pytest.mark.asyncio(timeout=10.0)(func)