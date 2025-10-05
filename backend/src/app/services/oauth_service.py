"""
OAuth service for Google integration.
"""
import asyncio
import secrets
from typing import Optional, Dict, Any
from urllib.parse import urlencode
import httpx

from ..core.config import settings
from ..core.exceptions import ExternalServiceError
from ..models.oauth_token import GoogleOAuthResponse, GoogleUserInfo
from ..models.user import UserInDB, UserRole
from .auth_service import AuthService


class OAuthService:
    """OAuth service for Google integration."""

    def __init__(self):
        """Initialize OAuth service."""
        self.auth_service = AuthService()
        self.google_oauth_url = "https://accounts.google.com/o/oauth2/auth"
        self.google_token_url = "https://oauth2.googleapis.com/token"
        self.google_userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    async def get_google_auth_url(self, state: Optional[str] = None) -> str:
        """
        Generate Google OAuth authorization URL.

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            Google OAuth authorization URL
        """
        if not state:
            state = secrets.token_urlsafe(32)

        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.google_redirect_uri,
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }

        return f"{self.google_oauth_url}?{urlencode(params)}"

    async def exchange_code_for_token(
        self,
        code: str,
        state: Optional[str] = None
    ) -> GoogleOAuthResponse:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code from Google
            state: State parameter for CSRF protection

        Returns:
            Google OAuth response with tokens

        Raises:
            ExternalServiceError: If token exchange fails
        """
        token_data = {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.google_redirect_uri,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await asyncio.wait_for(
                    client.post(
                        self.google_token_url,
                        data=token_data,
                        headers={"Accept": "application/json"}
                    ),
                    timeout=10.0
                )

                if response.status_code != 200:
                    raise ExternalServiceError(
                        f"Google token exchange failed: {response.status_code}"
                    )

                token_response = response.json()
                return GoogleOAuthResponse(**token_response)

        except asyncio.TimeoutError:
            raise ExternalServiceError("Google token exchange timeout")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Google token exchange error: {str(e)}")

    async def get_user_info(self, access_token: str) -> GoogleUserInfo:
        """
        Get user information from Google API.

        Args:
            access_token: Google access token

        Returns:
            Google user information

        Raises:
            ExternalServiceError: If user info retrieval fails
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await asyncio.wait_for(
                    client.get(self.google_userinfo_url, headers=headers),
                    timeout=10.0
                )

                if response.status_code != 200:
                    raise ExternalServiceError(
                        f"Google userinfo failed: {response.status_code}"
                    )

                user_data = response.json()
                return GoogleUserInfo(**user_data)

        except asyncio.TimeoutError:
            raise ExternalServiceError("Google userinfo timeout")
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Google userinfo error: {str(e)}")

    async def authenticate_with_google(
        self,
        code: str,
        state: Optional[str] = None
    ) -> tuple[UserInDB, str]:
        """
        Authenticate user with Google OAuth code.

        Args:
            code: Authorization code from Google
            state: State parameter for CSRF protection

        Returns:
            Tuple of (UserInDB, JWT token)

        Raises:
            ExternalServiceError: If authentication fails
        """
        # Exchange code for token
        oauth_response = await self.exchange_code_for_token(code, state)

        # Get user info from Google
        user_info = await self.get_user_info(oauth_response.access_token)

        # Find or create user
        user = await self._find_or_create_user(user_info)

        # Create JWT token
        jwt_token = await self.auth_service.create_token(user)

        return user, jwt_token

    async def _find_or_create_user(self, user_info: GoogleUserInfo) -> UserInDB:
        """
        Find existing user or create new one based on Google user info.

        Args:
            user_info: Google user information

        Returns:
            UserInDB object
        """
        # Try to find existing user by email
        existing_user = await self.auth_service._get_user_by_email(user_info.email)

        if existing_user:
            return existing_user

        # For mock implementation, return a default user
        # In real implementation, this would create a new user in the database
        from datetime import datetime
        return UserInDB(
            id=f"google-{user_info.id}",
            email=user_info.email,
            name=user_info.name,
            role=UserRole.STUDENT,  # Default role for new Google users
            hashed_password="",  # No password for OAuth users
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )