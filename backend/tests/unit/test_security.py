"""
Tests para seguridad
Prevención Pattern 4: AsyncMock para funciones async
"""
import pytest
from unittest.mock import AsyncMock
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token
)


def test_password_hashing():
    """Test hash de password"""
    password = "secret123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_create_access_token():
    """Test creación de access token"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)


def test_decode_token():
    """Test decodificación de token"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    payload = decode_token(token)
    
    assert payload is not None
    assert payload["sub"] == "test@example.com"
    assert payload["type"] == "access"
