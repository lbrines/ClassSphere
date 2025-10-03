"""
Security utilities for authentication and authorization.
"""
import secrets
import string
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from loguru import logger

from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "sub": data.get("user_id", "unknown")  # Standard JWT subject field
    })
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        logger.info(f"Access token created for user: {data.get('user_id', 'unknown')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        raise


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
        "sub": data.get("user_id", "unknown")
    })
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        logger.info(f"Refresh token created for user: {data.get('user_id', 'unknown')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating refresh token: {e}")
        raise


def verify_token(token: str) -> Dict[str, Any]:
    """Verify JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise JWTError("Token has expired")
        
        logger.info(f"Token verified for user: {payload.get('sub', 'unknown')}")
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {e}")
        raise


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    try:
        hashed = pwd_context.hash(password)
        logger.info("Password hashed successfully")
        return hashed
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    try:
        is_valid = pwd_context.verify(plain_password, hashed_password)
        logger.info(f"Password verification: {'success' if is_valid else 'failed'}")
        return is_valid
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False


def generate_random_string(length: int = 32) -> str:
    """Generate random string for tokens."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_csrf_token() -> str:
    """Generate CSRF token."""
    return generate_random_string(32)


def validate_password_strength(password: str) -> bool:
    """Validate password strength."""
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    return has_upper and has_lower and has_digit and has_special


def validate_email_format(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_user_permissions_by_role(role: str) -> list:
    """Get user permissions based on role."""
    role_permissions = {
        "admin": [
            "read:all", "write:all", "delete:all",
            "manage:users", "manage:courses", "manage:system"
        ],
        "teacher": [
            "read:own_courses", "write:own_courses",
            "manage:own_students", "read:own_analytics"
        ],
        "student": [
            "read:own_courses", "read:own_grades",
            "read:own_assignments"
        ],
        "coordinator": [
            "read:department_courses", "write:department_courses",
            "read:department_analytics", "manage:department_students"
        ]
    }
    
    return role_permissions.get(role, [])


def check_permission(user_permissions: list, required_permission: str) -> bool:
    """Check if user has required permission."""
    return required_permission in user_permissions