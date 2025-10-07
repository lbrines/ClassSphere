package http

import (
	"net/http"
	"time"

	echo "github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"

	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/shared"
)

// Handler wires HTTP routes to use cases.
type Handler struct {
	authService *app.AuthService
	userService *app.UserService
}

// New creates an Echo engine configured with routes and middleware.
func New(authService *app.AuthService, userService *app.UserService) *echo.Echo {
	h := &Handler{
		authService: authService,
		userService: userService,
	}

	e := echo.New()
	e.HideBanner = true

	e.Use(middleware.Recover())
	e.Use(middleware.CORS())
	e.Use(middleware.RequestID())
	e.Use(middleware.Secure())

	e.GET("/health", h.health)

	api := e.Group("/api/v1")
	api.POST("/auth/login", h.login)
	api.GET("/auth/oauth/google", h.oauthStart)
	api.GET("/auth/oauth/callback", h.oauthCallback)

	protected := api.Group("")
	protected.Use(AuthMiddleware(authService))

	protected.GET("/users/me", h.me)
	protected.GET("/admin/ping", h.adminPing, RequireRole(domain.RoleAdmin))

	return e
}

func (h *Handler) health(c echo.Context) error {
	return c.JSON(http.StatusOK, map[string]string{
		"status": "ok",
	})
}

func (h *Handler) login(c echo.Context) error {
	var req loginRequest
	if err := c.Bind(&req); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid request payload")
	}
	ctx := c.Request().Context()
	result, err := h.authService.LoginWithPassword(ctx, req.Email, req.Password)
	if err != nil {
		return echo.NewHTTPError(http.StatusUnauthorized, err.Error())
	}
	return c.JSON(http.StatusOK, authResponse{
		AccessToken: result.AccessToken,
		ExpiresAt:   result.ExpiresAt,
		User:        result.User,
	})
}

func (h *Handler) oauthStart(c echo.Context) error {
	ctx := c.Request().Context()
	state, url, err := h.authService.StartOAuth(ctx)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, map[string]string{
		"state": state,
		"url":   url,
	})
}

func (h *Handler) oauthCallback(c echo.Context) error {
	code := c.QueryParam("code")
	state := c.QueryParam("state")
	ctx := c.Request().Context()
	result, err := h.authService.CompleteOAuth(ctx, code, state)
	if err != nil {
		if err == shared.ErrUnauthorized {
			return echo.NewHTTPError(http.StatusUnauthorized, err.Error())
		}
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	return c.JSON(http.StatusOK, authResponse{
		AccessToken: result.AccessToken,
		ExpiresAt:   result.ExpiresAt,
		User:        result.User,
	})
}

func (h *Handler) me(c echo.Context) error {
	user := CurrentUser(c)
	return c.JSON(http.StatusOK, user)
}

func (h *Handler) adminPing(c echo.Context) error {
	return c.JSON(http.StatusOK, map[string]string{
		"message": "admin pong",
	})
}

type loginRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type authResponse struct {
	AccessToken string      `json:"accessToken"`
	ExpiresAt   time.Time   `json:"expiresAt"`
	User        domain.User `json:"user"`
}
