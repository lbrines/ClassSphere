package auth

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

func TestJWTMiddleware(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")
	middleware := JWTMiddleware(jwtManager)

	// Create a test handler
	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Generate a valid token
	token, err := jwtManager.GenerateToken("user123", "admin", 1*time.Hour)
	assert.NoError(t, err)

	// Test with valid token
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Authorization", "Bearer "+token)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	handler := middleware(testHandler)
	err = handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	// Check if user context is set
	userClaims := c.Get("user")
	assert.NotNil(t, userClaims)
	claims, ok := userClaims.(*Claims)
	assert.True(t, ok)
	assert.Equal(t, "user123", claims.UserID)
	assert.Equal(t, "admin", claims.Role)
}

func TestJWTMiddlewareMissingToken(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")
	middleware := JWTMiddleware(jwtManager)

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Test without Authorization header
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	handler := middleware(testHandler)
	err := handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	assert.Contains(t, rec.Body.String(), "missing authorization header")
}

func TestJWTMiddlewareInvalidTokenFormat(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")
	middleware := JWTMiddleware(jwtManager)

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Test with invalid token format
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Authorization", "InvalidFormat")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	handler := middleware(testHandler)
	err := handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	assert.Contains(t, rec.Body.String(), "invalid authorization format")
}

func TestJWTMiddlewareInvalidToken(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")
	middleware := JWTMiddleware(jwtManager)

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Test with invalid token
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Authorization", "Bearer invalid.token.here")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	handler := middleware(testHandler)
	err := handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	assert.Contains(t, rec.Body.String(), "invalid token")
}

func TestJWTMiddlewareExpiredToken(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")
	middleware := JWTMiddleware(jwtManager)

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Generate an expired token
	expiredToken, err := jwtManager.GenerateToken("user123", "admin", -1*time.Hour)
	assert.NoError(t, err)

	// Test with expired token
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Authorization", "Bearer "+expiredToken)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	handler := middleware(testHandler)
	err = handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	assert.Contains(t, rec.Body.String(), "invalid token")
}

func TestJWTMiddlewareAuthorizationCaseInsensitive(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")
	middleware := JWTMiddleware(jwtManager)

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	token, err := jwtManager.GenerateToken("user123", "admin", 1*time.Hour)
	assert.NoError(t, err)

	// Test with lowercase bearer
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	req.Header.Set("Authorization", "bearer "+token)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	handler := middleware(testHandler)
	err = handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestRequireRole(t *testing.T) {
	middleware := RequireRole("admin")

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Test with admin role
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Set user context with admin role
	claims := &Claims{
		UserID: "user123",
		Role:   "admin",
	}
	c.Set("user", claims)

	handler := middleware(testHandler)
	err := handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestRequireRoleInsufficientPermissions(t *testing.T) {
	middleware := RequireRole("admin")

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Test with user role when admin required
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Set user context with user role
	claims := &Claims{
		UserID: "user123",
		Role:   "user",
	}
	c.Set("user", claims)

	handler := middleware(testHandler)
	err := handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusForbidden, rec.Code)
	assert.Contains(t, rec.Body.String(), "insufficient permissions")
}

func TestRequireRoleNoUserContext(t *testing.T) {
	middleware := RequireRole("admin")

	testHandler := func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"message": "success"})
	}

	// Test without user context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	handler := middleware(testHandler)
	err := handler(c)

	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	assert.Contains(t, rec.Body.String(), "user not authenticated")
}