"""Authentication service for JWT and user management."""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import secrets

from ..core.security import SecurityService
from ..core.exceptions import AuthenticationError, TokenExpiredError
from ..models.user import UserInDB, UserRole, UserStatus
from ..core.config import settings


class AuthService:
    """Authentication service for JWT operations."""

    def __init__(self):
        self.security = SecurityService()

    async def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT access token with standard payload."""
        payload = {
            "sub": user_data.get("id"),  # Standard JWT subject field
            "email": user_data.get("email"),
            "id": user_data.get("id"),
            "role": user_data.get("role"),
            "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes),
            "iat": datetime.utcnow()
        }
        return self.security.create_access_token(payload)

    async def create_refresh_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT refresh token."""
        payload = {
            "sub": user_data.get("id"),
            "email": user_data.get("email"),
            "id": user_data.get("id"),
            "role": user_data.get("role"),
            "exp": datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days),
            "iat": datetime.utcnow()
        }
        return self.security.create_refresh_token(payload)

    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token and return payload."""
        try:
            payload = self.security.verify_token(token)
            
            # Validate required fields
            if not payload.get("sub"):
                raise AuthenticationError("Token missing subject")
            
            return payload
            
        except TokenExpiredError:
            raise
        except Exception as e:
            raise AuthenticationError(f"Token verification failed: {str(e)}")

    async def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return self.security.hash_password(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return self.security.verify_password(plain_password, hashed_password)

    async def get_user_permissions_by_role(self, role: str) -> list[str]:
        """Get permissions for user role."""
        return self.security.get_user_permissions_by_role(role)

    async def generate_password_reset_token(self) -> str:
        """Generate secure password reset token."""
        return self.security.generate_password_reset_token()

    async def create_user_tokens(self, user: UserInDB) -> Dict[str, str]:
        """Create both access and refresh tokens for user."""
        user_data = {
            "id": user.id,
            "email": user.email,
            "role": user.role.value if isinstance(user.role, UserRole) else user.role
        }
        
        access_token = await self.create_access_token(user_data)
        refresh_token = await self.create_refresh_token(user_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
