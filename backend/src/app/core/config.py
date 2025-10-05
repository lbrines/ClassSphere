"""
Configuración de la aplicación con Pydantic v2
Prevención Pattern 1: ConfigDict import obligatorio
"""
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Application
    app_name: str = "ClassSphere"
    app_version: str = "1.0.0"
    debug: bool = True

    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:3000/auth/callback"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    model_config = ConfigDict(
        env_file="/home/lbrines/projects/AI/ClassSphere/backend/.env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()