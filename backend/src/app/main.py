"""
Main FastAPI application for ClassSphere

CRITICAL OBJECTIVES:
- Create FastAPI app with proper configuration
- Ensure server runs on port 8000
- Implement health check endpoint
- Configure CORS and middleware

DEPENDENCIES:
- FastAPI
- uvicorn
- pydantic
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging
from typing import Dict, Any

from src.app.core.config import get_settings
from src.app.core.cache import get_cache, close_cache
from src.app.api.auth import router as auth_router
from src.app.api.roles import router as roles_router
from src.app.middleware.security_middleware import setup_security_middleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting ClassSphere application...")
    
    # Initialize cache
    cache = await get_cache()
    if cache.is_connected():
        logger.info("✅ Cache initialized successfully")
    else:
        logger.warning("⚠️ Cache not available, running without cache")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down ClassSphere application...")
    await close_cache()
    logger.info("✅ Application shutdown complete")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="ClassSphere - Educational Dashboard System",
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["127.0.0.1", "localhost", "testserver", "*.classsphere.com"]
)

# Setup security middleware
setup_security_middleware(app)

# Include routers
app.include_router(auth_router)
app.include_router(roles_router)

@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ClassSphere API",
        "version": settings.version,
        "status": "running",
        "port": settings.port
    }

@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint"""
    cache = await get_cache()
    
    return {
        "status": "healthy",
        "version": settings.version,
        "port": settings.port,
        "cache_connected": cache.is_connected(),
        "testing": settings.testing
    }

@app.get("/info", response_model=Dict[str, Any])
async def app_info():
    """Application information endpoint"""
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
        "port": settings.port,
        "host": settings.host,
        "cors_origins": settings.cors_origins
    }

if __name__ == "__main__":
    # Ensure port 8000 is used
    if settings.port != 8000:
        raise ValueError("Port must be 8000 according to architectural standards")
    
    logger.info(f"🚀 Starting server on {settings.host}:{settings.port}")
    
    uvicorn.run(
        "src.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level="info"
    )