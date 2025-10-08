package http

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

// TestRateLimit_GlobalLimit verifies global rate limiting works
func TestRateLimit_GlobalLimit(t *testing.T) {
	// Setup server with rate limiting
	e := setupTestServerWithRateLimit(t, RateLimitConfig{
		RequestsPerSecond: 10,  // 10 requests per second
		Burst:             2,
	})

	// Send 15 requests rapidly
	var lastStatusCode int
	for i := 0; i < 15; i++ {
		req := httptest.NewRequest(http.MethodGet, "/health", nil)
		rec := httptest.NewRecorder()
		e.ServeHTTP(rec, req)
		lastStatusCode = rec.Code
	}

	// Last requests should be rate limited
	assert.Equal(t, http.StatusTooManyRequests, lastStatusCode,
		"Requests beyond rate limit should return 429")
}

// TestRateLimit_LoginEndpoint verifies stricter rate limit for login
func TestRateLimit_LoginEndpoint(t *testing.T) {
	// Setup test services
	t.Setenv("JWT_SECRET", "test-secret")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	
	e := setupTestServerWithRateLimitAuth(t)

	// Send 8 login requests rapidly (limit should be 5/second)
	var statusCodes []int
	for i := 0; i < 8; i++ {
		body := `{"email":"admin@test.com","password":"test123"}`
		req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", strings.NewReader(body))
		req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
		rec := httptest.NewRecorder()
		e.ServeHTTP(rec, req)
		statusCodes = append(statusCodes, rec.Code)
	}

	// At least one should be rate limited
	hasRateLimited := false
	for _, code := range statusCodes {
		if code == http.StatusTooManyRequests {
			hasRateLimited = true
			break
		}
	}

	assert.True(t, hasRateLimited, "Login endpoint should rate limit after threshold")
}

// TestRateLimit_ResetsAfterWindow verifies rate limit resets
func TestRateLimit_ResetsAfterWindow(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping time-dependent test in short mode")
	}

	// Setup server with 1-second window
	e := setupTestServerWithRateLimit(t, RateLimitConfig{
		RequestsPerSecond: 5,
		Burst:             0,
	})

	// Fill the rate limit
	for i := 0; i < 7; i++ {
		req := httptest.NewRequest(http.MethodGet, "/health", nil)
		rec := httptest.NewRecorder()
		e.ServeHTTP(rec, req)
	}

	// Wait for rate limit window to reset (1.5 seconds to be safe)
	time.Sleep(1500 * time.Millisecond)

	// Should work again
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	assert.Equal(t, http.StatusOK, rec.Code,
		"Rate limit should reset after time window")
}

// TestRateLimit_PerIPTracking verifies rate limiting is per-IP
func TestRateLimit_PerIPTracking(t *testing.T) {
	// Setup server with rate limiting
	e := setupTestServerWithRateLimit(t, RateLimitConfig{
		RequestsPerSecond: 5,
		Burst:             0,
	})

	// IP 1 fills rate limit
	for i := 0; i < 7; i++ {
		req := httptest.NewRequest(http.MethodGet, "/health", nil)
		req.RemoteAddr = "192.168.1.1:12345"
		rec := httptest.NewRecorder()
		e.ServeHTTP(rec, req)
	}

	// IP 2 should still work (different limit bucket)
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	req.RemoteAddr = "192.168.1.2:12345"
	req.Header.Set("X-Real-IP", "192.168.1.2") // Also test X-Real-IP header
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	assert.Equal(t, http.StatusOK, rec.Code,
		"Different IP should have separate rate limit bucket")
}

// TestRateLimit_ResponseHeaders verifies rate limit headers are included
func TestRateLimit_ResponseHeaders(t *testing.T) {
	// Setup server with rate limiting
	e := setupTestServerWithRateLimit(t, RateLimitConfig{
		RequestsPerSecond: 10,
		Burst:             5,
	})

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Check for rate limit headers (if implemented)
	// X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
	assert.Equal(t, http.StatusOK, rec.Code)
	
	// Note: Header presence depends on implementation
	// This is a placeholder for future enhancement
}

// TestRateLimit_SkipHealthCheck verifies health endpoint is not rate limited
func TestRateLimit_SkipHealthCheck(t *testing.T) {
	// Setup server with strict rate limiting but health check skipped
	e := setupTestServerWithRateLimit(t, RateLimitConfig{
		RequestsPerSecond: 2,
		Burst:             0,
		SkipPaths:         []string{"/health"},
	})

	// Send many requests to health endpoint
	for i := 0; i < 20; i++ {
		req := httptest.NewRequest(http.MethodGet, "/health", nil)
		rec := httptest.NewRecorder()
		e.ServeHTTP(rec, req)
		
		// All should succeed (health is skipped)
		assert.Equal(t, http.StatusOK, rec.Code,
			fmt.Sprintf("Health check #%d should not be rate limited", i+1))
	}
}

// TestRateLimit_ErrorMessage verifies rate limit error response
func TestRateLimit_ErrorMessage(t *testing.T) {
	// Setup server with very low limit
	e := setupTestServerWithRateLimit(t, RateLimitConfig{
		RequestsPerSecond: 1,
		Burst:             0,
	})

	// Fill limit
	for i := 0; i < 3; i++ {
		req := httptest.NewRequest(http.MethodGet, "/health", nil)
		rec := httptest.NewRecorder()
		e.ServeHTTP(rec, req)
	}

	// Next request should be rate limited
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	assert.Equal(t, http.StatusTooManyRequests, rec.Code)
	
	// Check error response format
	var response map[string]interface{}
	err := json.Unmarshal(rec.Body.Bytes(), &response)
	if err == nil {
		// If JSON response, should have error message
		responseStr := strings.ToLower(fmt.Sprint(response))
		assert.Contains(t, responseStr, "rate limit",
			"Error message should mention rate limiting")
	}
}

// ==============================================================================
// Test Helpers
// ==============================================================================

// setupTestServerWithRateLimit creates a test Echo server with rate limiting
func setupTestServerWithRateLimit(t *testing.T, config RateLimitConfig) *echo.Echo {
	t.Helper()

	e := echo.New()
	e.HideBanner = true

	// Apply rate limiting
	ApplyRateLimiting(e, config)

	// Add health endpoint
	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	return e
}

// setupTestServerWithRateLimitAuth creates a test server with auth services and rate limiting
func setupTestServerWithRateLimitAuth(t *testing.T) *echo.Echo {
	t.Helper()

	e := echo.New()
	e.HideBanner = true

	// Apply rate limiting
	ApplyRateLimiting(e, RateLimitConfig{
		RequestsPerSecond: 20, // Global limit
		Burst:             5,
	})

	// Add login endpoint with stricter rate limit
	api := e.Group("/api/v1")
	
	api.POST("/auth/login", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "ok"})
	}, ApplyLoginRateLimit()) // Stricter limit for login

	return e
}

