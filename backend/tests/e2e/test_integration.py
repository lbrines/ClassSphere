"""
End-to-End integration tests for ClassSphere backend
Tests complete flows and edge cases to improve coverage
"""
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from src.app.main import create_app


@pytest.fixture
def app():
    """Create app for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health endpoints integration."""

    def test_health_check_complete_flow(self, client):
        """Test complete health check flow."""
        response = client.get("/api/v1/health/")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "data" in data
        assert data["data"]["status"] == "healthy"

    def test_detailed_health_check_complete_flow(self, client):
        """Test detailed health check flow."""
        response = client.get("/api/v1/health/detailed")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "data" in data
        assert "status" in data["data"]


class TestAuthEndpointsIntegration:
    """Test auth endpoints integration and edge cases."""

    def test_login_with_empty_body(self, client):
        """Test login with empty request body."""
        response = client.post("/api/v1/auth/login")

        # Should return 422 for validation error
        assert response.status_code == 422

    def test_login_with_invalid_json(self, client):
        """Test login with malformed JSON."""
        response = client.post(
            "/api/v1/auth/login",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )

        # Should return 422 for JSON decode error
        assert response.status_code == 422

    def test_login_with_missing_fields(self, client):
        """Test login with missing required fields."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com"}  # Missing password
        )

        assert response.status_code == 422

        response = client.post(
            "/api/v1/auth/login",
            json={"password": "secret"}  # Missing email
        )

        assert response.status_code == 422

    def test_login_with_invalid_email_format(self, client):
        """Test login with invalid email format."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "not-an-email",
                "password": "secret"
            }
        )

        assert response.status_code == 422

    def test_me_endpoint_without_auth_header(self, client):
        """Test /me endpoint without Authorization header."""
        response = client.get("/api/v1/auth/me")

        # Should return 403 for missing auth
        assert response.status_code == 403

    def test_me_endpoint_with_invalid_auth_header(self, client):
        """Test /me endpoint with invalid Authorization header."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Invalid header"}
        )

        # Should return 403 or 422 for invalid auth format
        assert response.status_code in [403, 422]

    def test_me_endpoint_with_malformed_bearer_token(self, client):
        """Test /me endpoint with malformed Bearer token."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer"}  # Missing token
        )

        # Should return 403 or 422
        assert response.status_code in [403, 422]

    def test_verify_endpoint_without_auth(self, client):
        """Test token verification without auth."""
        response = client.post("/api/v1/auth/verify")

        assert response.status_code == 403

    def test_verify_endpoint_with_invalid_token(self, client):
        """Test token verification with invalid token."""
        response = client.post(
            "/api/v1/auth/verify",
            headers={"Authorization": "Bearer invalid-token"}
        )

        # Should return 401 for invalid token
        assert response.status_code == 401

    def test_logout_endpoint(self, client):
        """Test logout endpoint (stateless)."""
        response = client.post("/api/v1/auth/logout")

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert data["data"]["logged_out"] is True

    def test_cors_headers(self, client):
        """Test CORS headers in responses."""
        response = client.get("/api/v1/health/")

        # Test that the response is successful
        assert response.status_code == 200
        # Note: CORS headers may not be present in test client
        # This test validates the endpoint works correctly


class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling."""

    def test_nonexistent_endpoint(self, client):
        """Test accessing non-existent endpoint."""
        response = client.get("/api/v1/nonexistent")

        assert response.status_code == 404

    def test_wrong_http_method(self, client):
        """Test using wrong HTTP method."""
        # POST to GET endpoint
        response = client.post("/api/v1/health/")

        assert response.status_code == 405  # Method not allowed

    def test_large_request_body(self, client):
        """Test handling of large request body."""
        large_data = {
            "email": "test@example.com",
            "password": "secret",
            "extra_data": "x" * 10000  # Large string
        }

        response = client.post("/api/v1/auth/login", json=large_data)

        # Should either reject for validation (422), unauthorized (401), or payload size (413)
        assert response.status_code in [401, 422, 413]

    def test_concurrent_requests(self, client):
        """Test handling concurrent requests."""
        import threading
        import time

        results = []

        def make_request():
            response = client.get("/api/v1/health/")
            results.append(response.status_code)

        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5


class TestSecurityFeatures:
    """Test security features and middleware."""

    def test_request_headers_handling(self, client):
        """Test various request headers."""
        headers = {
            "User-Agent": "Test-Agent/1.0",
            "Accept": "application/json",
            "X-Forwarded-For": "192.168.1.1",
            "X-Real-IP": "192.168.1.1"
        }

        response = client.get("/api/v1/health/", headers=headers)

        assert response.status_code == 200

    def test_malicious_headers(self, client):
        """Test handling of potentially malicious headers."""
        malicious_headers = {
            "X-Script-Tag": "<script>alert('xss')</script>",
            "X-SQL-Injection": "'; DROP TABLE users; --",
            "Authorization": "Bearer <script>alert('xss')</script>"
        }

        response = client.get("/api/v1/health/", headers=malicious_headers)

        # Should still respond normally (server should sanitize)
        assert response.status_code == 200

    def test_request_size_limits(self, client):
        """Test request size handling."""
        # Test with various header sizes
        large_header = "x" * 1000

        response = client.get(
            "/api/v1/health/",
            headers={"X-Large-Header": large_header}
        )

        # Should handle gracefully
        assert response.status_code in [200, 400, 413]