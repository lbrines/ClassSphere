"""
Authentication service for JWT token management.
"""
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext

from src.app.core.config import settings
from src.app.exceptions.auth import TokenExpiredError, TokenInvalidError, AuthenticationError


class AuthService:
    """Service for JWT authentication."""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        # Ensure 'sub' field is present (JWT standard)
        if "sub" not in to_encode:
            to_encode["sub"] = str(data.get("id", data.get("email", "unknown")))
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        # Ensure 'sub' field is present (JWT standard)
        if "sub" not in to_encode:
            to_encode["sub"] = str(data.get("id", data.get("email", "unknown")))
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Verify token type
            token_type = payload.get("type")
            if token_type not in ["access", "refresh"]:
                raise TokenInvalidError("Invalid token type")
            
            # Verify 'sub' field is present
            if "sub" not in payload:
                raise TokenInvalidError("Missing 'sub' field in token")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError:
            raise TokenInvalidError("Invalid token")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_user_permissions_by_role(self, role: str) -> list[str]:
        """Get user permissions based on role."""
        permissions_map = {
            "student": [
                "read:own_courses",
                "read:own_assignments",
                "read:own_grades",
                "read:own_profile"
            ],
            "teacher": [
                "read:own_courses",
                "write:own_courses",
                "read:own_students",
                "write:own_assignments",
                "write:own_grades",
                "read:own_profile",
                "write:own_profile"
            ],
            "admin": [
                "read:all_users",
                "write:all_users",
                "read:all_courses",
                "write:all_courses",
                "read:all_assignments",
                "write:all_assignments",
                "read:all_grades",
                "write:all_grades",
                "read:system_settings",
                "write:system_settings",
                "read:own_profile",
                "write:own_profile"
            ]
        }
        
        return permissions_map.get(role, [])


# Global instance
auth_service = AuthService()