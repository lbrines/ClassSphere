"""
Security utilities for authentication and authorization.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Union
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityError(Exception):
    """Base exception for security-related errors."""
    pass


class AuthenticationError(SecurityError):
    """Exception raised for authentication failures."""
    pass


async def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token with timeout protection.

    Args:
        data: Data to encode in token
        expires_delta: Optional expiration time

    Returns:
        JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})

    # Create token with timeout protection
    try:
        encoded_jwt = await asyncio.wait_for(
            asyncio.create_task(_encode_jwt(to_encode)),
            timeout=2.0
        )
        return encoded_jwt
    except asyncio.TimeoutError:
        raise SecurityError("Token creation timeout")


async def _encode_jwt(data: dict) -> str:
    """Internal JWT encoding with async support."""
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


async def verify_token(token: str) -> dict:
    """
    Verify JWT token with timeout protection.

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload

    Raises:
        AuthenticationError: If token is invalid
    """
    try:
        payload = await asyncio.wait_for(
            asyncio.create_task(_decode_jwt(token)),
            timeout=2.0
        )
        return payload
    except asyncio.TimeoutError:
        raise AuthenticationError("Token verification timeout")
    except JWTError:
        raise AuthenticationError("Invalid token")


async def _decode_jwt(token: str) -> dict:
    """Internal JWT decoding with async support."""
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)