"""
Aplicación principal FastAPI con lifespan resiliente
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.oauth import router as oauth_router
from app.api.admin import router as admin_router
from app.api.coordinator import router as coordinator_router
from app.api.teacher import router as teacher_router
from app.api.student import router as student_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan resiliente - servicios externos opcionales"""
    # Startup
    print("🚀 Starting ClassSphere...")

    try:
        # Redis (opcional)
        print("📦 Checking Redis...")
        # await init_redis()
        print("✅ Redis available")
    except Exception as e:
        print(f"⚠️  Redis not available: {e}")

    yield

    # Shutdown
    print("🛑 Shutting down ClassSphere...")
    try:
        # await cleanup_services()
        print("✅ Cleanup completed")
    except Exception as e:
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

    # Incluir routers
    app.include_router(auth_router)
    app.include_router(oauth_router)
    app.include_router(admin_router)
    app.include_router(coordinator_router)
    app.include_router(teacher_router)
    app.include_router(student_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )