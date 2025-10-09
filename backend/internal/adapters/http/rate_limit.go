package http

import (
	"net/http"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"golang.org/x/time/rate"
)

// RateLimitConfig defines rate limiting configuration
type RateLimitConfig struct {
	RequestsPerSecond float64  // Number of requests allowed per second
	Burst             int      // Maximum burst size
	SkipPaths         []string // Paths to skip rate limiting (e.g., /health)
}

// ApplyRateLimiting applies rate limiting middleware to the Echo server.
// Rate limiting is applied per-IP address to prevent DoS attacks.
//
// Configuration:
//   - RequestsPerSecond: Maximum requests per second (e.g., 20)
//   - Burst: Additional requests allowed in bursts (e.g., 5)
//   - SkipPaths: Endpoints to exclude from rate limiting (e.g., ["/health", "/metrics"])
//
// Example:
//
//	ApplyRateLimiting(e, RateLimitConfig{
//	    RequestsPerSecond: 20,
//	    Burst:             5,
//	    SkipPaths:         []string{"/health"},
//	})
func ApplyRateLimiting(e *echo.Echo, config RateLimitConfig) {
	// Create in-memory rate limiter store
	store := middleware.NewRateLimiterMemoryStore(rate.Limit(config.RequestsPerSecond))

	e.Use(middleware.RateLimiterWithConfig(middleware.RateLimiterConfig{
		Store: store,
		
		// Extract identifier (IP address)
		IdentifierExtractor: func(c echo.Context) (string, error) {
			// Try X-Real-IP header first (for reverse proxy scenarios)
			if realIP := c.Request().Header.Get("X-Real-IP"); realIP != "" {
				return realIP, nil
			}
			
			// Try X-Forwarded-For header
			if forwardedFor := c.Request().Header.Get("X-Forwarded-For"); forwardedFor != "" {
				return forwardedFor, nil
			}
			
			// Fallback to RemoteAddr
			return c.RealIP(), nil
		},
		
		// Error handler when rate limit is exceeded
		ErrorHandler: func(c echo.Context, err error) error {
			return nil // Continue to DenyHandler
		},
		
		// DenyHandler returns 429 when rate limit is exceeded
		DenyHandler: func(c echo.Context, identifier string, err error) error {
			return echo.NewHTTPError(http.StatusTooManyRequests, 
				"Rate limit exceeded. Please try again later.")
		},
		
		// Skipper decides which requests to skip
		Skipper: func(c echo.Context) bool {
			// Skip rate limiting for configured paths
			for _, path := range config.SkipPaths {
				if c.Path() == path {
					return true
				}
			}
			return false
		},
	}))
}

// ApplyLoginRateLimit returns a middleware for stricter rate limiting on login endpoint.
// This prevents brute force attacks on authentication.
//
// Default configuration:
//   - 5 requests per second
//   - No burst allowance
func ApplyLoginRateLimit() echo.MiddlewareFunc {
	store := middleware.NewRateLimiterMemoryStore(rate.Limit(5)) // 5 login attempts per second

	return middleware.RateLimiterWithConfig(middleware.RateLimiterConfig{
		Store: store,
		
		IdentifierExtractor: func(c echo.Context) (string, error) {
			// Use IP for rate limiting
			return c.RealIP(), nil
		},
		
		ErrorHandler: func(c echo.Context, err error) error {
			return nil
		},
		
		DenyHandler: func(c echo.Context, identifier string, err error) error {
			return echo.NewHTTPError(http.StatusTooManyRequests,
				"Too many login attempts. Please try again later.")
		},
	})
}

// ConfigureRateLimiting sets up rate limiting for the entire application.
// Uses configuration from environment variables.
//
// Environment variables:
//   - RATE_LIMIT_REQUESTS: Requests per second (default: 20)
//   - RATE_LIMIT_BURST: Burst size (default: 5)
func ConfigureRateLimiting(e *echo.Echo) {
	// Default configuration
	config := RateLimitConfig{
		RequestsPerSecond: 20,
		Burst:             5,
		SkipPaths:         []string{"/health", "/metrics"},
	}

	ApplyRateLimiting(e, config)
}

