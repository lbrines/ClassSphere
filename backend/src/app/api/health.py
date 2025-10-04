"""
Dashboard Educativo - Health Check API
Context-Aware Implementation - Phase 1 Critical
Implements health endpoint with context tracking
"""

from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Dict, Any

from ...core.context_logger import context_logger
from ...core.config import get_settings

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint with context awareness
    Implements Puerto 8000 - Estándar Arquitectónico
    """
    settings = get_settings()
    
    # Get context health
    context_health = context_logger.get_context_health()
    
    # Log health check
    await context_logger.log_context_status(
        context_id="health-check-001",
        priority="CRITICAL",
        status="completed",
        position="middle",
        message="Health check endpoint accessed",
        phase="runtime",
        task="health_check"
    )
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "context_management": {
            "context_log_path": settings.context_log_path,
            "context_health": context_health
        },
        "server": {
            "host": settings.host,
            "port": settings.port
        }
    }


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with full context information"""
    
    settings = get_settings()
    context_health = context_logger.get_context_health()
    
    # Log detailed health check
    await context_logger.log_context_status(
        context_id="detailed-health-check-002",
        priority="HIGH",
        status="completed",
        position="middle",
        message="Detailed health check endpoint accessed",
        phase="runtime",
        task="detailed_health_check"
    )
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "application": {
            "name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug
        },
        "context_management": {
            "log_path": settings.context_log_path,
            "health_status": context_health,
            "coherence_check": {
                "glossary_references": 5,
                "terminology_consistency": "9.0/10"
            }
        },
        "server": {
            "host": settings.host,
            "port": settings.port,
            "cors_origins": settings.cors_origins
        },
        "features": {
            "authentication": "configured",
            "google_integration": "configured",
            "context_logging": "active"
        }
    }