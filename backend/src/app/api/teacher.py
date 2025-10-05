"""
Endpoints para profesores
"""
from fastapi import APIRouter

from app.models.auth import User
from app.middleware.auth import RequireTeacher


router = APIRouter(prefix="/api/v1/teacher", tags=["teacher"])


@router.get("/dashboard")
async def teacher_dashboard(current_user: User = RequireTeacher):
    """Dashboard de profesor"""
    return {
        "message": f"Welcome to teacher dashboard, {current_user.first_name}!",
        "user_role": current_user.role,
        "permissions": [
            "manage_classes",
            "grade_students",
            "view_student_progress"
        ],
        "stats": {
            "my_courses": 2,
            "total_students": 45,
            "pending_grades": 8
        }
    }


@router.get("/courses")
async def get_my_courses(current_user: User = RequireTeacher):
    """Obtener mis cursos"""
    return {
        "message": f"Courses taught by {current_user.first_name}",
        "teacher_id": current_user.id,
        "courses": [
            {
                "id": 1,
                "name": "Mathematics 101",
                "students_count": 25,
                "status": "active"
            },
            {
                "id": 2,
                "name": "Advanced Calculus",
                "students_count": 20,
                "status": "active"
            }
        ]
    }


@router.get("/students")
async def get_my_students(current_user: User = RequireTeacher):
    """Obtener mis estudiantes"""
    return {
        "message": f"Students taught by {current_user.first_name}",
        "teacher_id": current_user.id,
        "students": [
            {
                "id": 4,
                "name": "Student User",
                "email": "student@classsphere.com",
                "courses": ["Mathematics 101"],
                "average_grade": 85.5
            }
        ]
    }