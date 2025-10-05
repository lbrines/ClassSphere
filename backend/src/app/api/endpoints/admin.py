"""
Endpoints de administración
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel
from app.middleware.auth_middleware import require_admin, require_manage_users, get_current_active_user
from app.models.user import User, UserRole
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


class UserCreateRequest(BaseModel):
    """Request para crear usuario"""
    email: str
    name: str
    role: UserRole
    password: str


class UserUpdateRequest(BaseModel):
    """Request para actualizar usuario"""
    name: str = None
    role: UserRole = None
    is_active: bool = None


class UserResponse(BaseModel):
    """Response de usuario"""
    id: str
    email: str
    name: str
    role: UserRole
    is_active: bool


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(require_admin)
):
    """Obtener todos los usuarios (solo admin)"""
    # En un entorno real, esto vendría de la base de datos
    # Por ahora, retornamos los usuarios mock
    from app.services.auth_service import MOCK_USERS
    
    users = []
    for user_data in MOCK_USERS.values():
        user = User(**user_data.model_dump())
        users.append(UserResponse(**user.model_dump()))
    
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(require_admin)
):
    """Obtener usuario específico (solo admin)"""
    from app.services.auth_service import MOCK_USERS
    
    # Buscar usuario por ID
    for user_data in MOCK_USERS.values():
        if user_data.id == user_id:
            user = User(**user_data.model_dump())
            return UserResponse(**user.model_dump())
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.post("/users", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    current_user: User = Depends(require_manage_users)
):
    """Crear nuevo usuario (admin o coordinator)"""
    # En un entorno real, esto se guardaría en la base de datos
    # Por ahora, simulamos la creación
    from app.services.auth_service import MOCK_USERS
    
    new_user = User(
        id=f"user-{len(MOCK_USERS) + 1:03d}",
        email=request.email,
        name=request.name,
        role=request.role,
        is_active=True
    )
    
    return UserResponse(**new_user.model_dump())


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    current_user: User = Depends(require_manage_users)
):
    """Actualizar usuario (admin o coordinator)"""
    from app.services.auth_service import MOCK_USERS
    
    # Buscar usuario existente
    user_data = None
    for data in MOCK_USERS.values():
        if data.id == user_id:
            user_data = data
            break
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Actualizar campos
    if request.name is not None:
        user_data.name = request.name
    if request.role is not None:
        user_data.role = request.role
    if request.is_active is not None:
        user_data.is_active = request.is_active
    
    user = User(**user_data.model_dump())
    return UserResponse(**user.model_dump())


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(require_admin)
):
    """Eliminar usuario (solo admin)"""
    from app.services.auth_service import MOCK_USERS
    
    # Buscar y eliminar usuario
    for email, user_data in list(MOCK_USERS.items()):
        if user_data.id == user_id:
            del MOCK_USERS[email]
            return {"message": "User deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.get("/system/status")
async def get_system_status(
    current_user: User = Depends(require_admin)
):
    """Obtener estado del sistema (solo admin)"""
    from app.services.auth_service import MOCK_USERS
    
    return {
        "status": "healthy",
        "users_count": len(MOCK_USERS),
        "active_users": sum(1 for user in MOCK_USERS.values() if user.is_active),
        "roles_distribution": {
            role.value: sum(1 for user in MOCK_USERS.values() if user.role == role)
            for role in UserRole
        }
    }


@router.get("/analytics/overview")
async def get_analytics_overview(
    current_user: User = Depends(require_admin)
):
    """Obtener resumen de analytics (solo admin)"""
    from app.services.auth_service import MOCK_USERS
    
    return {
        "total_users": len(MOCK_USERS),
        "active_users": sum(1 for user in MOCK_USERS.values() if user.is_active),
        "users_by_role": {
            role.value: sum(1 for user in MOCK_USERS.values() if user.role == role)
            for role in UserRole
        },
        "recent_activity": [
            {"action": "user_login", "timestamp": "2025-01-05T10:00:00Z", "user": "admin@classsphere.edu"},
            {"action": "user_created", "timestamp": "2025-01-05T09:30:00Z", "user": "teacher@classsphere.edu"},
        ]
    }
