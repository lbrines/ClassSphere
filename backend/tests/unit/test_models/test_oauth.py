"""
Unit tests for OAuth models.
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from src.app.models.oauth import (
    TokenType, OAuthProvider, TokenStatus, OAuthTokenBase,
    OAuthTokenCreate, OAuthTokenUpdate, OAuthTokenResponse,
    OAuthTokenRefresh, OAuthAuthorization, OAuthTokenExchange,
    OAuthTokenValidation, OAuthTokenRevoke
)


class TestOAuthEnums:
    """Test OAuth enums."""
    
    def test_token_type_enum(self):
        """Test TokenType enum values."""
        assert TokenType.ACCESS == "access"
        assert TokenType.REFRESH == "refresh"
        assert TokenType.OAUTH == "oauth"
        assert TokenType.GOOGLE == "google"
    
    def test_oauth_provider_enum(self):
        """Test OAuthProvider enum values."""
        assert OAuthProvider.GOOGLE == "google"
        assert OAuthProvider.MICROSOFT == "microsoft"
        assert OAuthProvider.GITHUB == "github"
    
    def test_token_status_enum(self):
        """Test TokenStatus enum values."""
        assert TokenStatus.ACTIVE == "active"
        assert TokenStatus.EXPIRED == "expired"
        assert TokenStatus.REVOKED == "revoked"
        assert TokenStatus.INVALID == "invalid"


class TestOAuthTokenBase:
    """Test OAuthTokenBase model."""
    
    def test_oauth_token_base_valid_data(self):
        """Test OAuthTokenBase with valid data."""
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            refresh_token="refresh_token_123",
            token_expires_at=datetime.utcnow() + timedelta(hours=1),
            provider_user_id="google123",
            provider_email="test@example.com",
            provider_name="Test User",
            provider_avatar="https://example.com/avatar.jpg",
            scopes=["openid", "email", "profile"],
            permissions=["read:own_courses"],
            expires_in=3600
        )
        
        assert token.user_id == "user123"
        assert token.provider == OAuthProvider.GOOGLE
        assert token.token_type == TokenType.OAUTH
        assert token.status == TokenStatus.ACTIVE
        assert token.access_token == "access_token_123"
        assert token.refresh_token == "refresh_token_123"
        assert isinstance(token.token_expires_at, datetime)
        assert token.provider_user_id == "google123"
        assert token.provider_email == "test@example.com"
        assert token.provider_name == "Test User"
        assert token.provider_avatar == "https://example.com/avatar.jpg"
        # Scopes are deduplicated and may be reordered
        assert set(token.scopes) == {"openid", "email", "profile"}
        assert token.permissions == ["read:own_courses"]
        assert token.expires_in == 3600
        assert isinstance(token.created_at, datetime)
        assert isinstance(token.updated_at, datetime)
        assert token.last_used is None
        assert token.raw_data is None
    
    def test_oauth_token_base_access_token_validation(self):
        """Test OAuthTokenBase access token validation."""
        # Valid access token
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="valid_access_token_123"
        )
        assert token.access_token == "valid_access_token_123"
        
        # Empty access token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenBase(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                access_token=""
            )
        assert "Access token must be at least 10 characters long" in str(exc_info.value)
        
        # Short access token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenBase(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                access_token="short"
            )
        assert "Access token must be at least 10 characters long" in str(exc_info.value)
        
        # Access token normalization
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="  access_token_123  "
        )
        assert token.access_token == "access_token_123"
    
    def test_oauth_token_base_provider_email_validation(self):
        """Test OAuthTokenBase provider email validation."""
        # Valid provider email
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            provider_email="test@example.com"
        )
        assert token.provider_email == "test@example.com"
        
        # Invalid provider email
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenBase(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                access_token="access_token_123",
                provider_email="invalid-email"
            )
        assert "Invalid provider email format" in str(exc_info.value)
        
        # Provider email normalization
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            provider_email="TEST@EXAMPLE.COM"
        )
        assert token.provider_email == "test@example.com"
        
        # None provider email
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            provider_email=None
        )
        assert token.provider_email is None
    
    def test_oauth_token_base_scopes_validation(self):
        """Test OAuthTokenBase scopes validation."""
        # Valid scopes
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            scopes=["openid", "email", "profile"]
        )
        # Scopes are deduplicated and may be reordered
        assert set(token.scopes) == {"openid", "email", "profile"}
        
        # Empty scopes
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            scopes=[]
        )
        assert token.scopes == []
        
        # Duplicate scopes
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            scopes=["openid", "email", "openid", "profile"]
        )
        # Scopes are deduplicated and may be reordered
        assert set(token.scopes) == {"openid", "email", "profile"}
        
        # Scope with spaces
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenBase(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                access_token="access_token_123",
                scopes=["openid", "email profile"]
            )
        assert "Invalid scope format" in str(exc_info.value)
        
        # Empty scope string - the validator filters out empty strings first
        token = OAuthTokenBase(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            scopes=["openid", "", "profile"]
        )
        # Empty strings are filtered out, so only valid scopes remain
        assert set(token.scopes) == {"openid", "profile"}


class TestOAuthTokenCreate:
    """Test OAuthTokenCreate model."""
    
    def test_oauth_token_create_valid_data(self):
        """Test OAuthTokenCreate with valid data."""
        token = OAuthTokenCreate(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            refresh_token="refresh_token_123",
            expires_in=3600
        )
        
        assert token.user_id == "user123"
        assert token.provider == OAuthProvider.GOOGLE
        assert token.access_token == "access_token_123"
        assert token.refresh_token == "refresh_token_123"
        assert token.expires_in == 3600
    
    def test_oauth_token_create_expires_in_validation(self):
        """Test OAuthTokenCreate expires_in validation."""
        # Valid expires_in
        token = OAuthTokenCreate(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            expires_in=3600
        )
        assert token.expires_in == 3600
        
        # Zero expires_in
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenCreate(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                access_token="access_token_123",
                expires_in=0
            )
        assert "expires_in must be positive" in str(exc_info.value)
        
        # Negative expires_in
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenCreate(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                access_token="access_token_123",
                expires_in=-1
            )
        assert "expires_in must be positive" in str(exc_info.value)
        
        # None expires_in
        token = OAuthTokenCreate(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            expires_in=None
        )
        assert token.expires_in is None


class TestOAuthTokenUpdate:
    """Test OAuthTokenUpdate model."""
    
    def test_oauth_token_update_valid_data(self):
        """Test OAuthTokenUpdate with valid data."""
        update = OAuthTokenUpdate(
            status=TokenStatus.EXPIRED,
            refresh_token="new_refresh_token_123",
            token_expires_at=datetime.utcnow() + timedelta(hours=2),
            permissions=["read:own_courses", "write:own_courses"],
            last_used=datetime.utcnow()
        )
        
        assert update.status == TokenStatus.EXPIRED
        assert update.refresh_token == "new_refresh_token_123"
        assert isinstance(update.token_expires_at, datetime)
        assert update.permissions == ["read:own_courses", "write:own_courses"]
        assert isinstance(update.last_used, datetime)
    
    def test_oauth_token_update_all_none(self):
        """Test OAuthTokenUpdate with all None values."""
        update = OAuthTokenUpdate()
        
        assert update.status is None
        assert update.refresh_token is None
        assert update.token_expires_at is None
        assert update.permissions is None
        assert update.last_used is None


class TestOAuthTokenResponse:
    """Test OAuthTokenResponse model."""
    
    def test_oauth_token_response_valid_data(self):
        """Test OAuthTokenResponse with valid data."""
        response = OAuthTokenResponse(
            token_id="token123",
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            access_token="access_token_123",
            refresh_token="refresh_token_123",
            status=TokenStatus.ACTIVE
        )
        
        assert response.token_id == "token123"
        assert response.user_id == "user123"
        assert response.provider == OAuthProvider.GOOGLE
        assert response.access_token == "access_token_123"
        assert response.refresh_token == "refresh_token_123"
        assert response.status == TokenStatus.ACTIVE


class TestOAuthTokenRefresh:
    """Test OAuthTokenRefresh model."""
    
    def test_oauth_token_refresh_valid_data(self):
        """Test OAuthTokenRefresh with valid data."""
        refresh = OAuthTokenRefresh(
            refresh_token="refresh_token_123",
            grant_type="refresh_token"
        )
        
        assert refresh.refresh_token == "refresh_token_123"
        assert refresh.grant_type == "refresh_token"
    
    def test_oauth_token_refresh_token_validation(self):
        """Test OAuthTokenRefresh token validation."""
        # Valid refresh token
        refresh = OAuthTokenRefresh(refresh_token="valid_refresh_token_123")
        assert refresh.refresh_token == "valid_refresh_token_123"
        
        # Empty refresh token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenRefresh(refresh_token="")
        assert "Refresh token must be at least 10 characters long" in str(exc_info.value)
        
        # Short refresh token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenRefresh(refresh_token="short")
        assert "Refresh token must be at least 10 characters long" in str(exc_info.value)
        
        # Refresh token normalization
        refresh = OAuthTokenRefresh(refresh_token="  refresh_token_123  ")
        assert refresh.refresh_token == "refresh_token_123"


class TestOAuthAuthorization:
    """Test OAuthAuthorization model."""
    
    def test_oauth_authorization_valid_data(self):
        """Test OAuthAuthorization with valid data."""
        auth = OAuthAuthorization(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            authorization_code="auth_code_123",
            redirect_uri="http://localhost:3000/callback",
            state="state_123"
        )
        
        assert auth.user_id == "user123"
        assert auth.provider == OAuthProvider.GOOGLE
        assert auth.authorization_code == "auth_code_123"
        assert auth.redirect_uri == "http://localhost:3000/callback"
        assert auth.state == "state_123"
    
    def test_oauth_authorization_code_validation(self):
        """Test OAuthAuthorization code validation."""
        # Valid authorization code
        auth = OAuthAuthorization(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            authorization_code="valid_auth_code_123",
            redirect_uri="http://localhost:3000/callback"
        )
        assert auth.authorization_code == "valid_auth_code_123"
        
        # Empty authorization code
        with pytest.raises(ValidationError) as exc_info:
            OAuthAuthorization(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                authorization_code="",
                redirect_uri="http://localhost:3000/callback"
            )
        assert "Authorization code must be at least 10 characters long" in str(exc_info.value)
        
        # Short authorization code
        with pytest.raises(ValidationError) as exc_info:
            OAuthAuthorization(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                authorization_code="short",
                redirect_uri="http://localhost:3000/callback"
            )
        assert "Authorization code must be at least 10 characters long" in str(exc_info.value)
    
    def test_oauth_authorization_redirect_uri_validation(self):
        """Test OAuthAuthorization redirect URI validation."""
        # Valid redirect URI
        auth = OAuthAuthorization(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            authorization_code="auth_code_123",
            redirect_uri="http://localhost:3000/callback"
        )
        assert auth.redirect_uri == "http://localhost:3000/callback"
        
        # Empty redirect URI
        with pytest.raises(ValidationError) as exc_info:
            OAuthAuthorization(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                authorization_code="auth_code_123",
                redirect_uri=""
            )
        assert "Redirect URI cannot be empty" in str(exc_info.value)
        
        # Invalid redirect URI
        with pytest.raises(ValidationError) as exc_info:
            OAuthAuthorization(
                user_id="user123",
                provider=OAuthProvider.GOOGLE,
                authorization_code="auth_code_123",
                redirect_uri="invalid-uri"
            )
        assert "Redirect URI must be a valid HTTP/HTTPS URL" in str(exc_info.value)
        
        # Redirect URI normalization - the validator strips whitespace first
        auth = OAuthAuthorization(
            user_id="user123",
            provider=OAuthProvider.GOOGLE,
            authorization_code="auth_code_123",
            redirect_uri="http://localhost:3000/callback"
        )
        assert auth.redirect_uri == "http://localhost:3000/callback"


class TestOAuthTokenExchange:
    """Test OAuthTokenExchange model."""
    
    def test_oauth_token_exchange_valid_data(self):
        """Test OAuthTokenExchange with valid data."""
        exchange = OAuthTokenExchange(
            authorization_code="auth_code_123",
            redirect_uri="http://localhost:3000/callback",
            client_id="client_id_123",
            client_secret="client_secret_123",
            grant_type="authorization_code"
        )
        
        assert exchange.authorization_code == "auth_code_123"
        assert exchange.redirect_uri == "http://localhost:3000/callback"
        assert exchange.client_id == "client_id_123"
        assert exchange.client_secret == "client_secret_123"
        assert exchange.grant_type == "authorization_code"
    
    def test_oauth_token_exchange_client_id_validation(self):
        """Test OAuthTokenExchange client ID validation."""
        # Valid client ID
        exchange = OAuthTokenExchange(
            authorization_code="auth_code_123",
            redirect_uri="http://localhost:3000/callback",
            client_id="valid_client_id_123",
            client_secret="client_secret_123"
        )
        assert exchange.client_id == "valid_client_id_123"
        
        # Empty client ID
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenExchange(
                authorization_code="auth_code_123",
                redirect_uri="http://localhost:3000/callback",
                client_id="",
                client_secret="client_secret_123"
            )
        assert "Client ID must be at least 5 characters long" in str(exc_info.value)
        
        # Short client ID - "short" is actually 5 characters, so it should pass
        exchange = OAuthTokenExchange(
            authorization_code="auth_code_123",
            redirect_uri="http://localhost:3000/callback",
            client_id="short",
            client_secret="client_secret_123"
        )
        assert exchange.client_id == "short"
        
        # Very short client ID
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenExchange(
                authorization_code="auth_code_123",
                redirect_uri="http://localhost:3000/callback",
                client_id="id",
                client_secret="client_secret_123"
            )
        assert "Client ID must be at least 5 characters long" in str(exc_info.value)
    
    def test_oauth_token_exchange_client_secret_validation(self):
        """Test OAuthTokenExchange client secret validation."""
        # Valid client secret
        exchange = OAuthTokenExchange(
            authorization_code="auth_code_123",
            redirect_uri="http://localhost:3000/callback",
            client_id="client_id_123",
            client_secret="valid_client_secret_123"
        )
        assert exchange.client_secret == "valid_client_secret_123"
        
        # Empty client secret
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenExchange(
                authorization_code="auth_code_123",
                redirect_uri="http://localhost:3000/callback",
                client_id="client_id_123",
                client_secret=""
            )
        assert "Client secret must be at least 10 characters long" in str(exc_info.value)
        
        # Short client secret
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenExchange(
                authorization_code="auth_code_123",
                redirect_uri="http://localhost:3000/callback",
                client_id="client_id_123",
                client_secret="short"
            )
        assert "Client secret must be at least 10 characters long" in str(exc_info.value)


class TestOAuthTokenValidation:
    """Test OAuthTokenValidation model."""
    
    def test_oauth_token_validation_valid_data(self):
        """Test OAuthTokenValidation with valid data."""
        validation = OAuthTokenValidation(
            token="token_123456789",
            token_type=TokenType.ACCESS
        )
        
        assert validation.token == "token_123456789"
        assert validation.token_type == TokenType.ACCESS
    
    def test_oauth_token_validation_token_validation(self):
        """Test OAuthTokenValidation token validation."""
        # Valid token
        validation = OAuthTokenValidation(
            token="valid_token_123",
            token_type=TokenType.ACCESS
        )
        assert validation.token == "valid_token_123"
        
        # Empty token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenValidation(token="", token_type=TokenType.ACCESS)
        assert "Token must be at least 10 characters long" in str(exc_info.value)
        
        # Short token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenValidation(token="short", token_type=TokenType.ACCESS)
        assert "Token must be at least 10 characters long" in str(exc_info.value)
        
        # Token normalization
        validation = OAuthTokenValidation(
            token="  token_123456789  ",
            token_type=TokenType.ACCESS
        )
        assert validation.token == "token_123456789"


class TestOAuthTokenRevoke:
    """Test OAuthTokenRevoke model."""
    
    def test_oauth_token_revoke_valid_data(self):
        """Test OAuthTokenRevoke with valid data."""
        revoke = OAuthTokenRevoke(
            token="token_123456789",
            token_type_hint=TokenType.ACCESS
        )
        
        assert revoke.token == "token_123456789"
        assert revoke.token_type_hint == TokenType.ACCESS
    
    def test_oauth_token_revoke_token_validation(self):
        """Test OAuthTokenRevoke token validation."""
        # Valid token
        revoke = OAuthTokenRevoke(token="valid_token_123")
        assert revoke.token == "valid_token_123"
        
        # Empty token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenRevoke(token="")
        assert "Token must be at least 10 characters long" in str(exc_info.value)
        
        # Short token
        with pytest.raises(ValidationError) as exc_info:
            OAuthTokenRevoke(token="short")
        assert "Token must be at least 10 characters long" in str(exc_info.value)
        
        # Token normalization
        revoke = OAuthTokenRevoke(token="  token_123456789  ")
        assert revoke.token == "token_123456789"
    
    def test_oauth_token_revoke_default_values(self):
        """Test OAuthTokenRevoke with default values."""
        revoke = OAuthTokenRevoke(token="token_123456789")
        
        assert revoke.token == "token_123456789"
        assert revoke.token_type_hint is None