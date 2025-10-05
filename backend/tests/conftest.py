"""
Fixtures globales para testing
"""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client():
    """TestClient para FastAPI"""
    app = create_app()
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Settings mockeados para testing"""
    from app.core.config import Settings
    return Settings(
        secret_key="test-secret-key",
        google_client_id="test-client-id",
        google_client_secret="test-client-secret"
    )
