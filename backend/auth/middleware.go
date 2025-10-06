package auth

import (
	"net/http"
	"strings"

	"github.com/labstack/echo/v4"
)

// JWTMiddleware creates a JWT authentication middleware
func JWTMiddleware(jwtManager *JWTManager) echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			// Get Authorization header
			authHeader := c.Request().Header.Get("Authorization")
			if authHeader == "" {
				return c.JSON(http.StatusUnauthorized, map[string]string{
					"error": "missing authorization header",
				})
			}

			// Check Bearer format (case insensitive)
			parts := strings.Split(authHeader, " ")
			if len(parts) != 2 || strings.ToLower(parts[0]) != "bearer" {
				return c.JSON(http.StatusUnauthorized, map[string]string{
					"error": "invalid authorization format",
				})
			}

			// Validate token
			token := parts[1]
			claims, err := jwtManager.ValidateToken(token)
			if err != nil {
				return c.JSON(http.StatusUnauthorized, map[string]string{
					"error": "invalid token",
				})
			}

			// Set user context
			c.Set("user", claims)

			return next(c)
		}
	}
}

// RequireRole creates a middleware that requires a specific role
func RequireRole(requiredRole string) echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			// Get user from context
			user := c.Get("user")
			if user == nil {
				return c.JSON(http.StatusUnauthorized, map[string]string{
					"error": "user not authenticated",
				})
			}

			// Type assert to Claims
			claims, ok := user.(*Claims)
			if !ok {
				return c.JSON(http.StatusUnauthorized, map[string]string{
					"error": "invalid user context",
				})
			}

			// Check role
			if claims.Role != requiredRole {
				return c.JSON(http.StatusForbidden, map[string]string{
					"error": "insufficient permissions",
				})
			}

			return next(c)
		}
	}
}

// GetCurrentUser extracts the current user from the context
func GetCurrentUser(c echo.Context) (*Claims, bool) {
	user := c.Get("user")
	if user == nil {
		return nil, false
	}

	claims, ok := user.(*Claims)
	return claims, ok
}