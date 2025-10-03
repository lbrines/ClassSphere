"""
Configuration module for Dashboard Educativo Backend
Using Pydantic v2 with ConfigDict for modern configuration management
"""
import os
from typing import List, Optional
from pydantic import ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with Pydantic v2 configuration."""
    
    # Application Settings
    APP_NAME: str = Field(default="Dashboard Educativo", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    ENVIRONMENT: str = Field(default="production", description="Environment")
    
    # Server Configuration
    HOST: str = Field(default="127.0.0.1", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    WORKERS: int = Field(default=1, description="Number of workers")
    
    # Database Configuration
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URL"
    )
    MONGODB_DATABASE: str = Field(
        default="dashboard_educativo",
        description="MongoDB database name"
    )
    MONGODB_COLLECTION_USERS: str = Field(
        default="users",
        description="MongoDB users collection name"
    )
    MONGODB_COLLECTION_COURSES: str = Field(
        default="courses",
        description="MongoDB courses collection name"
    )
    MONGODB_COLLECTION_METRICS: str = Field(
        default="metrics",
        description="MongoDB metrics collection name"
    )
    
    # Redis Configuration
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL"
    )
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    
    # JWT Configuration
    JWT_SECRET_KEY: str = Field(
        default="your-super-secret-jwt-key-change-this-in-production",
        description="JWT secret key"
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="JWT access token expiration in minutes"
    )
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="JWT refresh token expiration in days"
    )
    
    # OAuth 2.0 Configuration
    GOOGLE_CLIENT_ID: str = Field(
        default="",
        description="Google OAuth client ID"
    )
    GOOGLE_CLIENT_SECRET: str = Field(
        default="",
        description="Google OAuth client secret"
    )
    GOOGLE_REDIRECT_URI: str = Field(
        default="http://localhost:8000/auth/google/callback",
        description="Google OAuth redirect URI"
    )
    GOOGLE_SCOPES: List[str] = Field(
        default=[
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.rosters.readonly"
        ],
        description="Google OAuth scopes"
    )
    
    # Google Classroom API
    GOOGLE_CLASSROOM_API_VERSION: str = Field(
        default="v1",
        description="Google Classroom API version"
    )
    GOOGLE_API_RATE_LIMIT: int = Field(
        default=100,
        description="Google API rate limit per window"
    )
    GOOGLE_API_RATE_WINDOW: int = Field(
        default=100,
        description="Google API rate limit window in seconds"
    )
    
    # Security Settings
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="CORS allowed origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True,
        description="CORS allow credentials"
    )
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="CORS allowed methods"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"],
        description="CORS allowed headers"
    )
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    LOG_FORMAT: str = Field(default="json", description="Log format")
    LOG_FILE: str = Field(default="logs/app.log", description="Log file path")
    
    # Cache Configuration
    CACHE_TTL_SECONDS: int = Field(
        default=300,
        description="Cache TTL in seconds"
    )
    CACHE_MAX_SIZE: int = Field(
        default=1000,
        description="Cache maximum size"
    )
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(
        default=100,
        description="Rate limit requests per window"
    )
    RATE_LIMIT_WINDOW: int = Field(
        default=60,
        description="Rate limit window in seconds"
    )
    
    # Health Check Configuration
    HEALTH_CHECK_TIMEOUT: int = Field(
        default=5,
        description="Health check timeout in seconds"
    )
    HEALTH_CHECK_RETRIES: int = Field(
        default=3,
        description="Health check retries"
    )
    HEALTH_CHECK_INTERVAL: int = Field(
        default=30,
        description="Health check interval in seconds"
    )
    
    # Mock Service Configuration
    MOCK_SERVICE_ENABLED: bool = Field(
        default=False,
        description="Enable mock service for development"
    )
    MOCK_DATA_PATH: str = Field(
        default="./mock_data/",
        description="Mock data path"
    )
    
    # Error Prevention Settings
    ERROR_PREVENTION_ENABLED: bool = Field(
        default=True,
        description="Enable error prevention features"
    )
    AUTO_CLEANUP_ENABLED: bool = Field(
        default=True,
        description="Enable automatic cleanup"
    )
    CONTEXT_MANAGER_TIMEOUT: int = Field(
        default=30,
        description="Context manager timeout in seconds"
    )
    
    # Performance Settings
    MAX_CONNECTIONS: int = Field(
        default=100,
        description="Maximum connections"
    )
    CONNECTION_TIMEOUT: int = Field(
        default=30,
        description="Connection timeout in seconds"
    )
    REQUEST_TIMEOUT: int = Field(
        default=60,
        description="Request timeout in seconds"
    )
    
    # Monitoring Settings
    METRICS_ENABLED: bool = Field(
        default=True,
        description="Enable metrics collection"
    )
    METRICS_PORT: int = Field(
        default=9090,
        description="Metrics port"
    )
    
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
    
    @field_validator('JWT_ALGORITHM')
    @classmethod
    def validate_jwt_algorithm(cls, v: str) -> str:
        """Validate JWT algorithm."""
        allowed_algorithms = ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
        if v not in allowed_algorithms:
            raise ValueError(f"JWT algorithm must be one of: {allowed_algorithms}")
        return v
    
    @field_validator('LOG_LEVEL')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v.upper()
    
    @field_validator('ENVIRONMENT')
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment."""
        allowed_environments = ["development", "staging", "production", "testing"]
        if v.lower() not in allowed_environments:
            raise ValueError(f"Environment must be one of: {allowed_environments}")
        return v.lower()


# Global settings instance
settings = Settings()