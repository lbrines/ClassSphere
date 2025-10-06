package auth

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

func TestGetCurrentUser(t *testing.T) {
	// Test with valid user in context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Create test claims
	claims := &Claims{
		UserID: "123",
		Role:   "user",
	}

	// Set user in context
	c.Set("user", claims)

	// Test GetCurrentUser
	userClaims, ok := GetCurrentUser(c)
	assert.True(t, ok)
	assert.Equal(t, "123", userClaims.UserID)
	assert.Equal(t, "user", userClaims.Role)

	// Test with no user in context
	c2 := e.NewContext(req, rec)
	_, ok = GetCurrentUser(c2)
	assert.False(t, ok)
}

func TestRequireRole_ValidRole(t *testing.T) {
	// Create middleware
	middleware := RequireRole("admin")

	// Create test context with admin user
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Create admin claims
	claims := &Claims{
		UserID: "123",
		Role:   "admin",
	}
	c.Set("user", claims)

	// Test middleware
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	err := handler(c)
	assert.NoError(t, err)
}

func TestRequireRole_InvalidRole(t *testing.T) {
	// Create middleware
	middleware := RequireRole("admin")

	// Create test context with user role
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Create user claims (not admin)
	claims := &Claims{
		UserID: "123",
		Role:   "user",
	}
	c.Set("user", claims)

	// Test middleware
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	err := handler(c)
	assert.Error(t, err)
	assert.Equal(t, http.StatusForbidden, err.(*echo.HTTPError).Code)
}

func TestRequireRole_NoUser(t *testing.T) {
	// Create middleware
	middleware := RequireRole("admin")

	// Create test context without user
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test middleware
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})

	err := handler(c)
	assert.Error(t, err)
	assert.Equal(t, http.StatusUnauthorized, err.(*echo.HTTPError).Code)
}