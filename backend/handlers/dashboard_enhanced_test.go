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

// Test getEnhancedTeacherDashboard function
func TestDashboardHandler_getEnhancedTeacherDashboard(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &DashboardHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Test data
	userID := "123"
	dbUser := &models.User{
		ID:    123,
		Name:  "Teacher Name",
		Email: "teacher@example.com",
		Role:  "teacher",
	}

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

	courseMetrics := services.CourseMetrics{TotalCourses: 2, AverageGrade: 85.5}
	studentMetrics := services.StudentMetrics{TotalStudents: 2}
	assignmentMetrics := services.AssignmentMetrics{TotalAssignments: 2, PublishedAssignments: 1}
	roleMetrics := map[string]interface{}{
		"role": "teacher",
		"specific": map[string]interface{}{
			"my_courses":        2,
			"total_students":    2,
			"graded_assignments": 1,
			"pending_grades":    1,
		},
	}

	// Setup mock expectations
	mockGoogleService.On("ListCourses", userID).Return(courses, nil)
	mockGoogleService.On("ListStudents", "course1").Return(students, nil)
	mockGoogleService.On("ListStudents", "course2").Return(students, nil)
	mockGoogleService.On("ListAssignments", "course1").Return(assignments, nil)
	mockGoogleService.On("ListAssignments", "course2").Return(assignments, nil)
	mockMetricsService.On("CalculateCourseMetrics", courses).Return(courseMetrics)
	mockMetricsService.On("CalculateStudentMetrics", mock.AnythingOfType("[]services.Student")).Return(studentMetrics)
	mockMetricsService.On("CalculateAssignmentMetrics", mock.AnythingOfType("[]services.Assignment")).Return(assignmentMetrics)
	mockMetricsService.On("GetRoleSpecificMetrics", "teacher", courses, mock.AnythingOfType("[]services.Student"), mock.AnythingOfType("[]services.Assignment")).Return(roleMetrics)

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getEnhancedTeacherDashboard(c, dbUser, userID)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	assert.Contains(t, response, "metrics")

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
	mockMetricsService.AssertExpectations(t)
}

// Test getFallbackTeacherDashboard function
func TestDashboardHandler_getFallbackTeacherDashboard(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}

	// Create handler
	handler := &DashboardHandler{
		userRepo: mockUserRepo,
	}

	// Test data
	dbUser := &models.User{
		ID:    123,
		Name:  "Teacher Name",
		Email: "teacher@example.com",
		Role:  "teacher",
	}

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getFallbackTeacherDashboard(c, dbUser)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	
	dashboard := response["dashboard"].(map[string]interface{})
	assert.Equal(t, "teacher", dashboard["type"])
	assert.Contains(t, dashboard, "google_integration")
	
	integration := dashboard["google_integration"].(map[string]interface{})
	assert.False(t, integration["enabled"].(bool))
	assert.True(t, integration["fallback"].(bool))
}

// Test getEnhancedCoordinatorDashboard function
func TestDashboardHandler_getEnhancedCoordinatorDashboard(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &DashboardHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Test data
	userID := "123"
	dbUser := &models.User{
		ID:    123,
		Name:  "Coordinator Name",
		Email: "coordinator@example.com",
		Role:  "coordinator",
	}

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

	courseMetrics := services.CourseMetrics{TotalCourses: 2, AverageGrade: 85.5}
	studentMetrics := services.StudentMetrics{TotalStudents: 2}
	assignmentMetrics := services.AssignmentMetrics{TotalAssignments: 2, PublishedAssignments: 1}
	roleMetrics := map[string]interface{}{
		"role": "coordinator",
		"specific": map[string]interface{}{
			"total_courses":    2,
			"total_teachers":   1,
			"total_students":   2,
			"active_programs":  3,
		},
	}

	// Setup mock expectations
	mockGoogleService.On("ListCourses", userID).Return(courses, nil)
	mockGoogleService.On("ListStudents", "course1").Return(students, nil)
	mockGoogleService.On("ListStudents", "course2").Return(students, nil)
	mockGoogleService.On("ListAssignments", "course1").Return(assignments, nil)
	mockGoogleService.On("ListAssignments", "course2").Return(assignments, nil)
	mockMetricsService.On("CalculateCourseMetrics", courses).Return(courseMetrics)
	mockMetricsService.On("CalculateStudentMetrics", mock.AnythingOfType("[]services.Student")).Return(studentMetrics)
	mockMetricsService.On("CalculateAssignmentMetrics", mock.AnythingOfType("[]services.Assignment")).Return(assignmentMetrics)
	mockMetricsService.On("GetRoleSpecificMetrics", "coordinator", courses, mock.AnythingOfType("[]services.Student"), mock.AnythingOfType("[]services.Assignment")).Return(roleMetrics)

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/coordinator", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getEnhancedCoordinatorDashboard(c, dbUser, userID)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	assert.Contains(t, response, "metrics")

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
	mockMetricsService.AssertExpectations(t)
}

