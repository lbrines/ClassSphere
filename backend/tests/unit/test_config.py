"""Tests for configuration module."""

import pytest
from unittest.mock import patch
from src.app.core.config import Settings, settings


class TestSettings:
    """Test Settings class."""

    def test_settings_defaults(self):
        """Test default settings values."""
        # Create settings without reading .env file
        test_settings = Settings(secret_key="test-secret", debug=False)

        assert test_settings.app_name == "Dashboard Educativo"
        assert test_settings.app_version == "1.0.0"
        assert test_settings.debug is False
        assert test_settings.port == 8000
        assert test_settings.host == "127.0.0.1"

    def test_settings_cors_origins_string(self):
        """Test CORS origins parsing from string."""
        test_settings = Settings(
            secret_key="test-secret",
            cors_origins="http://localhost:3000,http://127.0.0.1:3000"
        )

        assert test_settings.cors_origins == ["http://localhost:3000", "http://127.0.0.1:3000"]

    def test_settings_cors_origins_list(self):
        """Test CORS origins as list."""
        origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
        test_settings = Settings(
            secret_key="test-secret",
            cors_origins=origins
        )

        assert test_settings.cors_origins == origins

    def test_settings_properties(self):
        """Test settings properties."""
        # Development mode
        dev_settings = Settings(secret_key="test-secret", debug=True)
        assert dev_settings.is_development is True
        assert dev_settings.is_production is False

        # Production mode
        prod_settings = Settings(secret_key="test-secret", debug=False)
        assert prod_settings.is_development is False
        assert prod_settings.is_production is True

    def test_settings_redis_configuration(self):
        """Test Redis configuration."""
        test_settings = Settings(
            secret_key="test-secret",
            redis_url="redis://localhost:6380",
            redis_db=1
        )

        assert test_settings.redis_url == "redis://localhost:6380"
        assert test_settings.redis_db == 1

    def test_settings_google_configuration(self):
        """Test Google configuration."""
        test_settings = Settings(
            secret_key="test-secret",
            google_client_id="test-client-id",
            google_client_secret="test-client-secret"
        )

        assert test_settings.google_client_id == "test-client-id"
        assert test_settings.google_client_secret == "test-client-secret"

    def test_settings_mode_configuration(self):
        """Test mode configuration."""
        test_settings = Settings(
            secret_key="test-secret",
            google_mode=True,
            mock_mode=False
        )

        assert test_settings.google_mode is True
        assert test_settings.mock_mode is False

    def test_global_settings_instance(self):
        """Test global settings instance."""
        assert settings is not None
        assert isinstance(settings, Settings)

    @patch.dict('os.environ', {'SECRET_KEY': 'env-secret', 'DEBUG': 'true'})
    def test_settings_from_environment(self):
        """Test settings loading from environment."""
        test_settings = Settings()

        assert test_settings.secret_key == "env-secret"
        assert test_settings.debug is True

    def test_settings_config_dict(self):
        """Test ConfigDict configuration."""
        test_settings = Settings(secret_key="test-secret")

        # Verify ConfigDict is properly configured
        config = test_settings.model_config
        assert config["case_sensitive"] is False
        assert config["extra"] == "ignore"
        assert config["env_file"] == ".env"