"""
Endpoints para administradores
"""
from typing import List
from fastapi import APIRouter, Depends

from app.models.auth import User
from app.middleware.auth import RequireAdmin, get_auth_service
from app.services.auth_service import AuthService


router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


@router.get("/users", response_model=List[User])
async def get_all_users(
    current_user: User = RequireAdmin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Obtener todos los usuarios (solo admin)"""
    return auth_service.get_all_users()


@router.get("/dashboard")
async def admin_dashboard(current_user: User = RequireAdmin):
    """Dashboard de administrador"""
    return {
        "message": f"Welcome to admin dashboard, {current_user.first_name}!",
        "user_role": current_user.role,
        "permissions": [
            "manage_users",
            "manage_courses",
            "view_analytics",
            "system_settings"
        ],
        "stats": {
            "total_users": 4,
            "active_courses": 0,
            "pending_requests": 0
        }
    }


@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = RequireAdmin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Activar usuario (solo admin)"""
    # En un sistema real, esto actualizaría la base de datos
    return {
        "message": f"User {user_id} activated by admin {current_user.first_name}",
        "action": "activate_user",
        "user_id": user_id,
        "admin_id": current_user.id
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = RequireAdmin
):
    """Eliminar usuario (solo admin)"""
    if user_id == current_user.id:
        return {"error": "Cannot delete your own account"}

    return {
        "message": f"User {user_id} deleted by admin {current_user.first_name}",
        "action": "delete_user",
        "user_id": user_id,
        "admin_id": current_user.id
    }