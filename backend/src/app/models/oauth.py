"""
OAuth token models using Pydantic v2 with ConfigDict.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class TokenType(str, Enum):
    """Token type enum."""
    ACCESS = "access"
    REFRESH = "refresh"
    OAUTH = "oauth"
    GOOGLE = "google"


class OAuthProvider(str, Enum):
    """OAuth provider enum."""
    GOOGLE = "google"
    MICROSOFT = "microsoft"
    GITHUB = "github"


class TokenStatus(str, Enum):
    """Token status enum."""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    INVALID = "invalid"


class OAuthTokenBase(BaseModel):
    """Base OAuth token model."""
    user_id: str = Field(..., description="User unique identifier")
    provider: OAuthProvider = Field(..., description="OAuth provider")
    token_type: TokenType = Field(default=TokenType.OAUTH, description="Token type")
    status: TokenStatus = Field(default=TokenStatus.ACTIVE, description="Token status")
    
    # Token data
    access_token: str = Field(..., description="OAuth access token")
    refresh_token: Optional[str] = Field(None, description="OAuth refresh token")
    token_expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")
    
    # Provider-specific data
    provider_user_id: Optional[str] = Field(None, description="Provider user ID")
    provider_email: Optional[str] = Field(None, description="Provider email")
    provider_name: Optional[str] = Field(None, description="Provider display name")
    provider_avatar: Optional[str] = Field(None, description="Provider avatar URL")
    
    # Scopes and permissions
    scopes: List[str] = Field(default_factory=list, description="OAuth scopes")
    permissions: List[str] = Field(default_factory=list, description="Granted permissions")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")
    
    # Additional metadata for compatibility with MockService and Google API
    raw_data: Optional[Dict[str, Any]] = Field(default=None, description="Raw provider response data")
    expires_in: Optional[int] = Field(None, description="Token expiration in seconds")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    @field_validator('access_token')
    @classmethod
    def validate_access_token(cls, v: str) -> str:
        """Validate access token format."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Access token must be at least 10 characters long')
        return v.strip()
    
    @field_validator('provider_email')
    @classmethod
    def validate_provider_email(cls, v: Optional[str]) -> Optional[str]:
        """Validate provider email format."""
        if v is None:
            return v
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid provider email format')
        return v.lower()
    
    @field_validator('scopes')
    @classmethod
    def validate_scopes(cls, v: List[str]) -> List[str]:
        """Validate OAuth scopes."""
        if not v:
            return v
        
        # Remove duplicates and empty strings
        scopes = list(set(filter(None, v)))
        
        # Validate scope format
        for scope in scopes:
            if not scope.strip() or ' ' in scope:
                raise ValueError(f'Invalid scope format: {scope}')
        
        return scopes


class OAuthTokenCreate(OAuthTokenBase):
    """OAuth token creation model."""
    # Override to make access_token required for creation
    access_token: str = Field(..., description="OAuth access token")
    
    @field_validator('expires_in')
    @classmethod
    def validate_expires_in(cls, v: Optional[int]) -> Optional[int]:
        """Validate expires_in value."""
        if v is not None and v <= 0:
            raise ValueError('expires_in must be positive')
        return v


class OAuthTokenUpdate(BaseModel):
    """OAuth token update model."""
    status: Optional[TokenStatus] = Field(None, description="Token status")
    refresh_token: Optional[str] = Field(None, description="OAuth refresh token")
    token_expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")
    permissions: Optional[List[str]] = Field(None, description="Granted permissions")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class OAuthTokenResponse(OAuthTokenBase):
    """OAuth token response model."""
    token_id: str = Field(..., description="Token unique identifier")
    
    # Exclude sensitive fields from response
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class OAuthTokenRefresh(BaseModel):
    """OAuth token refresh model."""
    refresh_token: str = Field(..., description="OAuth refresh token")
    grant_type: str = Field(default="refresh_token", description="OAuth grant type")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True
    )
    
    @field_validator('refresh_token')
    @classmethod
    def validate_refresh_token(cls, v: str) -> str:
        """Validate refresh token format."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Refresh token must be at least 10 characters long')
        return v.strip()


class OAuthAuthorization(BaseModel):
    """OAuth authorization model."""
    user_id: str = Field(..., description="User unique identifier")
    provider: OAuthProvider = Field(..., description="OAuth provider")
    authorization_code: str = Field(..., description="OAuth authorization code")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    state: Optional[str] = Field(None, description="OAuth state parameter")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True
    )
    
    @field_validator('authorization_code')
    @classmethod
    def validate_authorization_code(cls, v: str) -> str:
        """Validate authorization code format."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Authorization code must be at least 10 characters long')
        return v.strip()
    
    @field_validator('redirect_uri')
    @classmethod
    def validate_redirect_uri(cls, v: str) -> str:
        """Validate redirect URI format."""
        if not v.strip():
            raise ValueError('Redirect URI cannot be empty')
        
        # Basic URL validation
        if not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError('Redirect URI must be a valid HTTP/HTTPS URL')
        
        return v.strip()


class OAuthTokenExchange(BaseModel):
    """OAuth token exchange model."""
    authorization_code: str = Field(..., description="OAuth authorization code")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    client_id: str = Field(..., description="OAuth client ID")
    client_secret: str = Field(..., description="OAuth client secret")
    grant_type: str = Field(default="authorization_code", description="OAuth grant type")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True
    )
    
    @field_validator('authorization_code')
    @classmethod
    def validate_authorization_code(cls, v: str) -> str:
        """Validate authorization code format."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Authorization code must be at least 10 characters long')
        return v.strip()
    
    @field_validator('client_id')
    @classmethod
    def validate_client_id(cls, v: str) -> str:
        """Validate client ID format."""
        if not v or len(v.strip()) < 5:
            raise ValueError('Client ID must be at least 5 characters long')
        return v.strip()
    
    @field_validator('client_secret')
    @classmethod
    def validate_client_secret(cls, v: str) -> str:
        """Validate client secret format."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Client secret must be at least 10 characters long')
        return v.strip()


class OAuthTokenValidation(BaseModel):
    """OAuth token validation model."""
    token: str = Field(..., description="Token to validate")
    token_type: TokenType = Field(..., description="Token type")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True
    )
    
    @field_validator('token')
    @classmethod
    def validate_token(cls, v: str) -> str:
        """Validate token format."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Token must be at least 10 characters long')
        return v.strip()


class OAuthTokenRevoke(BaseModel):
    """OAuth token revocation model."""
    token: str = Field(..., description="Token to revoke")
    token_type_hint: Optional[TokenType] = Field(None, description="Token type hint")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True
    )
    
    @field_validator('token')
    @classmethod
    def validate_token(cls, v: str) -> str:
        """Validate token format."""
        if not v or len(v.strip()) < 10:
            raise ValueError('Token must be at least 10 characters long')
        return v.strip()