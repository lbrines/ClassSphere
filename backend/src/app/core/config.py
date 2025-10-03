from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    app_name: str = "Dashboard Educativo"
    app_version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"
    
    # Security Settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "dashboard_educativo"
    redis_url: str = "redis://localhost:6379"
    
    # Google OAuth Settings
    google_client_id: str = "your-google-client-id"
    google_client_secret: str = "your-google-client-secret"
    google_redirect_uri: str = "http://localhost:3000/auth/google/callback"
    
    # Email Settings
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = "your-email@gmail.com"
    smtp_password: str = "your-app-password"
    smtp_tls: bool = True
    
    # File Storage Settings
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB
    
    # Logging Settings
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

# Singleton instance
settings = Settings()