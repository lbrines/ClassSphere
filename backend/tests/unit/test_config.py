import pytest
from src.app.core.config import Settings, settings

class TestSettings:
    def test_default_values(self):
        test_settings = Settings()
        assert test_settings.app_name == "Dashboard Educativo"
        assert test_settings.app_version == "0.1.0"
        assert test_settings.debug is True
        assert test_settings.environment == "development"
    
    def test_secret_key_required(self):
        test_settings = Settings()
        assert test_settings.secret_key is not None
        assert len(test_settings.secret_key) > 0
    
    def test_database_urls(self):
        test_settings = Settings()
        assert test_settings.mongodb_url is not None
        assert test_settings.redis_url is not None
    
    def test_google_settings(self):
        test_settings = Settings()
        assert test_settings.google_client_id is not None
        assert test_settings.google_client_secret is not None
    
    def test_settings_singleton(self):
        assert settings is not None
        assert isinstance(settings, Settings)