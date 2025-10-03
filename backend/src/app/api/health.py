"""
Health check endpoints for monitoring and diagnostics.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from loguru import logger

from ..core.database import db_manager

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """Comprehensive health check endpoint."""
    try:
        health_status = await db_manager.health_check()
        
        return {
            "status": health_status["overall"],
            "timestamp": "2025-10-03T19:00:00Z",
            "version": "1.0.0",
            "services": {
                "database": health_status["database"],
                "redis": health_status["redis"]
            },
            "uptime": "0s",  # Will be calculated in production
            "environment": "development"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@router.get("/ready", response_model=Dict[str, Any])
async def readiness_check() -> Dict[str, Any]:
    """Readiness check for Kubernetes/container orchestration."""
    try:
        health_status = await db_manager.health_check()
        
        if health_status["overall"] == "healthy":
            return {
                "status": "ready",
                "message": "Service is ready to accept requests"
            }
        else:
            raise HTTPException(
                status_code=503,
                detail="Service is not ready"
            )
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/live", response_model=Dict[str, Any])
async def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes/container orchestration."""
    return {
        "status": "alive",
        "message": "Service is running"
    }


@router.get("/services", response_model=Dict[str, Any])
async def services_status() -> Dict[str, Any]:
    """Detailed services status."""
    try:
        health_status = await db_manager.health_check()
        
        return {
            "database": {
                "status": health_status["database"],
                "type": "MongoDB",
                "url": "mongodb://localhost:27017"
            },
            "redis": {
                "status": health_status["redis"],
                "type": "Redis",
                "url": "redis://localhost:6379"
            },
            "overall": health_status["overall"]
        }
    except Exception as e:
        logger.error(f"Services status check failed: {e}")
        raise HTTPException(status_code=503, detail="Services status unavailable")