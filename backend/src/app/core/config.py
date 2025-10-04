"""
Configuration settings for ClassSphere

CRITICAL OBJECTIVES:
- Configure application settings with environment variables
- Ensure port 8000 is always used
- Provide secure defaults for all settings

DEPENDENCIES:
- pydantic-settings
- python-dotenv
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    app_name: str = Field(default="ClassSphere", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Server - PORT 8000 IS MANDATORY
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port - MUST BE 8000")
    reload: bool = Field(default=True, description="Auto-reload on changes")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", description="Secret key for JWT")
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="Access token expiration in minutes")
    refresh_token_expire_days: int = Field(default=7, description="Refresh token expiration in days")
    
    # Database
    database_url: str = Field(default="sqlite:///./classsphere.db", description="Database URL")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379/1", description="Redis URL")
    
    # Google OAuth
    google_client_id: Optional[str] = Field(default=None, description="Google OAuth client ID")
    google_client_secret: Optional[str] = Field(default=None, description="Google OAuth client secret")
    google_redirect_uri: str = Field(default="http://127.0.0.1:8000/auth/google/callback", description="Google OAuth redirect URI")
    
    # CORS
    cors_origins: list[str] = Field(default=["http://127.0.0.1:3000", "http://localhost:3000"], description="CORS allowed origins")
    
    # Security
    allowed_hosts: list[str] = Field(default=["127.0.0.1", "localhost", "testserver", "*.classsphere.com"], description="Allowed hosts for TrustedHostMiddleware")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per minute")
    rate_limit_window: int = Field(default=60, description="Rate limit window in seconds")
    
    # Testing
    testing: bool = Field(default=False, description="Testing mode")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

    def model_post_init(self, __context):
        """Post-initialization validation"""
        # Ensure port is always 8000
        if self.port != 8000:
            raise ValueError("Port must be 8000 according to architectural standards")

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings