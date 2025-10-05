"""
Tests de integración para OAuth
"""
import pytest
from unittest.mock import patch, Mock


def test_get_google_auth_url(client):
    """Test obtención de URL de autorización Google"""
    with patch('app.api.endpoints.oauth.GoogleOAuthService') as mock_service_class:
        mock_service = Mock()
        mock_service.get_authorization_url.return_value = (
            "https://accounts.google.com/o/oauth2/auth?test=1",
            "test-verifier"
        )
        mock_service_class.return_value = mock_service
        
        response = client.post("/api/v1/oauth/google/url")
        
        assert response.status_code == 200
        data = response.json()
        assert "authorization_url" in data
        assert "state" in data
        assert "accounts.google.com" in data["authorization_url"]


def test_get_google_auth_url_with_state(client):
    """Test obtención de URL con state personalizado"""
    with patch('app.api.endpoints.oauth.GoogleOAuthService') as mock_service_class:
        mock_service = Mock()
        mock_service.get_authorization_url.return_value = (
            "https://accounts.google.com/o/oauth2/auth?test=1",
            "test-verifier"
        )
        mock_service_class.return_value = mock_service
        
        response = client.post("/api/v1/oauth/google/url?state=custom-state")
        
        assert response.status_code == 200
        data = response.json()
        assert data["state"] == "custom-state"


def test_google_oauth_callback_success(client):
    """Test callback exitoso de OAuth"""
    with patch('app.api.endpoints.oauth.GoogleOAuthService') as mock_service_class, \
         patch('app.api.endpoints.oauth.AuthService') as mock_auth_class:
        
        # Mock Google service
        mock_google_service = Mock()
        mock_credentials = Mock()
        mock_google_service.exchange_code_for_token.return_value = mock_credentials
        mock_google_service.get_user_info.return_value = {
            'id': '123456789',
            'email': 'test@example.com',
            'name': 'Test User',
            'picture': 'https://example.com/pic.jpg',
            'verified_email': True
        }
        mock_service_class.return_value = mock_google_service
        
        # Mock Auth service
        mock_auth_service = Mock()
        mock_auth_service.get_user_by_email.return_value = None  # Usuario nuevo
        mock_auth_class.return_value = mock_auth_service
        
        response = client.post(
            "/api/v1/oauth/google/callback",
            json={
                "code": "test-code",
                "state": "test-state",
                "code_verifier": "test-verifier"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"


def test_google_oauth_callback_existing_user(client):
    """Test callback con usuario existente"""
    with patch('app.api.endpoints.oauth.GoogleOAuthService') as mock_service_class, \
         patch('app.api.endpoints.oauth.AuthService') as mock_auth_class:
        
        # Mock Google service
        mock_google_service = Mock()
        mock_credentials = Mock()
        mock_google_service.exchange_code_for_token.return_value = mock_credentials
        mock_google_service.get_user_info.return_value = {
            'id': '123456789',
            'email': 'existing@example.com',
            'name': 'Existing User',
            'picture': 'https://example.com/pic.jpg',
            'verified_email': True
        }
        mock_service_class.return_value = mock_google_service
        
        # Mock Auth service - usuario existente
        from app.models.user import User, UserRole
        existing_user = User(
            id="user-001",
            email="existing@example.com",
            name="Existing User",
            role=UserRole.TEACHER,
            is_active=True
        )
        mock_auth_service = Mock()
        mock_auth_service.get_user_by_email.return_value = existing_user
        mock_auth_class.return_value = mock_auth_service
        
        response = client.post(
            "/api/v1/oauth/google/callback",
            json={
                "code": "test-code",
                "state": "test-state",
                "code_verifier": "test-verifier"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "existing@example.com"
        assert data["user"]["id"] == "user-001"


def test_google_oauth_callback_token_exchange_failure(client):
    """Test fallo en intercambio de token"""
    with patch('app.api.endpoints.oauth.GoogleOAuthService') as mock_service_class:
        mock_google_service = Mock()
        mock_google_service.exchange_code_for_token.return_value = None
        mock_service_class.return_value = mock_google_service
        
        response = client.post(
            "/api/v1/oauth/google/callback",
            json={
                "code": "invalid-code",
                "state": "test-state",
                "code_verifier": "test-verifier"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Failed to exchange code for token" in data["detail"]


def test_google_oauth_callback_user_info_failure(client):
    """Test fallo en obtención de información de usuario"""
    with patch('app.api.endpoints.oauth.GoogleOAuthService') as mock_service_class:
        mock_google_service = Mock()
        mock_credentials = Mock()
        mock_google_service.exchange_code_for_token.return_value = mock_credentials
        mock_google_service.get_user_info.return_value = None
        mock_service_class.return_value = mock_google_service
        
        response = client.post(
            "/api/v1/oauth/google/callback",
            json={
                "code": "test-code",
                "state": "test-state",
                "code_verifier": "test-verifier"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Failed to get user information" in data["detail"]


def test_get_google_mode(client):
    """Test obtención del modo de Google"""
    response = client.get("/api/v1/oauth/google/mode")
    
    assert response.status_code == 200
    data = response.json()
    assert "mode" in data
    assert "client_id_configured" in data
    assert "redirect_uri" in data
    assert data["redirect_uri"] == "http://localhost:3000/auth/callback"
