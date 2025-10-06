package auth

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestJWTMiddleware(t *testing.T) {
	// Create JWT manager
	jwtManager := NewJWTManager("test-secret")
	
	// Create middleware
	middleware := JWTMiddleware(jwtManager)
	
	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Test middleware without token
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	
	err := handler(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestJWTMiddleware_WithValidToken(t *testing.T) {
	// Create JWT manager
	jwtManager := NewJWTManager("test-secret")
	
	// Generate valid token
	token, err := jwtManager.GenerateToken("1", "user", 1*time.Hour)
	require.NoError(t, err)
	
	// Create middleware
	middleware := JWTMiddleware(jwtManager)
	
	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	req.Header.Set("Authorization", "Bearer "+token)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Test middleware with valid token
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	
	err = handler(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	// Verify user is set in context
	user := c.Get("user")
	assert.NotNil(t, user)
	claims, ok := user.(*Claims)
	assert.True(t, ok)
	assert.Equal(t, "1", claims.UserID)
	assert.Equal(t, "user", claims.Role)
}

func TestJWTMiddleware_WithInvalidToken(t *testing.T) {
	// Create JWT manager
	jwtManager := NewJWTManager("test-secret")
	
	// Create middleware
	middleware := JWTMiddleware(jwtManager)
	
	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	req.Header.Set("Authorization", "Bearer invalid-token")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Test middleware with invalid token
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	
	err := handler(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestJWTMiddleware_WithExpiredToken(t *testing.T) {
	// Create JWT manager
	jwtManager := NewJWTManager("test-secret")
	
	// Generate expired token
	token, err := jwtManager.GenerateToken("1", "user", -1*time.Hour)
	require.NoError(t, err)
	
	// Create middleware
	middleware := JWTMiddleware(jwtManager)
	
	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	req.Header.Set("Authorization", "Bearer "+token)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Test middleware with expired token
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	
	err = handler(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestRequireRole(t *testing.T) {
	// Create middleware
	middleware := RequireRole("admin")
	
	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Test without user in context
	handler := middleware(func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	
	err := handler(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	
	// Test with user but wrong role
	rec = httptest.NewRecorder()
	c = e.NewContext(req, rec)
	c.Set("user", &Claims{UserID: "1", Role: "user"})
	
	err = handler(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusForbidden, rec.Code)
	
	// Test with correct role
	rec = httptest.NewRecorder()
	c = e.NewContext(req, rec)
	c.Set("user", &Claims{UserID: "1", Role: "admin"})
	
	err = handler(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestGetCurrentUser(t *testing.T) {
	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Test without user in context
	user, ok := GetCurrentUser(c)
	assert.Nil(t, user)
	assert.False(t, ok)
	
	// Test with user in context
	claims := &Claims{UserID: "1", Role: "user"}
	c.Set("user", claims)
	
	user, ok = GetCurrentUser(c)
	assert.NotNil(t, user)
	assert.True(t, ok)
	assert.Equal(t, "1", user.UserID)
	assert.Equal(t, "user", user.Role)
}

func TestHashPassword(t *testing.T) {
	password := "testpassword123"
	
	hashed, err := HashPassword(password)
	assert.NoError(t, err)
	assert.NotEmpty(t, hashed)
	assert.NotEqual(t, password, hashed)
	
	// Test that the same password produces different hashes (due to salt)
	hashed2, err := HashPassword(password)
	assert.NoError(t, err)
	assert.NotEqual(t, hashed, hashed2)
}

func TestCheckPassword(t *testing.T) {
	password := "testpassword123"
	hashed, _ := HashPassword(password)
	
	// Test correct password
	valid := CheckPassword(password, hashed)
	assert.True(t, valid)
	
	// Test incorrect password
	valid = CheckPassword("wrongpassword", hashed)
	assert.False(t, valid)
}