"""
Security module for Dashboard Educativo Backend
Handles JWT tokens, password hashing, and security utilities
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt

from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    Implements secure token generation with proper expiration.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token.
    Implements secure refresh token generation.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT token.
    Returns payload if valid, None if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check token type
        if payload.get("type") not in ["access", "refresh"]:
            return None
        
        # Check expiration
        if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
            return None
        
        return payload
        
    except JWTError:
        return None


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT access token specifically.
    Returns payload if valid access token, None otherwise.
    """
    payload = verify_token(token)
    
    if payload and payload.get("type") == "access":
        return payload
    
    return None


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT refresh token specifically.
    Returns payload if valid refresh token, None otherwise.
    """
    payload = verify_token(token)
    
    if payload and payload.get("type") == "refresh":
        return payload
    
    return None


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    Implements secure password hashing.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    Implements secure password verification.
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_random_string(length: int = 32) -> str:
    """
    Generate cryptographically secure random string.
    Used for tokens, secrets, etc.
    """
    return secrets.token_urlsafe(length)


def generate_csrf_token() -> str:
    """
    Generate CSRF token.
    Implements secure CSRF token generation.
    """
    return generate_random_string(32)


def validate_csrf_token(token: str, expected_token: str) -> bool:
    """
    Validate CSRF token.
    Implements secure CSRF token validation.
    """
    return secrets.compare_digest(token, expected_token)


def get_password_strength(password: str) -> Dict[str, Any]:
    """
    Analyze password strength.
    Returns strength analysis and recommendations.
    """
    strength_score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        strength_score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Character variety checks
    if any(c.islower() for c in password):
        strength_score += 1
    else:
        feedback.append("Password should contain lowercase letters")
    
    if any(c.isupper() for c in password):
        strength_score += 1
    else:
        feedback.append("Password should contain uppercase letters")
    
    if any(c.isdigit() for c in password):
        strength_score += 1
    else:
        feedback.append("Password should contain numbers")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        strength_score += 1
    else:
        feedback.append("Password should contain special characters")
    
    # Determine strength level
    if strength_score <= 2:
        strength_level = "weak"
    elif strength_score <= 4:
        strength_level = "medium"
    else:
        strength_level = "strong"
    
    return {
        "score": strength_score,
        "level": strength_level,
        "feedback": feedback,
        "is_strong": strength_score >= 4
    }


def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input.
    Removes potentially dangerous characters.
    """
    if not isinstance(input_string, str):
        return str(input_string)
    
    # Remove null bytes and control characters
    sanitized = input_string.replace('\x00', '')
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\t\n\r')
    
    # Limit length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    return sanitized.strip()


def validate_email(email: str) -> bool:
    """
    Validate email format.
    Implements basic email validation.
    """
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_policy(password: str) -> Dict[str, Any]:
    """
    Validate password against security policy.
    Returns validation result and feedback.
    """
    min_length = 8
    max_length = 128
    
    errors = []
    warnings = []
    
    # Length validation
    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long")
    elif len(password) > max_length:
        errors.append(f"Password must be no more than {max_length} characters long")
    
    # Character requirements
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        warnings.append("Consider adding special characters for better security")
    
    # Common password check
    common_passwords = [
        "password", "123456", "123456789", "qwerty", "abc123",
        "password123", "admin", "letmein", "welcome", "monkey"
    ]
    
    if password.lower() in common_passwords:
        errors.append("Password is too common, please choose a more unique password")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "strength": get_password_strength(password)
    }