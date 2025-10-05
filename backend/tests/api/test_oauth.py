"""
Tests for OAuth 2.0 Google endpoints
"""
import pytest
from unittest.mock import patch, MagicMock


class TestOAuthGoogle:
    """Test Google OAuth functionality"""

    def test_google_oauth_url_generation(self, client):
        """Test Google OAuth URL generation"""
        response = client.get("/api/v1/oauth/google/url")
        assert response.status_code == 200

        data = response.json()
        assert "url" in data
        assert "code_verifier" in data

        # Verify URL contains required parameters
        url = data["url"]
        assert "accounts.google.com/o/oauth2/v2/auth" in url
        assert "response_type=code" in url
        assert "client_id=" in url
        assert "redirect_uri=" in url
        assert "scope=" in url
        assert "code_challenge=" in url
        assert "code_challenge_method=S256" in url

    def test_google_oauth_url_multiple_calls(self, client):
        """Test multiple OAuth URL generations return different verifiers"""
        response1 = client.get("/api/v1/oauth/google/url")
        response2 = client.get("/api/v1/oauth/google/url")

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        # Each call should generate different code verifiers
        assert data1["code_verifier"] != data2["code_verifier"]

    @patch('app.services.google_oauth_service.requests.post')
    def test_google_oauth_callback_success(self, mock_post, client):
        """Test successful Google OAuth callback"""
        # Mock Google token response
        mock_token_response = MagicMock()
        mock_token_response.status_code = 200
        mock_token_response.json.return_value = {
            "access_token": "mock_access_token",
            "id_token": "mock_id_token"
        }

        # Mock Google userinfo response
        mock_userinfo_response = MagicMock()
        mock_userinfo_response.status_code = 200
        mock_userinfo_response.json.return_value = {
            "sub": "123456789",
            "email": "test@gmail.com",
            "given_name": "Test",
            "family_name": "User",
            "picture": "https://example.com/avatar.jpg"
        }

        mock_post.return_value = mock_token_response

        with patch('app.services.google_oauth_service.requests.get',
                  return_value=mock_userinfo_response):
            response = client.post(
                "/api/v1/oauth/google/callback",
                json={
                    "code": "mock_auth_code",
                    "code_verifier": "mock_code_verifier"
                }
            )

        assert response.status_code == 200
        data = response.json()

        assert "user" in data
        assert "token" in data

        user = data["user"]
        assert user["email"] == "test@gmail.com"
        assert user["google_id"] == "123456789"

    def test_google_oauth_callback_missing_code(self, client):
        """Test OAuth callback with missing authorization code"""
        response = client.post(
            "/api/v1/oauth/google/callback",
            json={"code_verifier": "mock_code_verifier"}
        )
        assert response.status_code == 422

    def test_google_oauth_callback_missing_verifier(self, client):
        """Test OAuth callback with missing code verifier"""
        response = client.post(
            "/api/v1/oauth/google/callback",
            json={"code": "mock_auth_code"}
        )
        assert response.status_code == 422

    @patch('app.services.google_oauth_service.requests.post')
    def test_google_oauth_callback_invalid_code(self, mock_post, client):
        """Test OAuth callback with invalid authorization code"""
        # Mock Google error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "invalid_grant"}
        mock_post.return_value = mock_response

        response = client.post(
            "/api/v1/oauth/google/callback",
            json={
                "code": "invalid_auth_code",
                "code_verifier": "mock_code_verifier"
            }
        )
        assert response.status_code == 400

    def test_google_oauth_callback_empty_request(self, client):
        """Test OAuth callback with empty request body"""
        response = client.post("/api/v1/oauth/google/callback", json={})
        assert response.status_code == 422

    def test_google_oauth_callback_invalid_json(self, client):
        """Test OAuth callback with invalid JSON"""
        response = client.post(
            "/api/v1/oauth/google/callback",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422