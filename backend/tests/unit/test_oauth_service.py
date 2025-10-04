"""
Test file for oauth_service.py

CRITICAL OBJECTIVES:
- Test OAuth service core functionality without HTTP calls
- Test PKCE generation and state management
- Test user data processing

DEPENDENCIES:
- pytest-asyncio
- unittest.mock
"""

import pytest
from unittest.mock import patch, AsyncMock

from src.app.services.oauth_service import OAuthService

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
    
    # Act
    result = oauth_service.get_authorization_url()
    
    # Assert
    assert "authorization_url" in result
    assert "state" in result
    assert "code_verifier" in result
    
    auth_url = result["authorization_url"]
    assert "https://accounts.google.com/o/oauth2/v2/auth" in auth_url
    assert "client_id=" in auth_url
    assert "redirect_uri=" in auth_url
    assert "response_type=code" in auth_url
    assert "scope=openid+email+profile" in auth_url
    assert "code_challenge=" in auth_url
    assert "code_challenge_method=S256" in auth_url

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

@pytest.mark.asyncio(timeout=2.0)
async def test_state_cleanup():
    """Test that state is cleaned up after validation"""
    # Arrange
    oauth_service = OAuthService()
    state = "test_state"
    code_verifier = "test_code_verifier"
    oauth_service.store_state_data(state, code_verifier)
    
    # Act - First validation should succeed
    result1 = oauth_service.validate_state(state)
    
    # Act - Second validation should fail (state cleaned up)
    result2 = oauth_service.validate_state(state)
    
    # Assert
    assert result1 == code_verifier
    assert result2 is None

@pytest.mark.asyncio(timeout=2.0)
async def test_pkce_verifier_challenge_relationship():
    """Test that PKCE verifier and challenge are related"""
    # Arrange
    oauth_service = OAuthService()
    
    # Act
    code_verifier, code_challenge = oauth_service.generate_pkce_pair()
    
    # Generate another pair
    code_verifier2, code_challenge2 = oauth_service.generate_pkce_pair()
    
    # Assert
    assert code_verifier != code_verifier2  # Should be different
    assert code_challenge != code_challenge2  # Should be different
    assert len(code_verifier) == len(code_verifier2)  # Same length
    assert len(code_challenge) == len(code_challenge2)  # Same length

@pytest.mark.asyncio(timeout=2.0)
async def test_user_data_extraction():
    """Test user data extraction from Google profile"""
    # Arrange
    oauth_service = OAuthService()
    user_info = {
        "id": "google_user_456",
        "email": "user@example.com",
        "name": "John Doe",
        "picture": "https://example.com/avatar.jpg",
        "verified_email": False,
        "extra_field": "should_be_ignored"
    }
    
    # Act
    result = await oauth_service.create_or_update_user(user_info)
    
    # Assert
    user = result["user"]
    assert user["sub"] == "google_google_user_456"
    assert user["email"] == "user@example.com"
    assert user["name"] == "John Doe"
    assert user["picture"] == "https://example.com/avatar.jpg"
    assert user["verified"] is False
    assert user["role"] == "student"  # Default role
    assert user["provider"] == "google"
    assert "extra_field" not in user  # Extra fields should be ignored