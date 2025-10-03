"""
Health check API endpoints
"""
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from ...core.database import db_manager
from ...core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint.
    Returns status of all services and system information.
    """
    try:
        # Get health status from database manager
        health_status = await db_manager.health_check()
        
        return {
            "status": health_status["overall"],
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "services": health_status,
            "system": {
                "host": settings.HOST,
                "port": settings.PORT,
                "debug": settings.DEBUG,
                "error_prevention_enabled": settings.ERROR_PREVENTION_ENABLED,
                "auto_cleanup_enabled": settings.AUTO_CLEANUP_ENABLED
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/ready", response_model=Dict[str, Any])
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check endpoint.
    Returns whether the service is ready to accept requests.
    """
    try:
        health_status = await db_manager.health_check()
        
        if health_status["overall"] == "healthy":
            return {
                "status": "ready",
                "timestamp": datetime.utcnow().isoformat(),
                "services": health_status
            }
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "not_ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "services": health_status,
                    "reason": "One or more services are unhealthy"
                }
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
        )


@router.get("/live", response_model=Dict[str, Any])
async def liveness_check() -> Dict[str, Any]:
    """
    Liveness check endpoint.
    Returns whether the service is alive and running.
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "uptime": "running"
    }


@router.get("/services", response_model=Dict[str, Any])
async def services_status() -> Dict[str, Any]:
    """
    Detailed services status endpoint.
    Returns detailed status of each service.
    """
    try:
        health_status = await db_manager.health_check()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "services": health_status,
            "configuration": {
                "mongodb_url": settings.MONGODB_URL,
                "redis_url": settings.REDIS_URL,
                "max_connections": settings.MAX_CONNECTIONS,
                "connection_timeout": settings.CONNECTION_TIMEOUT,
                "request_timeout": settings.REQUEST_TIMEOUT
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Services status check failed: {str(e)}"
        )