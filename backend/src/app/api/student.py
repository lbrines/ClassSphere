"""
Endpoints para estudiantes
"""
from fastapi import APIRouter

from app.models.auth import User
from app.middleware.auth import RequireStudent


router = APIRouter(prefix="/api/v1/student", tags=["student"])


@router.get("/dashboard")
async def student_dashboard(current_user: User = RequireStudent):
    """Dashboard de estudiante"""
    return {
        "message": f"Welcome to student dashboard, {current_user.first_name}!",
        "user_role": current_user.role,
        "permissions": [
            "view_courses",
            "view_grades",
            "submit_assignments"
        ],
        "stats": {
            "enrolled_courses": 3,
            "average_grade": 88.5,
            "pending_assignments": 2
        }
    }


@router.get("/courses")
async def get_my_courses(current_user: User = RequireStudent):
    """Obtener mis cursos como estudiante"""
    return {
        "message": f"Courses for student {current_user.first_name}",
        "student_id": current_user.id,
        "courses": [
            {
                "id": 1,
                "name": "Mathematics 101",
                "teacher": "Teacher User",
                "grade": 92.5,
                "status": "enrolled"
            },
            {
                "id": 2,
                "name": "Physics 201",
                "teacher": "Dr. Physics",
                "grade": 87.0,
                "status": "enrolled"
            },
            {
                "id": 3,
                "name": "Chemistry 101",
                "teacher": "Prof. Chemistry",
                "grade": 85.5,
                "status": "enrolled"
            }
        ]
    }


@router.get("/grades")
async def get_my_grades(current_user: User = RequireStudent):
    """Obtener mis calificaciones"""
    return {
        "message": f"Grades for student {current_user.first_name}",
        "student_id": current_user.id,
        "overall_gpa": 88.33,
        "grades": [
            {
                "course": "Mathematics 101",
                "assignments": [
                    {"name": "Quiz 1", "grade": 95, "weight": 0.2},
                    {"name": "Midterm", "grade": 88, "weight": 0.3},
                    {"name": "Final Project", "grade": 92, "weight": 0.5}
                ],
                "final_grade": 92.5
            },
            {
                "course": "Physics 201",
                "assignments": [
                    {"name": "Lab Report 1", "grade": 85, "weight": 0.3},
                    {"name": "Exam 1", "grade": 90, "weight": 0.7}
                ],
                "final_grade": 87.0
            }
        ]
    }