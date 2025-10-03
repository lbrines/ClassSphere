"""
Unit tests for configuration module.
"""
import pytest
import os
from src.app.core.config import Settings


class TestSettings:
    """Test Settings class."""
    
    def test_settings_default_values(self):
        """Test default values."""
        import os
        original_debug = os.environ.get("DEBUG")
        if "DEBUG" in os.environ:
            del os.environ["DEBUG"]
        
        settings = Settings()
        
        assert settings.APP_NAME == "Dashboard Educativo"
        assert settings.APP_VERSION == "1.0.0"
        assert settings.DEBUG is False
        assert settings.ENVIRONMENT == "development"
        assert settings.HOST == "127.0.0.1"
        assert settings.PORT == 8000
        assert settings.MONGODB_URL == "mongodb://localhost:27017"
        assert settings.REDIS_URL == "redis://localhost:6379"
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
        
        if original_debug is not None:
            os.environ["DEBUG"] = original_debug
    
    def test_settings_environment_variables(self):
        """Test environment variable loading."""
        os.environ["APP_NAME"] = "Test App"
        os.environ["PORT"] = "9000"
        os.environ["DEBUG"] = "true"
        
        settings = Settings()
        
        assert settings.APP_NAME == "Test App"
        assert settings.PORT == 9000
        assert settings.DEBUG is True
        
        # Cleanup
        del os.environ["APP_NAME"]
        del os.environ["PORT"]
        del os.environ["DEBUG"]
    
    def test_settings_validation(self):
        """Test field validation."""
        # Test valid port
        settings = Settings(PORT=8080)
        assert settings.PORT == 8080
        
        # Test invalid port
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            Settings(PORT=70000)
        
        # Test invalid JWT secret
        with pytest.raises(ValueError, match="JWT secret key must be at least 32 characters"):
            Settings(JWT_SECRET_KEY="short")
    
    def test_settings_cors_configuration(self):
        """Test CORS configuration."""
        settings = Settings()
        
        assert isinstance(settings.CORS_ORIGINS, list)
        assert "http://localhost:3000" in settings.CORS_ORIGINS
        assert settings.CORS_ALLOW_CREDENTIALS is True
        assert "GET" in settings.CORS_ALLOW_METHODS
        assert "POST" in settings.CORS_ALLOW_METHODS
    
    def test_settings_database_configuration(self):
        """Test database configuration."""
        settings = Settings()
        
        assert settings.MONGODB_DATABASE == "dashboard_educativo"
        assert settings.MONGODB_MAX_CONNECTIONS == 10
        assert settings.MONGODB_MIN_CONNECTIONS == 1
        assert settings.REDIS_DB == 0
        assert settings.REDIS_MAX_CONNECTIONS == 10
    
    def test_settings_google_api_configuration(self):
        """Test Google API configuration."""
        settings = Settings()
        
        assert isinstance(settings.GOOGLE_SCOPES, list)
        assert "https://www.googleapis.com/auth/classroom.courses.readonly" in settings.GOOGLE_SCOPES
        assert settings.GOOGLE_REDIRECT_URI == "http://localhost:3000/auth/google/callback"
    
    def test_settings_model_config(self):
        """Test Pydantic v2 model configuration."""
        settings = Settings()
        
        assert hasattr(settings, 'model_config')
        assert settings.model_config.get('env_file') == '.env'
        assert settings.model_config.get('case_sensitive') is False
        assert settings.model_config.get('extra') == 'ignore'
    
    def test_settings_oauth_configuration(self):
        """Test OAuth configuration."""
        settings = Settings()
        
        assert isinstance(settings.OAUTH_SCOPES, list)
        assert "openid" in settings.OAUTH_SCOPES
        assert "email" in settings.OAUTH_SCOPES
        assert "profile" in settings.OAUTH_SCOPES
        assert settings.OAUTH_REDIRECT_URI == "http://localhost:3000/auth/callback"
    
    def test_settings_security_configuration(self):
        """Test security configuration."""
        settings = Settings()
        
        assert settings.SECRET_KEY is not None
        assert isinstance(settings.ALLOWED_HOSTS, list)
        assert "localhost" in settings.ALLOWED_HOSTS
        assert settings.CORS_ALLOW_CREDENTIALS is True
    
    def test_settings_logging_configuration(self):
        """Test logging configuration."""
        settings = Settings()
        
        assert settings.LOG_LEVEL == "INFO"
        assert settings.LOG_FORMAT == "json"
        assert settings.LOG_FILE is None
    
    def test_settings_cache_configuration(self):
        """Test cache configuration."""
        settings = Settings()
        
        assert settings.CACHE_TTL == 300
        assert settings.CACHE_MAX_SIZE == 1000
    
    def test_settings_rate_limiting_configuration(self):
        """Test rate limiting configuration."""
        settings = Settings()
        
        assert settings.RATE_LIMIT_REQUESTS == 100
        assert settings.RATE_LIMIT_WINDOW == 60
    
    def test_settings_health_check_configuration(self):
        """Test health check configuration."""
        settings = Settings()
        
        assert settings.HEALTH_CHECK_TIMEOUT == 5
        assert settings.HEALTH_CHECK_RETRIES == 3
    
    def test_settings_mock_services_configuration(self):
        """Test mock services configuration."""
        settings = Settings()
        
        assert settings.MOCK_GOOGLE_API is True
        assert settings.MOCK_DATABASE is False
        assert settings.MOCK_REDIS is False
    
    def test_settings_error_prevention_configuration(self):
        """Test error prevention configuration."""
        settings = Settings()
        
        assert settings.ERROR_PREVENTION_ENABLED is True
        assert settings.AUTO_CLEANUP_ENABLED is True
        assert settings.GRACEFUL_SHUTDOWN_TIMEOUT == 30
    
    def test_settings_performance_configuration(self):
        """Test performance configuration."""
        settings = Settings()
        
        assert settings.PERFORMANCE_MONITORING is True
        assert settings.METRICS_ENABLED is True
        assert settings.SLOW_QUERY_THRESHOLD == 1000
    
    def test_settings_development_configuration(self):
        """Test development configuration."""
        settings = Settings()
        
        assert settings.DEV_MODE is True
        assert settings.HOT_RELOAD is True
        assert settings.DEBUG_TOOLBAR is False