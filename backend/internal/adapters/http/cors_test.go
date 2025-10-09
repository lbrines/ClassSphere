package http

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/shared"
)

// TestCORS_AllowedOrigin verifies that requests from configured origins are allowed
func TestCORS_AllowedOrigin(t *testing.T) {
	// Setup environment
	t.Setenv("FRONTEND_URL", "http://localhost:4200")
	t.Setenv("APP_ENV", "development")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	// Create OPTIONS preflight request
	req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
	req.Header.Set("Origin", "http://localhost:4200")
	req.Header.Set("Access-Control-Request-Method", "GET")
	rec := httptest.NewRecorder()
	
	// Execute
	e.ServeHTTP(rec, req)
	
	// Assert
	assert.Equal(t, http.StatusNoContent, rec.Code, "Preflight should return 204")
	assert.Equal(t, "http://localhost:4200", rec.Header().Get("Access-Control-Allow-Origin"), 
		"Should allow configured origin")
	assert.Equal(t, "true", rec.Header().Get("Access-Control-Allow-Credentials"), 
		"Should allow credentials")
	assert.NotEmpty(t, rec.Header().Get("Access-Control-Allow-Methods"), 
		"Should include allowed methods")
}

// TestCORS_DisallowedOrigin verifies that requests from non-configured origins are blocked
func TestCORS_DisallowedOrigin(t *testing.T) {
	// Setup environment
	t.Setenv("FRONTEND_URL", "http://localhost:4200")
	t.Setenv("APP_ENV", "development")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	// Create OPTIONS request from malicious origin
	req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
	req.Header.Set("Origin", "https://malicious-site.com")
	req.Header.Set("Access-Control-Request-Method", "GET")
	rec := httptest.NewRecorder()
	
	// Execute
	e.ServeHTTP(rec, req)
	
	// Assert - No CORS headers should be present for disallowed origin
	assert.Empty(t, rec.Header().Get("Access-Control-Allow-Origin"), 
		"Should NOT allow non-configured origin")
}

// TestCORS_AllowedMethods verifies that only configured HTTP methods are allowed
func TestCORS_AllowedMethods(t *testing.T) {
	// Setup environment
	t.Setenv("FRONTEND_URL", "http://localhost:4200")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	// Create OPTIONS request
	req := httptest.NewRequest(http.MethodOptions, "/api/v1/auth/login", nil)
	req.Header.Set("Origin", "http://localhost:4200")
	req.Header.Set("Access-Control-Request-Method", "POST")
	rec := httptest.NewRecorder()
	
	// Execute
	e.ServeHTTP(rec, req)
	
	// Assert
	allowedMethods := rec.Header().Get("Access-Control-Allow-Methods")
	assert.Contains(t, allowedMethods, "POST", "Should allow POST method")
	assert.Contains(t, allowedMethods, "GET", "Should allow GET method")
	assert.Contains(t, allowedMethods, "OPTIONS", "Should allow OPTIONS method")
}

// TestCORS_AllowedHeaders verifies that required headers are allowed
func TestCORS_AllowedHeaders(t *testing.T) {
	// Setup environment
	t.Setenv("FRONTEND_URL", "http://localhost:4200")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	// Create OPTIONS request
	req := httptest.NewRequest(http.MethodOptions, "/api/v1/users/me", nil)
	req.Header.Set("Origin", "http://localhost:4200")
	req.Header.Set("Access-Control-Request-Method", "GET")
	req.Header.Set("Access-Control-Request-Headers", "Authorization, Content-Type")
	rec := httptest.NewRecorder()
	
	// Execute
	e.ServeHTTP(rec, req)
	
	// Assert
	allowedHeaders := rec.Header().Get("Access-Control-Allow-Headers")
	assert.Contains(t, allowedHeaders, "Authorization", "Should allow Authorization header")
	assert.Contains(t, allowedHeaders, "Content-Type", "Should allow Content-Type header")
}

// TestCORS_ProductionOrigins verifies that production origins work correctly
func TestCORS_ProductionOrigins(t *testing.T) {
	// Setup production environment
	t.Setenv("FRONTEND_URL", "https://classsphere.com")
	t.Setenv("APP_ENV", "production")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	// Create OPTIONS request from production origin
	req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
	req.Header.Set("Origin", "https://classsphere.com")
	req.Header.Set("Access-Control-Request-Method", "GET")
	rec := httptest.NewRecorder()
	
	// Execute
	e.ServeHTTP(rec, req)
	
	// Assert
	assert.Equal(t, "https://classsphere.com", rec.Header().Get("Access-Control-Allow-Origin"),
		"Should allow production origin")
}

