"""
Unit tests for health endpoints.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


def test_health_check_success(client):
    """Test successful health check."""
    response = client.get("/api/v1/health/")

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "data" in data
    assert data["data"]["status"] == "healthy"
    assert "timestamp" in data["data"]
    assert "checks" in data["data"]


def test_health_check_timeout():
    """Test health check timeout handling."""
    from src.app.main import create_app

    app = create_app()

    with patch('src.app.services.mock_service.MockService.health_check') as mock_health:
        # Mock timeout
        import asyncio

        async def timeout_health():
            await asyncio.sleep(6.0)  # Longer than timeout
            return {"status": "healthy"}

        mock_health.side_effect = timeout_health

        client = TestClient(app)
        response = client.get("/api/v1/health/")

        assert response.status_code == 503
        data = response.json()

        assert data["success"] is False
        assert data["data"]["status"] == "timeout"


def test_detailed_health_check_success(client):
    """Test successful detailed health check."""
    response = client.get("/api/v1/health/detailed")

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "data" in data
    assert data["data"]["status"] == "healthy"
    assert "version" in data["data"]
    assert "environment" in data["data"]
    assert "uptime" in data["data"]
    assert "port" in data["data"]
    assert data["data"]["port"] == 8000


def test_detailed_health_check_with_degraded_services():
    """Test detailed health check with degraded services."""
    from src.app.main import create_app

    app = create_app()

    # Mock degraded health status
    with patch('src.app.services.mock_service.MockService.health_check') as mock_health:
        mock_health.return_value = {
            "status": "degraded",
            "timestamp": "2024-01-01T00:00:00Z",
            "checks": {
                "database": "healthy",
                "redis": "degraded",
                "external_apis": "healthy"
            }
        }

        client = TestClient(app)
        response = client.get("/api/v1/health/detailed")

        assert response.status_code == 503
        data = response.json()

        assert data["success"] is True
        assert data["data"]["status"] == "degraded"
        assert data["data"]["checks"]["redis"] == "degraded"


def test_detailed_health_check_timeout():
    """Test detailed health check timeout handling."""
    from src.app.main import create_app

    app = create_app()

    with patch('src.app.services.mock_service.MockService.health_check') as mock_health:
        # Mock timeout
        import asyncio

        async def timeout_health():
            await asyncio.sleep(6.0)  # Longer than timeout
            return {"status": "healthy"}

        mock_health.side_effect = timeout_health

        client = TestClient(app)
        response = client.get("/api/v1/health/detailed")

        assert response.status_code == 503
        data = response.json()

        assert data["success"] is False
        assert data["data"]["status"] == "timeout"
        assert "version" in data["data"]
        assert "environment" in data["data"]