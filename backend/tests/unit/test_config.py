"""
Tests for configuration module
"""
import pytest
from src.app.core.config import Settings, settings


class TestSettings:
    """Test Settings class"""
    
    def test_default_values(self):
        """Test default configuration values"""
        test_settings = Settings()
        
        assert test_settings.app_name == "Dashboard Educativo"
        assert test_settings.app_version == "0.1.0"
        assert test_settings.debug is False
        assert test_settings.environment == "development"
        assert test_settings.secret_key == "your-secret-key-here"
        assert test_settings.access_token_expire_minutes == 30
        assert test_settings.refresh_token_expire_days == 7
    
    def test_mongodb_url_default(self):
        """Test MongoDB URL default value"""
        test_settings = Settings()
        assert test_settings.mongodb_url == "mongodb://localhost:27017/dashboard_educativo"
    
    def test_redis_url_default(self):
        """Test Redis URL default value"""
        test_settings = Settings()
        assert test_settings.redis_url == "redis://localhost:6379/0"
    
    def test_google_redirect_uri_default(self):
        """Test Google redirect URI default value"""
        test_settings = Settings()
        assert test_settings.google_redirect_uri == "http://localhost:8000/auth/google/callback"
    
    def test_upload_dir_default(self):
        """Test upload directory default value"""
        test_settings = Settings()
        assert test_settings.upload_dir == "uploads"
    
    def test_max_file_size_default(self):
        """Test max file size default value"""
        test_settings = Settings()
        assert test_settings.max_file_size == 10485760  # 10MB
    
    def test_log_level_default(self):
        """Test log level default value"""
        test_settings = Settings()
        assert test_settings.log_level == "INFO"
    
    def test_log_file_default(self):
        """Test log file default value"""
        test_settings = Settings()
        assert test_settings.log_file == "logs/app.log"
    
    def test_smtp_port_default(self):
        """Test SMTP port default value"""
        test_settings = Settings()
        assert test_settings.smtp_port == 587
    
    def test_smtp_tls_default(self):
        """Test SMTP TLS default value"""
        test_settings = Settings()
        assert test_settings.smtp_tls is True


class TestGlobalSettings:
    """Test global settings instance"""
    
    def test_global_settings_instance(self):
        """Test that global settings instance exists"""
        assert settings is not None
        assert isinstance(settings, Settings)
    
    def test_global_settings_values(self):
        """Test global settings values"""
        assert settings.app_name == "Dashboard Educativo"
        assert settings.app_version == "0.1.0"
