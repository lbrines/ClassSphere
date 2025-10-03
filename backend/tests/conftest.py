"""
Test configuration and fixtures for Dashboard Educativo Backend
"""
import asyncio
import os
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis

from src.app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_client() -> TestClient:
    """Create a test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_mongodb():
    """Mock MongoDB client for testing."""
    mock_client = AsyncMock()
    mock_client.admin.command = AsyncMock(return_value={"ok": 1})
    mock_client.server_info = AsyncMock(return_value={"version": "6.0.0"})
    
    # Mock database and collections
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
    """Mock Redis client for testing."""
    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock(return_value=True)
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)
    mock_redis.delete = AsyncMock(return_value=1)
    mock_redis.exists = AsyncMock(return_value=False)
    mock_redis.close = AsyncMock()
    return mock_redis


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch('src.app.core.config.settings') as mock:
        mock.MONGODB_URL = "mongodb://test:27017"
        mock.REDIS_URL = "redis://test:6379"
        mock.JWT_SECRET_KEY = "test-secret-key"
        mock.DEBUG = True
        mock.PORT = 8000
        mock.HOST = "127.0.0.1"
        yield mock


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": "test_user_id",
        "email": "test@example.com",
        "name": "Test User",
        "role": "student",
        "google_id": "google_123",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_course_data():
    """Sample course data for testing."""
    return {
        "id": "test_course_id",
        "name": "Test Course",
        "description": "A test course",
        "teacher_id": "teacher_123",
        "students": ["student_1", "student_2"],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def sample_jwt_token():
    """Sample JWT token for testing."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfaWQiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJyb2xlIjoic3R1ZGVudCIsImV4cCI6OTk5OTk5OTk5OX0.test_signature"


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables."""
    os.environ.update({
        "TESTING": "true",
        "MONGODB_URL": "mongodb://test:27017",
        "REDIS_URL": "redis://test:6379",
        "JWT_SECRET_KEY": "test-secret-key",
        "DEBUG": "true",
        "PORT": "8000",
        "HOST": "127.0.0.1"
    })
    yield
    # Cleanup after test
    for key in ["TESTING", "MONGODB_URL", "REDIS_URL", "JWT_SECRET_KEY", "DEBUG", "PORT", "HOST"]:
        os.environ.pop(key, None)