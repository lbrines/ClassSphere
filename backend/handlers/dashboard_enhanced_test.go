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

// MockGoogleClassroomService and MockMetricsService are defined in google_test.go

// MockUserRepository for testing
type MockUserRepository struct {
	mock.Mock
}

func (m *MockUserRepository) CreateUser(user *models.User) error {
	args := m.Called(user)
	return args.Error(0)
}

func (m *MockUserRepository) GetUserByEmail(email string) (*models.User, error) {
	args := m.Called(email)
	return args.Get(0).(*models.User), args.Error(1)
}

func (m *MockUserRepository) GetUserByID(id uint) (*models.User, error) {
	args := m.Called(id)
	return args.Get(0).(*models.User), args.Error(1)
}

func (m *MockUserRepository) UpdateUser(user *models.User) error {
	args := m.Called(user)
	return args.Error(0)
}

func (m *MockUserRepository) DeleteUser(id uint) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockUserRepository) ListUsers(offset, limit int) ([]*models.User, error) {
	args := m.Called(offset, limit)
	return args.Get(0).([]*models.User), args.Error(1)
}

func (m *MockUserRepository) GetUserCount() (int64, error) {
	args := m.Called()
	return args.Get(0).(int64), args.Error(1)
}

func (m *MockUserRepository) DeactivateUser(id uint) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockUserRepository) ActivateUser(id uint) error {
	args := m.Called(id)
	return args.Error(0)
}

func TestDashboardHandler_GetStudentDashboard_Enhanced(t *testing.T) {
	e := echo.New()
	
	// Create mocks
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}
	
	// Create handler with enhanced services
	handler := NewEnhancedDashboardHandler(mockUserRepo, mockGoogleService, mockMetricsService)
	
	// Mock user data
	mockUser := &models.User{
		ID:    1,
		Name:  "Test Student",
		Email: "student@test.com",
		Role:  "student",
	}
	
	// Mock courses
	mockCourses := []services.Course{
		{
			ID:          "course_1",
			Name:        "Math",
			Description: "Mathematics course",
			Section:     "A",
			Room:        "Room 101",
			OwnerID:     "teacher_1",
			CourseState: "ACTIVE",
		},
	}
	
	// Mock assignments
	mockAssignments := []services.Assignment{
		{
			ID:          "assignment_1",
			Title:       "Math Homework",
			Description: "Complete exercises",
			DueDate:     "2025-10-10",
			MaxPoints:   100,
			State:       "PUBLISHED",
		},
	}
	
	// Mock metrics
	mockCourseMetrics := services.CourseMetrics{
		TotalCourses:     1,
		ActiveCourses:    1,
		ArchivedCourses:  0,
		TotalStudents:    10,
		AverageGrade:     85.5,
		TotalAssignments: 1,
	}
	
	mockAssignmentMetrics := services.AssignmentMetrics{
		TotalAssignments:     1,
		PublishedAssignments: 1,
		DraftAssignments:     0,
		TotalPoints:          100,
		AveragePoints:        100.0,
	}
	
	mockRoleMetrics := map[string]interface{}{
		"student_specific": "data",
	}
	
	// Setup mock expectations
	mockUserRepo.On("GetUserByID", uint(1)).Return(mockUser, nil)
	mockGoogleService.On("ListCourses", "1").Return(mockCourses, nil)
	mockGoogleService.On("ListAssignments", "course_1").Return(mockAssignments, nil)
	mockMetricsService.On("CalculateCourseMetrics", mockCourses).Return(mockCourseMetrics)
	mockMetricsService.On("CalculateAssignmentMetrics", mockAssignments).Return(mockAssignmentMetrics)
	mockMetricsService.On("GetRoleSpecificMetrics", "student", mockCourses, []services.Student{}, mockAssignments).Return(mockRoleMetrics)
	
	// Create request
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context
	claims := &auth.Claims{
		UserID: "1",
		Role:   "student",
	}
	c.Set("user", claims)
	
	// Test
	err := handler.GetStudentDashboard(c)
	
	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	// Parse response
	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	
	// Verify response structure
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	assert.Contains(t, response, "metrics")
	assert.Contains(t, response, "timestamp")
	
	// Verify dashboard data
	dashboard := response["dashboard"].(map[string]interface{})
	assert.Equal(t, "student", dashboard["type"])
	
	// Verify Google integration is enabled
	googleIntegration := dashboard["google_integration"].(map[string]interface{})
	assert.True(t, googleIntegration["enabled"].(bool))
	assert.Equal(t, float64(1), googleIntegration["courses_count"])
	assert.Equal(t, float64(1), googleIntegration["assignments_count"])
	
	// Verify mock expectations
	mockUserRepo.AssertExpectations(t)
	mockGoogleService.AssertExpectations(t)
	mockMetricsService.AssertExpectations(t)
}

