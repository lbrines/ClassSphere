"""
Global test configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from src.app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def test_data():
    """Common test data"""
    return {
        "test_email": "test@example.com",
        "test_password": "TestPassword123!",
        "test_name": "Test User"
    }
