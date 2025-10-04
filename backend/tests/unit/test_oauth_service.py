"""Tests for OAuthService."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch, MagicMock

from src.app.services.oauth_service import OAuthService
from src.app.core.exceptions import OAuthError, GoogleAPIError
from src.app.models.oauth import OAuthTokenResponse, GoogleOAuthProfile


class TestOAuthService:
    """Test cases for OAuthService."""

    @pytest.fixture
    def oauth_service(self):
        """Create OAuthService instance."""
        with patch('src.app.services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = "test_client_id"
            mock_settings.google_client_secret = "test_client_secret"
            mock_settings.google_redirect_uri = "http://localhost:3000/auth/google/callback"
            mock_settings.google_classroom_scopes = "scope1,scope2"
            yield OAuthService()

    @pytest.fixture
    def mock_credentials(self):
        """Mock Google credentials."""
        credentials = MagicMock()
        credentials.token = "access_token_123"
        credentials.refresh_token = "refresh_token_123"
        credentials.expiry = 3600
        credentials.scopes = ["scope1", "scope2"]
        return credentials

    @pytest.fixture
    def mock_user_info(self):
        """Mock Google user info."""
        return {
            "id": "google_user_123",
            "email": "user@gmail.com",
            "verified_email": True,
            "name": "Test User",
            "given_name": "Test",
            "family_name": "User",
            "picture": "https://example.com/picture.jpg",
            "locale": "en"
        }

    def test_generate_oauth_url_success(self, oauth_service):
        """Test generating OAuth URL successfully."""
        url = oauth_service.generate_oauth_url()
        
        assert "https://accounts.google.com/o/oauth2/v2/auth" in url
        assert "client_id=test_client_id" in url
        assert "redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fauth%2Fgoogle%2Fcallback" in url
        assert "scope=scope1+scope2" in url
        assert "response_type=code" in url
        assert "access_type=offline" in url
        assert "prompt=consent" in url
        assert "state=" in url

    def test_generate_oauth_url_with_state(self, oauth_service):
        """Test generating OAuth URL with custom state."""
        custom_state = "custom_state_123"
        url = oauth_service.generate_oauth_url(state=custom_state)
        
        assert f"state={custom_state}" in url

    def test_generate_oauth_url_no_client_id(self):
        """Test generating OAuth URL without client ID."""
        with patch('src.app.services.oauth_service.settings') as mock_settings:
            mock_settings.google_client_id = None
            mock_settings.google_client_secret = "test_secret"
            mock_settings.google_redirect_uri = "http://localhost:3000/auth/google/callback"
            mock_settings.google_classroom_scopes = "scope1,scope2"
            
            oauth_service = OAuthService()
            
            with pytest.raises(OAuthError, match="Google client ID not configured"):
                oauth_service.generate_oauth_url()

    @pytest.mark.asyncio
    async def test_exchange_code_for_token_success(self, oauth_service, mock_credentials):
        """Test successful code exchange for token."""
        with patch('src.app.services.oauth_service.Flow') as mock_flow_class:
            mock_flow = MagicMock()
            mock_flow_class.from_client_config.return_value = mock_flow
            mock_flow.credentials = mock_credentials
            
            result = await oauth_service.exchange_code_for_token("auth_code_123")
            
            assert isinstance(result, OAuthTokenResponse)
            assert result.token_type == "Bearer"
            assert result.provider == "google"
            assert result.scope == "scope1 scope2"

    @pytest.mark.asyncio
    async def test_exchange_code_for_token_error(self, oauth_service):
        """Test code exchange with error."""
        with patch('src.app.services.oauth_service.Flow') as mock_flow_class:
            mock_flow = MagicMock()
            mock_flow_class.from_client_config.return_value = mock_flow
            mock_flow.fetch_token.side_effect = Exception("Exchange failed")
            
            with pytest.raises(OAuthError, match="Failed to exchange code for token"):
                await oauth_service.exchange_code_for_token("invalid_code")

    @pytest.mark.asyncio
    async def test_refresh_access_token_success(self, oauth_service, mock_credentials):
        """Test successful token refresh."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class, \
             patch('src.app.services.oauth_service.Request') as mock_request_class:
            
            mock_creds_instance = MagicMock()
            mock_creds_class.return_value = mock_creds_instance
            mock_creds_instance.token = "new_access_token"
            mock_creds_instance.refresh_token = "new_refresh_token"
            mock_creds_instance.expiry = 3600
            mock_creds_instance.scopes = ["scope1", "scope2"]
            
            result = await oauth_service.refresh_access_token("old_refresh_token")
            
            assert isinstance(result, OAuthTokenResponse)
            assert result.token_type == "Bearer"
            assert result.provider == "google"
            assert result.scope == "scope1 scope2"

    @pytest.mark.asyncio
    async def test_refresh_access_token_error(self, oauth_service):
        """Test token refresh with error."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class:
            mock_creds_instance = MagicMock()
            mock_creds_class.return_value = mock_creds_instance
            mock_creds_instance.refresh.side_effect = Exception("Refresh failed")
            
            with pytest.raises(OAuthError, match="Failed to refresh token"):
                await oauth_service.refresh_access_token("invalid_refresh_token")

    @pytest.mark.asyncio
    async def test_get_user_profile_success(self, oauth_service, mock_user_info):
        """Test successful user profile retrieval."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class, \
             patch('src.app.services.oauth_service.build') as mock_build:
            
            mock_service = MagicMock()
            mock_service.userinfo.return_value.get.return_value.execute.return_value = mock_user_info
            mock_build.return_value = mock_service
            
            result = await oauth_service.get_user_profile("access_token_123")
            
            assert isinstance(result, GoogleOAuthProfile)
            assert result.id == "google_user_123"
            assert result.email == "user@gmail.com"
            assert result.verified_email is True
            assert result.name == "Test User"
            assert result.given_name == "Test"
            assert result.family_name == "User"
            assert str(result.picture) == "https://example.com/picture.jpg"
            assert result.locale == "en"

    @pytest.mark.asyncio
    async def test_get_user_profile_error(self, oauth_service):
        """Test user profile retrieval with error."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class, \
             patch('src.app.services.oauth_service.build') as mock_build:
            
            mock_service = MagicMock()
            mock_service.userinfo.return_value.get.return_value.execute.side_effect = Exception("API Error")
            mock_build.return_value = mock_service
            
            with pytest.raises(GoogleAPIError, match="Failed to get user profile"):
                await oauth_service.get_user_profile("invalid_token")

    @pytest.mark.asyncio
    async def test_validate_token_success(self, oauth_service):
        """Test successful token validation."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class, \
             patch('src.app.services.oauth_service.build') as mock_build:
            
            mock_service = MagicMock()
            mock_service.userinfo.return_value.get.return_value.execute.return_value = {"id": "user123"}
            mock_build.return_value = mock_service
            
            result = await oauth_service.validate_token("valid_token")
            
            assert result is True

    @pytest.mark.asyncio
    async def test_validate_token_failure(self, oauth_service):
        """Test token validation failure."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class, \
             patch('src.app.services.oauth_service.build') as mock_build:
            
            mock_service = MagicMock()
            mock_service.userinfo.return_value.get.return_value.execute.side_effect = Exception("Invalid token")
            mock_build.return_value = mock_service
            
            result = await oauth_service.validate_token("invalid_token")
            
            assert result is False

    def test_get_classroom_service_success(self, oauth_service):
        """Test successful Classroom service creation."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class, \
             patch('src.app.services.oauth_service.build') as mock_build:
            
            mock_service = MagicMock()
            mock_build.return_value = mock_service
            
            result = oauth_service.get_classroom_service("access_token_123")
            
            assert result == mock_service
            mock_build.assert_called_once_with('classroom', 'v1', credentials=mock_creds_class.return_value)

    def test_get_classroom_service_error(self, oauth_service):
        """Test Classroom service creation with error."""
        with patch('src.app.services.oauth_service.Credentials') as mock_creds_class, \
             patch('src.app.services.oauth_service.build') as mock_build:
            
            mock_build.side_effect = Exception("Service creation failed")
            
            with pytest.raises(GoogleAPIError, match="Failed to create Classroom service"):
                oauth_service.get_classroom_service("invalid_token")

    def test_oauth_service_initialization(self, oauth_service):
        """Test OAuth service initialization."""
        assert oauth_service.client_id == "test_client_id"
        assert oauth_service.client_secret == "test_client_secret"
        assert oauth_service.redirect_uri == "http://localhost:3000/auth/google/callback"
        assert oauth_service.scopes == ["scope1", "scope2"]