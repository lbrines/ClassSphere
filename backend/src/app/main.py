from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
import time
from src.app.core.config import settings

app = FastAPI(
    title="Dashboard Educativo API",
    version="1.0.0",
    description="API para el Dashboard Educativo Full-Stack",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (deshabilitado para testing con curl si TRUSTED_HOST_ENABLED es False)
if settings.TRUSTED_HOST_ENABLED:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOST_ALLOWED
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware para añadir el tiempo de procesamiento a las respuestas.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/", summary="Root endpoint", response_description="Root message and API info")
async def read_root():
    """
    Root endpoint of the API.
    Returns a welcome message and basic API information.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Dashboard Educativo API",
            "version": app.version,
            "docs": app.docs_url,
            "health": "/health"
        }
    )

@app.get("/health", summary="Health check endpoint", response_description="API health status")
async def health_check():
    """
    Health check endpoint to verify API status.
    Returns a healthy status with current timestamp and environment.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "timestamp": time.time(),
            "environment": settings.ENVIRONMENT,
            "version": app.version
        }
    )
