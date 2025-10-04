"""
Test file for auth_service.py

CRITICAL OBJECTIVES:
- Verify JWT token generation and validation
- Test refresh token rotation
- Test password hashing and verification
- Test error handling

DEPENDENCIES:
- AsyncMock for async methods
- pytest-asyncio
- JWT tokens
"""

import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta, timezone
from jose import jwt

from src.app.services.auth_service import AuthService
from src.app.core.config import get_settings

# BEGINNING: Critical tests for core functionality
@pytest.mark.asyncio(timeout=2.0)
async def test_password_hashing():
    """Test password hashing and verification"""
    # Arrange
    auth_service = AuthService()
    test_password = "test_password_123"
    
    # Act
    hashed = auth_service.get_password_hash(test_password)
    
    # Assert
    assert hashed != test_password
    assert len(hashed) > 0
    assert auth_service.verify_password(test_password, hashed)
    assert not auth_service.verify_password("wrong_password", hashed)

@pytest.mark.asyncio(timeout=2.0)
async def test_access_token_creation():
    """Test access token creation"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    
    # Act
    token = auth_service.create_access_token(user_data)
    
    # Assert
    assert token is not None
    assert len(token) > 0
    
    # Verify token can be decoded
    decoded = auth_service.verify_token(token, "access")
    assert decoded is not None
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "teacher"
    assert decoded["email"] == "test@classsphere.com"
    assert decoded["type"] == "access"

@pytest.mark.asyncio(timeout=2.0)
async def test_refresh_token_creation():
    """Test refresh token creation"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    
    # Act
    token = auth_service.create_refresh_token(user_data)
    
    # Assert
    assert token is not None
    assert len(token) > 0
    
    # Verify token can be decoded
    decoded = auth_service.verify_token(token, "refresh")
    assert decoded is not None
    assert decoded["sub"] == "user123"
    assert decoded["role"] == "teacher"
    assert decoded["email"] == "test@classsphere.com"
    assert decoded["type"] == "refresh"

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=2.0)
async def test_token_verification():
    """Test token verification with different scenarios"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher"}
    
    # Act & Assert: Valid token
    token = auth_service.create_access_token(user_data)
    decoded = auth_service.verify_token(token, "access")
    assert decoded is not None
    assert decoded["sub"] == "user123"
    
    # Act & Assert: Wrong token type
    refresh_token = auth_service.create_refresh_token(user_data)
    decoded = auth_service.verify_token(refresh_token, "access")
    assert decoded is None
    
    # Act & Assert: Invalid token
    decoded = auth_service.verify_token("invalid.token.here", "access")
    assert decoded is None

@pytest.mark.asyncio(timeout=2.0)
async def test_token_refresh():
    """Test token refresh functionality"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    refresh_token = auth_service.create_refresh_token(user_data)
    
    # Act
    result = auth_service.refresh_access_token(refresh_token)
    
    # Assert
    assert result is not None
    assert "access_token" in result
    assert "refresh_token" in result
    assert "token_type" in result
    assert result["token_type"] == "bearer"
    
    # Verify new access token works
    new_access = auth_service.verify_token(result["access_token"], "access")
    assert new_access is not None
    assert new_access["sub"] == "user123"

@pytest.mark.asyncio(timeout=2.0)
async def test_token_pair_creation():
    """Test creating both access and refresh tokens"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    
    # Act
    tokens = auth_service.create_token_pair(user_data)
    
    # Assert
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert "token_type" in tokens
    assert "expires_in" in tokens
    assert tokens["token_type"] == "bearer"
    
    # Verify both tokens work
    access_decoded = auth_service.verify_token(tokens["access_token"], "access")
    refresh_decoded = auth_service.verify_token(tokens["refresh_token"], "refresh")
    
    assert access_decoded is not None
    assert refresh_decoded is not None
    assert access_decoded["sub"] == refresh_decoded["sub"]

# END: Verification and next steps
@pytest.mark.asyncio(timeout=2.0)
async def test_expired_token_handling():
    """Test handling of expired tokens"""
    # Arrange
    auth_service = AuthService()
    settings = get_settings()
    
    # Create expired token manually
    expired_data = {
        "sub": "user123",
        "role": "teacher",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
        "type": "access"
    }
    expired_token = jwt.encode(expired_data, settings.secret_key, algorithm=settings.algorithm)
    
    # Act
    decoded = auth_service.verify_token(expired_token, "access")
    
    # Assert
    assert decoded is None

@pytest.mark.asyncio(timeout=2.0)
async def test_invalid_token_handling():
    """Test handling of invalid tokens"""
    # Arrange
    auth_service = AuthService()
    
    # Act & Assert: Empty token
    decoded = auth_service.verify_token("", "access")
    assert decoded is None
    
    # Act & Assert: Malformed token
    decoded = auth_service.verify_token("not.a.token", "access")
    assert decoded is None
    
    # Act & Assert: Token with wrong signature
    wrong_token = jwt.encode({"sub": "user123"}, "wrong_secret", algorithm="HS256")
    decoded = auth_service.verify_token(wrong_token, "access")
    assert decoded is None

@pytest.mark.asyncio(timeout=2.0)
async def test_password_hashing_error_handling():
    """Test password hashing error handling"""
    # Arrange
    auth_service = AuthService()
    
    # Act & Assert: Empty password (should work with bcrypt)
    hashed_empty = auth_service.get_password_hash("")
    assert hashed_empty is not None
    assert auth_service.verify_password("", hashed_empty)
    
    # Act & Assert: None password (should raise TypeError)
    with pytest.raises((TypeError, ValueError)):
        auth_service.get_password_hash(None)