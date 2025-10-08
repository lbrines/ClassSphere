package http

import (
	"net/http"
	"strings"

	echo "github.com/labstack/echo/v4"

	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/shared"
)

type contextKey string

const userContextKey contextKey = "current_user"

// AuthMiddleware validates bearer tokens and injects the authenticated user.
func AuthMiddleware(auth *app.AuthService) echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			header := c.Request().Header.Get("Authorization")
			if header == "" {
				return echo.NewHTTPError(http.StatusUnauthorized, shared.ErrUnauthorized.Error())
			}

			parts := strings.SplitN(header, " ", 2)
			if len(parts) != 2 || !strings.EqualFold(parts[0], "Bearer") {
				return echo.NewHTTPError(http.StatusUnauthorized, shared.ErrUnauthorized.Error())
			}

			user, err := auth.ValidateToken(c.Request().Context(), parts[1])
			if err != nil {
				return echo.NewHTTPError(http.StatusUnauthorized, shared.ErrUnauthorized.Error())
			}

			c.Set(string(userContextKey), user)
			return next(c)
		}
	}
}

// RequireRole ensures the authenticated user has the required role or higher.
func RequireRole(role domain.Role) echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			user := CurrentUser(c)
			if !user.Role.Allows(role) {
				return echo.NewHTTPError(http.StatusForbidden, shared.ErrForbidden.Error())
			}
			return next(c)
		}
	}
}

// CurrentUser returns the authenticated user stored in the context.
func CurrentUser(c echo.Context) domain.User {
	if value, ok := c.Get(string(userContextKey)).(domain.User); ok {
		return value
	}
	return domain.User{}
}
