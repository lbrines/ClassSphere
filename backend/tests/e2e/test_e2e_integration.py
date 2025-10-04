"""
Dashboard Educativo - E2E Tests
Context-Aware Implementation - Day 10 Medium Priority
"""

import pytest
import asyncio
from playwright.async_api import async_playwright
import httpx
import json


class TestE2EIntegration:
    """End-to-End Integration Tests with Context Tracking"""
    
    @pytest.fixture
    async def browser_context(self):
        """Browser context fixture"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            yield context
            await browser.close()
    
    @pytest.fixture
    def backend_url(self):
        """Backend URL fixture"""
        return "http://127.0.0.1:8003"
    
    @pytest.fixture
    def context_id(self):
        """Context ID for testing"""
        return "test-e2e-integration-001"
    
    async def test_backend_health_e2e(self, backend_url, context_id):
        """Test backend health endpoint E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Backend health test started")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{backend_url}/api/v1/health")
            
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "status" in data
            assert data["status"] == "healthy"
            assert "context_management" in data
            
            # Verify context health
            context_health = data["context_management"]["context_health"]
            assert context_health["healthy"] == True
            
            print(f"[CONTEXT-{context_id}] E2E Backend health test completed successfully")
    
    async def test_auth_flow_e2e(self, backend_url, context_id):
        """Test authentication flow E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Auth flow test started")
        
        async with httpx.AsyncClient() as client:
            # Test login
            login_data = {
                "username": "test_user",
                "password": "test_password"
            }
            
            login_response = await client.post(f"{backend_url}/api/v1/auth/login", json=login_data)
            assert login_response.status_code == 200
            
            login_data = login_response.json()
            access_token = login_data["access_token"]
            
            # Test protected endpoint
            headers = {"Authorization": f"Bearer {access_token}"}
            me_response = await client.get(f"{backend_url}/api/v1/auth/me", headers=headers)
            assert me_response.status_code == 200
            
            me_data = me_response.json()
            assert "user_id" in me_data
            assert "username" in me_data
            
            print(f"[CONTEXT-{context_id}] E2E Auth flow test completed successfully")
    
    async def test_google_oauth_e2e(self, backend_url, context_id):
        """Test Google OAuth flow E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Google OAuth test started")
        
        async with httpx.AsyncClient() as client:
            # Test OAuth authorization URL
            auth_response = await client.get(f"{backend_url}/api/v1/auth/google/authorize")
            assert auth_response.status_code == 200
            
            auth_data = auth_response.json()
            assert "authorization_url" in auth_data
            assert "state" in auth_data
            assert "scopes" in auth_data
            
            # Verify authorization URL
            auth_url = auth_data["authorization_url"]
            assert "https://accounts.google.com/o/oauth2/v2/auth" in auth_url
            
            print(f"[CONTEXT-{context_id}] E2E Google OAuth test completed successfully")
    
    async def test_google_api_e2e(self, backend_url, context_id):
        """Test Google API E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Google API test started")
        
        async with httpx.AsyncClient() as client:
            # Test Google API health
            google_response = await client.get(f"{backend_url}/api/v1/google/health")
            assert google_response.status_code == 200
            
            google_data = google_response.json()
            assert "status" in google_data
            assert google_data["status"] == "healthy"
            assert "service" in google_data
            assert google_data["service"] == "google_classroom"
            
            print(f"[CONTEXT-{context_id}] E2E Google API test completed successfully")
    
    async def test_context_logging_e2e(self, backend_url, context_id):
        """Test context logging E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Context logging test started")
        
        async with httpx.AsyncClient() as client:
            # Make multiple requests to generate context logs
            for i in range(3):
                response = await client.get(f"{backend_url}/api/v1/health")
                assert response.status_code == 200
            
            # Test that context logging is working
            # This would typically check the context log file
            # For now, we'll verify the health endpoint includes context data
            
            response = await client.get(f"{backend_url}/api/v1/health")
            data = response.json()
            
            # Verify context management data is present
            assert "context_management" in data
            context_management = data["context_management"]
            assert "context_log_path" in context_management
            assert "context_health" in context_management
            
            print(f"[CONTEXT-{context_id}] E2E Context logging test completed successfully")
    
    async def test_error_handling_e2e(self, backend_url, context_id):
        """Test error handling E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Error handling test started")
        
        async with httpx.AsyncClient() as client:
            # Test invalid endpoint
            response = await client.get(f"{backend_url}/api/v1/invalid-endpoint")
            assert response.status_code == 404
            
            # Test invalid token
            headers = {"Authorization": "Bearer invalid_token"}
            response = await client.get(f"{backend_url}/api/v1/auth/me", headers=headers)
            assert response.status_code == 401
            
            data = response.json()
            assert "detail" in data
            
            print(f"[CONTEXT-{context_id}] E2E Error handling test completed successfully")
    
    async def test_performance_e2e(self, backend_url, context_id):
        """Test performance E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Performance test started")
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            import time
            
            # Test response time
            start_time = time.time()
            response = await client.get(f"{backend_url}/api/v1/health")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Verify response time is under 2 seconds
            assert response_time < 2.0
            assert response.status_code == 200
            
            print(f"[CONTEXT-{context_id}] E2E Performance test completed successfully - Response time: {response_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_full_integration_e2e(self, browser_context, backend_url, context_id):
        """Test full integration E2E"""
        
        # Log test start
        print(f"[CONTEXT-{context_id}] E2E Full integration test started")
        
        # Test backend is running
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{backend_url}/api/v1/health")
            assert response.status_code == 200
        
        # Test all major endpoints
        endpoints_to_test = [
            "/api/v1/health",
            "/api/v1/auth/google/authorize",
            "/api/v1/google/health"
        ]
        
        async with httpx.AsyncClient() as client:
            for endpoint in endpoints_to_test:
                response = await client.get(f"{backend_url}{endpoint}")
                assert response.status_code == 200
                print(f"[CONTEXT-{context_id}] Endpoint {endpoint} working correctly")
        
        print(f"[CONTEXT-{context_id}] E2E Full integration test completed successfully")