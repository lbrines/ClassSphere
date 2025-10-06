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
	"github.com/stretchr/testify/mock"
)

// Test GetPerformanceMetrics function - test successful case
func TestGoogleHandler_GetPerformanceMetrics_Success(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Test data
	courses := []services.Course{
		{ID: "course1", Name: "Math", CourseState: "ACTIVE"},
		{ID: "course2", Name: "Science", CourseState: "ACTIVE"},
	}
	students := []services.Student{
		{ID: "student1", Name: "John", Email: "john@example.com"},
		{ID: "student2", Name: "Jane", Email: "jane@example.com"},
	}
	assignments := []services.Assignment{
		{ID: "assignment1", Title: "HW1", State: "PUBLISHED", MaxPoints: 100},
		{ID: "assignment2", Title: "HW2", State: "DRAFT", MaxPoints: 150},
	}

	// Setup mock expectations
	mockGoogleService.On("ListCourses", "123").Return(courses, nil)
	mockGoogleService.On("ListStudents", "course1").Return(students, nil)
	mockGoogleService.On("ListStudents", "course2").Return(students, nil)
	mockGoogleService.On("ListAssignments", "course1").Return(assignments, nil)
	mockGoogleService.On("ListAssignments", "course2").Return(assignments, nil)

	// Create handler
	handler := &GoogleHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Create test context with user
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/google/performance/metrics", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context
	claims := &auth.Claims{
		UserID: "123",
		Role:   "admin",
	}
	c.Set("user", claims)

	// Test the function
	err := handler.GetPerformanceMetrics(c)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user_id")
	assert.Contains(t, response, "metrics")
	assert.Contains(t, response, "trends")
	assert.Contains(t, response, "timestamp")
	assert.Equal(t, "123", response["user_id"])

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
}

// Test GetDashboardMetrics function - test successful case
func TestGoogleHandler_GetDashboardMetrics_Success(t *testing.T) {
	// Create mock services
	mockUserRepo := &models.UserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Test data
	courses := []services.Course{
		{ID: "course1", Name: "Math", CourseState: "ACTIVE"},
		{ID: "course2", Name: "Science", CourseState: "ACTIVE"},
	}
	students := []services.Student{
		{ID: "student1", Name: "John", Email: "john@example.com"},
		{ID: "student2", Name: "Jane", Email: "jane@example.com"},
	}
	assignments := []services.Assignment{
		{ID: "assignment1", Title: "HW1", State: "PUBLISHED", MaxPoints: 100},
		{ID: "assignment2", Title: "HW2", State: "DRAFT", MaxPoints: 150},
	}

	roleMetrics := map[string]interface{}{
		"role": "admin",
		"base": map[string]interface{}{
			"courses": map[string]interface{}{
				"total_courses": 2,
			},
		},
		"specific": map[string]interface{}{
			"total_users":   3,
			"total_courses": 2,
		},
	}

	// Setup mock expectations
	mockGoogleService.On("ListCourses", "123").Return(courses, nil)
	mockGoogleService.On("ListStudents", "course1").Return(students, nil)
	mockGoogleService.On("ListStudents", "course2").Return(students, nil)
	mockGoogleService.On("ListAssignments", "course1").Return(assignments, nil)
	mockGoogleService.On("ListAssignments", "course2").Return(assignments, nil)
	mockMetricsService.On("GetRoleSpecificMetrics", "admin", courses, mock.AnythingOfType("[]services.Student"), mock.AnythingOfType("[]services.Assignment")).Return(roleMetrics)

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

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "role")
	assert.Equal(t, "admin", response["role"])

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
	mockMetricsService.AssertExpectations(t)
}
