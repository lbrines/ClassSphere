"""
Tests de integración para endpoints de administración
"""
import pytest
from unittest.mock import patch


def test_get_all_users_as_admin(client):
    """Test obtener todos los usuarios como admin"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Obtener usuarios
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # admin y teacher


def test_get_all_users_as_teacher_denied(client):
    """Test obtener usuarios como teacher (denegado)"""
    # Login como teacher
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "teacher@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Intentar obtener usuarios
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    data = response.json()
    assert "Access denied" in data["detail"]


def test_get_user_by_id_as_admin(client):
    """Test obtener usuario por ID como admin"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Obtener usuario específico
    response = client.get(
        "/api/v1/admin/users/user-001",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "user-001"
    assert data["email"] == "admin@classsphere.edu"
    assert data["role"] == "admin"


def test_get_user_by_id_not_found(client):
    """Test obtener usuario inexistente"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Intentar obtener usuario inexistente
    response = client.get(
        "/api/v1/admin/users/nonexistent-id",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "User not found" in data["detail"]


def test_create_user_as_admin(client):
    """Test crear usuario como admin"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Crear nuevo usuario
    response = client.post(
        "/api/v1/admin/users",
        json={
            "email": "newuser@classsphere.edu",
            "name": "New User",
            "role": "teacher",
            "password": "secret123"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@classsphere.edu"
    assert data["name"] == "New User"
    assert data["role"] == "teacher"
    assert data["is_active"] is True


def test_update_user_as_admin(client):
    """Test actualizar usuario como admin"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Actualizar usuario
    response = client.put(
        "/api/v1/admin/users/user-002",
        json={
            "name": "Updated Teacher",
            "role": "coordinator",
            "is_active": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "user-002"
    assert data["name"] == "Updated Teacher"
    assert data["role"] == "coordinator"
    assert data["is_active"] is False


def test_delete_user_as_admin(client):
    """Test eliminar usuario como admin"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Eliminar usuario
    response = client.delete(
        "/api/v1/admin/users/user-002",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data["message"]


def test_get_system_status_as_admin(client):
    """Test obtener estado del sistema como admin"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Obtener estado del sistema
    response = client.get(
        "/api/v1/admin/system/status",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "users_count" in data
    assert "active_users" in data
    assert "roles_distribution" in data
    assert data["status"] == "healthy"


def test_get_analytics_overview_as_admin(client):
    """Test obtener analytics como admin"""
    # Login como admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin@classsphere.edu",
            "password": "secret"
        }
    )
    token = login_response.json()["access_token"]
    
    # Obtener analytics
    response = client.get(
        "/api/v1/admin/analytics/overview",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "active_users" in data
    assert "users_by_role" in data
    assert "recent_activity" in data


def test_admin_endpoints_without_token(client):
    """Test endpoints de admin sin token"""
    response = client.get("/api/v1/admin/users")
    assert response.status_code == 401


def test_admin_endpoints_with_invalid_token(client):
    """Test endpoints de admin con token inválido"""
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
