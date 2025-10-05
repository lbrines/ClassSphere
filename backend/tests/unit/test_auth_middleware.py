"""
Tests para middleware de autenticación
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, status
from app.middleware.auth_middleware import (
    get_current_user,
    get_current_active_user,
    require_roles,
    require_permission,
    require_admin,
    require_coordinator,
    require_teacher,
    require_student
)
from app.models.user import User, UserRole


class TestAuthMiddleware:
    """Tests para middleware de autenticación"""
    
    @patch('app.middleware.auth_middleware.decode_token')
    @patch('app.middleware.auth_middleware.AuthService')
    async def test_get_current_user_success(self, mock_auth_service, mock_decode_token):
        """Test obtención exitosa de usuario actual"""
        # Mock token payload
        mock_decode_token.return_value = {"sub": "test@example.com"}
        
        # Mock user
        mock_user = User(
            id="user-001",
            email="test@example.com",
            name="Test User",
            role=UserRole.TEACHER,
            is_active=True
        )
        
        # Mock auth service
        from unittest.mock import AsyncMock
        mock_auth_instance = Mock()
        mock_auth_instance.get_user_by_email = AsyncMock(return_value=mock_user)
        mock_auth_service.return_value = mock_auth_instance
        
        # Test
        result = await get_current_user("valid-token")
        
        assert result == mock_user
        mock_decode_token.assert_called_once_with("valid-token")
        mock_auth_instance.get_user_by_email.assert_called_once_with("test@example.com")
    
    @patch('app.middleware.auth_middleware.decode_token')
    async def test_get_current_user_invalid_token(self, mock_decode_token):
        """Test token inválido"""
        mock_decode_token.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("invalid-token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in exc_info.value.detail
    
    @patch('app.middleware.auth_middleware.decode_token')
    async def test_get_current_user_missing_sub(self, mock_decode_token):
        """Test token sin sub"""
        mock_decode_token.return_value = {"other": "value"}
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("token-without-sub")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token payload" in exc_info.value.detail
    
    @patch('app.middleware.auth_middleware.decode_token')
    @patch('app.middleware.auth_middleware.AuthService')
    async def test_get_current_user_not_found(self, mock_auth_service, mock_decode_token):
        """Test usuario no encontrado"""
        mock_decode_token.return_value = {"sub": "nonexistent@example.com"}
        
        from unittest.mock import AsyncMock
        mock_auth_instance = Mock()
        mock_auth_instance.get_user_by_email = AsyncMock(return_value=None)
        mock_auth_service.return_value = mock_auth_instance
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user("valid-token")
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "User not found" in exc_info.value.detail
    
    async def test_get_current_active_user_success(self):
        """Test usuario activo exitoso"""
        active_user = User(
            id="user-001",
            email="test@example.com",
            name="Test User",
            role=UserRole.TEACHER,
            is_active=True
        )
        
        result = await get_current_active_user(active_user)
        assert result == active_user
    
    async def test_get_current_active_user_inactive(self):
        """Test usuario inactivo"""
        inactive_user = User(
            id="user-001",
            email="test@example.com",
            name="Test User",
            role=UserRole.TEACHER,
            is_active=False
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_active_user(inactive_user)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Inactive user" in exc_info.value.detail
    
    def test_require_roles_success(self):
        """Test requerimiento de roles exitoso"""
        user = User(
            id="user-001",
            email="admin@example.com",
            name="Admin User",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        role_checker = require_roles([UserRole.ADMIN, UserRole.COORDINATOR])
        result = role_checker(user)
        
        assert result == user
    
    def test_require_roles_failure(self):
        """Test requerimiento de roles fallido"""
        user = User(
            id="user-001",
            email="student@example.com",
            name="Student User",
            role=UserRole.STUDENT,
            is_active=True
        )
        
        role_checker = require_roles([UserRole.ADMIN, UserRole.COORDINATOR])
        
        with pytest.raises(HTTPException) as exc_info:
            role_checker(user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Access denied" in exc_info.value.detail
        assert "admin" in exc_info.value.detail
        assert "coordinator" in exc_info.value.detail
    
    def test_require_permission_success(self):
        """Test requerimiento de permisos exitoso"""
        user = User(
            id="user-001",
            email="admin@example.com",
            name="Admin User",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        permission_checker = require_permission("read:all")
        result = permission_checker(user)
        
        assert result == user
    
    def test_require_permission_failure(self):
        """Test requerimiento de permisos fallido"""
        user = User(
            id="user-001",
            email="student@example.com",
            name="Student User",
            role=UserRole.STUDENT,
            is_active=True
        )
        
        permission_checker = require_permission("manage:users")
        
        with pytest.raises(HTTPException) as exc_info:
            permission_checker(user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Access denied" in exc_info.value.detail
        assert "manage:users" in exc_info.value.detail
    
    def test_require_admin_success(self):
        """Test requerimiento de admin exitoso"""
        user = User(
            id="user-001",
            email="admin@example.com",
            name="Admin User",
            role=UserRole.ADMIN,
            is_active=True
        )
        
        result = require_admin(user)
        assert result == user
    
    def test_require_admin_failure(self):
        """Test requerimiento de admin fallido"""
        user = User(
            id="user-001",
            email="teacher@example.com",
            name="Teacher User",
            role=UserRole.TEACHER,
            is_active=True
        )
        
        with pytest.raises(HTTPException) as exc_info:
            require_admin(user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    
    def test_require_coordinator_success(self):
        """Test requerimiento de coordinator exitoso"""
        user = User(
            id="user-001",
            email="coordinator@example.com",
            name="Coordinator User",
            role=UserRole.COORDINATOR,
            is_active=True
        )
        
        result = require_coordinator(user)
        assert result == user
    
    def test_require_teacher_success(self):
        """Test requerimiento de teacher exitoso"""
        user = User(
            id="user-001",
            email="teacher@example.com",
            name="Teacher User",
            role=UserRole.TEACHER,
            is_active=True
        )
        
        result = require_teacher(user)
        assert result == user
    
    def test_require_student_success(self):
        """Test requerimiento de student exitoso"""
        user = User(
            id="user-001",
            email="student@example.com",
            name="Student User",
            role=UserRole.STUDENT,
            is_active=True
        )
        
        result = require_student(user)
        assert result == user
