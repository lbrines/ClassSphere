package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)


// Test getFallbackAdminDashboard with ListUsers error
func TestDashboardHandler_getFallbackAdminDashboard_ListUsersError(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Setup mock to return error for ListUsers
	mockUserRepo.On("ListUsers", 0, 100).Return([]*models.User{}, assert.AnError)

	// Create handler
	handler := &DashboardHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test user
	testUser := &models.User{
		ID:    123,
		Name:  "Test Admin",
		Email: "admin@test.com",
		Role:  "admin",
	}

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getFallbackAdminDashboard(c, testUser)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "dashboard")
	
	dashboard := response["dashboard"].(map[string]interface{})
	stats := dashboard["stats"].(map[string]interface{})
	assert.Equal(t, float64(0), stats["total_users"]) // Should be 0 due to error fallback

	// Verify mock expectations
	mockUserRepo.AssertExpectations(t)
}

// Test getFallbackAdminDashboard with successful ListUsers
func TestDashboardHandler_getFallbackAdminDashboard_Success(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Setup mock to return success for ListUsers
	testUsers := []*models.User{
		{ID: 1, Name: "User 1", Email: "user1@test.com", Role: "student"},
		{ID: 2, Name: "User 2", Email: "user2@test.com", Role: "teacher"},
		{ID: 3, Name: "User 3", Email: "user3@test.com", Role: "admin"},
	}
	mockUserRepo.On("ListUsers", 0, 100).Return(testUsers, nil)

	// Create handler
	handler := &DashboardHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test user
	testUser := &models.User{
		ID:    123,
		Name:  "Test Admin",
		Email: "admin@test.com",
		Role:  "admin",
	}

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getFallbackAdminDashboard(c, testUser)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "dashboard")
	
	dashboard := response["dashboard"].(map[string]interface{})
	stats := dashboard["stats"].(map[string]interface{})
	assert.Equal(t, float64(3), stats["total_users"]) // Should be 3 users

	// Verify mock expectations
	mockUserRepo.AssertExpectations(t)
}
