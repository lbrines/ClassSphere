"""Tests for OAuth models with Pydantic v2."""

import pytest
from datetime import datetime
from pydantic import ValidationError
from pydantic.types import SecretStr

from src.app.models.oauth import (
    OAuthProvider,
    TokenType,
    OAuthTokenBase,
    OAuthTokenCreate,
    OAuthTokenUpdate,
    OAuthTokenResponse,
    OAuthTokenInDB,
    GoogleOAuthProfile,
    OAuthAuthorizationCode,
    OAuthConfig,
    OAuthError,
    OAuthTokenValidation,
    OAuthRefreshRequest
)


class TestOAuthProvider:
    """Test OAuthProvider enumeration."""

    def test_oauth_providers(self):
        """Test all OAuth providers."""
        assert OAuthProvider.GOOGLE == "google"
        assert OAuthProvider.MICROSOFT == "microsoft"
        assert OAuthProvider.GITHUB == "github"


class TestTokenType:
    """Test TokenType enumeration."""

    def test_token_types(self):
        """Test all token types."""
        assert TokenType.BEARER == "Bearer"
        assert TokenType.JWT == "JWT"


class TestOAuthTokenBase:
    """Test OAuthTokenBase model."""

    def test_valid_oauth_token_base(self):
        """Test valid OAuth token base."""
        token = OAuthTokenBase(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("access_token_123"),
            token_type=TokenType.BEARER,
            expires_in=3600,
            scope="https://www.googleapis.com/auth/classroom.courses.readonly"
        )

        assert token.provider == OAuthProvider.GOOGLE
        assert token.access_token.get_secret_value() == "access_token_123"
        assert token.token_type == TokenType.BEARER
        assert token.expires_in == 3600
        assert "classroom.courses.readonly" in token.scope

    def test_defaults(self):
        """Test default values."""
        token = OAuthTokenBase(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("access_token_123")
        )

        assert token.token_type == TokenType.BEARER
        assert token.expires_in is None
        assert token.scope is None

    def test_scope_validation(self):
        """Test scope validation and normalization."""
        # Valid scope with multiple scopes
        token = OAuthTokenBase(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("token"),
            scope="  scope1   scope2  scope3  "
        )
        assert token.scope == "scope1 scope2 scope3"

        # Empty scope
        token = OAuthTokenBase(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("token"),
            scope="   "
        )
        assert token.scope is None

        # None scope
        token = OAuthTokenBase(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("token"),
            scope=None
        )
        assert token.scope is None

    def test_config_dict(self):
        """Test ConfigDict configuration."""
        token = OAuthTokenBase(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("token")
        )

        config = token.model_config
        assert config['from_attributes'] is True
        assert config['str_strip_whitespace'] is True
        assert config['validate_assignment'] is True
        assert config['extra'] == "forbid"


class TestOAuthTokenCreate:
    """Test OAuthTokenCreate model."""

    def test_valid_oauth_token_create(self):
        """Test valid OAuth token creation."""
        token = OAuthTokenCreate(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("access_token_123"),
            refresh_token=SecretStr("refresh_token_123"),
            id_token=SecretStr("id_token_123"),
            user_id="user_123",
            expires_in=3600
        )

        assert token.provider == OAuthProvider.GOOGLE
        assert token.user_id == "user_123"
        assert token.refresh_token.get_secret_value() == "refresh_token_123"
        assert token.id_token.get_secret_value() == "id_token_123"

    def test_user_id_validation(self):
        """Test user ID validation."""
        # Valid user ID
        token = OAuthTokenCreate(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("token"),
            user_id="  user_123  "
        )
        assert token.user_id == "user_123"

        # Empty user ID
        with pytest.raises(ValidationError, match="User ID cannot be empty"):
            OAuthTokenCreate(
                provider=OAuthProvider.GOOGLE,
                access_token=SecretStr("token"),
                user_id=""
            )

        # Whitespace-only user ID
        with pytest.raises(ValidationError, match="User ID cannot be empty"):
            OAuthTokenCreate(
                provider=OAuthProvider.GOOGLE,
                access_token=SecretStr("token"),
                user_id="   "
            )

    def test_optional_fields(self):
        """Test optional fields."""
        token = OAuthTokenCreate(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("token"),
            user_id="user_123"
        )

        assert token.refresh_token is None
        assert token.id_token is None


