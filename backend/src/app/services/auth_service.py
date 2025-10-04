"""
JWT Authentication service for ClassSphere

CRITICAL OBJECTIVES:
- Implement JWT token generation and validation
- Implement refresh token rotation
- Handle token expiration and renewal
- Secure token storage and validation

DEPENDENCIES:
- python-jose[cryptography]
- passlib[bcrypt]
- datetime
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging

from src.app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """JWT Authentication service with refresh token rotation"""
    
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_days = settings.refresh_token_expire_days
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        try:
            return pwd_context.hash(password)
        except Exception as e:
            logger.error(f"Password hashing error: {e}")
            raise ValueError("Password hashing failed")
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        try:
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
            to_encode.update({"exp": expire, "type": "access"})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Access token created for user: {data.get('sub', 'unknown')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Access token creation error: {e}")
            raise ValueError("Token creation failed")
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        try:
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
            to_encode.update({"exp": expire, "type": "refresh"})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            logger.info(f"Refresh token created for user: {data.get('sub', 'unknown')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Refresh token creation error: {e}")
            raise ValueError("Refresh token creation failed")
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Verify token type
            if payload.get("type") != token_type:
                logger.warning(f"Invalid token type: expected {token_type}, got {payload.get('type')}")
                return None
            
            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
                logger.warning("Token has expired")
                return None
            
            return payload
        except JWTError as e:
            logger.warning(f"JWT verification error: {e}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """Refresh access token using refresh token"""
        try:
            # Verify refresh token
            payload = self.verify_token(refresh_token, "refresh")
            if not payload:
                return None
            
            # Create new access token
            user_data = {
                "sub": payload.get("sub"),
                "role": payload.get("role"),
                "email": payload.get("email")
            }
            
            new_access_token = self.create_access_token(user_data)
            
            # Optionally create new refresh token (rotation)
            new_refresh_token = self.create_refresh_token(user_data)
            
            logger.info(f"Tokens refreshed for user: {user_data.get('sub')}")
            
            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return None
    
    def create_token_pair(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """Create both access and refresh tokens"""
        try:
            access_token = self.create_access_token(user_data)
            refresh_token = self.create_refresh_token(user_data)
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": self.access_token_expire_minutes * 60
            }
        except Exception as e:
            logger.error(f"Token pair creation error: {e}")
            raise ValueError("Token pair creation failed")
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode token without verification (for debugging)"""
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_signature": False})
        except Exception as e:
            logger.error(f"Token decode error: {e}")
            return None