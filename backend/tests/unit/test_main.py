"""
Tests para la aplicación principal
"""
import pytest
from fastapi.testclient import TestClient
from app.main import create_app, app


def test_create_app():
    """Test creación de la aplicación"""
    test_app = create_app()
    assert test_app.title == "ClassSphere"
    assert test_app.version == "1.0.0"


def test_app_routes():
    """Test que la app tiene rutas configuradas"""
    test_app = create_app()
    routes = [route.path for route in test_app.routes]
    assert "/health" in routes


def test_app_instance():
    """Test que el módulo exporta una instancia de app"""
    assert app is not None
    assert hasattr(app, 'routes')


def test_lifespan_startup_shutdown():
    """Test lifespan startup y shutdown"""
    client = TestClient(app)
    # El TestClient ya maneja el lifespan automáticamente
    response = client.get("/health")
    assert response.status_code == 200
