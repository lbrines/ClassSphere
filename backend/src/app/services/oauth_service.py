"""
OAuth service for Google OAuth 2.0 integration.
"""
import httpx
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from src.app.core.config import settings
from src.app.exceptions.oauth import OAuthError, OAuthTokenError, OAuthAuthorizationError


class OAuthService:
    """Service for Google OAuth 2.0 authentication."""
    
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.scope = settings.GOOGLE_SCOPE
        self.google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.google_token_url = "https://oauth2.googleapis.com/token"
        self.google_userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def google_oauth_flow(self, state: Optional[str] = None) -> str:
        """Generate Google OAuth authorization URL."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent"
        }
        
        if state:
            params["state"] = state
        
        auth_url = f"{self.google_auth_url}?{urlencode(params)}"
        return auth_url
    
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token."""
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.google_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                await response.raise_for_status()
                
                token_response = await response.json()
                
                # Validate token response
                if "access_token" not in token_response:
                    raise OAuthTokenError("No access token in response")
                
                return token_response
                
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"HTTP error during token exchange: {e.response.status_code}")
        except httpx.RequestError as e:
            raise OAuthError(f"Request error during token exchange: {str(e)}")
        except Exception as e:
            raise OAuthError(f"Unexpected error during token exchange: {str(e)}")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google API."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.google_userinfo_url,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                await response.raise_for_status()
                
                user_info = await response.json()
                
                # Validate user info
                if "id" not in user_info:
                    raise OAuthError("No user ID in Google response")
                
                return user_info
                
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"HTTP error getting user info: {e.response.status_code}")
        except httpx.RequestError as e:
            raise OAuthError(f"Request error getting user info: {str(e)}")
        except Exception as e:
            raise OAuthError(f"Unexpected error getting user info: {str(e)}")
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token."""
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.google_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                await response.raise_for_status()
                
                token_response = await response.json()
                
                # Validate token response
                if "access_token" not in token_response:
                    raise OAuthTokenError("No access token in refresh response")
                
                return token_response
                
        except httpx.HTTPStatusError as e:
            raise OAuthError(f"HTTP error during token refresh: {e.response.status_code}")
        except httpx.RequestError as e:
            raise OAuthError(f"Request error during token refresh: {str(e)}")
        except Exception as e:
            raise OAuthError(f"Unexpected error during token refresh: {str(e)}")


# Global instance
oauth_service = OAuthService()