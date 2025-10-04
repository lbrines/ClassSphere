"""
Dashboard Educativo - Main Application
Context-Aware Implementation - Phase 1 Critical
Implements FastAPI with Lifespan Context Manager
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from ..core.config import get_settings
from ..core.context_logger import context_logger, log_application_context
from .api import health, auth, google


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan - Context Manager Estándar
    Implements resilient startup/shutdown with context tracking
    """
    settings = get_settings()
    
    # Startup
    await log_application_context("startup", "lifespan_start", "started")
    
    try:
        # Initialize context logging
        await context_logger.log_context_status(
            context_id="app-startup-critical-001",
            priority="CRITICAL",
            status="started",
            position="beginning",
            message="FastAPI application startup initiated",
            phase="startup",
            task="lifespan_start"
        )
        
        print(f"🚀 [CONTEXT-STARTUP] Dashboard Educativo iniciando en puerto {settings.port}")
        print(f"📊 [CONTEXT-LOG] Context logging activo en: {settings.context_log_path}")
        
        yield
        
    except Exception as e:
        await log_application_context("startup", "lifespan_error", "failed")
        print(f"❌ [CONTEXT-ERROR] Error en startup: {e}")
        raise
    
    finally:
        # Shutdown
        await log_application_context("shutdown", "lifespan_end", "completed")
        await context_logger.log_context_status(
            context_id="app-shutdown-critical-002",
            priority="CRITICAL",
            status="completed",
            position="end",
            message="FastAPI application shutdown completed",
            phase="shutdown",
            task="lifespan_end"
        )
        print("🛑 [CONTEXT-SHUTDOWN] Dashboard Educativo cerrado correctamente")


def create_app() -> FastAPI:
    """Create FastAPI application with context-aware configuration"""
    
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Context-aware exception handler
    @app.exception_handler(Exception)
    async def context_aware_exception_handler(request: Request, exc: Exception):
        """Context-aware exception handler"""
        await context_logger.log_context_status(
            context_id=f"exception-{exc.__class__.__name__}",
            priority="CRITICAL",
            status="failed",
            position="middle",
            message=f"Exception occurred: {str(exc)}",
            phase="runtime",
            task="exception_handling"
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "context_id": f"exception-{exc.__class__.__name__}",
                "message": "An error occurred while processing your request"
            }
        )
    
    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
    app.include_router(google.router, prefix="/api/v1", tags=["google"])
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "src.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )