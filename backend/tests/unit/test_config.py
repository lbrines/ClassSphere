import pytest
from src.app.core.config import Settings

class TestSettings:
    """
    Test suite for the Settings class to ensure correct configuration loading and parsing.
    """

    def test_settings_creation(self):
        """
        Test that Settings object can be created and essential fields are present.
        """
        settings = Settings()
        assert settings is not None
        assert isinstance(settings.JWT_SECRET, str)
        assert isinstance(settings.GOOGLE_CLIENT_ID, str)
        assert isinstance(settings.GOOGLE_CLIENT_SECRET, str)

    def test_default_values(self):
        """
        Test that default values are correctly applied when not overridden by environment variables.
        """
        settings = Settings()
        assert settings.ENVIRONMENT == "development"
        assert settings.PORT == 8000
        assert settings.JWT_ALGORITHM == "HS256"
        assert settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert settings.DEFAULT_MODE == "MOCK"
        assert settings.TRUSTED_HOST_ENABLED is False

    def test_cors_origins_parsing(self):
        """
        Test that CORS_ORIGINS are parsed correctly as a list of strings.
        """
        settings = Settings()
        assert isinstance(settings.CORS_ORIGINS, list)
        assert "http://localhost:3000" in settings.CORS_ORIGINS
        assert "http://127.0.0.1:3000" in settings.CORS_ORIGINS

    def test_trusted_hosts_parsing(self):
        """
        Test that TRUSTED_HOST_ALLOWED are parsed correctly as a list of strings.
        """
        settings = Settings()
        assert isinstance(settings.TRUSTED_HOST_ALLOWED, list)
        assert "localhost" in settings.TRUSTED_HOST_ALLOWED
        assert "127.0.0.1" in settings.TRUSTED_HOST_ALLOWED

    def test_google_scopes_parsing(self):
        """
        Test that GOOGLE_API_SCOPES are parsed correctly as a list of strings.
        """
        settings = Settings()
        assert isinstance(settings.GOOGLE_API_SCOPES, list)
        assert "https://www.googleapis.com/auth/classroom.courses" in settings.GOOGLE_API_SCOPES

    def test_jwt_configuration(self):
        """
        Test specific JWT configuration fields.
        """
        settings = Settings()
        assert settings.JWT_SUBJECT_FIELD == "email"
        assert settings.JWT_INCLUDE_EMAIL is True
        assert settings.JWT_INCLUDE_ROLE is True

    def test_oauth_configuration(self):
        """
        Test specific OAuth configuration fields.
        """
        settings = Settings()
        assert settings.GOOGLE_REDIRECT_URI == "http://localhost:8000/api/v1/oauth/google/callback"

    def test_database_configuration(self):
        """
        Test database connection URLs.
        """
        settings = Settings()
        assert "mongodb://" in settings.MONGODB_URL
        assert "redis://" in settings.REDIS_URL

    def test_security_configuration(self):
        """
        Test security-related configuration fields.
        """
        settings = Settings()
        assert settings.ERROR_SANITIZE_SENSITIVE_DATA is True
        assert settings.ERROR_FRIENDLY_MESSAGES is True

    def test_testing_configuration(self):
        """
        Test testing-related configuration fields.
        """
        settings = Settings()
        assert settings.TEST_COVERAGE_THRESHOLD_CRITICAL == 90
        assert settings.TEST_COVERAGE_THRESHOLD_GLOBAL == 80
