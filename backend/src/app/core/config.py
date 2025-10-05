"""
Configuration management for ClassSphere backend.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False

    # Security
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # OAuth Configuration
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"

    # Database (Future)
    database_url: str = "sqlite:///./classsphere.db"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()