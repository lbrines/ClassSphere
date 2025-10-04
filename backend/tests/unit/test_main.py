"""Tests for main application module."""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.app.main import create_app, lifespan


class TestMainApp:
    """Test main application functionality."""

    def test_create_app(self):
        """Test FastAPI app creation."""
        app = create_app()

        assert app.title == "Dashboard Educativo"
        assert app.version == "1.0.0"

    def test_health_endpoint_success(self, test_client):
        """Test health endpoint success."""
        with patch('src.app.main.check_database_health') as mock_health:
            mock_health.return_value = {"redis": True}

            response = test_client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["app"] == "Dashboard Educativo"
            assert data["version"] == "1.0.0"
            assert "database" in data
            assert "mode" in data

    def test_health_endpoint_error(self, test_client):
        """Test health endpoint with error."""
        with patch('src.app.main.check_database_health') as mock_health:
            mock_health.side_effect = Exception("Health check failed")

            response = test_client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"
            assert "error" in data

    def test_cors_headers(self, test_client):
        """Test CORS headers are present."""
        # Make an OPTIONS request to trigger CORS headers
        response = test_client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            }
        )

        assert response.status_code == 200
        # Check that CORS headers are present (case-insensitive)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        assert "access-control-allow-origin" in headers_lower

    @pytest.mark.asyncio
    async def test_lifespan_startup_success(self):
        """Test lifespan startup success."""
        app = create_app()

        with patch('src.app.main.check_database_health') as mock_health:
            mock_health.return_value = {"redis": True}

            async with lifespan(app):
                mock_health.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_startup_error(self):
        """Test lifespan startup with error."""
        app = create_app()

        with patch('src.app.main.check_database_health') as mock_health:
            mock_health.side_effect = Exception("Startup failed")

            # Should not raise exception, just log warning
            async with lifespan(app):
                mock_health.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_shutdown_success(self):
        """Test lifespan shutdown success."""
        app = create_app()

        with patch('src.app.main.check_database_health'), \
             patch('src.app.main.cleanup_database') as mock_cleanup:
            mock_cleanup.return_value = None

            async with lifespan(app):
                pass

            mock_cleanup.assert_called_once()

    @pytest.mark.asyncio
    async def test_lifespan_shutdown_error(self):
        """Test lifespan shutdown with error."""
        app = create_app()

        with patch('src.app.main.check_database_health'), \
             patch('src.app.main.cleanup_database') as mock_cleanup:
            mock_cleanup.side_effect = Exception("Shutdown failed")

            # Should not raise exception, just log warning
            async with lifespan(app):
                pass

            mock_cleanup.assert_called_once()

    def test_app_middleware_configuration(self, test_app):
        """Test app middleware configuration."""
        # Check that CORS middleware is properly configured
        middleware_stack = test_app.user_middleware
        cors_middleware = None

        for middleware in middleware_stack:
            if "CORSMiddleware" in str(middleware.cls):
                cors_middleware = middleware
                break

        assert cors_middleware is not None

    def test_app_routes(self, test_app):
        """Test app routes are properly configured."""
        routes = [route.path for route in test_app.routes]
        assert "/health" in routes