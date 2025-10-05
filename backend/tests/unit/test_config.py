"""
Tests para configuración
"""
import pytest
from app.core.config import Settings


def test_settings_creation():
    """Test creación de settings"""
    settings = Settings(secret_key="test-key")
    assert settings.app_name == "ClassSphere"
    assert settings.port == 8000


def test_settings_from_env(monkeypatch):
    """Test settings desde variables de entorno"""
    monkeypatch.setenv("SECRET_KEY", "env-secret")
    monkeypatch.setenv("PORT", "9000")
    
    settings = Settings()
    assert settings.secret_key == "env-secret"
    assert settings.port == 9000
