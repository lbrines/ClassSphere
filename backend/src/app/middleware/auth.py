"""
Middleware de autenticación y autorización
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.auth import User, UserRole, TokenData
from app.services.auth_service import AuthService
from app.utils.auth import verify_token, check_role_permission


# Security scheme
security = HTTPBearer()

# Singleton del servicio de autenticación
auth_service = AuthService()


def get_auth_service() -> AuthService:
    """Dependency para obtener el servicio de autenticación"""
    return auth_service


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Obtener usuario actual desde token JWT"""
    token_data = verify_token(credentials.credentials)

    user = auth_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario activo actual"""
    return current_user


def require_role(required_role: UserRole):
    """Decorator para requerir un rol específico"""

    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if not check_role_permission(current_user.role, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_role.value} role or higher"
            )
        return current_user

    return role_checker


# Shortcuts para roles específicos
RequireAdmin = Depends(require_role(UserRole.ADMIN))
RequireCoordinator = Depends(require_role(UserRole.COORDINATOR))
RequireTeacher = Depends(require_role(UserRole.TEACHER))
RequireStudent = Depends(require_role(UserRole.STUDENT))


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[User]:
    """Obtener usuario opcional (para endpoints públicos con funcionalidad adicional para usuarios logueados)"""
    if not credentials:
        return None

    try:
        token_data = verify_token(credentials.credentials)
        user = auth_service.get_user_by_id(token_data.user_id)

        if user and user.is_active:
            return user
    except HTTPException:
        pass

    return None