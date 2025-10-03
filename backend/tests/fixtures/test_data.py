"""
Test data fixtures
"""
from typing import Dict, Any


def get_user_data() -> Dict[str, Any]:
    """Get sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "Test User",
        "role": "student"
    }


def get_teacher_data() -> Dict[str, Any]:
    """Get sample teacher data for testing"""
    return {
        "email": "teacher@example.com",
        "password": "TeacherPass123!",
        "name": "Test Teacher",
        "role": "teacher"
    }


def get_admin_data() -> Dict[str, Any]:
    """Get sample admin data for testing"""
    return {
        "email": "admin@example.com",
        "password": "AdminPass123!",
        "name": "Test Admin",
        "role": "admin"
    }
