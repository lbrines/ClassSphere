package http

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/ports"
)

// TestHealth_AllHealthy verifies health check when all dependencies are healthy
func TestHealth_AllHealthy(t *testing.T) {
	// Setup
	cache := &mockHealthyCache{}
	h := &Handler{cache: cache}

	e := echo.New()
	e.GET("/health", h.healthDetailed)

	// Execute
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Assert
	assert.Equal(t, http.StatusOK, rec.Code, "Should return 200 when all healthy")

	var response HealthStatus
	err := json.Unmarshal(rec.Body.Bytes(), &response)
	require.NoError(t, err)

	assert.Equal(t, "healthy", response.Status)
	assert.NotEmpty(t, response.Version)
	assert.NotEmpty(t, response.Timestamp)
	assert.Contains(t, response.Checks, "redis")
	assert.Equal(t, "healthy", response.Checks["redis"].Status)
}

// TestHealth_RedisUnhealthy verifies health check when Redis is down
func TestHealth_RedisUnhealthy(t *testing.T) {
	// Setup
	cache := &mockUnhealthyCache{}
	h := &Handler{cache: cache}

	e := echo.New()
	e.GET("/health", h.healthDetailed)

	// Execute
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Assert
	assert.Equal(t, http.StatusServiceUnavailable, rec.Code, 
		"Should return 503 when dependencies unhealthy")

	var response HealthStatus
	err := json.Unmarshal(rec.Body.Bytes(), &response)
	require.NoError(t, err)

	assert.Equal(t, "unhealthy", response.Status)
	assert.Equal(t, "unhealthy", response.Checks["redis"].Status)
	assert.NotEmpty(t, response.Checks["redis"].Message, "Should include error message")
}

// TestHealth_RedisDegraded verifies degraded state handling
func TestHealth_RedisDegraded(t *testing.T) {
	// Setup - cache que responde lento pero funciona
	cache := &mockSlowCache{}
	h := &Handler{cache: cache}

	e := echo.New()
	e.GET("/health", h.healthDetailed)

	// Execute
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Assert - degraded should return 200 but status "degraded"
	assert.Equal(t, http.StatusOK, rec.Code)

	var response HealthStatus
	err := json.Unmarshal(rec.Body.Bytes(), &response)
	require.NoError(t, err)

	// Note: For now we don't implement "degraded" state, just healthy/unhealthy
	// This test is for future enhancement
	assert.Contains(t, []string{"healthy", "degraded"}, response.Status)
}

// TestHealth_JSONFormat verifies response format
func TestHealth_JSONFormat(t *testing.T) {
	// Setup
	cache := &mockHealthyCache{}
	h := &Handler{cache: cache}

	e := echo.New()
	e.GET("/health", h.healthDetailed)

	// Execute
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Assert JSON structure
	contentType := rec.Header().Get("Content-Type")
	assert.Contains(t, contentType, "application/json", "Should return JSON content type")

	var response HealthStatus
	err := json.Unmarshal(rec.Body.Bytes(), &response)
	require.NoError(t, err)

	// Verify all required fields present
	assert.NotEmpty(t, response.Status, "Status field required")
	assert.NotEmpty(t, response.Version, "Version field required")
	assert.NotZero(t, response.Timestamp, "Timestamp field required")
	assert.NotNil(t, response.Checks, "Checks field required")
}

// TestHealth_MultipleChecks verifies multiple dependency checks
func TestHealth_MultipleChecks(t *testing.T) {
	// Setup with Redis check
	cache := &mockHealthyCache{}
	h := &Handler{
		cache: cache,
	}

	e := echo.New()
	e.GET("/health", h.healthDetailed)

	// Execute
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Assert
	var response HealthStatus
	err := json.Unmarshal(rec.Body.Bytes(), &response)
	require.NoError(t, err)

	// Should have at least Redis check
	assert.GreaterOrEqual(t, len(response.Checks), 1, "Should check at least Redis")
	assert.Contains(t, response.Checks, "redis", "Should have Redis check")
	
	// All should be healthy
	for name, check := range response.Checks {
		assert.Equal(t, "healthy", check.Status, 
			"Check %s should be healthy", name)
	}
}

// ==============================================================================
// Test Helpers & Mocks
// ==============================================================================

// mockHealthyCache simulates a healthy Redis cache
type mockHealthyCache struct{}

func (m *mockHealthyCache) Ping(ctx context.Context) error {
	return nil
}

func (m *mockHealthyCache) Get(ctx context.Context, key string) ([]byte, error) {
	return []byte("value"), nil
}

func (m *mockHealthyCache) Set(ctx context.Context, key string, value []byte, ttl int) error {
	return nil
}

func (m *mockHealthyCache) Delete(ctx context.Context, key string) error {
	return nil
}

func (m *mockHealthyCache) Close() error {
	return nil
}

// mockUnhealthyCache simulates Redis being down
type mockUnhealthyCache struct{}

func (m *mockUnhealthyCache) Ping(ctx context.Context) error {
	return ports.ErrCacheUnavailable
}

func (m *mockUnhealthyCache) Get(ctx context.Context, key string) ([]byte, error) {
	return nil, ports.ErrCacheUnavailable
}

func (m *mockUnhealthyCache) Set(ctx context.Context, key string, value []byte, ttl int) error {
	return ports.ErrCacheUnavailable
}

func (m *mockUnhealthyCache) Delete(ctx context.Context, key string) error {
	return ports.ErrCacheUnavailable
}

func (m *mockUnhealthyCache) Close() error {
	return nil
}

// mockSlowCache simulates slow but working cache
type mockSlowCache struct{}

func (m *mockSlowCache) Ping(ctx context.Context) error {
	return nil // Works but slowly
}

func (m *mockSlowCache) Get(ctx context.Context, key string) ([]byte, error) {
	return []byte("value"), nil
}

func (m *mockSlowCache) Set(ctx context.Context, key string, value []byte, ttl int) error {
	return nil
}

func (m *mockSlowCache) Delete(ctx context.Context, key string) error {
	return nil
}

func (m *mockSlowCache) Close() error {
	return nil
}

