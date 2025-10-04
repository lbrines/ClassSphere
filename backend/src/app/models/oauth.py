"""OAuth models with Pydantic v2."""

from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator, field_serializer, AnyUrl
from pydantic.types import SecretStr


class OAuthProvider(str, Enum):
    """OAuth provider enumeration."""
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    GITHUB = "github"
    MOCK = "mock"


class TokenType(str, Enum):
    """Token type enumeration."""
    BEARER = "Bearer"
    JWT = "JWT"


class OAuthTokenBase(BaseModel):
    """Base OAuth token model."""

    provider: OAuthProvider
    access_token: SecretStr
    token_type: TokenType = TokenType.BEARER
    expires_in: Optional[int] = None
    scope: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    @field_validator("scope")
    @classmethod
    def validate_scope(cls, v: Optional[str]) -> Optional[str]:
        """Validate OAuth scope format."""
        if v is None:
            return v

        # Remove extra whitespace and validate scope format
        scopes = [scope.strip() for scope in v.split() if scope.strip()]
        return " ".join(scopes) if scopes else None


class OAuthTokenCreate(OAuthTokenBase):
    """OAuth token creation model."""

    refresh_token: Optional[SecretStr] = None
    id_token: Optional[SecretStr] = None
    user_id: str

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Validate user ID."""
        if not v or not v.strip():
            raise ValueError("User ID cannot be empty")
        return v.strip()


class OAuthTokenUpdate(BaseModel):
    """OAuth token update model."""

    access_token: Optional[SecretStr] = None
    refresh_token: Optional[SecretStr] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )


class OAuthTokenResponse(BaseModel):
    """OAuth token response model."""

    id: str
    provider: OAuthProvider
    token_type: TokenType
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_expired: bool = False

    model_config = ConfigDict(
        from_attributes=True
    )

    @field_serializer('created_at', 'updated_at', 'expires_at', when_used='json')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO format."""
        return value.isoformat() if value else None


class OAuthTokenInDB(OAuthTokenResponse):
    """OAuth token model as stored in database."""

    user_id: str
    access_token: str  # Encrypted in storage
    refresh_token: Optional[str] = None  # Encrypted in storage
    id_token: Optional[str] = None  # Encrypted in storage


class GoogleOAuthProfile(BaseModel):
    """Google OAuth profile model."""

    id: str
    email: str
    name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[AnyUrl] = None
    locale: Optional[str] = None
    verified_email: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate and normalize email."""
        return v.lower().strip()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name."""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class OAuthAuthorizationCode(BaseModel):
    """OAuth authorization code model."""

    code: str
    state: Optional[str] = None
    scope: Optional[str] = None
    provider: OAuthProvider = OAuthProvider.GOOGLE

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid"
    )

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Validate authorization code."""
        if not v or not v.strip():
            raise ValueError("Authorization code cannot be empty")
        return v.strip()


class OAuthConfig(BaseModel):
    """OAuth configuration model."""

    provider: OAuthProvider
    client_id: str
    client_secret: SecretStr
    redirect_uri: AnyUrl
    scopes: List[str]
    authorization_url: AnyUrl
    token_url: AnyUrl
    userinfo_url: Optional[AnyUrl] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid"
    )

    @field_validator("client_id")
    @classmethod
    def validate_client_id(cls, v: str) -> str:
        """Validate client ID."""
        if not v or not v.strip():
            raise ValueError("Client ID cannot be empty")
        return v.strip()

    @field_validator("scopes")
    @classmethod
    def validate_scopes(cls, v: List[str]) -> List[str]:
        """Validate OAuth scopes."""
        if not v:
            raise ValueError("At least one scope is required")

        # Remove duplicates and empty scopes
        scopes = list(set(scope.strip() for scope in v if scope.strip()))
        if not scopes:
            raise ValueError("At least one valid scope is required")

        return scopes


class OAuthError(BaseModel):
    """OAuth error model."""

    error: str
    error_description: Optional[str] = None
    error_uri: Optional[AnyUrl] = None
    state: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid"
    )


class OAuthTokenValidation(BaseModel):
    """OAuth token validation model."""

    is_valid: bool
    expires_at: Optional[datetime] = None
    scope: Optional[str] = None
    audience: Optional[str] = None
    issuer: Optional[str] = None
    subject: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )

    @field_serializer('expires_at', when_used='json')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO format."""
        return value.isoformat() if value else None


class OAuthRefreshRequest(BaseModel):
    """OAuth token refresh request model."""

    refresh_token: SecretStr
    provider: OAuthProvider = OAuthProvider.GOOGLE

    model_config = ConfigDict(extra="forbid")

    @field_validator("refresh_token")
    @classmethod
    def validate_refresh_token(cls, v: SecretStr) -> SecretStr:
        """Validate refresh token."""
        token = v.get_secret_value()
        if not token or not token.strip():
            raise ValueError("Refresh token cannot be empty")
        return v