class TestOAuthTokenUpdate:
    """Test OAuthTokenUpdate model."""

    def test_valid_oauth_token_update(self):
        """Test valid OAuth token update."""
        update = OAuthTokenUpdate(
            access_token=SecretStr("new_access_token"),
            refresh_token=SecretStr("new_refresh_token"),
            expires_in=7200,
            scope="new scope"
        )

        assert update.access_token.get_secret_value() == "new_access_token"
        assert update.refresh_token.get_secret_value() == "new_refresh_token"
        assert update.expires_in == 7200
        assert update.scope == "new scope"

    def test_partial_update(self):
        """Test partial OAuth token update."""
        update = OAuthTokenUpdate(
            access_token=SecretStr("new_token")
        )

        assert update.access_token.get_secret_value() == "new_token"
        assert update.refresh_token is None
        assert update.expires_in is None
        assert update.scope is None

    def test_empty_update(self):
        """Test empty OAuth token update."""
        update = OAuthTokenUpdate()

        assert update.access_token is None
        assert update.refresh_token is None
        assert update.expires_in is None
        assert update.scope is None


class TestOAuthTokenResponse:
    """Test OAuthTokenResponse model."""

    def test_valid_oauth_token_response(self):
        """Test valid OAuth token response."""
        now = datetime.now()
        token = OAuthTokenResponse(
            id="token_123",
            provider=OAuthProvider.GOOGLE,
            token_type=TokenType.BEARER,
            expires_in=3600,
            scope="scope1 scope2",
            created_at=now,
            updated_at=now,
            expires_at=now,
            is_expired=False
        )

        assert token.id == "token_123"
        assert token.provider == OAuthProvider.GOOGLE
        assert token.created_at == now
        assert token.is_expired is False

    def test_optional_fields(self):
        """Test optional fields in response."""
        token = OAuthTokenResponse(
            id="token_123",
            provider=OAuthProvider.GOOGLE,
            token_type=TokenType.BEARER,
            created_at=datetime.now()
        )

        assert token.expires_in is None
        assert token.scope is None
        assert token.updated_at is None
        assert token.expires_at is None
        assert token.is_expired is False

    def test_datetime_serialization(self):
        """Test datetime serialization."""
        now = datetime.now()
        token = OAuthTokenResponse(
            id="token_123",
            provider=OAuthProvider.GOOGLE,
            token_type=TokenType.BEARER,
            created_at=now
        )

        # Test that datetime serialization method exists
        assert hasattr(token, 'serialize_datetime')

        # Test datetime serialization
        result = token.serialize_datetime(now)
        assert result == now.isoformat()

        # Test None serialization
        result = token.serialize_datetime(None)
        assert result is None


class TestOAuthTokenInDB:
    """Test OAuthTokenInDB model."""

    def test_valid_oauth_token_in_db(self):
        """Test valid OAuth token in database."""
        now = datetime.now()
        token = OAuthTokenInDB(
            id="token_123",
            provider=OAuthProvider.GOOGLE,
            token_type=TokenType.BEARER,
            created_at=now,
            user_id="user_123",
            access_token="encrypted_access_token",
            refresh_token="encrypted_refresh_token",
            id_token="encrypted_id_token"
        )

        assert token.id == "token_123"
        assert token.user_id == "user_123"
        assert token.access_token == "encrypted_access_token"
        assert token.refresh_token == "encrypted_refresh_token"
        assert token.id_token == "encrypted_id_token"


class TestGoogleOAuthProfile:
    """Test GoogleOAuthProfile model."""

    def test_valid_google_profile(self):
        """Test valid Google OAuth profile."""
        profile = GoogleOAuthProfile(
            id="google_123",
            email="test@example.com",
            name="Test User",
            given_name="Test",
            family_name="User",
            picture="https://example.com/photo.jpg",
            locale="en",
            verified_email=True
        )

        assert profile.id == "google_123"
        assert profile.email == "test@example.com"
        assert profile.name == "Test User"
        assert profile.verified_email is True

    def test_email_normalization(self):
        """Test email normalization."""
        profile = GoogleOAuthProfile(
            id="google_123",
            email="  TEST@EXAMPLE.COM  ",
            name="Test User"
        )
        assert profile.email == "test@example.com"

    def test_name_validation(self):
        """Test name validation."""
        # Valid name
        profile = GoogleOAuthProfile(
            id="google_123",
            email="test@example.com",
            name="  Test User  "
        )
        assert profile.name == "Test User"

        # Empty name
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            GoogleOAuthProfile(
                id="google_123",
                email="test@example.com",
                name=""
            )

        # Whitespace-only name
        with pytest.raises(ValidationError, match="Name cannot be empty"):
            GoogleOAuthProfile(
                id="google_123",
                email="test@example.com",
                name="   "
            )

    def test_optional_fields(self):
        """Test optional fields."""
        profile = GoogleOAuthProfile(
            id="google_123",
            email="test@example.com",
            name="Test User"
        )

        assert profile.given_name is None
        assert profile.family_name is None
        assert profile.picture is None
        assert profile.locale is None
        assert profile.verified_email is False


