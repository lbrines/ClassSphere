"""
Health check endpoints for ClassSphere API.
"""
import asyncio
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from ...services.mock_service import MockService


router = APIRouter(prefix="/health", tags=["health"])


def get_mock_service() -> MockService:
    """Dependency to get mock service instance."""
    return MockService()


@router.get("/")
async def health_check(
    mock_service: MockService = Depends(get_mock_service)
) -> JSONResponse:
    """
    Basic health check endpoint.

    Returns:
        JSON response with health status
    """
    try:
        health_data = await asyncio.wait_for(
            mock_service.health_check(),
            timeout=5.0
        )

        status_code = 200 if health_data["status"] == "healthy" else 503

        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "data": health_data,
                "message": "Health check completed"
            }
        )

    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "data": {
                    "status": "timeout",
                    "timestamp": datetime.utcnow().isoformat()
                },
                "message": "Health check timeout"
            }
        )


@router.get("/detailed")
async def detailed_health_check(
    mock_service: MockService = Depends(get_mock_service)
) -> JSONResponse:
    """
    Detailed health check with component status.

    Returns:
        JSON response with detailed health information
    """
    try:
        # Perform health check with timeout
        health_data = await asyncio.wait_for(
            mock_service.health_check(),
            timeout=5.0
        )

        # Add additional system information
        health_data.update({
            "version": "1.0.0",
            "environment": "development",
            "uptime": "running",
            "port": 8000
        })

        status_code = 200 if health_data["status"] == "healthy" else 503

        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "data": health_data,
                "message": "Detailed health check completed"
            }
        )

    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "data": {
                    "status": "timeout",
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": "1.0.0",
                    "environment": "development"
                },
                "message": "Detailed health check timeout"
            }
        )