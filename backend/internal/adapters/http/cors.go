package http

import (
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"

	"github.com/lbrines/classsphere/internal/shared"
)

// ConfigureCORS applies CORS middleware with restricted origins based on configuration.
// This prevents CSRF attacks and restricts API access to configured domains only.
//
// Configuration via environment variables:
//   - FRONTEND_URL: Single frontend URL (default: http://localhost:4200)
//   - ALLOWED_ORIGINS: Comma-separated list of allowed origins (overrides FRONTEND_URL)
//
// Example:
//   ALLOWED_ORIGINS="https://classsphere.com,https://app.classsphere.com"
func ConfigureCORS(e *echo.Echo, cfg shared.Config) {
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: cfg.AllowedOrigins,
		AllowMethods: []string{
			echo.GET,
			echo.POST,
			echo.PUT,
			echo.DELETE,
			echo.PATCH,
			echo.OPTIONS,
		},
		AllowHeaders: []string{
			echo.HeaderAuthorization,
			echo.HeaderContentType,
			echo.HeaderAccept,
		},
		AllowCredentials: true,
		MaxAge:           3600, // 1 hour (browser caches preflight response)
	}))
}

