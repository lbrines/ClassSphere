"""
Main FastAPI application for Dashboard Educativo Backend
Implements lifespan context manager and error prevention protocols
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.database import db_manager, cleanup_database, cleanup_redis

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown with error prevention.
    """
    # Startup
    logger.info("Starting Dashboard Educativo Backend...")
    
    try:
        # Initialize database connections
        await db_manager.get_database()
        await db_manager.get_redis()
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        # Continue startup even if some services fail
        # This allows the app to start in degraded mode
    
    yield
    
    # Shutdown
    logger.info("Shutting down Dashboard Educativo Backend...")
    
    try:
        # Cleanup database connections
        await cleanup_database()
        await cleanup_redis()
        
        logger.info("All services cleaned up successfully")
        
    except Exception as e:
        logger.error(f"Shutdown error: {e}")
        # Continue shutdown even if cleanup fails


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    Implements CORS, error handling, and health checks.
    """
    app = FastAPI(
        title="Dashboard Educativo API",
        version=settings.APP_VERSION,
        description="API for Dashboard Educativo - Sistema Completo Unificado",
        debug=settings.DEBUG,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Error handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """Handle HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """Handle general exceptions."""
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "status_code": 500,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check() -> Dict[str, Any]:
        """
        Health check endpoint.
        Returns status of all services.
        """
        try:
            health_status = await db_manager.health_check()
            
            return {
                "status": health_status["overall"],
                "timestamp": datetime.utcnow().isoformat(),
                "version": settings.APP_VERSION,
                "environment": settings.ENVIRONMENT,
                "services": health_status
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": settings.APP_VERSION,
                "environment": settings.ENVIRONMENT,
                "error": str(e)
            }
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root() -> Dict[str, str]:
        """
        Root endpoint.
        Returns basic application information.
        """
        return {
            "message": f"Welcome to {settings.APP_NAME} API",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "docs": "/docs",
            "health": "/health"
        }
    
    # API info endpoint
    @app.get("/api/info", tags=["API"])
    async def api_info() -> Dict[str, Any]:
        """
        API information endpoint.
        Returns detailed API information.
        """
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
            "host": settings.HOST,
            "port": settings.PORT,
            "features": {
                "cors_enabled": True,
                "error_prevention": settings.ERROR_PREVENTION_ENABLED,
                "auto_cleanup": settings.AUTO_CLEANUP_ENABLED,
                "metrics_enabled": settings.METRICS_ENABLED
            },
            "endpoints": {
                "health": "/health",
                "docs": "/docs",
                "redoc": "/redoc",
                "openapi": "/openapi.json"
            }
        }
    
    return app


# Create FastAPI application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
        log_level=settings.LOG_LEVEL.lower()
    )