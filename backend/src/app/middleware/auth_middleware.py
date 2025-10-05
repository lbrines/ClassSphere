"""
Middleware de autenticación y autorización
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from app.core.security import decode_token
from app.services.auth_service import AuthService
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Obtener usuario actual desde token JWT"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    auth_service = AuthService()
    user = await auth_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario activo actual"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_roles(allowed_roles: List[UserRole]):
    """Decorator para requerir roles específicos"""
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_user
    return role_checker


# Dependencias predefinidas para roles específicos
require_admin = require_roles([UserRole.ADMIN])
require_coordinator = require_roles([UserRole.ADMIN, UserRole.COORDINATOR])
require_teacher = require_roles([UserRole.ADMIN, UserRole.COORDINATOR, UserRole.TEACHER])
require_student = require_roles([UserRole.ADMIN, UserRole.COORDINATOR, UserRole.TEACHER, UserRole.STUDENT])


def require_permission(permission: str):
    """Decorator para requerir permisos específicos"""
    def permission_checker(current_user: User = Depends(get_current_active_user)) -> User:
        # Mapeo de permisos por rol
        role_permissions = {
            UserRole.ADMIN: [
                "read:all", "write:all", "delete:all", "manage:users", 
                "manage:system", "view:analytics", "manage:classes"
            ],
            UserRole.COORDINATOR: [
                "read:all", "write:classes", "manage:teachers", 
                "view:analytics", "manage:classes"
            ],
            UserRole.TEACHER: [
                "read:own_classes", "write:own_classes", "manage:students",
                "view:own_analytics"
            ],
            UserRole.STUDENT: [
                "read:own_data", "write:own_data"
            ]
        }
        
        user_permissions = role_permissions.get(current_user.role, [])
        
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required permission: {permission}"
            )
        
        return current_user
    return permission_checker


# Dependencias predefinidas para permisos específicos
require_read_all = require_permission("read:all")
require_write_all = require_permission("write:all")
require_manage_users = require_permission("manage:users")
require_manage_system = require_permission("manage:system")
require_view_analytics = require_permission("view:analytics")
require_manage_classes = require_permission("manage:classes")
