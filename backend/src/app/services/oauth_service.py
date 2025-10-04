"""
OAuth 2.0 service for Google integration

CRITICAL OBJECTIVES:
- Implement Google OAuth 2.0 with PKCE
- State validation for security
- User profile fetching from Google
- Integration with JWT authentication

DEPENDENCIES:
- httpx for HTTP requests
- secrets for PKCE code generation
- base64 for encoding
- hashlib for code challenge
"""

import secrets
import base64
import hashlib
import urllib.parse
from typing import Optional, Dict, Any, Tuple
import httpx
import logging

from src.app.core.config import get_settings
from src.app.services.auth_service import AuthService

logger = logging.getLogger(__name__)
settings = get_settings()

class OAuthService:
    """Google OAuth 2.0 service with PKCE"""
    
    def __init__(self):
        self.auth_service = AuthService()
        self.google_client_id = settings.google_client_id
        self.google_client_secret = settings.google_client_secret
        self.google_redirect_uri = settings.google_redirect_uri
        self.google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.google_token_url = "https://oauth2.googleapis.com/token"
        self.google_user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        
        # Store state and code verifier for PKCE
        self._state_store: Dict[str, str] = {}
    
    def generate_pkce_pair(self) -> Tuple[str, str]:
        """Generate PKCE code verifier and challenge"""
        try:
            # Generate code verifier (43-128 characters)
            code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
            
            # Generate code challenge (SHA256 hash of verifier)
            code_challenge = base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode('utf-8')).digest()
            ).decode('utf-8').rstrip('=')
            
            logger.info("PKCE pair generated successfully")
            return code_verifier, code_challenge
            
        except Exception as e:
            logger.error(f"PKCE generation error: {e}")
            raise ValueError("Failed to generate PKCE pair")
    
    def generate_state(self) -> str:
        """Generate secure state parameter"""
        try:
            state = secrets.token_urlsafe(32)
            logger.info(f"State generated: {state[:8]}...")
            return state
        except Exception as e:
            logger.error(f"State generation error: {e}")
            raise ValueError("Failed to generate state")
    
    def store_state_data(self, state: str, code_verifier: str) -> None:
        """Store state and code verifier for validation"""
        try:
            self._state_store[state] = code_verifier
            logger.info(f"State data stored for: {state[:8]}...")
        except Exception as e:
            logger.error(f"State storage error: {e}")
            raise ValueError("Failed to store state data")
    
    def validate_state(self, state: str) -> Optional[str]:
        """Validate state and return code verifier"""
        try:
            code_verifier = self._state_store.pop(state, None)
            if code_verifier:
                logger.info(f"State validated for: {state[:8]}...")
                return code_verifier
            else:
                logger.warning(f"Invalid state: {state[:8]}...")
                return None
        except Exception as e:
            logger.error(f"State validation error: {e}")
            return None
    
    def get_authorization_url(self) -> Dict[str, str]:
        """Get Google OAuth authorization URL with PKCE"""
        try:
            # Generate PKCE pair
            code_verifier, code_challenge = self.generate_pkce_pair()
            
            # Generate state
            state = self.generate_state()
            
            # Store state data
            self.store_state_data(state, code_verifier)
            
            # Build authorization URL
            params = {
                "client_id": self.google_client_id,
                "redirect_uri": self.google_redirect_uri,
                "response_type": "code",
                "scope": "openid email profile",
                "state": state,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
                "access_type": "offline",
                "prompt": "consent"
            }
            
            auth_url = f"{self.google_auth_url}?{urllib.parse.urlencode(params)}"
            
            logger.info(f"Authorization URL generated for state: {state[:8]}...")
            
            return {
                "authorization_url": auth_url,
                "state": state,
                "code_verifier": code_verifier
            }
            
        except Exception as e:
            logger.error(f"Authorization URL generation error: {e}")
            raise ValueError("Failed to generate authorization URL")
    
    async def exchange_code_for_tokens(self, code: str, state: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for access and refresh tokens"""
        try:
            # Validate state
            code_verifier = self.validate_state(state)
            if not code_verifier:
                logger.warning("Invalid state parameter")
                return None
            
            # Prepare token request
            token_data = {
                "client_id": self.google_client_id,
                "client_secret": self.google_client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.google_redirect_uri,
                "code_verifier": code_verifier
            }
            
            # Make token request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.google_token_url,
                    data=token_data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if response.status_code != 200:
                    logger.error(f"Token exchange failed: {response.status_code} - {response.text}")
                    return None
                
                token_response = response.json()
                logger.info("Tokens exchanged successfully")
                
                return token_response
                
        except Exception as e:
            logger.error(f"Token exchange error: {e}")
            return None
    
    async def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get user information from Google"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.google_user_info_url,
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                if response.status_code != 200:
                    logger.error(f"User info request failed: {response.status_code} - {response.text}")
                    return None
                
                user_info = response.json()
                logger.info(f"User info retrieved for: {user_info.get('email', 'unknown')}")
                
                return user_info
                
        except Exception as e:
            logger.error(f"User info retrieval error: {e}")
            return None
    
    async def create_or_update_user(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update user from Google profile"""
        try:
            # Extract user data from Google profile
            google_id = user_info.get("id")
            email = user_info.get("email")
            name = user_info.get("name")
            picture = user_info.get("picture")
            verified_email = user_info.get("verified_email", False)
            
            if not google_id or not email:
                raise ValueError("Invalid user data from Google")
            
            # Create user data for JWT
            user_data = {
                "sub": f"google_{google_id}",
                "email": email,
                "name": name,
                "picture": picture,
                "role": "student",  # Default role for new users
                "provider": "google",
                "verified": verified_email
            }
            
            # Generate JWT tokens
            tokens = self.auth_service.create_token_pair(user_data)
            
            logger.info(f"User created/updated: {email}")
            
            return {
                "user": user_data,
                "tokens": tokens
            }
            
        except Exception as e:
            logger.error(f"User creation/update error: {e}")
            raise ValueError("Failed to create or update user")
    
    async def handle_oauth_callback(self, code: str, state: str) -> Optional[Dict[str, Any]]:
        """Handle complete OAuth callback flow"""
        try:
            # Exchange code for tokens
            token_response = await self.exchange_code_for_tokens(code, state)
            if not token_response:
                return None
            
            # Get user info
            access_token = token_response.get("access_token")
            if not access_token:
                logger.error("No access token in response")
                return None
            
            user_info = await self.get_user_info(access_token)
            if not user_info:
                return None
            
            # Create or update user
            result = await self.create_or_update_user(user_info)
            
            # Add Google tokens to result
            result["google_tokens"] = {
                "access_token": access_token,
                "refresh_token": token_response.get("refresh_token"),
                "expires_in": token_response.get("expires_in"),
                "token_type": token_response.get("token_type")
            }
            
            logger.info("OAuth callback handled successfully")
            return result
            
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            return None