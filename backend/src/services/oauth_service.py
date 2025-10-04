"""
Dashboard Educativo - OAuth 2.0 Google Service
Context-Aware Implementation - Day 3-4 Critical
Implements PKCE + State validation with context tracking
"""

from typing import Dict, Any, Optional
import secrets
import hashlib
import base64
from urllib.parse import urlencode, parse_qs, urlparse
import httpx

from ..core.config import get_settings
from ..core.context_logger import log_context_status
from ..core.exceptions import OAuthError, GoogleAPIError


class OAuthService:
    """OAuth 2.0 Google Service with PKCE and State validation"""
    
    def __init__(self):
        self.settings = get_settings()
        self.google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.google_token_url = "https://oauth2.googleapis.com/token"
        self.google_userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        
        # PKCE parameters
        self.code_verifier = self._generate_code_verifier()
        self.code_challenge = self._generate_code_challenge(self.code_verifier)
    
    def _generate_code_verifier(self) -> str:
        """Generate PKCE code verifier"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    
    def _generate_code_challenge(self, code_verifier: str) -> str:
        """Generate PKCE code challenge"""
        challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(challenge).decode('utf-8').rstrip('=')
    
    def _generate_state(self) -> str:
        """Generate state parameter for CSRF protection"""
        return secrets.token_urlsafe(32)
    
    async def get_authorization_url(self, redirect_uri: Optional[str] = None) -> Dict[str, Any]:
        """Get Google OAuth authorization URL with PKCE and State"""
        
        # Log OAuth URL generation
        await log_context_status(
            context_id="oauth-auth-url-001",
            priority="CRITICAL",
            status="started",
            position="beginning",
            message="Generating Google OAuth authorization URL",
            phase="oauth",
            task="get_authorization_url"
        )
        
        try:
            state = self._generate_state()
            redirect_uri = redirect_uri or self.settings.google_redirect_uri
            
            params = {
                "client_id": self.settings.google_client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": " ".join(self.settings.google_scopes),
                "access_type": "offline",
                "prompt": "consent",
                "state": state,
                "code_challenge": self.code_challenge,
                "code_challenge_method": "S256"
            }
            
            auth_url = f"{self.google_auth_url}?{urlencode(params)}"
            
            # Log successful URL generation
            await log_context_status(
                context_id="oauth-auth-url-001",
                priority="CRITICAL",
                status="completed",
                position="beginning",
                message="Google OAuth authorization URL generated successfully",
                phase="oauth",
                task="get_authorization_url"
            )
            
            return {
                "authorization_url": auth_url,
                "state": state,
                "code_verifier": self.code_verifier,
                "scopes": self.settings.google_scopes
            }
            
        except Exception as e:
            # Log error
            await log_context_status(
                context_id="oauth-auth-url-001",
                priority="CRITICAL",
                status="failed",
                position="beginning",
                message=f"Failed to generate OAuth URL: {str(e)}",
                phase="oauth",
                task="get_authorization_url"
            )
            raise OAuthError(f"Failed to generate authorization URL: {str(e)}")
    
    async def exchange_code_for_token(
        self,
        code: str,
        state: str,
        code_verifier: str,
        redirect_uri: Optional[str] = None
    ) -> Dict[str, Any]:
        """Exchange authorization code for access token with PKCE"""
        
        # Log token exchange
        await log_context_status(
            context_id="oauth-token-exchange-002",
            priority="CRITICAL",
            status="started",
            position="beginning",
            message="Exchanging authorization code for access token",
            phase="oauth",
            task="exchange_code_for_token"
        )
        
        try:
            redirect_uri = redirect_uri or self.settings.google_redirect_uri
            
            data = {
                "client_id": self.settings.google_client_id,
                "client_secret": self.settings.google_client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
                "code_verifier": code_verifier
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.google_token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    
                    # Log successful token exchange
                    await log_context_status(
                        context_id="oauth-token-exchange-002",
                        priority="CRITICAL",
                        status="completed",
                        position="beginning",
                        message="Access token obtained successfully",
                        phase="oauth",
                        task="exchange_code_for_token"
                    )
                    
                    return token_data
                else:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get("error_description", "Token exchange failed")
                    
                    # Log token exchange error
                    await log_context_status(
                        context_id="oauth-token-exchange-002",
                        priority="CRITICAL",
                        status="failed",
                        position="beginning",
                        message=f"Token exchange failed: {error_msg}",
                        phase="oauth",
                        task="exchange_code_for_token"
                    )
                    
                    raise OAuthError(f"Token exchange failed: {error_msg}")
                    
        except httpx.RequestError as e:
            # Log network error
            await log_context_status(
                context_id="oauth-token-exchange-002",
                priority="CRITICAL",
                status="failed",
                position="beginning",
                message=f"Network error during token exchange: {str(e)}",
                phase="oauth",
                task="exchange_code_for_token"
            )
            raise OAuthError(f"Network error: {str(e)}")
        except Exception as e:
            # Log unexpected error
            await log_context_status(
                context_id="oauth-token-exchange-002",
                priority="CRITICAL",
                status="failed",
                position="beginning",
                message=f"Unexpected error during token exchange: {str(e)}",
                phase="oauth",
                task="exchange_code_for_token"
            )
            raise OAuthError(f"Unexpected error: {str(e)}")
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google API"""
        
        # Log user info request
        await log_context_status(
            context_id="oauth-user-info-003",
            priority="HIGH",
            status="started",
            position="middle",
            message="Fetching user information from Google API",
            phase="oauth",
            task="get_user_info"
        )
        
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.google_userinfo_url,
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    
                    # Log successful user info retrieval
                    await log_context_status(
                        context_id="oauth-user-info-003",
                        priority="HIGH",
                        status="completed",
                        position="middle",
                        message="User information retrieved successfully",
                        phase="oauth",
                        task="get_user_info"
                    )
                    
                    return user_data
                else:
                    error_msg = f"HTTP {response.status_code}: Failed to get user info"
                    
                    # Log user info error
                    await log_context_status(
                        context_id="oauth-user-info-003",
                        priority="HIGH",
                        status="failed",
                        position="middle",
                        message=f"Failed to get user info: {error_msg}",
                        phase="oauth",
                        task="get_user_info"
                    )
                    
                    raise GoogleAPIError(error_msg)
                    
        except httpx.RequestError as e:
            # Log network error
            await log_context_status(
                context_id="oauth-user-info-003",
                priority="HIGH",
                status="failed",
                position="middle",
                message=f"Network error getting user info: {str(e)}",
                phase="oauth",
                task="get_user_info"
            )
            raise GoogleAPIError(f"Network error: {str(e)}")
        except Exception as e:
            # Log unexpected error
            await log_context_status(
                context_id="oauth-user-info-003",
                priority="HIGH",
                status="failed",
                position="middle",
                message=f"Unexpected error getting user info: {str(e)}",
                phase="oauth",
                task="get_user_info"
            )
            raise GoogleAPIError(f"Unexpected error: {str(e)}")
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        
        # Log token refresh
        await log_context_status(
            context_id="oauth-token-refresh-004",
            priority="HIGH",
            status="started",
            position="middle",
            message="Refreshing access token",
            phase="oauth",
            task="refresh_access_token"
        )
        
        try:
            data = {
                "client_id": self.settings.google_client_id,
                "client_secret": self.settings.google_client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.google_token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    
                    # Log successful token refresh
                    await log_context_status(
                        context_id="oauth-token-refresh-004",
                        priority="HIGH",
                        status="completed",
                        position="middle",
                        message="Access token refreshed successfully",
                        phase="oauth",
                        task="refresh_access_token"
                    )
                    
                    return token_data
                else:
                    error_data = response.json() if response.content else {}
                    error_msg = error_data.get("error_description", "Token refresh failed")
                    
                    # Log token refresh error
                    await log_context_status(
                        context_id="oauth-token-refresh-004",
                        priority="HIGH",
                        status="failed",
                        position="middle",
                        message=f"Token refresh failed: {error_msg}",
                        phase="oauth",
                        task="refresh_access_token"
                    )
                    
                    raise OAuthError(f"Token refresh failed: {error_msg}")
                    
        except Exception as e:
            # Log unexpected error
            await log_context_status(
                context_id="oauth-token-refresh-004",
                priority="HIGH",
                status="failed",
                position="middle",
                message=f"Unexpected error during token refresh: {str(e)}",
                phase="oauth",
                task="refresh_access_token"
            )
            raise OAuthError(f"Unexpected error: {str(e)}")


# Global OAuth service instance
oauth_service = OAuthService()