package http_test

import (
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"

	echo "github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	httpadapter "github.com/lbrines/classsphere/internal/adapters/http"
	"github.com/lbrines/classsphere/internal/shared"
)

// ==============================================================================
// Error Handler Middleware Tests
// ==============================================================================

func TestErrorHandler_AppError(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns an AppError
	e.GET("/test", func(c echo.Context) error {
		return httpadapter.NewAppError("TEST_ERROR", "test error message", http.StatusBadRequest, nil)
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should return standardized error response
	assert.Equal(t, http.StatusBadRequest, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "test error message", response.Error)
	assert.Equal(t, "TEST_ERROR", response.Code)
}

func TestErrorHandler_EchoHTTPError(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns Echo's HTTPError
	e.GET("/test", func(c echo.Context) error {
		return echo.NewHTTPError(http.StatusNotFound, "resource not found")
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should return standardized error response
	assert.Equal(t, http.StatusNotFound, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "resource not found", response.Error)
	assert.Equal(t, "NOT_FOUND", response.Code)
}

func TestErrorHandler_DomainErrorUnauthorized(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns domain error
	e.GET("/test", func(c echo.Context) error {
		return shared.ErrUnauthorized
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should map to appropriate HTTP status
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "unauthorized", response.Error)
	assert.Equal(t, "UNAUTHORIZED", response.Code)
}

func TestErrorHandler_DomainErrorForbidden(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns forbidden error
	e.GET("/test", func(c echo.Context) error {
		return shared.ErrForbidden
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should return 403
	assert.Equal(t, http.StatusForbidden, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "forbidden", response.Error)
	assert.Equal(t, "FORBIDDEN", response.Code)
}

func TestErrorHandler_DomainErrorUserNotFound(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns user not found error
	e.GET("/test", func(c echo.Context) error {
		return shared.ErrUserNotFound
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should return 404
	assert.Equal(t, http.StatusNotFound, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "user not found", response.Error)
	assert.Equal(t, "USER_NOT_FOUND", response.Code)
}

func TestErrorHandler_DomainErrorInvalidCredentials(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns invalid credentials error
	e.GET("/test", func(c echo.Context) error {
		return shared.ErrInvalidCredentials
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should return 401
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "invalid credentials", response.Error)
	assert.Equal(t, "INVALID_CREDENTIALS", response.Code)
}

func TestErrorHandler_UnexpectedError(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns unexpected error
	e.GET("/test", func(c echo.Context) error {
		return errors.New("unexpected database error")
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should return 500 with generic message
	assert.Equal(t, http.StatusInternalServerError, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "internal server error", response.Error)
	assert.Equal(t, "INTERNAL_ERROR", response.Code)
}

func TestErrorHandler_NoError(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that succeeds
	e.GET("/test", func(c echo.Context) error {
		return c.JSON(http.StatusOK, map[string]string{"status": "ok"})
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Should return success response
	assert.Equal(t, http.StatusOK, rec.Code)
	
	var response map[string]string
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "ok", response["status"])
}

func TestErrorHandler_RequestIDIncluded(t *testing.T) {
	// GIVEN: Echo server with request ID middleware and error handler
	e := echo.New()
	e.Use(echo.MiddlewareFunc(func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			// Simulate request ID middleware
			c.Response().Header().Set(echo.HeaderXRequestID, "test-request-123")
			return next(c)
		}
	}))
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns an error
	e.GET("/test", func(c echo.Context) error {
		return httpadapter.ErrBadRequest("validation failed")
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Response should include request ID
	assert.Equal(t, http.StatusBadRequest, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "validation failed", response.Error)
	assert.Equal(t, "test-request-123", response.RequestID)
}

func TestErrorHandler_AppErrorWithDetails(t *testing.T) {
	// GIVEN: Echo server with error handler middleware
	e := echo.New()
	e.Use(httpadapter.ErrorHandlerMiddleware())
	
	// Handler that returns AppError with details
	e.GET("/test", func(c echo.Context) error {
		appErr := httpadapter.NewAppError("VALIDATION_ERROR", "validation failed", http.StatusBadRequest, nil)
		appErr.Details = "field 'email' is required"
		return appErr
	})
	
	// WHEN: Request is made
	req := httptest.NewRequest(http.MethodGet, "/test", nil)
	rec := httptest.NewRecorder()
	e.ServeHTTP(rec, req)
	
	// THEN: Response should include details
	assert.Equal(t, http.StatusBadRequest, rec.Code)
	
	var response httpadapter.ErrorResponse
	err := json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "validation failed", response.Error)
	assert.Equal(t, "VALIDATION_ERROR", response.Code)
	assert.Equal(t, "field 'email' is required", response.Details)
}

// ==============================================================================
// Helper Error Function Tests
// ==============================================================================

func TestErrorHelpers_BadRequest(t *testing.T) {
	err := httpadapter.ErrBadRequest("invalid input")
	
	assert.Equal(t, "BAD_REQUEST", err.Code)
	assert.Equal(t, "invalid input", err.Message)
	assert.Equal(t, http.StatusBadRequest, err.HTTPStatus)
}

func TestErrorHelpers_Unauthorized(t *testing.T) {
	err := httpadapter.ErrUnauthorized("token expired")
	
	assert.Equal(t, "UNAUTHORIZED", err.Code)
	assert.Equal(t, "token expired", err.Message)
	assert.Equal(t, http.StatusUnauthorized, err.HTTPStatus)
}

func TestErrorHelpers_Forbidden(t *testing.T) {
	err := httpadapter.ErrForbidden("insufficient permissions")
	
	assert.Equal(t, "FORBIDDEN", err.Code)
	assert.Equal(t, "insufficient permissions", err.Message)
	assert.Equal(t, http.StatusForbidden, err.HTTPStatus)
}

func TestErrorHelpers_NotFound(t *testing.T) {
	err := httpadapter.ErrNotFound("resource not found")
	
	assert.Equal(t, "NOT_FOUND", err.Code)
	assert.Equal(t, "resource not found", err.Message)
	assert.Equal(t, http.StatusNotFound, err.HTTPStatus)
}

func TestErrorHelpers_Internal(t *testing.T) {
	underlyingErr := errors.New("database connection failed")
	err := httpadapter.ErrInternal("database error", underlyingErr)
	
	assert.Equal(t, "INTERNAL_ERROR", err.Code)
	assert.Equal(t, "database error", err.Message)
	assert.Equal(t, http.StatusInternalServerError, err.HTTPStatus)
	assert.Equal(t, underlyingErr, err.Err)
}

func TestAppError_Error(t *testing.T) {
	// Without underlying error
	err1 := httpadapter.NewAppError("TEST", "test message", 400, nil)
	assert.Equal(t, "test message", err1.Error())
	
	// With underlying error
	underlyingErr := errors.New("underlying")
	err2 := httpadapter.NewAppError("TEST", "test message", 400, underlyingErr)
	assert.Equal(t, "test message: underlying", err2.Error())
}

func TestAppError_Unwrap(t *testing.T) {
	underlyingErr := errors.New("underlying error")
	err := httpadapter.NewAppError("TEST", "test", 400, underlyingErr)
	
	assert.Equal(t, underlyingErr, errors.Unwrap(err))
}

