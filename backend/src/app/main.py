"""
ClassSphere FastAPI application.
"""
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .api.endpoints import health, auth, oauth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager with graceful startup/shutdown.
    """
    # Startup
    print(f"🚀 Starting ClassSphere on port {settings.port}")
    print(f"⚙️  Environment: {'development' if settings.debug else 'production'}")

    try:
        # Initialize services (with graceful degradation)
        await _initialize_services()
        print("✅ Services initialized successfully")
    except Exception as e:
        print(f"⚠️  Service initialization warning: {e}")

    yield

    # Shutdown
    try:
        await _cleanup_services()
        print("🔄 Services cleaned up successfully")
    except Exception as e:
        print(f"⚠️  Service cleanup warning: {e}")


async def _initialize_services():
    """Initialize external services with timeout protection."""
    try:
        # Redis initialization (optional)
        await asyncio.wait_for(_init_redis(), timeout=2.0)
    except asyncio.TimeoutError:
        print("⚠️  Redis initialization timeout - using fallback")
    except Exception as e:
        print(f"⚠️  Redis not available: {e} - using fallback")


async def _init_redis():
    """Initialize Redis connection (mock implementation)."""
    await asyncio.sleep(0.1)  # Simulate connection
    print("📦 Redis cache initialized")


async def _cleanup_services():
    """Cleanup services on shutdown."""
    await asyncio.sleep(0.1)  # Simulate cleanup
    print("🧹 Services cleanup completed")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="ClassSphere API",
        description="Educational dashboard with Google Classroom integration",
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(oauth.router, prefix="/api/v1")

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with welcome message."""
        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "message": "Welcome to ClassSphere API",
                    "version": "1.0.0",
                    "timestamp": datetime.utcnow().isoformat(),
                    "docs": "/docs" if settings.debug else "disabled",
                    "port": settings.port
                },
                "message": "API is running"
            }
        )

    # Info endpoint
    @app.get("/info")
    async def info():
        """System information endpoint."""
        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "name": "ClassSphere API",
                    "version": "1.0.0",
                    "environment": "development" if settings.debug else "production",
                    "port": settings.port,
                    "timestamp": datetime.utcnow().isoformat(),
                    "features": [
                        "JWT Authentication",
                        "Google OAuth 2.0",
                        "Role-based Access Control",
                        "Redis Cache (with fallback)",
                        "Health Monitoring"
                    ]
                },
                "message": "System information"
            }
        )

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )