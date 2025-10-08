package http

import (
	"strconv"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	"github.com/lbrines/classsphere/internal/app"
)

func init() {
	// Initialize auth metrics recording when http module loads
	app.RecordAuthAttemptFunc = RecordAuthAttempt
}

// Prometheus metrics
var (
	httpRequestsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "classsphere_http_requests_total",
			Help: "Total number of HTTP requests processed, partitioned by method, endpoint, and status code",
		},
		[]string{"method", "endpoint", "status"},
	)

	httpRequestDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "classsphere_http_request_duration_seconds",
			Help:    "HTTP request duration in seconds",
			Buckets: prometheus.DefBuckets, // 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10
		},
		[]string{"method", "endpoint"},
	)

	activeConnections = promauto.NewGauge(
		prometheus.GaugeOpts{
			Name: "classsphere_active_connections",
			Help: "Number of currently active HTTP connections",
		},
	)

	authAttempts = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "classsphere_auth_attempts_total",
			Help: "Total authentication attempts, partitioned by method and result",
		},
		[]string{"method", "result"}, // method: password|oauth, result: success|failure
	)
)

// MetricsMiddleware tracks HTTP request metrics
func MetricsMiddleware() echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			start := time.Now()

			// Increment active connections
			activeConnections.Inc()
			defer activeConnections.Dec()

			// Execute handler
			err := next(c)

			// Calculate duration
			duration := time.Since(start).Seconds()

			// Get status code
			status := c.Response().Status

			// Record metrics
			httpRequestsTotal.WithLabelValues(
				c.Request().Method,
				c.Path(),
				strconv.Itoa(status),
			).Inc()

			httpRequestDuration.WithLabelValues(
				c.Request().Method,
				c.Path(),
			).Observe(duration)

			return err
		}
	}
}

// RecordAuthAttempt records an authentication attempt
func RecordAuthAttempt(method string, success bool) {
	result := "failure"
	if success {
		result = "success"
	}
	authAttempts.WithLabelValues(method, result).Inc()
}

// ConfigureMetrics sets up metrics collection and exposes /metrics endpoint
func ConfigureMetrics(e *echo.Echo) {
	// Add metrics middleware
	e.Use(MetricsMiddleware())

	// Expose /metrics endpoint (Prometheus scraping)
	e.GET("/metrics", echo.WrapHandler(promhttp.Handler()))
}

// ResetMetrics resets all metrics (for testing only)
func ResetMetrics() {
	// Reset counters and histograms
	httpRequestsTotal.Reset()
	httpRequestDuration.Reset()
	authAttempts.Reset()

	// Reset gauge to 0
	activeConnections.Set(0)
}

