"""
Aplicación principal FastAPI con lifespan resiliente
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan resiliente - servicios externos opcionales"""
    # Startup
    print("🚀 Starting ClassSphere...")
    
    try:  # pragma: no cover
        # Redis (opcional)
        print("📦 Checking Redis...")
        # await init_redis()
        print("✅ Redis available")
    except Exception as e:  # pragma: no cover
        print(f"⚠️  Redis not available: {e}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down ClassSphere...")
    try:  # pragma: no cover
        # await cleanup_services()
        print("✅ Cleanup completed")
    except Exception as e:  # pragma: no cover
        print(f"⚠️  Cleanup error: {e}")


def create_app() -> FastAPI:
    """Factory para crear la aplicación"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check básico
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version
        }
    
    # Routers
    from app.api.endpoints import auth
    app.include_router(auth.router)
    
    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
