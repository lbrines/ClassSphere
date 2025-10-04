"""
Test file for auth_middleware.py

CRITICAL OBJECTIVES:
- Verify JWT middleware functionality
- Test role-based access control
- Test authentication error handling
- Test optional authentication

DEPENDENCIES:
- FastAPI TestClient
- HTTPBearer
- pytest-asyncio
"""

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from fastapi.security import HTTPAuthorizationCredentials

from src.app.middleware.auth_middleware import (
    auth_middleware,
    get_current_user,
    get_current_user_optional,
    require_admin,
    require_coordinator,
    require_teacher,
    require_student
)
from src.app.services.auth_service import AuthService

# Create test app
app = FastAPI()

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

@app.get("/optional")
async def optional_route(current_user: dict = Depends(get_current_user_optional)):
    return {"user": current_user}

@app.get("/admin")
async def admin_route(current_user: dict = Depends(require_admin)):
    return {"user": current_user}

@app.get("/coordinator")
async def coordinator_route(current_user: dict = Depends(require_coordinator)):
    return {"user": current_user}

@app.get("/teacher")
async def teacher_route(current_user: dict = Depends(require_teacher)):
    return {"user": current_user}

@app.get("/student")
async def student_route(current_user: dict = Depends(require_student)):
    return {"user": current_user}

# BEGINNING: Critical tests for core functionality
@pytest.mark.asyncio(timeout=2.0)
async def test_get_current_user_success():
    """Test successful user authentication"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    token = auth_service.create_access_token(user_data)
    
    # Act
    result = await auth_middleware.get_current_user(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    )
    
    # Assert
    assert result["id"] == "user123"
    assert result["role"] == "teacher"
    assert result["email"] == "test@classsphere.com"

@pytest.mark.asyncio(timeout=2.0)
async def test_get_current_user_invalid_token():
    """Test authentication with invalid token"""
    # Arrange
    invalid_token = "invalid.token.here"
    
    # Act & Assert
    with pytest.raises(Exception):  # HTTPException from FastAPI
        await auth_middleware.get_current_user(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_token)
        )

@pytest.mark.asyncio(timeout=2.0)
async def test_get_current_user_optional_with_token():
    """Test optional authentication with valid token"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    token = auth_service.create_access_token(user_data)
    
    # Act
    result = await auth_middleware.get_current_user_optional(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    )
    
    # Assert
    assert result is not None
    assert result["id"] == "user123"
    assert result["role"] == "teacher"

@pytest.mark.asyncio(timeout=2.0)
async def test_get_current_user_optional_without_token():
    """Test optional authentication without token"""
    # Act
    result = await auth_middleware.get_current_user_optional(None)
    
    # Assert
    assert result is None

# MIDDLE: Detailed implementation tests
@pytest.mark.asyncio(timeout=2.0)
async def test_role_verification_admin():
    """Test admin role verification"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "admin123", "role": "admin", "email": "admin@classsphere.com"}
    token = auth_service.create_access_token(user_data)
    current_user = await auth_middleware.get_current_user(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    )
    
    # Act
    result = await auth_middleware.require_role("admin", current_user)
    
    # Assert
    assert result["role"] == "admin"

@pytest.mark.asyncio(timeout=2.0)
async def test_role_verification_insufficient_permissions():
    """Test role verification with insufficient permissions"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "student123", "role": "student", "email": "student@classsphere.com"}
    token = auth_service.create_access_token(user_data)
    current_user = await auth_middleware.get_current_user(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    )
    
    # Act & Assert
    with pytest.raises(Exception):  # HTTPException from FastAPI
        await auth_middleware.require_role("admin", current_user)

@pytest.mark.asyncio(timeout=2.0)
async def test_role_hierarchy():
    """Test role hierarchy (admin > coordinator > teacher > student)"""
    # Arrange
    auth_service = AuthService()
    
    # Test admin can access coordinator route
    admin_data = {"sub": "admin123", "role": "admin", "email": "admin@classsphere.com"}
    admin_token = auth_service.create_access_token(admin_data)
    admin_user = await auth_middleware.get_current_user(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=admin_token)
    )
    
    # Act
    result = await auth_middleware.require_role("coordinator", admin_user)
    
    # Assert
    assert result["role"] == "admin"

@pytest.mark.asyncio(timeout=2.0)
async def test_protected_route_success():
    """Test protected route with valid token"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    token = auth_service.create_access_token(user_data)
    
    # Act
    client = TestClient(app)
    response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["id"] == "user123"
    assert data["user"]["role"] == "teacher"

@pytest.mark.asyncio(timeout=2.0)
async def test_protected_route_no_token():
    """Test protected route without token"""
    # Act
    client = TestClient(app)
    response = client.get("/protected")
    
    # Assert
    assert response.status_code == 401  # Unauthorized - no token provided

@pytest.mark.asyncio(timeout=2.0)
async def test_optional_route_with_token():
    """Test optional route with token"""
    # Arrange
    auth_service = AuthService()
    user_data = {"sub": "user123", "role": "teacher", "email": "test@classsphere.com"}
    token = auth_service.create_access_token(user_data)
    
    # Act
    client = TestClient(app)
    response = client.get("/optional", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["id"] == "user123"

@pytest.mark.asyncio(timeout=2.0)
async def test_optional_route_without_token():
    """Test optional route without token"""
    # Act
    client = TestClient(app)
    response = client.get("/optional")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["user"] is None

# END: Verification and next steps
@pytest.mark.asyncio(timeout=2.0)
async def test_role_specific_routes():
    """Test role-specific routes"""
    # Arrange
    auth_service = AuthService()
    
    # Test admin route
    admin_data = {"sub": "admin123", "role": "admin", "email": "admin@classsphere.com"}
    admin_token = auth_service.create_access_token(admin_data)
    
    client = TestClient(app)
    
    # Act & Assert: Admin can access admin route
    response = client.get("/admin", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
    # Act & Assert: Admin can access coordinator route
    response = client.get("/coordinator", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
    # Act & Assert: Admin can access teacher route
    response = client.get("/teacher", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    
    # Act & Assert: Admin can access student route
    response = client.get("/student", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

@pytest.mark.asyncio(timeout=2.0)
async def test_student_role_restrictions():
    """Test student role restrictions"""
    # Arrange
    auth_service = AuthService()
    student_data = {"sub": "student123", "role": "student", "email": "student@classsphere.com"}
    student_token = auth_service.create_access_token(student_data)
    
    client = TestClient(app)
    
    # Act & Assert: Student can access student route
    response = client.get("/student", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 200
    
    # Act & Assert: Student cannot access teacher route
    response = client.get("/teacher", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403
    
    # Act & Assert: Student cannot access coordinator route
    response = client.get("/coordinator", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403
    
    # Act & Assert: Student cannot access admin route
    response = client.get("/admin", headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403