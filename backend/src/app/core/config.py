from typing import List, Optional
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables or .env file.
    Uses Pydantic-Settings for robust configuration management.
    """
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
        json_encoders={
            # Custom JSON encoder for datetime objects
            # datetime: lambda v: v.isoformat()
        }
    )

    # General
    ENVIRONMENT: str = Field("development", description="Application environment (development, production, testing)")
    PORT: int = Field(8000, description="Port for the FastAPI application")

    # Python/Uvicorn Configuration
    PYTHONPATH: str = Field("/app/src", description="Python path for module imports")
    PYTHONUNBUFFERED: int = Field(1, description="Ensures Python output is unbuffered")
    UVICORN_HOST: str = Field("127.0.0.1", description="Uvicorn host for local development")
    UVICORN_PORT: int = Field(8000, description="Uvicorn port for local development")

    # Middleware Configuration
    TRUSTED_HOST_ENABLED: bool = Field(False, description="Enable TrustedHostMiddleware")
    TRUSTED_HOST_ALLOWED: List[str] = Field(["localhost", "127.0.0.1"], description="Allowed hosts for TrustedHostMiddleware")

    # JWT Configuration
    JWT_SECRET: str = Field("super-secret-jwt-key-change-this-in-production", description="Secret key for JWT encoding")
    JWT_ALGORITHM: str = Field("HS256", description="Algorithm for JWT encoding")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, description="Access token expiration in minutes")
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(10080, description="Refresh token expiration in minutes (7 days)")
    JWT_SUBJECT_FIELD: str = Field("email", description="Field used as 'sub' in JWT payload")
    JWT_INCLUDE_EMAIL: bool = Field(True, description="Include email in JWT payload")
    JWT_INCLUDE_ROLE: bool = Field(True, description="Include role in JWT payload")

    # OAuth 2.0 Google Configuration
    GOOGLE_CLIENT_ID: str = Field("your_google_client_id", description="Google OAuth Client ID")
    GOOGLE_CLIENT_SECRET: str = Field("your_google_client_secret", description="Google OAuth Client Secret")
    GOOGLE_REDIRECT_URI: str = Field("http://localhost:8000/api/v1/oauth/google/callback", description="Google OAuth Redirect URI")
    GOOGLE_API_SCOPES: List[str] = Field(
        ["https://www.googleapis.com/auth/classroom.courses",
         "https://www.googleapis.com/auth/classroom.rosters.readonly",
         "https://www.googleapis.com/auth/userinfo.email",
         "https://www.googleapis.com/auth/userinfo.profile"],
        description="Google API Scopes"
    )
    DEFAULT_MODE: str = Field("MOCK", description="Default operational mode (MOCK or GOOGLE)")

    # Database
    MONGODB_URL: str = Field("mongodb://localhost:27017/dashboard_educativo_dev", description="MongoDB connection URL")
    REDIS_URL: str = Field("redis://localhost:6379/0", description="Redis connection URL")

    # CORS
    CORS_ORIGINS: List[str] = Field(["http://localhost:3000", "http://127.0.0.1:3000"], description="Allowed CORS origins")

    # Testing & Quality
    TEST_COVERAGE_THRESHOLD_CRITICAL: int = Field(90, description="Minimum coverage for critical modules")
    TEST_COVERAGE_THRESHOLD_GLOBAL: int = Field(80, description="Minimum global test coverage")

    # Security
    ERROR_SANITIZE_SENSITIVE_DATA: bool = Field(True, description="Sanitize sensitive data in error responses")
    ERROR_FRIENDLY_MESSAGES: bool = Field(True, description="Provide friendly error messages in production")

settings = Settings()
