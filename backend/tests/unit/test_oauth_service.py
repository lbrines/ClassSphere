"""
Test file for oauth_service.py

CRITICAL OBJECTIVES:
- Verify Google OAuth 2.0 with PKCE
- Test state validation for security
- Test user profile fetching
- Test integration with JWT authentication

DEPENDENCIES:
- httpx for HTTP requests
- pytest-asyncio
- unittest.mock
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import json

from src.app.services.oauth_service import OAuthService
from src.app.core.config import get_settings

# BEGINNING: Critical tests for core functionality
@pytest.mark.asyncio(timeout=2.0)
async def test_pkce_pair_generation():
    """Test PKCE code verifier and challenge generation"""
    # Arrange
    oauth_service = OAuthService()
    
    # Act
    code_verifier, code_challenge = oauth_service.generate_pkce_pair()
    
    # Assert
    assert code_verifier is not None
    assert code_challenge is not None
    assert len(code_verifier) >= 43
    assert len(code_verifier) <= 128
    assert len(code_challenge) == 43  # Base64 URL-safe encoded SHA256

@pytest.mark.asyncio(timeout=2.0)
async def test_state_generation_and_validation():
    """Test state generation and validation"""
    # Arrange
    oauth_service = OAuthService()
    
    # Act
    state = oauth_service.generate_state()
    code_verifier = "test_code_verifier"
    oauth_service.store_state_data(state, code_verifier)
    
    # Assert
    assert state is not None
    assert len(state) > 0
    
    # Test validation
    retrieved_verifier = oauth_service.validate_state(state)
    assert retrieved_verifier == code_verifier
    
    # Test invalid state
    invalid_verifier = oauth_service.validate_state("invalid_state")
    assert invalid_verifier is None

@pytest.mark.asyncio(timeout=2.0)
async def test_authorization_url_generation():
    """Test Google OAuth authorization URL generation"""
    # Arrange
    oauth_service = OAuthService()
    settings = get_settings()
    
    # Act
    result = oauth_service.get_authorization_url()
    
    # Assert
    assert "authorization_url" in result
    assert "state" in result
    assert "code_verifier" in result
    
    auth_url = result["authorization_url"]
    assert "https://accounts.google.com/o/oauth2/v2/auth" in auth_url
    assert f"client_id={settings.google_client_id}" in auth_url
    assert "redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth%2Fgoogle%2Fcallback" in auth_url
    assert "response_type=code" in auth_url
    assert "scope=openid+email+profile" in auth_url
    assert "code_challenge=" in auth_url
    assert "code_challenge_method=S256" in auth_url

@pytest.mark.asyncio(timeout=2.0)
async def test_token_exchange_success():
    """Test successful token exchange"""
    # Arrange
    oauth_service = OAuthService()
    state = "test_state"
    code_verifier = "test_code_verifier"
    oauth_service.store_state_data(state, code_verifier)
    
    mock_response = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "expires_in": 3600,
        "token_type": "Bearer"
    }
    
    with patch('httpx.AsyncClient') as mock_client_class:
        # Create a mock client instance
        mock_client = AsyncMock()
        mock_response_obj = AsyncMock()
        mock_response_obj.status_code = 200
        mock_response_obj.json = AsyncMock(return_value=mock_response)
        
        mock_client.post = AsyncMock(return_value=mock_response_obj)
        mock_client_class.return_value.__aenter__ = AsyncMock(return_value=mock_client)
        
        # Act
        result = await oauth_service.exchange_code_for_tokens("test_code", state)
        
        # Assert
        assert result is not None
        assert result["access_token"] == "mock_access_token"
        assert result["refresh_token"] == "mock_refresh_token"

@pytest.mark.asyncio(timeout=2.0)
async def test_token_exchange_invalid_state():
    """Test token exchange with invalid state"""
    # Arrange
    oauth_service = OAuthService()
    
    # Act
    result = await oauth_service.exchange_code_for_tokens("test_code", "invalid_state")
    
    # Assert
    assert result is None

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=2.0)
async def test_user_info_retrieval():
    """Test user information retrieval from Google"""
    # Arrange
    oauth_service = OAuthService()
    access_token = "mock_access_token"
    
    mock_user_info = {
        "id": "google_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "https://example.com/picture.jpg",
        "verified_email": True
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response_obj = AsyncMock()
        mock_response_obj.status_code = 200
        mock_response_obj.json = AsyncMock(return_value=mock_user_info)
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response_obj)
        
        # Act
        result = await oauth_service.get_user_info(access_token)
        
        # Assert
        assert result is not None
        assert result["id"] == "google_user_123"
        assert result["email"] == "test@example.com"
        assert result["name"] == "Test User"

@pytest.mark.asyncio(timeout=2.0)
async def test_user_creation_from_google_profile():
    """Test user creation from Google profile"""
    # Arrange
    oauth_service = OAuthService()
    user_info = {
        "id": "google_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "https://example.com/picture.jpg",
        "verified_email": True
    }
    
    # Act
    result = await oauth_service.create_or_update_user(user_info)
    
    # Assert
    assert "user" in result
    assert "tokens" in result
    
    user = result["user"]
    assert user["sub"] == "google_google_user_123"
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"
    assert user["role"] == "student"  # Default role
    assert user["provider"] == "google"
    assert user["verified"] is True
    
    tokens = result["tokens"]
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

@pytest.mark.asyncio(timeout=2.0)
async def test_oauth_callback_complete_flow():
    """Test complete OAuth callback flow"""
    # Arrange
    oauth_service = OAuthService()
    state = "test_state"
    code_verifier = "test_code_verifier"
    oauth_service.store_state_data(state, code_verifier)
    
    mock_token_response = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "expires_in": 3600,
        "token_type": "Bearer"
    }
    
    mock_user_info = {
        "id": "google_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "https://example.com/picture.jpg",
        "verified_email": True
    }
    
    with patch('httpx.AsyncClient') as mock_client:
        # Mock token exchange
        mock_post_response = AsyncMock()
        mock_post_response.status_code = 200
        mock_post_response.json = AsyncMock(return_value=mock_token_response)
        
        # Mock user info request
        mock_get_response = AsyncMock()
        mock_get_response.status_code = 200
        mock_get_response.json = AsyncMock(return_value=mock_user_info)
        
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_post_response)
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_get_response)
        
        # Act
        result = await oauth_service.handle_oauth_callback("test_code", state)
        
        # Assert
        assert result is not None
        assert "user" in result
        assert "tokens" in result
        assert "google_tokens" in result
        
        user = result["user"]
        assert user["sub"] == "google_google_user_123"
        assert user["email"] == "test@example.com"
        
        google_tokens = result["google_tokens"]
        assert google_tokens["access_token"] == "mock_access_token"
        assert google_tokens["refresh_token"] == "mock_refresh_token"

# END: Verification and next steps
@pytest.mark.asyncio(timeout=2.0)
async def test_token_exchange_failure():
    """Test token exchange failure handling"""
    # Arrange
    oauth_service = OAuthService()
    state = "test_state"
    code_verifier = "test_code_verifier"
    oauth_service.store_state_data(state, code_verifier)
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response_obj = AsyncMock()
        mock_response_obj.status_code = 400
        mock_response_obj.text = "Invalid request"
        
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_response_obj)
        
        # Act
        result = await oauth_service.exchange_code_for_tokens("test_code", state)
        
        # Assert
        assert result is None

@pytest.mark.asyncio(timeout=2.0)
async def test_user_info_retrieval_failure():
    """Test user info retrieval failure handling"""
    # Arrange
    oauth_service = OAuthService()
    access_token = "invalid_token"
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response_obj = AsyncMock()
        mock_response_obj.status_code = 401
        mock_response_obj.text = "Unauthorized"
        
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response_obj)
        
        # Act
        result = await oauth_service.get_user_info(access_token)
        
        # Assert
        assert result is None

@pytest.mark.asyncio(timeout=2.0)
async def test_invalid_user_data_handling():
    """Test handling of invalid user data from Google"""
    # Arrange
    oauth_service = OAuthService()
    invalid_user_info = {
        "id": None,  # Invalid ID
        "email": None  # Invalid email
    }
    
    # Act & Assert
    with pytest.raises(ValueError, match="Failed to create or update user"):
        await oauth_service.create_or_update_user(invalid_user_info)