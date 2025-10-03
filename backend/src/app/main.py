"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.core.config import settings
from src.app.core.database import database


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        description="Dashboard Educativo Backend API"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        try:
            await database.connect_to_mongodb()
            database.connect_to_redis()
        except Exception as e:
            print(f"Warning: Could not connect to databases: {e}")
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        await database.close_mongodb_connection()
        database.close_redis_connection()
    
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