// TestCORS_MultipleOrigins verifies that multiple origins can be configured
func TestCORS_MultipleOrigins(t *testing.T) {
	// Setup multiple allowed origins
	t.Setenv("ALLOWED_ORIGINS", "https://classsphere.com,https://app.classsphere.com,http://localhost:4200")
	t.Setenv("APP_ENV", "production")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	testCases := []struct {
		name          string
		origin        string
		shouldBeAllowed bool
	}{
		{
			name:          "First origin allowed",
			origin:        "https://classsphere.com",
			shouldBeAllowed: true,
		},
		{
			name:          "Second origin allowed",
			origin:        "https://app.classsphere.com",
			shouldBeAllowed: true,
		},
		{
			name:          "Third origin allowed",
			origin:        "http://localhost:4200",
			shouldBeAllowed: true,
		},
		{
			name:          "Non-configured origin blocked",
			origin:        "https://evil.com",
			shouldBeAllowed: false,
		},
	}
	
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
			req.Header.Set("Origin", tc.origin)
			req.Header.Set("Access-Control-Request-Method", "GET")
			rec := httptest.NewRecorder()
			
			e.ServeHTTP(rec, req)
			
			if tc.shouldBeAllowed {
				assert.Equal(t, tc.origin, rec.Header().Get("Access-Control-Allow-Origin"),
					"Origin %s should be allowed", tc.origin)
			} else {
				assert.Empty(t, rec.Header().Get("Access-Control-Allow-Origin"),
					"Origin %s should NOT be allowed", tc.origin)
			}
		})
	}
}

// TestCORS_MaxAge verifies that CORS max age is set
func TestCORS_MaxAge(t *testing.T) {
	// Setup environment
	t.Setenv("FRONTEND_URL", "http://localhost:4200")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	// Create OPTIONS request
	req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
	req.Header.Set("Origin", "http://localhost:4200")
	req.Header.Set("Access-Control-Request-Method", "GET")
	rec := httptest.NewRecorder()
	
	// Execute
	e.ServeHTTP(rec, req)
	
	// Assert
	maxAge := rec.Header().Get("Access-Control-Max-Age")
	assert.NotEmpty(t, maxAge, "Should set Max-Age header")
	assert.Equal(t, "3600", maxAge, "Max-Age should be 3600 seconds (1 hour)")
}

// TestCORS_ActualRequest verifies CORS headers on actual requests (not just preflight)
func TestCORS_ActualRequest(t *testing.T) {
	// Setup environment
	t.Setenv("FRONTEND_URL", "http://localhost:4200")
	t.Setenv("JWT_SECRET", "test-secret-key-for-cors-test")
	t.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	t.Setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost:4200/callback")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	// Create actual GET request (not OPTIONS)
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	req.Header.Set("Origin", "http://localhost:4200")
	rec := httptest.NewRecorder()
	
	// Execute
	e.ServeHTTP(rec, req)
	
	// Assert
	assert.Equal(t, http.StatusOK, rec.Code)
	assert.Equal(t, "http://localhost:4200", rec.Header().Get("Access-Control-Allow-Origin"),
		"Actual request should also have CORS headers")
}

// ============================================
// NEW TDD TESTS - Runtime Config Support
// ============================================

// TestCORS_RuntimeConfig_LocalhostPort80 verifies localhost:80 is allowed (fixes current bug)
func TestCORS_RuntimeConfig_LocalhostPort80(t *testing.T) {
	// Setup environment for mock mode with localhost:80
	t.Setenv("APP_ENV", "development")
	t.Setenv("ALLOWED_ORIGINS", "http://localhost,http://localhost:80,http://localhost:4200")
	
	// Setup server with CORS
	e := setupTestServerWithCORS(t)
	
	testCases := []struct {
		name   string
		origin string
	}{
		{"Localhost no port", "http://localhost"},
		{"Localhost port 80", "http://localhost:80"},
		{"Localhost port 4200", "http://localhost:4200"},
	}
	
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodOptions, "/api/v1/auth/login", nil)
			req.Header.Set("Origin", tc.origin)
			req.Header.Set("Access-Control-Request-Method", "POST")
			rec := httptest.NewRecorder()
			
			e.ServeHTTP(rec, req)
			
			assert.Equal(t, tc.origin, rec.Header().Get("Access-Control-Allow-Origin"),
				"Should allow %s origin", tc.origin)
			assert.Equal(t, "true", rec.Header().Get("Access-Control-Allow-Credentials"))
		})
	}
}