func TestDashboardHandler_GetStudentDashboard_Fallback(t *testing.T) {
	e := echo.New()
	
	// Create mocks
	mockUserRepo := &MockUserRepository{}
	
	// Create handler without enhanced services (fallback mode)
	handler := NewDashboardHandler(mockUserRepo)
	
	// Mock user data
	mockUser := &models.User{
		ID:    1,
		Name:  "Test Student",
		Email: "student@test.com",
		Role:  "student",
	}
	
	// Setup mock expectations
	mockUserRepo.On("GetUserByID", uint(1)).Return(mockUser, nil)
	
	// Create request
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context
	claims := &auth.Claims{
		UserID: "1",
		Role:   "student",
	}
	c.Set("user", claims)
	
	// Test
	err := handler.GetStudentDashboard(c)
	
	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	// Parse response
	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	
	// Verify response structure
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	assert.Contains(t, response, "timestamp")
	
	// Verify dashboard data
	dashboard := response["dashboard"].(map[string]interface{})
	assert.Equal(t, "student", dashboard["type"])
	
	// Verify mock expectations
	mockUserRepo.AssertExpectations(t)
}

func TestDashboardHandler_GetStudentDashboard_GoogleServiceError(t *testing.T) {
	e := echo.New()
	
	// Create mocks
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}
	
	// Create handler with enhanced services
	handler := NewEnhancedDashboardHandler(mockUserRepo, mockGoogleService, mockMetricsService)
	
	// Mock user data
	mockUser := &models.User{
		ID:    1,
		Name:  "Test Student",
		Email: "student@test.com",
		Role:  "student",
	}
	
	// Setup mock expectations - Google service returns error
	mockUserRepo.On("GetUserByID", uint(1)).Return(mockUser, nil)
	mockGoogleService.On("ListCourses", "1").Return([]services.Course{}, assert.AnError)
	
	// Create request
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context
	claims := &auth.Claims{
		UserID: "1",
		Role:   "student",
	}
	c.Set("user", claims)
	
	// Test
	err := handler.GetStudentDashboard(c)
	
	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	// Parse response
	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	
	// Verify response structure
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	
	// Verify fallback mode is used
	dashboard := response["dashboard"].(map[string]interface{})
	googleIntegration := dashboard["google_integration"].(map[string]interface{})
	assert.False(t, googleIntegration["enabled"].(bool))
	assert.True(t, googleIntegration["fallback"].(bool))
	
	// Verify mock expectations
	mockUserRepo.AssertExpectations(t)
	mockGoogleService.AssertExpectations(t)
}

func TestDashboardHandler_GetStudentDashboard_Unauthorized(t *testing.T) {
	e := echo.New()
	
	// Create handler
	handler := NewDashboardHandler(nil)
	
	// Create request
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Test without user in context
	err := handler.GetStudentDashboard(c)
	
	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
	
	// Verify error response
	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "User not authenticated", response["error"])
}

func TestDashboardHandler_GetStudentDashboard_InvalidUserID(t *testing.T) {
	e := echo.New()
	
	// Create handler
	handler := NewDashboardHandler(nil)
	
	// Create request
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set invalid user in context
	claims := &auth.Claims{
		UserID: "invalid",
		Role:   "student",
	}
	c.Set("user", claims)
	
	// Test
	err := handler.GetStudentDashboard(c)
	
	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
	
	// Verify error response
	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "Invalid user ID", response["error"])
}

func TestDashboardHandler_GetStudentDashboard_UserNotFound(t *testing.T) {
	e := echo.New()
	
	// Create mocks
	mockUserRepo := &MockUserRepository{}
	
	// Create handler
	handler := NewDashboardHandler(mockUserRepo)
	
	// Setup mock expectations - user not found
	mockUserRepo.On("GetUserByID", uint(1)).Return((*models.User)(nil), assert.AnError)
	
	// Create request
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context
	claims := &auth.Claims{
		UserID: "1",
		Role:   "student",
	}
	c.Set("user", claims)
	
	// Test
	err := handler.GetStudentDashboard(c)
	
	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusNotFound, rec.Code)
	
	// Verify error response
	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "User not found", response["error"])
	
	// Verify mock expectations
	mockUserRepo.AssertExpectations(t)
}
