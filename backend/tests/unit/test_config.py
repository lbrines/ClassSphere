"""
Unit tests for configuration module
"""
import os
import pytest
from pydantic import ValidationError

from src.app.core.config import Settings


class TestSettings:
    """Test cases for Settings configuration."""
    
    def test_settings_default_values(self):
        """Test that settings have correct default values."""
        # Clear environment variables that might affect defaults
        import os
        original_debug = os.environ.get("DEBUG")
        if "DEBUG" in os.environ:
            del os.environ["DEBUG"]
        
        settings = Settings()
        
        assert settings.APP_NAME == "Dashboard Educativo"
        assert settings.APP_VERSION == "1.0.0"
        assert settings.DEBUG is False
        assert settings.HOST == "127.0.0.1"
        assert settings.PORT == 8000
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
        
        # Restore original environment
        if original_debug is not None:
            os.environ["DEBUG"] = original_debug
    
    def test_settings_from_env(self):
        """Test that settings can be loaded from environment variables."""
        os.environ.update({
            "APP_NAME": "Test App",
            "DEBUG": "true",
            "PORT": "9000",
            "JWT_SECRET_KEY": "test-secret"
        })
        
        settings = Settings()
        
        assert settings.APP_NAME == "Test App"
        assert settings.DEBUG is True
        assert settings.PORT == 9000
        assert settings.JWT_SECRET_KEY == "test-secret"
    
    def test_settings_validation(self):
        """Test settings validation."""
        # Test invalid port
        with pytest.raises(ValidationError):
            Settings(PORT=-1)
        
        # Test invalid JWT algorithm
        with pytest.raises(ValidationError):
            Settings(JWT_ALGORITHM="INVALID")
    
    def test_settings_model_config(self):
        """Test that model_config is properly set."""
        settings = Settings()
        
        assert hasattr(settings, 'model_config')
        assert settings.model_config['env_file'] == ".env"
        assert settings.model_config['case_sensitive'] is False
    
    def test_cors_origins_default(self):
        """Test default CORS origins."""
        settings = Settings()
        
        assert isinstance(settings.CORS_ORIGINS, list)
        assert "http://localhost:3000" in settings.CORS_ORIGINS
        assert "http://127.0.0.1:3000" in settings.CORS_ORIGINS
    
    def test_database_urls(self):
        """Test database URL configurations."""
        settings = Settings()
        
        assert settings.MONGODB_URL.startswith("mongodb://")
        assert settings.REDIS_URL.startswith("redis://")
    
    def test_google_config(self):
        """Test Google API configuration."""
        settings = Settings()
        
        assert isinstance(settings.GOOGLE_SCOPES, list)
        assert "https://www.googleapis.com/auth/classroom.courses.readonly" in settings.GOOGLE_SCOPES
    
    def test_security_settings(self):
        """Test security-related settings."""
        settings = Settings()
        
        assert settings.CORS_ALLOW_CREDENTIALS is True
        assert "GET" in settings.CORS_ALLOW_METHODS
        assert "POST" in settings.CORS_ALLOW_METHODS
        assert "*" in settings.CORS_ALLOW_HEADERS
    
    def test_rate_limiting_settings(self):
        """Test rate limiting configuration."""
        settings = Settings()
        
        assert settings.RATE_LIMIT_REQUESTS == 100
        assert settings.RATE_LIMIT_WINDOW == 60
        assert settings.GOOGLE_API_RATE_LIMIT == 100
        assert settings.GOOGLE_API_RATE_WINDOW == 100
    
    def test_cache_settings(self):
        """Test cache configuration."""
        settings = Settings()
        
        assert settings.CACHE_TTL_SECONDS == 300
        assert settings.CACHE_MAX_SIZE == 1000
    
    def test_health_check_settings(self):
        """Test health check configuration."""
        settings = Settings()
        
        assert settings.HEALTH_CHECK_TIMEOUT == 5
        assert settings.HEALTH_CHECK_RETRIES == 3
        assert settings.HEALTH_CHECK_INTERVAL == 30
    
    def test_error_prevention_settings(self):
        """Test error prevention configuration."""
        settings = Settings()
        
        assert settings.ERROR_PREVENTION_ENABLED is True
        assert settings.AUTO_CLEANUP_ENABLED is True
        assert settings.CONTEXT_MANAGER_TIMEOUT == 30
    
    def test_performance_settings(self):
        """Test performance configuration."""
        settings = Settings()
        
        assert settings.MAX_CONNECTIONS == 100
        assert settings.CONNECTION_TIMEOUT == 30
        assert settings.REQUEST_TIMEOUT == 60
    
    def test_monitoring_settings(self):
        """Test monitoring configuration."""
        settings = Settings()
        
        assert settings.METRICS_ENABLED is True
        assert settings.METRICS_PORT == 9090