from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://classsphere_user:classsphere_pass@localhost:5432/classsphere"
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Google OAuth
    google_client_id: str = "your-google-client-id"
    google_client_secret: str = "your-google-client-secret"
    google_redirect_uri: str = "http://localhost:3000/oauth/callback"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

settings = Settings()