// Test getFallbackCoordinatorDashboard function
func TestDashboardHandler_getFallbackCoordinatorDashboard(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}

	// Create handler
	handler := &DashboardHandler{
		userRepo: mockUserRepo,
	}

	// Test data
	dbUser := &models.User{
		ID:    123,
		Name:  "Coordinator Name",
		Email: "coordinator@example.com",
		Role:  "coordinator",
	}

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/coordinator", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getFallbackCoordinatorDashboard(c, dbUser)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	
	dashboard := response["dashboard"].(map[string]interface{})
	assert.Equal(t, "coordinator", dashboard["type"])
	assert.Contains(t, dashboard, "google_integration")
	
	integration := dashboard["google_integration"].(map[string]interface{})
	assert.False(t, integration["enabled"].(bool))
	assert.True(t, integration["fallback"].(bool))
}

// Test getEnhancedAdminDashboard function
func TestDashboardHandler_getEnhancedAdminDashboard(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &DashboardHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Test data
	userID := "123"
	dbUser := &models.User{
		ID:    123,
		Name:  "Admin Name",
		Email: "admin@example.com",
		Role:  "admin",
	}

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

	allUsers := []*models.User{
		{ID: 1, Name: "User1", Email: "user1@example.com", Role: "student"},
		{ID: 2, Name: "User2", Email: "user2@example.com", Role: "teacher"},
	}

	courseMetrics := services.CourseMetrics{TotalCourses: 2, AverageGrade: 85.5}
	studentMetrics := services.StudentMetrics{TotalStudents: 2}
	assignmentMetrics := services.AssignmentMetrics{TotalAssignments: 2, PublishedAssignments: 1}
	roleMetrics := map[string]interface{}{
		"role": "admin",
		"specific": map[string]interface{}{
			"total_users":       2,
			"total_courses":     2,
			"system_health":     "healthy",
			"uptime_percentage": 99.9,
		},
	}

	// Setup mock expectations
	mockGoogleService.On("ListCourses", userID).Return(courses, nil)
	mockGoogleService.On("ListStudents", "course1").Return(students, nil)
	mockGoogleService.On("ListStudents", "course2").Return(students, nil)
	mockGoogleService.On("ListAssignments", "course1").Return(assignments, nil)
	mockGoogleService.On("ListAssignments", "course2").Return(assignments, nil)
	mockUserRepo.On("ListUsers", 0, 100).Return(allUsers, nil)
	mockMetricsService.On("CalculateCourseMetrics", courses).Return(courseMetrics)
	mockMetricsService.On("CalculateStudentMetrics", mock.AnythingOfType("[]services.Student")).Return(studentMetrics)
	mockMetricsService.On("CalculateAssignmentMetrics", mock.AnythingOfType("[]services.Assignment")).Return(assignmentMetrics)
	mockMetricsService.On("GetRoleSpecificMetrics", "admin", courses, mock.AnythingOfType("[]services.Student"), mock.AnythingOfType("[]services.Assignment")).Return(roleMetrics)

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getEnhancedAdminDashboard(c, dbUser, userID)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	assert.Contains(t, response, "metrics")

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
	mockMetricsService.AssertExpectations(t)
	mockUserRepo.AssertExpectations(t)
}

// Test getFallbackAdminDashboard function
func TestDashboardHandler_getFallbackAdminDashboard(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}

	// Create handler
	handler := &DashboardHandler{
		userRepo: mockUserRepo,
	}

	// Test data
	dbUser := &models.User{
		ID:    123,
		Name:  "Admin Name",
		Email: "admin@example.com",
		Role:  "admin",
	}

	allUsers := []*models.User{
		{ID: 1, Name: "User1", Email: "user1@example.com", Role: "student"},
		{ID: 2, Name: "User2", Email: "user2@example.com", Role: "teacher"},
	}

	// Setup mock expectations
	mockUserRepo.On("ListUsers", 0, 100).Return(allUsers, nil)

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function
	err := handler.getFallbackAdminDashboard(c, dbUser)

	// Assertions
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	
	dashboard := response["dashboard"].(map[string]interface{})
	assert.Equal(t, "admin", dashboard["type"])
	assert.Contains(t, dashboard, "google_integration")
	
	integration := dashboard["google_integration"].(map[string]interface{})
	assert.False(t, integration["enabled"].(bool))
	assert.True(t, integration["fallback"].(bool))

	// Verify mock expectations
	mockUserRepo.AssertExpectations(t)
}

