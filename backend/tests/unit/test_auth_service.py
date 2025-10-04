"""Tests for AuthService."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch, MagicMock

from src.app.services.auth_service import AuthService
from src.app.models.user import UserInDB, UserRole, UserStatus
from src.app.core.exceptions import AuthenticationError, TokenExpiredError
from src.app.core.config import settings


class TestAuthService:
    """Test cases for AuthService."""

    @pytest.fixture
    def auth_service(self):
        """Create AuthService instance."""
        return AuthService()

    @pytest.fixture
    def mock_user_data(self):
        """Mock user data."""
        return {
            "id": "user123",
            "email": "test@example.com",
            "role": "admin"
        }

    @pytest.fixture
    def mock_user(self):
        """Mock UserInDB instance."""
        return UserInDB(
            id="user123",
            email="test@example.com",
            full_name="Test User",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            hashed_password="hashed_password_123"
        )

    @pytest.mark.asyncio
    async def test_create_access_token(self, auth_service, mock_user_data):
        """Test creating access token."""
        with patch.object(auth_service.security, 'create_access_token') as mock_create:
            mock_create.return_value = "mock_access_token"
            
            token = await auth_service.create_access_token(mock_user_data)
            
            assert token == "mock_access_token"
            mock_create.assert_called_once()
            
            # Verify payload structure
            call_args = mock_create.call_args[0][0]
            assert call_args["sub"] == "user123"
            assert call_args["email"] == "test@example.com"
            assert call_args["id"] == "user123"
            assert call_args["role"] == "admin"
            assert "exp" in call_args
            assert "iat" in call_args

    @pytest.mark.asyncio
    async def test_create_refresh_token(self, auth_service, mock_user_data):
        """Test creating refresh token."""
        with patch.object(auth_service.security, 'create_refresh_token') as mock_create:
            mock_create.return_value = "mock_refresh_token"
            
            token = await auth_service.create_refresh_token(mock_user_data)
            
            assert token == "mock_refresh_token"
            mock_create.assert_called_once()
            
            # Verify payload structure
            call_args = mock_create.call_args[0][0]
            assert call_args["sub"] == "user123"
            assert call_args["email"] == "test@example.com"
            assert call_args["id"] == "user123"
            assert call_args["role"] == "admin"

    @pytest.mark.asyncio
    async def test_verify_token_success(self, auth_service):
        """Test successful token verification."""
        mock_payload = {
            "sub": "user123",
            "email": "test@example.com",
            "id": "user123",
            "role": "admin"
        }
        
        with patch.object(auth_service.security, 'verify_token') as mock_verify:
            mock_verify.return_value = mock_payload
            
            result = await auth_service.verify_token("valid_token")
            
            assert result == mock_payload
            mock_verify.assert_called_once_with("valid_token")

    @pytest.mark.asyncio
    async def test_verify_token_missing_sub(self, auth_service):
        """Test token verification with missing subject."""
        mock_payload = {
            "email": "test@example.com",
            "id": "user123",
            "role": "admin"
            # Missing "sub" field
        }
        
        with patch.object(auth_service.security, 'verify_token') as mock_verify:
            mock_verify.return_value = mock_payload
            
            with pytest.raises(AuthenticationError, match="Token missing subject"):
                await auth_service.verify_token("invalid_token")

    @pytest.mark.asyncio
    async def test_verify_token_expired(self, auth_service):
        """Test token verification with expired token."""
        with patch.object(auth_service.security, 'verify_token') as mock_verify:
            mock_verify.side_effect = TokenExpiredError("Token expired")
            
            with pytest.raises(TokenExpiredError):
                await auth_service.verify_token("expired_token")

    @pytest.mark.asyncio
    async def test_verify_token_general_error(self, auth_service):
        """Test token verification with general error."""
        with patch.object(auth_service.security, 'verify_token') as mock_verify:
            mock_verify.side_effect = Exception("General error")
            
            with pytest.raises(AuthenticationError, match="Token verification failed"):
                await auth_service.verify_token("invalid_token")

    @pytest.mark.asyncio
    async def test_hash_password(self, auth_service):
        """Test password hashing."""
        with patch.object(auth_service.security, 'hash_password') as mock_hash:
            mock_hash.return_value = "hashed_password"
            
            result = await auth_service.hash_password("plain_password")
            
            assert result == "hashed_password"
            mock_hash.assert_called_once_with("plain_password")

    @pytest.mark.asyncio
    async def test_verify_password(self, auth_service):
        """Test password verification."""
        with patch.object(auth_service.security, 'verify_password') as mock_verify:
            mock_verify.return_value = True
            
            result = await auth_service.verify_password("plain", "hashed")
            
            assert result is True
            mock_verify.assert_called_once_with("plain", "hashed")

    @pytest.mark.asyncio
    async def test_get_user_permissions_by_role(self, auth_service):
        """Test getting user permissions by role."""
        with patch.object(auth_service.security, 'get_user_permissions_by_role') as mock_permissions:
            mock_permissions.return_value = ["read", "write"]
            
            result = await auth_service.get_user_permissions_by_role("admin")
            
            assert result == ["read", "write"]
            mock_permissions.assert_called_once_with("admin")

    @pytest.mark.asyncio
    async def test_generate_password_reset_token(self, auth_service):
        """Test generating password reset token."""
        with patch.object(auth_service.security, 'generate_password_reset_token') as mock_generate:
            mock_generate.return_value = "reset_token_123"
            
            result = await auth_service.generate_password_reset_token()
            
            assert result == "reset_token_123"
            mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_tokens(self, auth_service, mock_user):
        """Test creating both access and refresh tokens for user."""
        with patch.object(auth_service, 'create_access_token') as mock_access, \
             patch.object(auth_service, 'create_refresh_token') as mock_refresh:
            
            mock_access.return_value = "access_token_123"
            mock_refresh.return_value = "refresh_token_123"
            
            result = await auth_service.create_user_tokens(mock_user)
            
            assert result == {
                "access_token": "access_token_123",
                "refresh_token": "refresh_token_123",
                "token_type": "bearer"
            }
            
            mock_access.assert_called_once()
            mock_refresh.assert_called_once()
            
            # Verify user data passed to token creation
            access_call_args = mock_access.call_args[0][0]
            assert access_call_args["id"] == "user123"
            assert access_call_args["email"] == "test@example.com"
            assert access_call_args["role"] == "admin"

    @pytest.mark.asyncio
    async def test_create_user_tokens_with_string_role(self, auth_service):
        """Test creating tokens with string role instead of enum."""
        user_with_string_role = UserInDB(
            id="user123",
            email="test@example.com",
            full_name="Test User",
            role="admin",  # String instead of enum
            status=UserStatus.ACTIVE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            hashed_password="hashed_password_123"
        )
        
        with patch.object(auth_service, 'create_access_token') as mock_access, \
             patch.object(auth_service, 'create_refresh_token') as mock_refresh:
            
            mock_access.return_value = "access_token_123"
            mock_refresh.return_value = "refresh_token_123"
            
            result = await auth_service.create_user_tokens(user_with_string_role)
            
            assert result["access_token"] == "access_token_123"
            assert result["refresh_token"] == "refresh_token_123"
            
            # Verify role handling
            access_call_args = mock_access.call_args[0][0]
            assert access_call_args["role"] == "admin"