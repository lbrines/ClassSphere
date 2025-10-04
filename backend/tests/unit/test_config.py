import pytest
from src.app.core.config import Settings

class TestSettings:
    def test_settings_default_values(self):
        """Test that settings have correct default values."""
        settings = Settings()
        
        # Database
        assert settings.database_url == "postgresql://classsphere_user:classsphere_pass@localhost:5432/classsphere"
        assert settings.redis_url == "redis://localhost:6379/0"
        
        # Security
        assert settings.secret_key == "your-secret-key-change-in-production"
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30
        assert settings.refresh_token_expire_days == 7
        
        # Google OAuth
        assert settings.google_client_id == "your-google-client-id"
        assert settings.google_client_secret == "your-google-client-secret"
        assert settings.google_redirect_uri == "http://localhost:3000/oauth/callback"
        
        # Server
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000
        assert settings.debug == True
        
        # CORS
        assert settings.allowed_origins == ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    def test_settings_port_type(self):
        """Test that port is integer type."""
        settings = Settings()
        assert isinstance(settings.port, int)
        assert settings.port == 8000
    
    def test_settings_allowed_origins_type(self):
        """Test that allowed_origins is list type."""
        settings = Settings()
        assert isinstance(settings.allowed_origins, list)
        assert len(settings.allowed_origins) == 2
