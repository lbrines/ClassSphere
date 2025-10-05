"""
Endpoints para coordinadores
"""
from fastapi import APIRouter

from app.models.auth import User
from app.middleware.auth import RequireCoordinator


router = APIRouter(prefix="/api/v1/coordinator", tags=["coordinator"])


@router.get("/dashboard")
async def coordinator_dashboard(current_user: User = RequireCoordinator):
    """Dashboard de coordinador"""
    return {
        "message": f"Welcome to coordinator dashboard, {current_user.first_name}!",
        "user_role": current_user.role,
        "permissions": [
            "manage_teachers",
            "manage_courses",
            "view_reports"
        ],
        "stats": {
            "assigned_teachers": 0,
            "managed_courses": 0,
            "pending_approvals": 0
        }
    }


@router.get("/teachers")
async def get_assigned_teachers(current_user: User = RequireCoordinator):
    """Obtener profesores asignados"""
    return {
        "message": f"Teachers managed by {current_user.first_name}",
        "coordinator_id": current_user.id,
        "teachers": [
            {
                "id": 3,
                "name": "Teacher User",
                "email": "teacher@classsphere.com",
                "status": "active",
                "courses_count": 2
            }
        ]
    }


@router.post("/courses")
async def create_course(current_user: User = RequireCoordinator):
    """Crear curso (coordinador o superior)"""
    return {
        "message": f"Course created by coordinator {current_user.first_name}",
        "coordinator_id": current_user.id,
        "action": "create_course"
    }