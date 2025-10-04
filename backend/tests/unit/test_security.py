import pytest
from datetime import datetime, timedelta
from src.app.core.security import (
    create_access_token, 
    create_refresh_token, 
    verify_token
)
from fastapi import HTTPException

class TestSecurity:
    def test_access_token_creation(self):
        """Test JWT access token creation."""
        data = {"sub": "test@example.com", "user_id": "123"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        assert "." in token  # JWT format
    
    def test_refresh_token_creation(self):
        """Test JWT refresh token creation."""
        data = {"sub": "test@example.com", "user_id": "123"}
        token = create_refresh_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        assert "." in token  # JWT format
    
    def test_token_verification_success(self):
        """Test successful token verification."""
        data = {"sub": "test@example.com", "user_id": "123"}
        token = create_access_token(data)
        
        payload = verify_token(token, "access")
        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == "123"
        assert payload["type"] == "access"
    
    def test_token_verification_invalid_token(self):
        """Test token verification with invalid token."""
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid_token", "access")
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)
    
    def test_token_verification_wrong_type(self):
        """Test token verification with wrong token type."""
        data = {"sub": "test@example.com", "user_id": "123"}
        access_token = create_access_token(data)
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token(access_token, "refresh")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token type" in str(exc_info.value.detail)
    
    def test_access_token_expiration(self):
        """Test access token with custom expiration."""
        data = {"sub": "test@example.com", "user_id": "123"}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data, expires_delta)
        
        payload = verify_token(token, "access")
        assert payload["sub"] == "test@example.com"
        assert payload["type"] == "access"
