"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Dashboard Educativo"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"
    
    # Security
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Database
    mongodb_url: str = "mongodb://localhost:27017/dashboard_educativo"
    redis_url: str = "redis://localhost:6379/0"
    
    # Google OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: str = "http://localhost:8000/auth/google/callback"
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_tls: bool = True
    
    # File Storage
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
