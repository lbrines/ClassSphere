"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def admin_token(client):
    """Admin authentication token"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@classsphere.com", "password": "admin123"}
    )
    return response.json()["token"]["access_token"]


@pytest.fixture
def coordinator_token(client):
    """Coordinator authentication token"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "coordinator@classsphere.com", "password": "coord123"}
    )
    return response.json()["token"]["access_token"]


@pytest.fixture
def teacher_token(client):
    """Teacher authentication token"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "teacher@classsphere.com", "password": "teacher123"}
    )
    return response.json()["token"]["access_token"]


@pytest.fixture
def student_token(client):
    """Student authentication token"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "student@classsphere.com", "password": "student123"}
    )
    return response.json()["token"]["access_token"]


@pytest.fixture
def auth_headers():
    """Helper to create auth headers"""
    def _auth_headers(token):
        return {"Authorization": f"Bearer {token}"}
    return _auth_headers