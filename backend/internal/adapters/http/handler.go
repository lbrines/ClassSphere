package http

import (
	"fmt"
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
	authService      *app.AuthService
	userService      *app.UserService
	classroomService *app.ClassroomService
	notificationHub  *app.NotificationHub
	searchService    *app.SearchService
}

// New creates an Echo engine configured with routes and middleware.
func New(authService *app.AuthService, userService *app.UserService, classroomService *app.ClassroomService, notificationHub *app.NotificationHub) *echo.Echo {
	h := &Handler{
		authService:      authService,
		userService:      userService,
		classroomService: classroomService,
		notificationHub:  notificationHub,
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

	protected.GET("/google/courses", h.listCourses)
	protected.GET("/classroom/courses", h.listCourses)

	protected.GET("/dashboard/admin", h.dashboardFor(domain.RoleAdmin), RequireRole(domain.RoleAdmin))
	protected.GET("/dashboard/coordinator", h.dashboardFor(domain.RoleCoordinator), RequireRole(domain.RoleCoordinator))
	protected.GET("/dashboard/teacher", h.dashboardFor(domain.RoleTeacher), RequireRole(domain.RoleTeacher))
	protected.GET("/dashboard/student", h.dashboardFor(domain.RoleStudent), RequireRole(domain.RoleStudent))

	// WebSocket endpoint
	e.GET("/api/v1/ws/notifications", h.handleWebSocket)

	// Search endpoint
	if h.searchService != nil {
		protected.GET("/search", h.handleSearch)
	}

	return e
}

// NewWithSearch creates an Echo engine with search service.
// This is a helper for testing that includes SearchService.
func NewWithSearch(authService *app.AuthService, userService *app.UserService, classroomService *app.ClassroomService, notificationHub *app.NotificationHub, searchService *app.SearchService) *echo.Echo {
	h := &Handler{
		authService:      authService,
		userService:      userService,
		classroomService: classroomService,
		notificationHub:  notificationHub,
		searchService:    searchService,
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

	protected.GET("/google/courses", h.listCourses)
	protected.GET("/classroom/courses", h.listCourses)

	protected.GET("/dashboard/admin", h.dashboardFor(domain.RoleAdmin), RequireRole(domain.RoleAdmin))
	protected.GET("/dashboard/coordinator", h.dashboardFor(domain.RoleCoordinator), RequireRole(domain.RoleCoordinator))
	protected.GET("/dashboard/teacher", h.dashboardFor(domain.RoleTeacher), RequireRole(domain.RoleTeacher))
	protected.GET("/dashboard/student", h.dashboardFor(domain.RoleStudent), RequireRole(domain.RoleStudent))

	// WebSocket endpoint
	e.GET("/api/v1/ws/notifications", h.handleWebSocket)

	// Search endpoint
	protected.GET("/search", h.handleSearch)

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

func (h *Handler) listCourses(c echo.Context) error {
	if h.classroomService == nil {
		return echo.NewHTTPError(http.StatusServiceUnavailable, "classroom integration not configured")
	}
	ctx := c.Request().Context()
	mode := c.QueryParam("mode")
	result, err := h.classroomService.ListCourses(ctx, mode)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, courseListResponse{
		Mode:           result.Mode,
		GeneratedAt:    result.GeneratedAt,
		Courses:        result.Courses,
		AvailableModes: h.classroomService.AvailableModes(),
	})
}

func (h *Handler) dashboardFor(role domain.Role) echo.HandlerFunc {
	return func(c echo.Context) error {
		if h.classroomService == nil {
			return echo.NewHTTPError(http.StatusServiceUnavailable, "classroom integration not configured")
		}
		user := CurrentUser(c)
		if user.ID == "" {
			return echo.NewHTTPError(http.StatusUnauthorized, "missing user")
		}
		if user.Role != role {
			return echo.NewHTTPError(http.StatusForbidden, fmt.Sprintf("dashboard available only for %s role", role))
		}
		ctx := c.Request().Context()
		mode := c.QueryParam("mode")
		data, err := h.classroomService.Dashboard(ctx, user, mode)
		if err != nil {
			return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
		}
		return c.JSON(http.StatusOK, data)
	}
}

type courseListResponse struct {
	Mode           string               `json:"mode"`
	GeneratedAt    time.Time            `json:"generatedAt"`
	Courses        []app.CourseOverview `json:"courses"`
	AvailableModes []string             `json:"availableModes"`
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
