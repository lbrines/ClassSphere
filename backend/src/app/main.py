"""
Main FastAPI application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.core.config import settings
from src.app.core.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    try:
        await database.connect_to_mongodb()
        database.connect_to_redis()
        print("Application startup completed")
    except Exception as e:
        print(f"Warning: Could not connect to databases: {e}")
    
    yield
    
    # Shutdown
    try:
        await database.close_mongodb_connection()
        database.close_redis_connection()
        print("Application shutdown completed")
    except Exception as e:
        print(f"Warning: Error during shutdown: {e}")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        description="Dashboard Educativo Backend API",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment
        }
    
    return app


# Create app instance
app = create_app()
