package http

import (
	"errors"
	"log/slog"
	"net/http"

	echo "github.com/labstack/echo/v4"

	"github.com/lbrines/classsphere/internal/shared"
)

// ErrorResponse represents a standardized error response structure.
type ErrorResponse struct {
	Error   string `json:"error"`           // Human-readable error message
	Code    string `json:"code,omitempty"`  // Application-specific error code
	Details string `json:"details,omitempty"` // Additional error details
	RequestID string `json:"requestId,omitempty"` // Request ID for tracing
}

// AppError represents an application-level error with metadata.
type AppError struct {
	Code       string // Application-specific error code (e.g., "AUTH_INVALID_TOKEN")
	Message    string // Human-readable message
	Details    string // Additional context
	HTTPStatus int    // HTTP status code to return
	Err        error  // Underlying error (for logging/debugging)
}

// Error implements the error interface.
func (e *AppError) Error() string {
	if e.Err != nil {
		return e.Message + ": " + e.Err.Error()
	}
	return e.Message
}

// Unwrap returns the underlying error.
func (e *AppError) Unwrap() error {
	return e.Err
}

// NewAppError creates a new application error.
func NewAppError(code, message string, httpStatus int, err error) *AppError {
	return &AppError{
		Code:       code,
		Message:    message,
		HTTPStatus: httpStatus,
		Err:        err,
	}
}

// Common application errors
var (
	ErrBadRequest = func(message string) *AppError {
		return NewAppError("BAD_REQUEST", message, http.StatusBadRequest, nil)
	}
	ErrUnauthorized = func(message string) *AppError {
		return NewAppError("UNAUTHORIZED", message, http.StatusUnauthorized, nil)
	}
	ErrForbidden = func(message string) *AppError {
		return NewAppError("FORBIDDEN", message, http.StatusForbidden, nil)
	}
	ErrNotFound = func(message string) *AppError {
		return NewAppError("NOT_FOUND", message, http.StatusNotFound, nil)
	}
	ErrInternal = func(message string, err error) *AppError {
		return NewAppError("INTERNAL_ERROR", message, http.StatusInternalServerError, err)
	}
)

// ErrorHandlerMiddleware is a centralized error handler for Echo framework.
// It catches all errors returned by handlers and formats them consistently.
// It also logs errors with appropriate context for debugging and monitoring.
func ErrorHandlerMiddleware() echo.MiddlewareFunc {
	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			// Execute the handler
			err := next(c)
			if err == nil {
				return nil
			}

			// Extract request ID for tracing
			requestID := c.Response().Header().Get(echo.HeaderXRequestID)

			// Determine the appropriate HTTP status and error response
			var (
				httpStatus int
				errorCode  string
				errorMsg   string
				details    string
			)

			// Handle different error types
			switch e := err.(type) {
			case *AppError:
				// Application-specific error with full metadata
				httpStatus = e.HTTPStatus
				errorCode = e.Code
				errorMsg = e.Message
				details = e.Details

				// Log based on severity
				if httpStatus >= 500 {
					slog.Error("internal error",
						"code", errorCode,
						"message", errorMsg,
						"error", e.Err,
						"requestId", requestID,
						"path", c.Request().URL.Path,
						"method", c.Request().Method)
				} else if httpStatus >= 400 {
					slog.Warn("client error",
						"code", errorCode,
						"message", errorMsg,
						"requestId", requestID,
						"path", c.Request().URL.Path,
						"method", c.Request().Method)
				}

			case *echo.HTTPError:
				// Echo's standard HTTP error
				httpStatus = e.Code
				errorMsg = extractMessage(e.Message)
				errorCode = httpStatusToCode(httpStatus)

				// Log based on status
				if httpStatus >= 500 {
					slog.Error("http error",
						"status", httpStatus,
						"message", errorMsg,
						"requestId", requestID,
						"path", c.Request().URL.Path,
						"method", c.Request().Method)
				} else if httpStatus >= 400 {
					slog.Debug("client error",
						"status", httpStatus,
						"message", errorMsg,
						"requestId", requestID,
						"path", c.Request().URL.Path)
				}

			default:
				// Handle known domain errors
				if errors.Is(err, shared.ErrUnauthorized) {
					httpStatus = http.StatusUnauthorized
					errorCode = "UNAUTHORIZED"
					errorMsg = "unauthorized"
				} else if errors.Is(err, shared.ErrForbidden) {
					httpStatus = http.StatusForbidden
					errorCode = "FORBIDDEN"
					errorMsg = "forbidden"
				} else if errors.Is(err, shared.ErrUserNotFound) {
					httpStatus = http.StatusNotFound
					errorCode = "USER_NOT_FOUND"
					errorMsg = "user not found"
				} else if errors.Is(err, shared.ErrInvalidCredentials) {
					httpStatus = http.StatusUnauthorized
					errorCode = "INVALID_CREDENTIALS"
					errorMsg = "invalid credentials"
				} else {
					// Unknown error - treat as internal server error
					httpStatus = http.StatusInternalServerError
					errorCode = "INTERNAL_ERROR"
					errorMsg = "internal server error"

					slog.Error("unexpected error",
						"error", err,
						"requestId", requestID,
						"path", c.Request().URL.Path,
						"method", c.Request().Method)
				}
			}

			// Create standardized error response
			response := ErrorResponse{
				Error:     errorMsg,
				Code:      errorCode,
				Details:   details,
				RequestID: requestID,
			}

			// Send JSON response
			// Don't return the error again as we've already handled it
			if err := c.JSON(httpStatus, response); err != nil {
				slog.Error("failed to send error response",
					"error", err,
					"requestId", requestID)
			}

			// Return nil to prevent Echo from processing the error again
			return nil
		}
	}
}

// extractMessage extracts a string message from various types.
func extractMessage(msg interface{}) string {
	switch v := msg.(type) {
	case string:
		return v
	case error:
		return v.Error()
	default:
		return "an error occurred"
	}
}

// httpStatusToCode maps HTTP status codes to error codes.
func httpStatusToCode(status int) string {
	switch status {
	case http.StatusBadRequest:
		return "BAD_REQUEST"
	case http.StatusUnauthorized:
		return "UNAUTHORIZED"
	case http.StatusForbidden:
		return "FORBIDDEN"
	case http.StatusNotFound:
		return "NOT_FOUND"
	case http.StatusConflict:
		return "CONFLICT"
	case http.StatusInternalServerError:
		return "INTERNAL_ERROR"
	case http.StatusServiceUnavailable:
		return "SERVICE_UNAVAILABLE"
	default:
		return "ERROR"
	}
}

