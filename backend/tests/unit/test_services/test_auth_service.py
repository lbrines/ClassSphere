"""
Unit tests for AuthService.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from jose import jwt

from src.app.services.auth_service import AuthService, auth_service
from src.app.exceptions.auth import TokenExpiredError, TokenInvalidError, AuthenticationError


class TestAuthService:
    """Test AuthService functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.auth_service = AuthService()
        self.test_user_data = {
            "id": "user123",
            "email": "test@example.com",
            "role": "student",
            "name": "Test User"
        }
    
    def test_create_access_token_success(self):
        """Test successful access token creation."""
        token = self.auth_service.create_access_token(self.test_user_data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode token to verify structure
        payload = jwt.decode(token, self.auth_service.secret_key, algorithms=[self.auth_service.algorithm])
        
        assert payload["sub"] == "user123"
        assert payload["type"] == "access"
        assert "exp" in payload
        assert "iat" in payload
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "student"
    
    def test_create_access_token_with_sub_field(self):
        """Test access token creation with explicit 'sub' field."""
        user_data = self.test_user_data.copy()
        user_data["sub"] = "explicit_sub"
        
        token = self.auth_service.create_access_token(user_data)
        payload = jwt.decode(token, self.auth_service.secret_key, algorithms=[self.auth_service.algorithm])
        
        assert payload["sub"] == "explicit_sub"
    
    def test_create_access_token_without_id_or_email(self):
        """Test access token creation without id or email."""
        user_data = {"role": "student"}
        
        token = self.auth_service.create_access_token(user_data)
        payload = jwt.decode(token, self.auth_service.secret_key, algorithms=[self.auth_service.algorithm])
        
        assert payload["sub"] == "unknown"
    
    def test_create_refresh_token_success(self):
        """Test successful refresh token creation."""
        token = self.auth_service.create_refresh_token(self.test_user_data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode token to verify structure
        payload = jwt.decode(token, self.auth_service.secret_key, algorithms=[self.auth_service.algorithm])
        
        assert payload["sub"] == "user123"
        assert payload["type"] == "refresh"
        assert "exp" in payload
        assert "iat" in payload
    
    def test_verify_token_success(self):
        """Test successful token verification."""
        token = self.auth_service.create_access_token(self.test_user_data)
        payload = self.auth_service.verify_token(token)
        
        assert payload["sub"] == "user123"
        assert payload["type"] == "access"
        assert payload["email"] == "test@example.com"
    
    def test_verify_token_expired(self):
        """Test token verification with expired token."""
        # Create token with past expiration
        to_encode = self.test_user_data.copy()
        to_encode.update({
            "exp": datetime.utcnow() - timedelta(minutes=1),
            "iat": datetime.utcnow() - timedelta(minutes=2),
            "type": "access",
            "sub": "user123"
        })
        
        expired_token = jwt.encode(to_encode, self.auth_service.secret_key, algorithm=self.auth_service.algorithm)
        
        with pytest.raises(TokenExpiredError):
            self.auth_service.verify_token(expired_token)
    
    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        invalid_token = "invalid.token.here"
        
        with pytest.raises(TokenInvalidError):
            self.auth_service.verify_token(invalid_token)
    
    def test_verify_token_missing_sub(self):
        """Test token verification with missing 'sub' field."""
        to_encode = self.test_user_data.copy()
        to_encode.update({
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "type": "access"
            # Missing 'sub' field
        })
        
        token_without_sub = jwt.encode(to_encode, self.auth_service.secret_key, algorithm=self.auth_service.algorithm)
        
        with pytest.raises(TokenInvalidError, match="Missing 'sub' field"):
            self.auth_service.verify_token(token_without_sub)
    
    def test_verify_token_invalid_type(self):
        """Test token verification with invalid token type."""
        to_encode = self.test_user_data.copy()
        to_encode.update({
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "type": "invalid_type",
            "sub": "user123"
        })
        
        invalid_type_token = jwt.encode(to_encode, self.auth_service.secret_key, algorithm=self.auth_service.algorithm)
        
        with pytest.raises(TokenInvalidError, match="Invalid token type"):
            self.auth_service.verify_token(invalid_type_token)
    
    def test_hash_password_success(self):
        """Test successful password hashing."""
        password = "test_password_123"
        hashed = self.auth_service.hash_password(password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password
        assert hashed.startswith("$2b$")  # bcrypt format
    
    def test_verify_password_success(self):
        """Test successful password verification."""
        password = "test_password_123"
        hashed = self.auth_service.hash_password(password)
        
        is_valid = self.auth_service.verify_password(password, hashed)
        assert is_valid is True
    
    def test_verify_password_failure(self):
        """Test password verification failure."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = self.auth_service.hash_password(password)
        
        is_valid = self.auth_service.verify_password(wrong_password, hashed)
        assert is_valid is False
    
    def test_get_user_permissions_by_role_student(self):
        """Test getting permissions for student role."""
        permissions = self.auth_service.get_user_permissions_by_role("student")
        
        expected_permissions = [
            "read:own_courses",
            "read:own_assignments",
            "read:own_grades",
            "read:own_profile"
        ]
        
        assert permissions == expected_permissions
    
    def test_get_user_permissions_by_role_teacher(self):
        """Test getting permissions for teacher role."""
        permissions = self.auth_service.get_user_permissions_by_role("teacher")
        
        expected_permissions = [
            "read:own_courses",
            "write:own_courses",
            "read:own_students",
            "write:own_assignments",
            "write:own_grades",
            "read:own_profile",
            "write:own_profile"
        ]
        
        assert permissions == expected_permissions
    
    def test_get_user_permissions_by_role_admin(self):
        """Test getting permissions for admin role."""
        permissions = self.auth_service.get_user_permissions_by_role("admin")
        
        expected_permissions = [
            "read:all_users",
            "write:all_users",
            "read:all_courses",
            "write:all_courses",
            "read:all_assignments",
            "write:all_assignments",
            "read:all_grades",
            "write:all_grades",
            "read:system_settings",
            "write:system_settings",
            "read:own_profile",
            "write:own_profile"
        ]
        
        assert permissions == expected_permissions
    
    def test_get_user_permissions_by_role_unknown(self):
        """Test getting permissions for unknown role."""
        permissions = self.auth_service.get_user_permissions_by_role("unknown_role")
        
        assert permissions == []
    
    def test_global_auth_service_instance(self):
        """Test global auth_service instance."""
        assert auth_service is not None
        assert isinstance(auth_service, AuthService)
        
        # Test that global instance works
        token = auth_service.create_access_token(self.test_user_data)
        assert isinstance(token, str)
        
        payload = auth_service.verify_token(token)
        assert payload["sub"] == "user123"