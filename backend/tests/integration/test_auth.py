"""
Tests de integración para autenticación
Prevención Pattern 4: Mock paths correctos para verify_token
"""
import pytest
from unittest.mock import patch, AsyncMock


def test_login_success(client):
    """Test login exitoso"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "admin@classsphere.edu"


def test_login_invalid_credentials(client):
    """Test login con credenciales inválidas"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "wrong"
        }
    )
    
    assert response.status_code == 401


def test_get_current_user(client):
    """Test obtener usuario actual"""
    # Login primero
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Obtener usuario
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@classsphere.edu"
    assert data["role"] == "admin"
