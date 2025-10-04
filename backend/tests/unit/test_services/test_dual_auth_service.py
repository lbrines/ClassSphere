"""
Unit tests for DualAuthService.
"""
import pytest
from unittest.mock import AsyncMock, patch

from src.app.services.dual_auth_service import DualAuthService, dual_auth_service, AuthMode
from src.app.exceptions.auth import AuthenticationError


class TestDualAuthService:
    """Test DualAuthService functionality."""
    
    def test_initial_mode(self):
        """Test initial authentication mode."""
        assert dual_auth_service.get_current_mode() == AuthMode.JWT_MOCK
        assert dual_auth_service.is_jwt_mock_mode() is True
        assert dual_auth_service.is_oauth_google_mode() is False
    
    def test_set_mode(self):
        """Test setting authentication mode."""
        dual_auth_service.set_mode(AuthMode.OAUTH_GOOGLE)
        assert dual_auth_service.get_current_mode() == AuthMode.OAUTH_GOOGLE
        assert dual_auth_service.is_oauth_google_mode() is True
        assert dual_auth_service.is_jwt_mock_mode() is False
        
        # Reset to default
        dual_auth_service.set_mode(AuthMode.JWT_MOCK)
        assert dual_auth_service.get_current_mode() == AuthMode.JWT_MOCK
    
    def test_switch_to_jwt_mock(self):
        """Test switching to JWT/Mock mode."""
        dual_auth_service.switch_to_oauth_google()
        assert dual_auth_service.is_oauth_google_mode() is True
        
        dual_auth_service.switch_to_jwt_mock()
        assert dual_auth_service.is_jwt_mock_mode() is True
        assert dual_auth_service.is_oauth_google_mode() is False
    
    def test_switch_to_oauth_google(self):
        """Test switching to OAuth/Google mode."""
        dual_auth_service.switch_to_jwt_mock()
        assert dual_auth_service.is_jwt_mock_mode() is True
        
        dual_auth_service.switch_to_oauth_google()
        assert dual_auth_service.is_oauth_google_mode() is True
        assert dual_auth_service.is_jwt_mock_mode() is False
    
    @pytest.mark.asyncio
    async def test_authenticate_user_jwt_mock_admin(self):
        """Test authenticating admin user in JWT/Mock mode."""
        # Ensure we're in JWT/Mock mode
        dual_auth_service.switch_to_jwt_mock()
        
        credentials = {
            "email": "admin@example.com",
            "password": "admin123"
        }
        
        result = await dual_auth_service.authenticate_user(credentials)
        
        assert "user" in result
        assert "access_token" in result
        assert "refresh_token" in result
        assert "token_type" in result
        assert "mode" in result
        
        assert result["user"]["email"] == "admin@example.com"
        assert result["user"]["role"] == "admin"
        assert result["user"]["id"] == "mock_admin_1"
        assert result["mode"] == "jwt_mock"
        assert result["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_authenticate_user_jwt_mock_teacher(self):
        """Test authenticating teacher user in JWT/Mock mode."""
        # Ensure we're in JWT/Mock mode
        dual_auth_service.switch_to_jwt_mock()
        
        credentials = {
            "email": "teacher@example.com",
            "password": "teacher123"
        }
        
        result = await dual_auth_service.authenticate_user(credentials)
        
        assert result["user"]["email"] == "teacher@example.com"
        assert result["user"]["role"] == "teacher"
        assert result["user"]["id"] == "mock_teacher_1"
        assert result["mode"] == "jwt_mock"
    
    @pytest.mark.asyncio
    async def test_authenticate_user_jwt_mock_student(self):
        """Test authenticating student user in JWT/Mock mode."""
        # Ensure we're in JWT/Mock mode
        dual_auth_service.switch_to_jwt_mock()
        
        credentials = {
            "email": "student@example.com",
            "password": "student123"
        }
        
        result = await dual_auth_service.authenticate_user(credentials)
        
        assert result["user"]["email"] == "student@example.com"
        assert result["user"]["role"] == "student"
        assert result["user"]["id"] == "mock_student_1"
        assert result["mode"] == "jwt_mock"
    
    @pytest.mark.asyncio
    async def test_authenticate_user_jwt_mock_invalid_credentials(self):
        """Test authenticating with invalid credentials in JWT/Mock mode."""
        # Ensure we're in JWT/Mock mode
        dual_auth_service.switch_to_jwt_mock()
        
        credentials = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        
        with pytest.raises(AuthenticationError, match="Invalid credentials for JWT/Mock mode"):
            await dual_auth_service.authenticate_user(credentials)
    
    @pytest.mark.asyncio
    async def test_authenticate_user_jwt_mock_missing_credentials(self):
        """Test authenticating with missing credentials in JWT/Mock mode."""
        # Ensure we're in JWT/Mock mode
        dual_auth_service.switch_to_jwt_mock()
        
        credentials = {
            "email": "test@example.com"
            # Missing password
        }
        
        with pytest.raises(AuthenticationError, match="Email and password required for JWT/Mock mode"):
            await dual_auth_service.authenticate_user(credentials)
    
    @pytest.mark.asyncio
    async def test_authenticate_user_oauth_google_success(self):
        """Test authenticating user in OAuth/Google mode."""
        # Switch to OAuth/Google mode
        dual_auth_service.switch_to_oauth_google()
        
        credentials = {
            "code": "mock_auth_code_123"
        }
        
        mock_token_response = {
            "access_token": "google_access_token",
            "refresh_token": "google_refresh_token",
            "expires_in": 3600
        }
        
        mock_user_info = {
            "id": "google_user_123",
            "email": "user@example.com",
            "name": "Google User",
            "picture": "https://example.com/photo.jpg"
        }
        
        with patch.object(dual_auth_service.oauth_service, 'exchange_code_for_token', 
                         return_value=mock_token_response) as mock_exchange, \
             patch.object(dual_auth_service.oauth_service, 'get_user_info', 
                         return_value=mock_user_info) as mock_user_info_func:
            
            result = await dual_auth_service.authenticate_user(credentials)
            
            assert "user" in result
            assert "access_token" in result
            assert "refresh_token" in result
            assert "token_type" in result
            assert "mode" in result
            assert "google_tokens" in result
            
            assert result["user"]["email"] == "user@example.com"
            assert result["user"]["role"] == "student"  # Default role
            assert result["user"]["google_id"] == "google_user_123"
            assert result["mode"] == "oauth_google"
            assert result["token_type"] == "bearer"
            assert result["google_tokens"] == mock_token_response
            
            mock_exchange.assert_called_once_with("mock_auth_code_123")
            mock_user_info_func.assert_called_once_with("google_access_token")
    
    @pytest.mark.asyncio
    async def test_authenticate_user_oauth_google_missing_code(self):
        """Test authenticating with missing code in OAuth/Google mode."""
        dual_auth_service.switch_to_oauth_google()
        
        credentials = {
            "email": "test@example.com"
            # Missing code
        }
        
        with pytest.raises(AuthenticationError, match="Authorization code required for OAuth/Google mode"):
            await dual_auth_service.authenticate_user(credentials)
    
    @pytest.mark.asyncio
    async def test_authenticate_user_oauth_google_exchange_error(self):
        """Test authenticating with OAuth exchange error."""
        dual_auth_service.switch_to_oauth_google()
        
        credentials = {
            "code": "invalid_code"
        }
        
        with patch.object(dual_auth_service.oauth_service, 'exchange_code_for_token', 
                         side_effect=Exception("OAuth error")):
            
            with pytest.raises(Exception, match="OAuth error"):
                await dual_auth_service.authenticate_user(credentials)
    
    def test_get_auth_url_jwt_mock(self):
        """Test getting auth URL for JWT/Mock mode."""
        dual_auth_service.switch_to_jwt_mock()
        auth_url = dual_auth_service.get_auth_url()
        
        assert auth_url == "/auth/mock"
    
    def test_get_auth_url_oauth_google(self):
        """Test getting auth URL for OAuth/Google mode."""
        dual_auth_service.switch_to_oauth_google()
        
        with patch.object(dual_auth_service.oauth_service, 'google_oauth_flow', 
                         return_value="https://accounts.google.com/o/oauth2/v2/auth?test=123") as mock_flow:
            
            auth_url = dual_auth_service.get_auth_url()
            
            assert auth_url == "https://accounts.google.com/o/oauth2/v2/auth?test=123"
            mock_flow.assert_called_once_with()
    
    def test_get_auth_url_specific_mode(self):
        """Test getting auth URL for specific mode."""
        with patch.object(dual_auth_service.oauth_service, 'google_oauth_flow', 
                         return_value="https://accounts.google.com/o/oauth2/v2/auth?test=123") as mock_flow:
            
            # Request OAuth URL while in JWT mode
            auth_url = dual_auth_service.get_auth_url(AuthMode.OAUTH_GOOGLE)
            
            assert auth_url == "https://accounts.google.com/o/oauth2/v2/auth?test=123"
            mock_flow.assert_called_once_with()
    
    def test_verify_token(self):
        """Test token verification."""
        user_data = {
            "id": "user123",
            "email": "test@example.com",
            "role": "student"
        }
        
        token = dual_auth_service.auth_service.create_access_token(user_data)
        payload = dual_auth_service.verify_token(token)
        
        assert payload["id"] == "user123"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "student"
    
    def test_dual_auth_service_initialization(self):
        """Test DualAuthService initialization."""
        # Reset to default mode
        dual_auth_service.switch_to_jwt_mock()
        
        assert dual_auth_service.auth_service is not None
        assert dual_auth_service.oauth_service is not None
        assert dual_auth_service.get_current_mode() == AuthMode.JWT_MOCK