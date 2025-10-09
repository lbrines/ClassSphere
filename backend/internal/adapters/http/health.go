package http

import (
	"context"
	"net/http"
	"time"

	"github.com/labstack/echo/v4"

	"github.com/lbrines/classsphere/internal/ports"
)

// HealthStatus represents the overall health status of the application
type HealthStatus struct {
	Status    string           `json:"status"`    // "healthy", "degraded", or "unhealthy"
	Version   string           `json:"version"`   // Application version
	Timestamp time.Time        `json:"timestamp"` // Current timestamp
	Checks    map[string]Check `json:"checks"`    // Individual dependency checks
}

// Check represents the health status of a single dependency
type Check struct {
	Status  string `json:"status"`            // "healthy", "degraded", or "unhealthy"
	Message string `json:"message,omitempty"` // Error message if unhealthy
}

// healthDetailed returns detailed health information including dependency status
func (h *Handler) healthDetailed(c echo.Context) error {
	ctx := c.Request().Context()

	checks := make(map[string]Check)

	// Check Redis if available
	if h.cache != nil {
		redisCheck := checkRedis(ctx, h.cache)
		checks["redis"] = redisCheck
	}

	// Check Classroom Service if available
	if h.classroomService != nil {
		// Classroom service is always available (mock fallback)
		checks["classroom"] = Check{Status: "healthy"}
	}

	// Determine overall status based on individual checks
	overallStatus := determineOverallStatus(checks)

	response := HealthStatus{
		Status:    overallStatus,
		Version:   "1.0.0", // TODO: Get from build info
		Timestamp: time.Now(),
		Checks:    checks,
	}

	// Return 503 if unhealthy, 200 otherwise
	statusCode := http.StatusOK
	if overallStatus == "unhealthy" {
		statusCode = http.StatusServiceUnavailable
	}

	return c.JSON(statusCode, response)
}

// checkRedis verifies Redis connectivity
func checkRedis(ctx context.Context, cache ports.Cache) Check {
	// Use a timeout for the health check
	ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()

	if err := cache.Ping(ctx); err != nil {
		return Check{
			Status:  "unhealthy",
			Message: err.Error(),
		}
	}

	return Check{Status: "healthy"}
}

// determineOverallStatus calculates overall health from individual checks
func determineOverallStatus(checks map[string]Check) string {
	if len(checks) == 0 {
		return "healthy" // No checks means basic health OK
	}

	hasUnhealthy := false
	hasDegraded := false

	for _, check := range checks {
		if check.Status == "unhealthy" {
			hasUnhealthy = true
		}
		if check.Status == "degraded" {
			hasDegraded = true
		}
	}

	if hasUnhealthy {
		return "unhealthy"
	}
	if hasDegraded {
		return "degraded"
	}

	return "healthy"
}

