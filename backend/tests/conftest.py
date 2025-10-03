"""
Test configuration and fixtures.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.app.main import app
from src.app.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Create async test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_mongodb():
    """Mock MongoDB client."""
    mock_client = AsyncMock()
    mock_client.admin.command = AsyncMock(return_value={"ok": 1})
    mock_client.server_info = AsyncMock(return_value={"version": "6.0.0"})
    
    # Mock database
    mock_db = AsyncMock()
    mock_collection = AsyncMock()
    mock_collection.find_one = AsyncMock(return_value=None)
    mock_collection.insert_one = AsyncMock(return_value=AsyncMock(inserted_id="test_id"))
    mock_db.users = mock_collection
    mock_db.courses = mock_collection
    mock_db.metrics = mock_collection
    mock_client.dashboard_educativo = mock_db
    
    return mock_client


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock(return_value=True)
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)
    mock_redis.delete = AsyncMock(return_value=1)
    mock_redis.exists = AsyncMock(return_value=False)
    mock_redis.close = AsyncMock()
    mock_redis.aclose = AsyncMock()  # For modern Redis
    return mock_redis


@pytest.fixture
def mock_settings():
    """Mock settings."""
    return settings


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "role": "student",
        "permissions": ["read:own_courses", "read:own_grades"]
    }


@pytest.fixture
def sample_course_data():
    """Sample course data for testing."""
    return {
        "course_id": "test_course_123",
        "name": "Test Course",
        "description": "A test course",
        "teacher_id": "teacher_123",
        "students": ["student_1", "student_2"]
    }


@pytest.fixture
def sample_jwt_token():
    """Sample JWT token for testing."""
    from src.app.core.security import create_access_token
    
    payload = {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "role": "student"
    }
    
    return create_access_token(payload)


@pytest.fixture
def setup_test_environment():
    """Setup test environment."""
    # Set test environment variables
    import os
    os.environ["DEBUG"] = "true"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["MONGODB_URL"] = "mongodb://test:27017"
    os.environ["REDIS_URL"] = "redis://test:6379"
    
    yield
    
    # Cleanup
    if "DEBUG" in os.environ:
        del os.environ["DEBUG"]
    if "ENVIRONMENT" in os.environ:
        del os.environ["ENVIRONMENT"]
    if "MONGODB_URL" in os.environ:
        del os.environ["MONGODB_URL"]
    if "REDIS_URL" in os.environ:
        del os.environ["REDIS_URL"]