// TestCORS_RuntimeConfig_MockMode verifies mock mode CORS configuration
func TestCORS_RuntimeConfig_MockMode(t *testing.T) {
	// Setup mock mode environment
	t.Setenv("APP_ENV", "development")
	t.Setenv("CLASSROOM_MODE", "mock")
	t.Setenv("ALLOWED_ORIGINS", "http://localhost,http://localhost:80,http://localhost:4200")
	
	// Setup server
	e := setupTestServerWithCORS(t)
	
	// Test from localhost:80 (where frontend container runs)
	req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", nil)
	req.Header.Set("Origin", "http://localhost:80")
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	
	e.ServeHTTP(rec, req)
	
	// Assert CORS headers present
	assert.NotEmpty(t, rec.Header().Get("Access-Control-Allow-Origin"),
		"Mock mode should allow localhost:80")
}

// TestCORS_RuntimeConfig_ProductionMode verifies production CORS is restrictive
func TestCORS_RuntimeConfig_ProductionMode(t *testing.T) {
	// Setup production environment
	t.Setenv("APP_ENV", "production")
	t.Setenv("ALLOWED_ORIGINS", "https://api.classsphere.example")
	
	// Setup server
	e := setupTestServerWithCORS(t)
	
	testCases := []struct {
		name            string
		origin          string
		shouldBeAllowed bool
	}{
		{"Production origin", "https://api.classsphere.example", true},
		{"Localhost blocked", "http://localhost", false},
		{"Localhost:80 blocked", "http://localhost:80", false},
		{"Evil origin blocked", "https://evil.com", false},
	}
	
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
			req.Header.Set("Origin", tc.origin)
			req.Header.Set("Access-Control-Request-Method", "GET")
			rec := httptest.NewRecorder()
			
			e.ServeHTTP(rec, req)
			
			if tc.shouldBeAllowed {
				assert.Equal(t, tc.origin, rec.Header().Get("Access-Control-Allow-Origin"))
			} else {
				assert.Empty(t, rec.Header().Get("Access-Control-Allow-Origin"))
			}
		})
	}
}

// TestCORS_RuntimeConfig_FallbackToDefault verifies default fallback works
func TestCORS_RuntimeConfig_FallbackToDefault(t *testing.T) {
	// Setup environment without ALLOWED_ORIGINS (should use FrontendURL)
	t.Setenv("APP_ENV", "development")
	t.Setenv("FRONTEND_URL", "http://localhost:4200")
	// Explicitly unset ALLOWED_ORIGINS
	t.Setenv("ALLOWED_ORIGINS", "")
	
	// Setup server
	e := setupTestServerWithCORS(t)
	
	// Should allow FrontendURL
	req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
	req.Header.Set("Origin", "http://localhost:4200")
	req.Header.Set("Access-Control-Request-Method", "GET")
	rec := httptest.NewRecorder()
	
	e.ServeHTTP(rec, req)
	
	assert.Equal(t, "http://localhost:4200", rec.Header().Get("Access-Control-Allow-Origin"),
		"Should fallback to FrontendURL when ALLOWED_ORIGINS not set")
}

// TestCORS_RuntimeConfig_TestMode verifies test environment configuration
func TestCORS_RuntimeConfig_TestMode(t *testing.T) {
	// Setup test environment
	t.Setenv("APP_ENV", "test")
	t.Setenv("ALLOWED_ORIGINS", "http://backend:8080,http://frontend:80")
	
	// Setup server
	e := setupTestServerWithCORS(t)
	
	testCases := []struct {
		name   string
		origin string
	}{
		{"Backend container", "http://backend:8080"},
		{"Frontend container", "http://frontend:80"},
	}
	
	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			req := httptest.NewRequest(http.MethodOptions, "/api/v1/health", nil)
			req.Header.Set("Origin", tc.origin)
			req.Header.Set("Access-Control-Request-Method", "GET")
			rec := httptest.NewRecorder()
			
			e.ServeHTTP(rec, req)
			
			assert.Equal(t, tc.origin, rec.Header().Get("Access-Control-Allow-Origin"))
		})
	}
}

// setupTestServerWithCORS creates a test Echo server with CORS configuration
func setupTestServerWithCORS(t *testing.T) *echo.Echo {
	// Load config from environment
	cfg, err := shared.LoadConfig()
	require.NoError(t, err, "Failed to load config")
	
	// Create minimal test server with CORS
	e := echo.New()
	e.HideBanner = true
	
	// Apply CORS middleware
	ConfigureCORS(e, cfg)
	
	// Add a simple health endpoint for testing
	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	
	// Add API group
	api := e.Group("/api/v1")
	api.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	api.POST("/auth/login", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"token": "test"})
	})
	
	return e
}

