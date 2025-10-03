"""
Endpoints de autenticación (placeholder para tests)
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def auth_info():
    """
    Información básica de autenticación.
    """
    return {
        "message": "Auth endpoints available",
        "endpoints": [
            "/login",
            "/register", 
            "/google/oauth",
            "/google/callback"
        ]
    }