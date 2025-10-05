"""
Unit tests for AuthService.
"""
import asyncio
import pytest
from unittest.mock import patch, mock_open

from src.app.services.auth_service import AuthService
from src.app.core.security import AuthenticationError
from src.app.models.user import UserRole


@pytest.mark.asyncio
async def test_authenticate_user_with_valid_credentials(auth_service):
    """Test authentication with valid credentials."""
    result = await asyncio.wait_for(
        auth_service.authenticate_user("admin@classsphere.edu", "secret"),
        timeout=2.0
    )

    assert result is not None
    assert result.email == "admin@classsphere.edu"
    assert result.role == UserRole.ADMIN
    assert result.is_active is True


@pytest.mark.asyncio
async def test_authenticate_user_with_invalid_password(auth_service):
    """Test authentication with invalid password."""
    with pytest.raises(AuthenticationError) as exc_info:
        await asyncio.wait_for(
            auth_service.authenticate_user("admin@classsphere.edu", "wrong"),
            timeout=2.0
        )

    assert "Invalid password" in str(exc_info.value)


@pytest.mark.asyncio
async def test_authenticate_user_with_nonexistent_email(auth_service):
    """Test authentication with nonexistent email."""
    with pytest.raises(AuthenticationError) as exc_info:
        await asyncio.wait_for(
            auth_service.authenticate_user("nonexistent@example.com", "password"),
            timeout=2.0
        )

    assert "User not found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_authenticate_user_timeout():
    """Test authentication timeout handling."""
    auth_service = AuthService()

    # Mock slow authentication
    with patch.object(auth_service, '_get_user_by_email') as mock_get_user:
        async def slow_get_user(*args):
            await asyncio.sleep(3.0)  # Longer than timeout
            return None

        mock_get_user.side_effect = slow_get_user

        with pytest.raises(AuthenticationError) as exc_info:
            await auth_service.authenticate_user("test@example.com", "password")

        assert "Authentication timeout" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_by_id(auth_service):
    """Test getting user by ID."""
    result = await asyncio.wait_for(
        auth_service.get_user_by_id("admin-001"),
        timeout=2.0
    )

    assert result is not None
    assert result.id == "admin-001"
    assert result.email == "admin@classsphere.edu"


@pytest.mark.asyncio
async def test_get_user_by_id_nonexistent(auth_service):
    """Test getting nonexistent user by ID."""
    result = await asyncio.wait_for(
        auth_service.get_user_by_id("nonexistent"),
        timeout=2.0
    )

    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_id_timeout():
    """Test get user by ID timeout handling."""
    auth_service = AuthService()

    # Mock slow user retrieval
    with patch.object(auth_service, '_get_user_by_id_internal') as mock_get_user:
        async def slow_get_user(*args):
            await asyncio.sleep(3.0)  # Longer than timeout
            return None

        mock_get_user.side_effect = slow_get_user

        result = await auth_service.get_user_by_id("test-id")
        assert result is None


@pytest.mark.asyncio
async def test_create_token(auth_service):
    """Test JWT token creation."""
    user = await auth_service.get_user_by_id("admin-001")
    assert user is not None

    token = await asyncio.wait_for(
        auth_service.create_token(user),
        timeout=2.0
    )

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 10  # Basic token format check


@pytest.mark.asyncio
async def test_load_mock_users_fallback():
    """Test fallback behavior when mock users file is not found."""
    with patch('builtins.open', side_effect=FileNotFoundError):
        auth_service = AuthService()

        # Should still have fallback data
        assert len(auth_service.users_data["users"]) >= 1

        # Should be able to authenticate with fallback admin
        user = await auth_service._get_user_by_email("admin@classsphere.edu")
        assert user is not None


def test_load_mock_users_with_valid_file():
    """Test loading mock users from valid JSON file."""
    mock_json_content = '''
    {
        "users": [
            {
                "id": "test-001",
                "email": "test@example.com",
                "name": "Test User",
                "role": "student",
                "hashed_password": "test-hash",
                "is_active": true,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        ]
    }
    '''

    with patch('builtins.open', mock_open(read_data=mock_json_content)):
        auth_service = AuthService()

        assert len(auth_service.users_data["users"]) == 1
        assert auth_service.users_data["users"][0]["email"] == "test@example.com"