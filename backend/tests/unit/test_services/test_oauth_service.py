"""
Unit tests for OAuthService.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from src.app.services.oauth_service import OAuthService, oauth_service
from src.app.exceptions.oauth import OAuthError, OAuthTokenError, OAuthAuthorizationError


class TestOAuthService:
    """Test OAuthService functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.oauth_service = OAuthService()
        self.test_code = "test_auth_code_123"
        self.test_access_token = "test_access_token_123"
        self.test_refresh_token = "test_refresh_token_123"
    
    def test_google_oauth_flow_success(self):
        """Test successful Google OAuth flow URL generation."""
        auth_url = self.oauth_service.google_oauth_flow()
        
        assert isinstance(auth_url, str)
        assert "accounts.google.com/o/oauth2/v2/auth" in auth_url
        assert "client_id=" in auth_url
        assert "redirect_uri=" in auth_url
        assert "scope=" in auth_url
        assert "response_type=code" in auth_url
        assert "access_type=offline" in auth_url
        assert "prompt=consent" in auth_url
    
    def test_google_oauth_flow_with_state(self):
        """Test Google OAuth flow URL generation with state parameter."""
        state = "test_state_123"
        auth_url = self.oauth_service.google_oauth_flow(state=state)
        
        assert isinstance(auth_url, str)
        assert f"state={state}" in auth_url
    
    @pytest.mark.asyncio
    async def test_exchange_code_for_token_success(self):
        """Test successful code exchange for token."""
        mock_response_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_response.raise_for_status = AsyncMock(return_value=None)
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
            
            result = await oauth_service.exchange_code_for_token("test_code")
            
            assert result == mock_response_data
            assert "access_token" in result
            assert "refresh_token" in result
    
    @pytest.mark.asyncio
    async def test_exchange_code_for_token_no_access_token(self):
        """Test code exchange with response missing access token."""
        mock_response_data = {
            "error": "invalid_grant",
            "error_description": "Invalid authorization code"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_response.raise_for_status = AsyncMock(return_value=None)
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
            
            with pytest.raises(OAuthError, match="No access token in response"):
                await oauth_service.exchange_code_for_token("test_code")
    
    @pytest.mark.asyncio
    async def test_exchange_code_for_token_http_error(self):
        """Test code exchange with HTTP error."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.side_effect = httpx.HTTPStatusError(
                "HTTP error", request=MagicMock(), response=MagicMock()
            )
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(OAuthError, match="HTTP error during token exchange"):
                await oauth_service.exchange_code_for_token("test_code")
    
    @pytest.mark.asyncio
    async def test_exchange_code_for_token_request_error(self):
        """Test code exchange with request error."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.side_effect = httpx.RequestError("Request failed")
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(OAuthError, match="Request error during token exchange"):
                await oauth_service.exchange_code_for_token("test_code")
    
    @pytest.mark.asyncio
    async def test_get_user_info_success(self):
        """Test successful user info retrieval."""
        mock_user_data = {
            "id": "google_user_123",
            "email": "user@example.com",
            "name": "Test User",
            "picture": "https://example.com/photo.jpg",
            "verified_email": True
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_user_data
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            result = await self.oauth_service.get_user_info(self.test_access_token)
            
            assert result == mock_user_data
            assert "id" in result
            assert "email" in result
    
    @pytest.mark.asyncio
    async def test_get_user_info_no_user_id(self):
        """Test user info retrieval with response missing user ID."""
        mock_user_data = {
            "email": "user@example.com",
            "name": "Test User"
            # Missing 'id' field
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_user_data
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = AsyncMock()
            mock_client_instance.get = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(OAuthError, match="No user ID in Google response"):
                await oauth_service.get_user_info("test_access_token")
    
    @pytest.mark.asyncio
    async def test_get_user_info_http_error(self):
        """Test user info retrieval with HTTP error."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.get.side_effect = httpx.HTTPStatusError(
                "HTTP error", request=MagicMock(), response=MagicMock()
            )
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(OAuthError, match="HTTP error getting user info"):
                await oauth_service.get_user_info("test_access_token")
    
    @pytest.mark.asyncio
    async def test_refresh_access_token_success(self):
        """Test successful access token refresh."""
        mock_response_data = {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_response.raise_for_status = AsyncMock(return_value=None)
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
            
            result = await self.oauth_service.refresh_access_token(self.test_refresh_token)
            
            assert result == mock_response_data
            assert "access_token" in result
    
    @pytest.mark.asyncio
    async def test_refresh_access_token_no_access_token(self):
        """Test token refresh with response missing access token."""
        mock_response_data = {
            "error": "invalid_grant",
            "error_description": "Invalid refresh token"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_response.raise_for_status = AsyncMock(return_value=None)
            
            mock_client_instance = AsyncMock()
            mock_client_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_client_instance)
            
            with pytest.raises(OAuthError, match="Unexpected error during token refresh"):
                await oauth_service.refresh_access_token("test_refresh_token")
    
    @pytest.mark.asyncio
    async def test_refresh_access_token_http_error(self):
        """Test token refresh with HTTP error."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client_instance = AsyncMock()
            mock_client_instance.post.side_effect = httpx.HTTPStatusError(
                "HTTP error", request=MagicMock(), response=MagicMock()
            )
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            with pytest.raises(OAuthError, match="HTTP error during token refresh"):
                await oauth_service.refresh_access_token("test_refresh_token")
    
    def test_global_oauth_service_instance(self):
        """Test global oauth_service instance."""
        assert oauth_service is not None
        assert isinstance(oauth_service, OAuthService)
        
        # Test that global instance works
        auth_url = oauth_service.google_oauth_flow()
        assert isinstance(auth_url, str)
        assert "accounts.google.com" in auth_url