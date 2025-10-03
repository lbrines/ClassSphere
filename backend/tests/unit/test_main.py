import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.core.config import settings

client = TestClient(app)

class TestHealthEndpoint:
    """
    Test suite for the /health endpoint.
    """

    def test_health_check_returns_200(self):
        """
        Test that the health check endpoint returns a 200 OK status.
        """
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_structure(self):
        """
        Test that the health check response has the expected structure and content.
        """
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "environment" in data
        assert data["environment"] == settings.ENVIRONMENT
        assert "version" in data
        assert data["version"] == app.version

    def test_health_check_has_process_time_header(self):
        """
        Test that the health check response includes the X-Process-Time header.
        """
        response = client.get("/health")
        assert "x-process-time" in response.headers
        assert float(response.headers["x-process-time"]) >= 0

class TestRootEndpoint:
    """
    Test suite for the root endpoint.
    """

    def test_root_returns_200(self):
        """
        Test that the root endpoint returns a 200 OK status.
        """
        response = client.get("/")
        assert response.status_code == 200

    def test_root_response_structure(self):
        """
        Test that the root endpoint response has the expected structure and content.
        """
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Dashboard Educativo API"
        assert "version" in data
        assert data["version"] == app.version
        assert "docs" in data
        assert data["docs"] == app.docs_url
        assert "health" in data
        assert data["health"] == "/health"

class TestErrorHandling:
    """
    Test suite for general error handling.
    """

    def test_validation_error_handling(self):
        """
        Test that invalid requests return a 422 Unprocessable Entity with a standard error structure.
        (This test assumes a route that expects a Pydantic model and will fail on invalid input)
        """
        # For now, we'll test a non-existent route to get a 404,
        # as specific validation errors will be tested with actual API routes.
        response = client.post("/non-existent-route", json={"invalid": "data"})
        assert response.status_code == 404 # Expecting 404 for now, will be 422 for validation errors later

    def test_cors_headers_present(self):
        """
        Test that CORS headers are present in responses.
        """
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert "access-control-allow-credentials" in response.headers
        assert response.headers["access-control-allow-credentials"] == "true"

class TestMiddleware:
    """
    Test suite for middleware functionality.
    """

    def test_process_time_middleware(self):
        """
        Test that the X-Process-Time header is added by the middleware.
        """
        response = client.get("/")
        assert "x-process-time" in response.headers
        assert float(response.headers["x-process-time"]) >= 0