class TestOAuthAuthorizationCode:
    """Test OAuthAuthorizationCode model."""

    def test_valid_authorization_code(self):
        """Test valid authorization code."""
        auth_code = OAuthAuthorizationCode(
            code="auth_code_123",
            state="state_value",
            scope="scope1 scope2",
            provider=OAuthProvider.GOOGLE
        )

        assert auth_code.code == "auth_code_123"
        assert auth_code.state == "state_value"
        assert auth_code.scope == "scope1 scope2"
        assert auth_code.provider == OAuthProvider.GOOGLE

    def test_code_validation(self):
        """Test authorization code validation."""
        # Valid code
        auth_code = OAuthAuthorizationCode(
            code="  auth_code_123  "
        )
        assert auth_code.code == "auth_code_123"

        # Empty code
        with pytest.raises(ValidationError, match="Authorization code cannot be empty"):
            OAuthAuthorizationCode(code="")

        # Whitespace-only code
        with pytest.raises(ValidationError, match="Authorization code cannot be empty"):
            OAuthAuthorizationCode(code="   ")

    def test_defaults(self):
        """Test default values."""
        auth_code = OAuthAuthorizationCode(
            code="auth_code_123"
        )

        assert auth_code.state is None
        assert auth_code.scope is None
        assert auth_code.provider == OAuthProvider.GOOGLE


class TestOAuthConfig:
    """Test OAuthConfig model."""

    def test_valid_oauth_config(self):
        """Test valid OAuth configuration."""
        config = OAuthConfig(
            provider=OAuthProvider.GOOGLE,
            client_id="client_123",
            client_secret=SecretStr("secret_123"),
            redirect_uri="https://example.com/callback",
            scopes=["scope1", "scope2"],
            authorization_url="https://accounts.google.com/oauth/authorize",
            token_url="https://oauth2.googleapis.com/token",
            userinfo_url="https://www.googleapis.com/oauth2/v2/userinfo"
        )

        assert config.provider == OAuthProvider.GOOGLE
        assert config.client_id == "client_123"
        assert config.client_secret.get_secret_value() == "secret_123"
        assert len(config.scopes) == 2

    def test_client_id_validation(self):
        """Test client ID validation."""
        # Valid client ID
        config = OAuthConfig(
            provider=OAuthProvider.GOOGLE,
            client_id="  client_123  ",
            client_secret=SecretStr("secret"),
            redirect_uri="https://example.com/callback",
            scopes=["scope1"],
            authorization_url="https://example.com/auth",
            token_url="https://example.com/token"
        )
        assert config.client_id == "client_123"

        # Empty client ID
        with pytest.raises(ValidationError, match="Client ID cannot be empty"):
            OAuthConfig(
                provider=OAuthProvider.GOOGLE,
                client_id="",
                client_secret=SecretStr("secret"),
                redirect_uri="https://example.com/callback",
                scopes=["scope1"],
                authorization_url="https://example.com/auth",
                token_url="https://example.com/token"
            )

    def test_scopes_validation(self):
        """Test scopes validation."""
        # Valid scopes
        config = OAuthConfig(
            provider=OAuthProvider.GOOGLE,
            client_id="client_123",
            client_secret=SecretStr("secret"),
            redirect_uri="https://example.com/callback",
            scopes=["  scope1  ", "scope2", "  scope1  "],  # Duplicates and whitespace
            authorization_url="https://example.com/auth",
            token_url="https://example.com/token"
        )
        # Should remove duplicates and strip whitespace
        assert "scope1" in config.scopes
        assert "scope2" in config.scopes
        assert len(config.scopes) == 2

        # Empty scopes list
        with pytest.raises(ValidationError, match="At least one scope is required"):
            OAuthConfig(
                provider=OAuthProvider.GOOGLE,
                client_id="client_123",
                client_secret=SecretStr("secret"),
                redirect_uri="https://example.com/callback",
                scopes=[],
                authorization_url="https://example.com/auth",
                token_url="https://example.com/token"
            )

        # Scopes with only whitespace
        with pytest.raises(ValidationError, match="At least one valid scope is required"):
            OAuthConfig(
                provider=OAuthProvider.GOOGLE,
                client_id="client_123",
                client_secret=SecretStr("secret"),
                redirect_uri="https://example.com/callback",
                scopes=["  ", "   "],
                authorization_url="https://example.com/auth",
                token_url="https://example.com/token"
            )


