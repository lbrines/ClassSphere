from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..core.database import get_db
import redis
from ..core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with database and Redis connectivity."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    try:
        # Test Redis connection
        r = redis.Redis.from_url(settings.redis_url)
        r.ping()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": "2025-01-27T12:00:00Z",
        "services": {
            "database": db_status,
            "redis": redis_status
        },
        "version": "1.0.0",
        "environment": "development"
    }
