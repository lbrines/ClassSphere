"""
Dual authentication service for switching between JWT/Mock and OAuth/Google modes.
"""
from typing import Optional, Dict, Any, Literal
from enum import Enum

from src.app.core.config import settings
from src.app.services.auth_service import auth_service
from src.app.services.oauth_service import oauth_service
from src.app.exceptions.auth import AuthenticationError


class AuthMode(Enum):
    """Authentication modes."""
    JWT_MOCK = "jwt_mock"
    OAUTH_GOOGLE = "oauth_google"


class DualAuthService:
    """Service for dual authentication mode switching."""
    
    def __init__(self):
        self.current_mode = AuthMode.JWT_MOCK  # Default mode
        self.auth_service = auth_service
        self.oauth_service = oauth_service
    
    def get_current_mode(self) -> AuthMode:
        """Get current authentication mode."""
        return self.current_mode
    
    def set_mode(self, mode: AuthMode) -> None:
        """Set authentication mode."""
        self.current_mode = mode
    
    def switch_to_jwt_mock(self) -> None:
        """Switch to JWT/Mock mode."""
        self.current_mode = AuthMode.JWT_MOCK
    
    def switch_to_oauth_google(self) -> None:
        """Switch to OAuth/Google mode."""
        self.current_mode = AuthMode.OAUTH_GOOGLE
    
    def is_jwt_mock_mode(self) -> bool:
        """Check if currently in JWT/Mock mode."""
        return self.current_mode == AuthMode.JWT_MOCK
    
    def is_oauth_google_mode(self) -> bool:
        """Check if currently in OAuth/Google mode."""
        return self.current_mode == AuthMode.OAUTH_GOOGLE
    
    async def authenticate_user(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate user based on current mode."""
        if self.is_jwt_mock_mode():
            return await self._authenticate_jwt_mock(credentials)
        elif self.is_oauth_google_mode():
            return await self._authenticate_oauth_google(credentials)
        else:
            raise AuthenticationError("Invalid authentication mode")
    
    async def _authenticate_jwt_mock(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate using JWT/Mock mode."""
        # Mock authentication for development
        email = credentials.get("email")
        password = credentials.get("password")
        
        if not email or not password:
            raise AuthenticationError("Email and password required for JWT/Mock mode")
        
        # Mock user validation (in real implementation, check against database)
        if email == "admin@example.com" and password == "admin123":
            user_data = {
                "id": "mock_admin_1",
                "email": email,
                "role": "admin",
                "name": "Mock Admin"
            }
        elif email == "teacher@example.com" and password == "teacher123":
            user_data = {
                "id": "mock_teacher_1",
                "email": email,
                "role": "teacher",
                "name": "Mock Teacher"
            }
        elif email == "student@example.com" and password == "student123":
            user_data = {
                "id": "mock_student_1",
                "email": email,
                "role": "student",
                "name": "Mock Student"
            }
        else:
            raise AuthenticationError("Invalid credentials for JWT/Mock mode")
        
        # Create JWT tokens
        access_token = self.auth_service.create_access_token(user_data)
        refresh_token = self.auth_service.create_refresh_token(user_data)
        
        return {
            "user": user_data,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "mode": "jwt_mock"
        }
    
    async def _authenticate_oauth_google(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate using OAuth/Google mode."""
        auth_code = credentials.get("code")
        
        if not auth_code:
            raise AuthenticationError("Authorization code required for OAuth/Google mode")
        
        # Exchange code for token
        token_response = await self.oauth_service.exchange_code_for_token(auth_code)
        
        # Get user info
        user_info = await self.oauth_service.get_user_info(token_response["access_token"])
        
        # Map Google user info to our user format
        user_data = {
            "id": user_info["id"],
            "email": user_info["email"],
            "name": user_info.get("name", user_info["email"]),
            "role": "student",  # Default role, can be updated based on domain or other logic
            "google_id": user_info["id"],
            "picture": user_info.get("picture")
        }
        
        # Create our own JWT tokens for consistency
        access_token = self.auth_service.create_access_token(user_data)
        refresh_token = self.auth_service.create_refresh_token(user_data)
        
        return {
            "user": user_data,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "mode": "oauth_google",
            "google_tokens": token_response
        }
    
    def get_auth_url(self, mode: Optional[AuthMode] = None) -> str:
        """Get authentication URL for the specified mode."""
        target_mode = mode or self.current_mode
        
        if target_mode == AuthMode.OAUTH_GOOGLE:
            return self.oauth_service.google_oauth_flow()
        else:
            # For JWT/Mock mode, return a mock URL or handle differently
            return "/auth/mock"
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify token regardless of mode."""
        return self.auth_service.verify_token(token)


# Global instance
dual_auth_service = DualAuthService()