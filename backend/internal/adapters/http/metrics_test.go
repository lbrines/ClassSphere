package http

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/labstack/echo/v4"
	"github.com/prometheus/client_golang/prometheus/testutil"
	"github.com/stretchr/testify/assert"
)

// TestMetrics_HTTPRequestsTotal verifies request counter metric
func TestMetrics_HTTPRequestsTotal(t *testing.T) {
	// Reset metrics for isolated test
	ResetMetrics()

	// Setup server with metrics
	e := setupTestServerWithMetrics(t)

	// Make 5 requests to /health
	for i := 0; i < 5; i++ {
		req := httptest.NewRequest(http.MethodGet, "/health", nil)
		rec := httptest.NewRecorder()
		e.ServeHTTP(rec, req)
	}

	// Verify counter incremented
	count := testutil.ToFloat64(httpRequestsTotal.WithLabelValues("GET", "/health", "200"))
	assert.Equal(t, float64(5), count, "Should count 5 requests to /health")
}

// TestMetrics_HTTPRequestDuration verifies request duration histogram
func TestMetrics_HTTPRequestDuration(t *testing.T) {
	ResetMetrics()

	e := setupTestServerWithMetrics(t)

	// Make request
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Verify histogram has observations (collect entire histogram vec)
	count := testutil.CollectAndCount(httpRequestDuration)
	assert.Greater(t, count, 0, "Duration histogram should have observations")
}

// TestMetrics_ActiveConnections verifies active connections gauge
func TestMetrics_ActiveConnections(t *testing.T) {
	ResetMetrics()

	e := setupTestServerWithMetrics(t)

	// Initially should be 0
	initial := testutil.ToFloat64(activeConnections)
	assert.Equal(t, float64(0), initial, "Should start with 0 active connections")

	// Make request (synchronous, so it increments then decrements)
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// After completion, should be 0 again
	final := testutil.ToFloat64(activeConnections)
	assert.Equal(t, float64(0), final, "Should return to 0 after request completes")
}

// TestMetrics_StatusCodeLabels verifies different status codes are tracked
func TestMetrics_StatusCodeLabels(t *testing.T) {
	ResetMetrics()

	e := setupTestServerWithMetrics(t)

	// Add endpoint that returns 201
	e.POST("/api/create", func(c echo.Context) error {
		return c.JSON(http.StatusCreated, map[string]string{"id": "123"})
	})

	// Request to /health (200)
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Request to /api/create (201)
	req = httptest.NewRequest(http.MethodPost, "/api/create", nil)
	rec = httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Verify both status codes tracked
	count200 := testutil.ToFloat64(httpRequestsTotal.WithLabelValues("GET", "/health", "200"))
	count201 := testutil.ToFloat64(httpRequestsTotal.WithLabelValues("POST", "/api/create", "201"))

	assert.Equal(t, float64(1), count200, "Should have 1 request with status 200")
	assert.Equal(t, float64(1), count201, "Should have 1 request with status 201")
}

// TestMetrics_MethodLabels verifies different HTTP methods are tracked
func TestMetrics_MethodLabels(t *testing.T) {
	ResetMetrics()

	e := setupTestServerWithMetrics(t)

	// Add POST endpoint
	e.POST("/api/test", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	// GET request
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// POST request
	req = httptest.NewRequest(http.MethodPost, "/api/test", strings.NewReader("{}"))
	req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
	rec = httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	// Verify both methods tracked
	countGET := testutil.ToFloat64(httpRequestsTotal.WithLabelValues("GET", "/health", "200"))
	countPOST := testutil.ToFloat64(httpRequestsTotal.WithLabelValues("POST", "/api/test", "200"))

	assert.Equal(t, float64(1), countGET, "Should track GET requests")
	assert.Equal(t, float64(1), countPOST, "Should track POST requests")
}

// TestMetrics_Endpoint verifies /metrics endpoint exists and returns Prometheus format
func TestMetrics_Endpoint(t *testing.T) {
	e := setupTestServerWithMetrics(t)

	req := httptest.NewRequest(http.MethodGet, "/metrics", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)

	assert.Equal(t, http.StatusOK, rec.Code, "Metrics endpoint should return 200")
	
	// Verify Prometheus format (should contain metric names)
	body := rec.Body.String()
	assert.Contains(t, body, "classsphere_http_requests_total", 
		"Should expose http_requests_total metric")
	assert.Contains(t, body, "classsphere_http_request_duration_seconds",
		"Should expose request_duration metric")
	assert.Contains(t, body, "classsphere_active_connections",
		"Should expose active_connections metric")
}

// ==============================================================================
// Test Helpers
// ==============================================================================

// setupTestServerWithMetrics creates a test Echo server with metrics enabled
func setupTestServerWithMetrics(t *testing.T) *echo.Echo {
	t.Helper()

	e := echo.New()
	e.HideBanner = true

	// Apply metrics middleware (to be implemented)
	ConfigureMetrics(e)

	// Add health endpoint
	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	return e
}

