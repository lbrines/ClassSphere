"""
OAuth token model definitions for ClassSphere.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class OAuthTokenBase(BaseModel):
    """Base OAuth token model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class OAuthToken(OAuthTokenBase):
    """OAuth token model with metadata."""
    id: str = Field(..., description="Token unique identifier")
    user_id: str = Field(..., description="Associated user ID")
    provider: str = Field(..., description="OAuth provider (e.g., google)")
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OAuthTokenCreate(BaseModel):
    """OAuth token creation model."""
    user_id: str
    provider: str
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class OAuthTokenUpdate(BaseModel):
    """OAuth token update model."""
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    scope: Optional[str] = None


class GoogleOAuthResponse(BaseModel):
    """Google OAuth response model."""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: str
    id_token: Optional[str] = None


class GoogleUserInfo(BaseModel):
    """Google user information model."""
    id: str
    email: str
    verified_email: bool
    name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None