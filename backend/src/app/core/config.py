"""
Configuration module using Pydantic v2 with BaseSettings and ConfigDict.
"""
import os
from typing import List, Optional
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings using Pydantic v2 BaseSettings."""
    
    # Application Settings
    APP_NAME: str = Field(default="Dashboard Educativo", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(default="development", description="Environment")
    
    # Server Configuration
    HOST: str = Field(default="127.0.0.1", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    RELOAD: bool = Field(default=False, description="Auto reload")
    
    # Database Configuration
    MONGODB_URL: str = Field(default="mongodb://localhost:27017", description="MongoDB URL")
    MONGODB_DATABASE: str = Field(default="dashboard_educativo", description="MongoDB database name")
    MONGODB_MAX_CONNECTIONS: int = Field(default=10, description="Max MongoDB connections")
    MONGODB_MIN_CONNECTIONS: int = Field(default=1, description="Min MongoDB connections")
    
    # Redis Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379", description="Redis URL")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_MAX_CONNECTIONS: int = Field(default=10, description="Max Redis connections")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = Field(default="your-super-secret-jwt-key-change-this-in-production", description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiration")
    
    # OAuth 2.0 Configuration
    OAUTH_CLIENT_ID: Optional[str] = Field(default=None, description="OAuth client ID")
    OAUTH_CLIENT_SECRET: Optional[str] = Field(default=None, description="OAuth client secret")
    OAUTH_REDIRECT_URI: str = Field(default="http://localhost:3000/auth/callback", description="OAuth redirect URI")
    OAUTH_SCOPES: List[str] = Field(default=["openid", "email", "profile"], description="OAuth scopes")
    
    # Google API Configuration
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, description="Google client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Google client secret")
    GOOGLE_REDIRECT_URI: str = Field(default="http://localhost:3000/auth/google/callback", description="Google redirect URI")
    GOOGLE_SCOPES: List[str] = Field(default=["https://www.googleapis.com/auth/classroom.courses.readonly"], description="Google scopes")
    
    # Security Settings
    SECRET_KEY: str = Field(default="your-super-secret-key-change-this-in-production", description="Secret key")
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "127.0.0.1"], description="Allowed hosts")
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://127.0.0.1:3000"], description="CORS origins")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="CORS allow credentials")
    CORS_ALLOW_METHODS: List[str] = Field(default=["GET", "POST", "PUT", "DELETE", "OPTIONS"], description="CORS allowed methods")
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"], description="CORS allowed headers")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    LOG_FORMAT: str = Field(default="json", description="Log format")
    LOG_FILE: Optional[str] = Field(default=None, description="Log file path")
    
    # Cache Configuration
    CACHE_TTL: int = Field(default=300, description="Cache TTL in seconds")
    CACHE_MAX_SIZE: int = Field(default=1000, description="Cache max size")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Rate limit requests")
    RATE_LIMIT_WINDOW: int = Field(default=60, description="Rate limit window in seconds")
    
    # Health Check Configuration
    HEALTH_CHECK_TIMEOUT: int = Field(default=5, description="Health check timeout")
    HEALTH_CHECK_RETRIES: int = Field(default=3, description="Health check retries")
    
    # Mock Services
    MOCK_GOOGLE_API: bool = Field(default=True, description="Mock Google API")
    MOCK_DATABASE: bool = Field(default=False, description="Mock database")
    MOCK_REDIS: bool = Field(default=False, description="Mock Redis")
    
    # Error Prevention
    ERROR_PREVENTION_ENABLED: bool = Field(default=True, description="Error prevention enabled")
    AUTO_CLEANUP_ENABLED: bool = Field(default=True, description="Auto cleanup enabled")
    GRACEFUL_SHUTDOWN_TIMEOUT: int = Field(default=30, description="Graceful shutdown timeout")
    
    # Performance Monitoring
    PERFORMANCE_MONITORING: bool = Field(default=True, description="Performance monitoring")
    METRICS_ENABLED: bool = Field(default=True, description="Metrics enabled")
    SLOW_QUERY_THRESHOLD: int = Field(default=1000, description="Slow query threshold in ms")
    
    # Development Settings
    DEV_MODE: bool = Field(default=True, description="Development mode")
    HOT_RELOAD: bool = Field(default=True, description="Hot reload")
    DEBUG_TOOLBAR: bool = Field(default=False, description="Debug toolbar")
    
    # Pydantic v2 Configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        use_enum_values=True
    )
    
    @field_validator('PORT')
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port number."""
        if not (1 <= v <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        return v
    
    @field_validator('JWT_SECRET_KEY')
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """Validate JWT secret key."""
        if len(v) < 32:
            raise ValueError("JWT secret key must be at least 32 characters long")
        return v
    
    @field_validator('CORS_ORIGINS')
    @classmethod
    def validate_cors_origins(cls, v: List[str]) -> List[str]:
        """Validate CORS origins."""
        if not v:
            raise ValueError("At least one CORS origin must be specified")
        return v


# Global settings instance
settings = Settings()