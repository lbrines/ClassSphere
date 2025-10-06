package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"classsphere-backend/auth"
	"classsphere-backend/models"
	"classsphere-backend/services"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

// Test NewGoogleHandler constructor
func TestNewGoogleHandler(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{} // Use actual UserRepository type
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Test the constructor
	handler := NewGoogleHandler(mockUserRepo, mockGoogleService, mockMetricsService)

	// Assertions
	assert.NotNil(t, handler)
	assert.Equal(t, mockUserRepo, handler.userRepo)
	assert.Equal(t, mockGoogleService, handler.googleService)
	assert.Equal(t, mockMetricsService, handler.metricsService)
}

// Test GetDashboardMetrics function - simplified version
func TestGoogleHandler_GetDashboardMetrics(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context without user (to test error path)
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/dashboard/metrics", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function without user context
	err := handler.GetDashboardMetrics(c)

	// Assertions - should return unauthorized
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "error")
	assert.Equal(t, "User not authenticated", response["error"])
}

// Test GetDashboardMetrics function - test invalid user context
func TestGoogleHandler_GetDashboardMetrics_InvalidUserContext(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context with invalid user context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/dashboard/metrics", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set invalid user context (not *auth.Claims)
	c.Set("user", "invalid_user_context")

	// Test the function
	err := handler.GetDashboardMetrics(c)

	// Assertions - should return unauthorized
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "error")
	assert.Equal(t, "Invalid user context", response["error"])
}

// Test GetDashboardMetrics function - test service error
func TestGoogleHandler_GetDashboardMetrics_ServiceError(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Setup mock to return error
	mockGoogleService.On("ListCourses", "123").Return([]services.Course{}, assert.AnError)

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context with user
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/dashboard/metrics", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context
	claims := &auth.Claims{
		UserID: "123",
		Role:   "admin",
	}
	c.Set("user", claims)

	// Test the function
	err := handler.GetDashboardMetrics(c)

	// Assertions - should return internal server error
	assert.NoError(t, err)
	assert.Equal(t, http.StatusInternalServerError, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "error")
	assert.Equal(t, "Failed to retrieve courses", response["error"])

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
}

// Test GetSystemStatus function
func TestGoogleHandler_GetSystemStatus(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context with user
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/system/status", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context
	claims := &auth.Claims{
		UserID: "123",
		Role:   "admin",
	}
	c.Set("user", claims)

	// Test the function
	err := handler.GetSystemStatus(c)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "service_status")
	assert.Equal(t, "operational", response["service_status"])
}

// Test GetSystemStatus function - test without user context
func TestGoogleHandler_GetSystemStatus_NoUser(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context without user
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/system/status", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.GetSystemStatus(c)

	// Assertions - should return unauthorized
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "error")
	assert.Equal(t, "User not authenticated", response["error"])
}

// Test GetSystemStatus function - test invalid user context
func TestGoogleHandler_GetSystemStatus_InvalidUserContext(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context with invalid user context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/system/status", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set invalid user context (not *auth.Claims)
	c.Set("user", "invalid_user_context")

	// Test the function
	err := handler.GetSystemStatus(c)

	// Assertions - should return unauthorized
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "error")
	assert.Equal(t, "Invalid user context", response["error"])
}

// Test GetPerformanceMetrics function - test error path
func TestGoogleHandler_GetPerformanceMetrics(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context without user (to test error path)
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/performance/metrics", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function without user context
	err := handler.GetPerformanceMetrics(c)

	// Assertions - should return unauthorized
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "error")
	assert.Equal(t, "User not authenticated", response["error"])
}