class TestOAuthError:
    """Test OAuthError model."""

    def test_valid_oauth_error(self):
        """Test valid OAuth error."""
        error = OAuthError(
            error="invalid_grant",
            error_description="The provided authorization grant is invalid",
            error_uri="https://example.com/error",
            state="state_value"
        )

        assert error.error == "invalid_grant"
        assert "authorization grant" in error.error_description
        assert str(error.error_uri) == "https://example.com/error"
        assert error.state == "state_value"

    def test_minimal_oauth_error(self):
        """Test minimal OAuth error."""
        error = OAuthError(error="invalid_request")

        assert error.error == "invalid_request"
        assert error.error_description is None
        assert error.error_uri is None
        assert error.state is None


class TestOAuthTokenValidation:
    """Test OAuthTokenValidation model."""

    def test_valid_token_validation(self):
        """Test valid token validation."""
        now = datetime.now()
        validation = OAuthTokenValidation(
            is_valid=True,
            expires_at=now,
            scope="scope1 scope2",
            audience="audience_value",
            issuer="https://accounts.google.com",
            subject="user_123"
        )

        assert validation.is_valid is True
        assert validation.expires_at == now
        assert validation.scope == "scope1 scope2"
        assert validation.subject == "user_123"

    def test_invalid_token_validation(self):
        """Test invalid token validation."""
        validation = OAuthTokenValidation(is_valid=False)

        assert validation.is_valid is False
        assert validation.expires_at is None
        assert validation.scope is None


class TestOAuthRefreshRequest:
    """Test OAuthRefreshRequest model."""

    def test_valid_refresh_request(self):
        """Test valid refresh request."""
        request = OAuthRefreshRequest(
            refresh_token=SecretStr("refresh_token_123"),
            provider=OAuthProvider.GOOGLE
        )

        assert request.refresh_token.get_secret_value() == "refresh_token_123"
        assert request.provider == OAuthProvider.GOOGLE

    def test_refresh_token_validation(self):
        """Test refresh token validation."""
        # Valid token
        request = OAuthRefreshRequest(
            refresh_token=SecretStr("  refresh_token_123  ")
        )
        # Should not strip secret values, validation happens on the raw value
        assert request.refresh_token.get_secret_value() == "  refresh_token_123  "

        # Empty token
        with pytest.raises(ValidationError, match="Refresh token cannot be empty"):
            OAuthRefreshRequest(
                refresh_token=SecretStr("")
            )

        # Whitespace-only token
        with pytest.raises(ValidationError, match="Refresh token cannot be empty"):
            OAuthRefreshRequest(
                refresh_token=SecretStr("   ")
            )

    def test_default_provider(self):
        """Test default provider."""
        request = OAuthRefreshRequest(
            refresh_token=SecretStr("refresh_token_123")
        )

        assert request.provider == OAuthProvider.GOOGLE


class TestModelSerialization:
    """Test model serialization and validation."""

    def test_oauth_token_serialization(self):
        """Test OAuth token serialization."""
        token = OAuthTokenBase(
            provider=OAuthProvider.GOOGLE,
            access_token=SecretStr("token")
        )

        # Test model dump
        data = token.model_dump()
        assert "provider" in data
        assert "access_token" in data
        assert "token_type" in data

        # Test model validation
        validated = OAuthTokenBase.model_validate(data)
        assert validated.provider == token.provider
        assert validated.token_type == token.token_type

    def test_google_profile_serialization(self):
        """Test Google profile serialization."""
        profile = GoogleOAuthProfile(
            id="google_123",
            email="test@example.com",
            name="Test User"
        )

        # Test model dump
        data = profile.model_dump()
        assert data["id"] == "google_123"
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

        # Test model validation
        validated = GoogleOAuthProfile.model_validate(data)
        assert validated.id == profile.id
        assert validated.email == profile.email
        assert validated.name == profile.name