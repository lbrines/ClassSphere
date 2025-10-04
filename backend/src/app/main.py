from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import create_tables
from .api import health

# Create FastAPI app
app = FastAPI(
    title="ClassSphere API",
    description="Dashboard Educativo Full-Stack",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    create_tables()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ClassSphere API",
        "version": "1.0.0",
        "status": "running",
        "port": settings.port
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
