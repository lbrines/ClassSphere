"""
Role-based API endpoints

CRITICAL OBJECTIVES:
- Test role-based access control
- Demonstrate role hierarchy
- Provide role management endpoints
- Test security middleware

DEPENDENCIES:
- FastAPI
- auth_middleware
- rate_limiter
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import logging

from src.app.middleware.auth_middleware import (
    get_current_user, 
    require_admin, 
    require_coordinator, 
    require_teacher, 
    require_student,
    require_role
)
from src.app.middleware.rate_limiter import check_rate_limit, get_rate_limit_status
from src.app.middleware.security_middleware import get_client_ip

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/admin/dashboard")
async def admin_dashboard(
    request: Request,
    user: Dict[str, Any] = Depends(require_admin)
):
    """Admin dashboard - only accessible by admin users"""
    # Check rate limit
    client_ip = get_client_ip(request)
    rate_limit_result = await check_rate_limit(client_ip, "admin_dashboard")
    
    if not rate_limit_result["allowed"]:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "remaining": rate_limit_result["remaining"],
                "reset_time": rate_limit_result["reset_time"]
            },
            headers={
                "X-Rate-Limit-Remaining": str(rate_limit_result["remaining"]),
                "X-Rate-Limit-Reset": str(rate_limit_result["reset_time"])
            }
        )
    
    return {
        "message": "Admin dashboard accessed successfully",
        "user": user["id"],
        "role": user["role"],
        "data": {
            "total_users": 150,
            "active_courses": 25,
            "system_health": "excellent"
        }
    }

@router.get("/coordinator/courses")
async def coordinator_courses(
    request: Request,
    user: Dict[str, Any] = Depends(require_coordinator)
):
    """Coordinator courses - accessible by coordinator and admin"""
    # Check rate limit
    client_ip = get_client_ip(request)
    rate_limit_result = await check_rate_limit(client_ip, "coordinator_courses")
    
    if not rate_limit_result["allowed"]:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "remaining": rate_limit_result["remaining"],
                "reset_time": rate_limit_result["reset_time"]
            }
        )
    
    return {
        "message": "Coordinator courses accessed successfully",
        "user": user["id"],
        "role": user["role"],
        "courses": [
            {"id": 1, "name": "Mathematics 101", "students": 30},
            {"id": 2, "name": "Physics 201", "students": 25},
            {"id": 3, "name": "Chemistry 301", "students": 20}
        ]
    }

@router.get("/teacher/classes")
async def teacher_classes(
    request: Request,
    user: Dict[str, Any] = Depends(require_teacher)
):
    """Teacher classes - accessible by teacher, coordinator, and admin"""
    # Check rate limit
    client_ip = get_client_ip(request)
    rate_limit_result = await check_rate_limit(client_ip, "teacher_classes")
    
    if not rate_limit_result["allowed"]:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "remaining": rate_limit_result["remaining"],
                "reset_time": rate_limit_result["reset_time"]
            }
        )
    
    return {
        "message": "Teacher classes accessed successfully",
        "user": user["id"],
        "role": user["role"],
        "classes": [
            {"id": 1, "name": "Math Class A", "students": 15},
            {"id": 2, "name": "Math Class B", "students": 12}
        ]
    }

@router.get("/student/assignments")
async def student_assignments(
    request: Request,
    user: Dict[str, Any] = Depends(require_student)
):
    """Student assignments - accessible by all authenticated users"""
    # Check rate limit
    client_ip = get_client_ip(request)
    rate_limit_result = await check_rate_limit(client_ip, "student_assignments")
    
    if not rate_limit_result["allowed"]:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "remaining": rate_limit_result["remaining"],
                "reset_time": rate_limit_result["reset_time"]
            }
        )
    
    return {
        "message": "Student assignments accessed successfully",
        "user": user["id"],
        "role": user["role"],
        "assignments": [
            {"id": 1, "title": "Math Homework 1", "due_date": "2025-10-10", "status": "pending"},
            {"id": 2, "title": "Physics Lab Report", "due_date": "2025-10-12", "status": "completed"}
        ]
    }

@router.get("/test/{role}")
async def test_role_access(
    role: str,
    request: Request,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Test role access - dynamically test any role requirement"""
    # Check rate limit
    client_ip = get_client_ip(request)
    rate_limit_result = await check_rate_limit(client_ip, f"test_role_{role}")
    
    if not rate_limit_result["allowed"]:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "remaining": rate_limit_result["remaining"],
                "reset_time": rate_limit_result["reset_time"]
            }
        )
    
    # Check role permission
    from src.app.middleware.auth_middleware import auth_middleware
    user_role = user.get("role", "student")
    
    if not auth_middleware.has_permission(user_role, role):
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Insufficient permissions. Required: {role}, Current: {user_role}",
                "user_role": user_role,
                "required_role": role
            }
        )
    
    return {
        "message": f"Role {role} access test successful",
        "user": user["id"],
        "user_role": user["role"],
        "required_role": role,
        "access_granted": True
    }

@router.get("/rate-limit/status")
async def get_rate_limit_info(
    request: Request,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get rate limit status for current user"""
    client_ip = get_client_ip(request)
    rate_status = await get_rate_limit_status(client_ip, "general")
    
    return {
        "message": "Rate limit status retrieved",
        "user": user["id"],
        "client_ip": client_ip,
        "rate_limits": rate_status
    }

@router.get("/permissions")
async def get_user_permissions(
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user permissions based on role"""
    from src.app.middleware.auth_middleware import auth_middleware
    
    user_role = user.get("role", "student")
    
    # Get all available roles
    all_roles = ["admin", "coordinator", "teacher", "student"]
    
    # Check permissions for each role
    permissions = {}
    for role in all_roles:
        permissions[role] = auth_middleware.has_permission(user_role, role)
    
    return {
        "message": "User permissions retrieved",
        "user": user["id"],
        "user_role": user_role,
        "permissions": permissions,
        "role_hierarchy": {
            "admin": 4,
            "coordinator": 3,
            "teacher": 2,
            "student": 1
        }
    }

@router.get("/security/headers")
async def test_security_headers(
    request: Request,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Test security headers in response"""
    return {
        "message": "Security headers test",
        "user": user["id"],
        "headers_info": {
            "user_agent": request.headers.get("user-agent"),
            "origin": request.headers.get("origin"),
            "referer": request.headers.get("referer"),
            "client_ip": get_client_ip(request)
        }
    }