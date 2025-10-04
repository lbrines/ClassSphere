"""OAuth service for Google OAuth 2.0 integration."""

import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from urllib.parse import urlencode, parse_qs, urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from ..core.config import settings
from ..core.exceptions import OAuthError, GoogleAPIError
from ..models.oauth import OAuthTokenCreate, OAuthTokenResponse, GoogleOAuthProfile


class OAuthService:
    """OAuth service for Google OAuth 2.0 operations."""

    def __init__(self):
        self.client_id = settings.google_client_id
        self.client_secret = settings.google_client_secret
        self.redirect_uri = settings.google_redirect_uri
        self.scopes = settings.google_classroom_scopes.split(',')

    def generate_oauth_url(self, state: Optional[str] = None) -> str:
        """Generate Google OAuth authorization URL."""
        if not self.client_id:
            raise OAuthError("Google client ID not configured")

        if not state:
            state = secrets.token_urlsafe(32)

        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent',
            'state': state
        }

        base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        return f"{base_url}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str, state: Optional[str] = None) -> OAuthTokenResponse:
        """Exchange authorization code for access token."""
        try:
            # Create OAuth flow
            flow = Flow.from_client_config(
                {
                    'web': {
                        'client_id': self.client_id,
                        'client_secret': self.client_secret,
                        'auth_uri': 'https://accounts.google.com/o/oauth2/v2/auth',
                        'token_uri': 'https://oauth2.googleapis.com/token',
                        'redirect_uris': [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri

            # Exchange code for token
            flow.fetch_token(code=code)

            # Get credentials
            credentials = flow.credentials

            # Create token response
            token_response = OAuthTokenResponse(
                id=str(secrets.token_urlsafe(16)),
                provider="google",
                token_type="Bearer",
                expires_at=datetime.utcnow() + timedelta(seconds=credentials.expiry),
                scope=" ".join(credentials.scopes) if credentials.scopes else None,
                created_at=datetime.utcnow(),
                updated_at=None
            )

            return token_response

        except Exception as e:
            raise OAuthError(
                f"Failed to exchange code for token: {str(e)}",
                provider="google",
                error_code="token_exchange_failed"
            )

    async def refresh_access_token(self, refresh_token: str) -> OAuthTokenResponse:
        """Refresh access token using refresh token."""
        try:
            credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.scopes
            )

            # Refresh token
            request = Request()
            credentials.refresh(request)

            # Create token response
            token_response = OAuthTokenResponse(
                id=str(secrets.token_urlsafe(16)),
                provider="google",
                token_type="Bearer",
                expires_at=datetime.utcnow() + timedelta(seconds=credentials.expiry),
                scope=" ".join(credentials.scopes) if credentials.scopes else None,
                created_at=datetime.utcnow(),
                updated_at=None
            )

            return token_response

        except Exception as e:
            raise OAuthError(
                f"Failed to refresh token: {str(e)}",
                provider="google",
                error_code="token_refresh_failed"
            )

    async def get_user_profile(self, access_token: str) -> GoogleOAuthProfile:
        """Get user profile from Google."""
        try:
            credentials = Credentials(token=access_token)
            service = build('oauth2', 'v2', credentials=credentials)
            
            user_info = service.userinfo().get().execute()

            return GoogleOAuthProfile(
                id=user_info.get('id'),
                email=user_info.get('email'),
                verified_email=user_info.get('verified_email', False),
                name=user_info.get('name'),
                given_name=user_info.get('given_name'),
                family_name=user_info.get('family_name'),
                picture=user_info.get('picture'),
                locale=user_info.get('locale')
            )

        except Exception as e:
            raise GoogleAPIError(
                f"Failed to get user profile: {str(e)}",
                api_name="Google OAuth2",
                error_code="profile_fetch_failed"
            )

    async def validate_token(self, access_token: str) -> bool:
        """Validate access token with Google."""
        try:
            credentials = Credentials(token=access_token)
            service = build('oauth2', 'v2', credentials=credentials)
            
            # Try to get user info to validate token
            service.userinfo().get().execute()
            return True

        except Exception:
            return False

    def get_classroom_service(self, access_token: str):
        """Get Google Classroom service instance."""
        try:
            credentials = Credentials(token=access_token)
            return build('classroom', 'v1', credentials=credentials)
        except Exception as e:
            raise GoogleAPIError(
                f"Failed to create Classroom service: {str(e)}",
                api_name="Google Classroom",
                error_code="service_creation_failed"
            )
