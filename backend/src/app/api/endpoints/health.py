"""
Endpoint de health check con verificación de servicios
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import health_check_mongodb, health_check_redis

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint que verifica el estado de todos los servicios.
    """
    try:
        # Verificar MongoDB
        mongodb_healthy = await health_check_mongodb()
        
        # Verificar Redis
        redis_healthy = await health_check_redis()
        
        # Determinar estado general
        overall_status = "healthy" if mongodb_healthy and redis_healthy else "degraded"
        
        response_data = {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.app_version,
            "environment": settings.environment,
            "services": {
                "mongodb": {
                    "status": "healthy" if mongodb_healthy else "unhealthy",
                    "required": True
                },
                "redis": {
                    "status": "healthy" if redis_healthy else "unhealthy",
                    "required": False  # Redis es opcional
                }
            }
        }
        
        # Si algún servicio crítico está caído, retornar 503
        if not mongodb_healthy:
            return JSONResponse(
                status_code=503,
                content=response_data
            )
        
        return response_data
        
    except Exception as e:
        # En caso de error inesperado, retornar 500
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": settings.app_version,
                "error": str(e)
            }
        )


@router.get("/health/live")
async def liveness_check():
    """
    Liveness check simple - solo verifica que la aplicación responde.
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check - verifica que la aplicación está lista para recibir tráfico.
    """
    try:
        # Verificar servicios críticos
        mongodb_healthy = await health_check_mongodb()
        
        if not mongodb_healthy:
            raise HTTPException(
                status_code=503,
                detail="Application not ready - MongoDB unavailable"
            )
        
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "mongodb": "ready"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Application not ready - {str(e)}"
        )