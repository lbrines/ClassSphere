"""
Dashboard Educativo - Core Configuration
Context-Aware Implementation - Phase 1 Critical
Implements Pydantic v2 with ConfigDict modern approach
"""

from typing import Optional, List
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with Pydantic v2 ConfigDict"""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = Field(default="Dashboard Educativo", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server Configuration - Puerto 8000 Estándar Arquitectónico
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port - Estándar Arquitectónico")
    
    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost/dashboard_educativo",
        description="Database connection URL"
    )
    
    # Redis Cache
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis URL")
    
    # JWT Configuration
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT secret key"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration")
    refresh_token_expire_days: int = Field(default=7, description="Refresh token expiration")
    
    # Google OAuth
    google_client_id: Optional[str] = Field(default=None, description="Google OAuth client ID")
    google_client_secret: Optional[str] = Field(default=None, description="Google OAuth client secret")
    google_redirect_uri: str = Field(
        default="http://localhost:3000/auth/callback",
        description="Google OAuth redirect URI"
    )
    
    # CORS Configuration
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="CORS allowed origins"
    )
    
    # Context Management
    context_log_path: str = Field(
        default="/tmp/dashboard_context_status.json",
        description="Context log file path"
    )
    
    # Google Classroom Scopes
    google_scopes: List[str] = Field(
        default=[
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.rosters.readonly",
            "https://www.googleapis.com/auth/classroom.profile.emails"
        ],
        description="Google Classroom API scopes"
    )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance"""
    return settings