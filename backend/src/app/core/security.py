"""Security utilities for JWT and password handling."""

import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt

from .config import settings
from .exceptions import AuthenticationError, TokenExpiredError

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityService:
    """Security service for JWT and password operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.refresh_token_expire_days
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            
            # Check token expiration
            exp = payload.get("exp")
            if exp is None:
                raise TokenExpiredError("Token missing expiration")
            
            if datetime.utcnow() > datetime.fromtimestamp(exp):
                raise TokenExpiredError(
                    "Token has expired",
                    expired_at=datetime.fromtimestamp(exp).isoformat()
                )
            
            return payload
            
        except JWTError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")

    @staticmethod
    def generate_password_reset_token() -> str:
        """Generate a secure password reset token."""
        return secrets.token_urlsafe(32)

    @staticmethod
    def get_user_permissions_by_role(role: str) -> list[str]:
        """Get permissions for a user role."""
        role_permissions = {
            "admin": [
                "read:all", "write:all", "delete:all",
                "manage:users", "manage:system", "manage:courses"
            ],
            "coordinator": [
                "read:courses", "write:courses", "read:users",
                "write:students", "read:metrics", "manage:courses"
            ],
            "teacher": [
                "read:own_courses", "write:own_courses", "read:students",
                "write:grades", "read:metrics"
            ],
            "student": [
                "read:own_data", "read:own_courses", "read:own_grades"
            ]
        }
        return role_permissions.get(role, [])


# Convenience functions
def hash_password(password: str) -> str:
    """Hash a password."""
    return SecurityService.hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password."""
    return SecurityService.verify_password(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """Create an access token."""
    return SecurityService.create_access_token(data)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a refresh token."""
    return SecurityService.create_refresh_token(data)


def verify_token(token: str) -> Dict[str, Any]:
    """Verify a token."""
    return SecurityService.verify_token(token)


def get_user_permissions_by_role(role: str) -> list[str]:
    """Get user permissions by role."""
    return SecurityService.get_user_permissions_by_role(role)
