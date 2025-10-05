"""
Endpoints de autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.auth import (
    UserLogin, UserCreate, AuthResponse, Token, User
)
from app.services.auth_service import AuthService
from app.middleware.auth import (
    get_auth_service, get_current_active_user, RequireAdmin
)


router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/login", response_model=AuthResponse)
async def login(
    user_login: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Login de usuario con email y contraseña"""
    try:
        auth_response = auth_service.login(user_login)
        return auth_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/register", response_model=User, dependencies=[RequireAdmin])
async def register(
    user_create: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Registrar nuevo usuario (solo admin)"""
    try:
        user = auth_service.create_user(user_create)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Renovar token de acceso"""
    try:
        token = auth_service.refresh_token(refresh_token)
        return token
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.get("/me", response_model=User)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Obtener perfil del usuario actual"""
    return current_user


@router.post("/logout")
async def logout():
    """Logout de usuario (invalidación del lado del cliente)"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Successfully logged out"}
    )


@router.get("/users", response_model=list[User], dependencies=[RequireAdmin])
async def get_all_users(
    auth_service: AuthService = Depends(get_auth_service)
):
    """Obtener todos los usuarios (solo admin)"""
    try:
        users = auth_service.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        )