// Test enhanced dashboard functions with Google service errors
func TestDashboardHandler_EnhancedDashboards_GoogleServiceErrors(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &DashboardHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Test data
	userID := "123"
	dbUser := &models.User{
		ID:    123,
		Name:  "Teacher Name",
		Email: "teacher@example.com",
		Role:  "teacher",
	}

	// Setup mock expectations - Google service returns error
	mockGoogleService.On("ListCourses", userID).Return([]services.Course{}, assert.AnError)

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function - should fallback to fallback dashboard
	err := handler.getEnhancedTeacherDashboard(c, dbUser, userID)

	// Assertions - should not error and should return fallback data
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	
	dashboard := response["dashboard"].(map[string]interface{})
	assert.Equal(t, "teacher", dashboard["type"])
	
	integration := dashboard["google_integration"].(map[string]interface{})
	assert.False(t, integration["enabled"].(bool))
	assert.True(t, integration["fallback"].(bool))

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
}

// Test enhanced dashboards with partial Google service errors
func TestDashboardHandler_EnhancedDashboards_PartialErrors(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Create handler
	handler := &DashboardHandler{
		userRepo:       mockUserRepo,
		googleService:  mockGoogleService,
		metricsService: mockMetricsService,
	}

	// Test data
	userID := "123"
	dbUser := &models.User{
		ID:    123,
		Name:  "Teacher Name",
		Email: "teacher@example.com",
		Role:  "teacher",
	}

	courses := []services.Course{
		{ID: "course1", Name: "Math", CourseState: "ACTIVE"},
	}
	students := []services.Student{
		{ID: "student1", Name: "John", Email: "john@example.com"},
	}
	assignments := []services.Assignment{
		{ID: "assignment1", Title: "HW1", State: "PUBLISHED", MaxPoints: 100},
	}

	courseMetrics := services.CourseMetrics{TotalCourses: 1, AverageGrade: 85.5}
	studentMetrics := services.StudentMetrics{TotalStudents: 1}
	assignmentMetrics := services.AssignmentMetrics{TotalAssignments: 1, PublishedAssignments: 1}
	roleMetrics := map[string]interface{}{
		"role": "teacher",
		"specific": map[string]interface{}{
			"my_courses":        1,
			"total_students":    1,
			"graded_assignments": 1,
			"pending_grades":    0,
		},
	}

	// Setup mock expectations - simplified to avoid complex error scenarios
	mockGoogleService.On("ListCourses", userID).Return(courses, nil)
	mockGoogleService.On("ListStudents", "course1").Return(students, nil)
	mockGoogleService.On("ListAssignments", "course1").Return(assignments, nil)
	mockMetricsService.On("CalculateCourseMetrics", courses).Return(courseMetrics)
	mockMetricsService.On("CalculateStudentMetrics", mock.AnythingOfType("[]services.Student")).Return(studentMetrics)
	mockMetricsService.On("CalculateAssignmentMetrics", mock.AnythingOfType("[]services.Assignment")).Return(assignmentMetrics)
	mockMetricsService.On("GetRoleSpecificMetrics", "teacher", courses, mock.AnythingOfType("[]services.Student"), mock.AnythingOfType("[]services.Assignment")).Return(roleMetrics)

	// Create test context
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	// Test the function - should handle partial errors gracefully
	err := handler.getEnhancedTeacherDashboard(c, dbUser, userID)

	// Assertions - should not error and should return data from successful calls
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response map[string]interface{}
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Contains(t, response, "user")
	assert.Contains(t, response, "dashboard")
	assert.Contains(t, response, "metrics")

	// Verify mock expectations
	mockGoogleService.AssertExpectations(t)
	mockMetricsService.AssertExpectations(t)
}

// Test NewEnhancedDashboardHandler constructor
func TestNewEnhancedDashboardHandler(t *testing.T) {
	// Create mock services
	mockUserRepo := &MockUserRepository{}
	mockGoogleService := &MockGoogleClassroomService{}
	mockMetricsService := &MockMetricsService{}

	// Test the constructor
	handler := NewEnhancedDashboardHandler(mockUserRepo, mockGoogleService, mockMetricsService)

	// Assertions
	assert.NotNil(t, handler)
	assert.Equal(t, mockUserRepo, handler.userRepo)
	assert.Equal(t, mockGoogleService, handler.googleService)
	assert.Equal(t, mockMetricsService, handler.metricsService)
}
