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
	
	return e
}

