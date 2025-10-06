package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"classsphere-backend/services"
)


func TestDashboardAPI_Integration(t *testing.T) {
	t.Run("GET /api/dashboard/admin - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock data
		mockData := map[string]interface{}{
			"user": map[string]interface{}{
				"id":    1,
				"name":  "Admin User",
				"email": "admin@test.com",
				"role":  "admin",
			},
			"timestamp": time.Now().Format(time.RFC3339),
			"dashboard": map[string]interface{}{
				"type": "admin",
				"stats": map[string]interface{}{
					"total_users":     150,
					"total_courses":   25,
					"total_students":  1200,
					"total_teachers":  50,
					"system_uptime":   "99.9%",
					"active_sessions": 45,
				},
			},
		}
		
		mockDashboardService.On("GetAdminMetrics").Return(mockData, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/admin", handler.GetAdminDashboard)
		
		// Create request
		req := createTestRequest("GET", "/api/dashboard/admin", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Execute
		err := handler.GetAdminDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		if dashboard, ok := response["dashboard"].(map[string]interface{}); ok {
			assert.Equal(t, "admin", dashboard["type"])
		} else {
			t.Errorf("Dashboard field not found or not a map")
		}
		
		mockDashboardService.AssertExpectations(t)
	})

	t.Run("GET /api/dashboard/teacher - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock data
		mockData := map[string]interface{}{
			"user": map[string]interface{}{
				"id":    2,
				"name":  "Teacher User",
				"email": "teacher@test.com",
				"role":  "teacher",
			},
			"timestamp": time.Now().Format(time.RFC3339),
			"dashboard": map[string]interface{}{
				"type": "teacher",
				"stats": map[string]interface{}{
					"my_courses":       3,
					"total_students":   45,
					"total_assignments": 20,
					"average_grade":    "85.5",
				},
			},
		}
		
		mockDashboardService.On("GetTeacherMetrics", "2").Return(mockData, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/teacher", handler.GetTeacherDashboard)
		
		// Create request
		req := createTestRequest("GET", "/api/dashboard/teacher", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Add user ID to context
		c.Set("user_id", "2")
		
		// Execute
		err := handler.GetTeacherDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		if dashboard, ok := response["dashboard"].(map[string]interface{}); ok {
			assert.Equal(t, "teacher", dashboard["type"])
		} else {
			t.Errorf("Dashboard field not found or not a map")
		}
		
		mockDashboardService.AssertExpectations(t)
	})

	t.Run("GET /api/dashboard/student - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock data
		mockData := map[string]interface{}{
			"user": map[string]interface{}{
				"id":    3,
				"name":  "Student User",
				"email": "student@test.com",
				"role":  "student",
			},
			"timestamp": time.Now().Format(time.RFC3339),
			"dashboard": map[string]interface{}{
				"type": "student",
				"stats": map[string]interface{}{
					"total_courses":         4,
					"total_assignments":     20,
					"completed_assignments": 15,
					"average_grade":         "88.5",
				},
			},
		}
		
		mockDashboardService.On("GetStudentMetrics", "3").Return(mockData, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/student", handler.GetStudentDashboard)
		
		// Create request
		req := createTestRequest("GET", "/api/dashboard/student", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Add user ID to context
		c.Set("user_id", "3")
		
		// Execute
		err := handler.GetStudentDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		if dashboard, ok := response["dashboard"].(map[string]interface{}); ok {
			assert.Equal(t, "student", dashboard["type"])
		} else {
			t.Errorf("Dashboard field not found or not a map")
		}
		
		mockDashboardService.AssertExpectations(t)
	})

	t.Run("GET /api/dashboard/coordinator - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock data
		mockData := map[string]interface{}{
			"user": map[string]interface{}{
				"id":    4,
				"name":  "Coordinator User",
				"email": "coordinator@test.com",
				"role":  "coordinator",
			},
			"timestamp": time.Now().Format(time.RFC3339),
			"dashboard": map[string]interface{}{
				"type": "coordinator",
				"stats": map[string]interface{}{
					"department_courses":   12,
					"department_teachers":  8,
					"department_students":  200,
					"department_performance": "87.2",
				},
			},
		}
		
		mockDashboardService.On("GetCoordinatorMetrics", "4").Return(mockData, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/coordinator", handler.GetCoordinatorDashboard)
		
		// Create request
		req := createTestRequest("GET", "/api/dashboard/coordinator", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Add user ID to context
		c.Set("user_id", "4")
		
		// Execute
		err := handler.GetCoordinatorDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		if dashboard, ok := response["dashboard"].(map[string]interface{}); ok {
			assert.Equal(t, "coordinator", dashboard["type"])
		} else {
			t.Errorf("Dashboard field not found or not a map")
		}
		
		mockDashboardService.AssertExpectations(t)
	})

	t.Run("POST /api/dashboard/export - successful export", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock export data
		exportData := []byte("PDF export data")
		mockDashboardService.On("ExportDashboardData", "1", "admin", "pdf").Return(exportData, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.POST("/api/dashboard/export", handler.ExportDashboard)
		
		// Create request body
		requestBody := map[string]interface{}{
			"format": "pdf",
		}
		
		req := createTestRequest("POST", "/api/dashboard/export", requestBody)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Add user ID and role to context
		c.Set("user_id", "1")
		c.Set("user_role", "admin")
		
		// Execute
		err := handler.ExportDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		assert.Equal(t, "application/pdf", rec.Header().Get("Content-Type"))
		assert.Equal(t, "attachment; filename=dashboard_export.pdf", rec.Header().Get("Content-Disposition"))
		
		mockDashboardService.AssertExpectations(t)
	})

	t.Run("GET /api/metrics/course-stats - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock course stats
		mockStats := map[string]interface{}{
			"course_id":             "course123",
			"total_students":        25,
			"total_assignments":     10,
			"published_assignments": 8,
			"draft_assignments":     2,
		}
		
		mockGoogleService.On("GetCourseStats", "course123").Return(mockStats, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/metrics/course-stats/:courseId", handler.GetCourseStats)
		
		// Create request
		req := createTestRequest("GET", "/api/metrics/course-stats/course123", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Set course ID parameter
		c.SetParamNames("courseId")
		c.SetParamValues("course123")
		
		// Execute
		err := handler.GetCourseStats(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Equal(t, "course123", response["course_id"])
		assert.Equal(t, float64(25), response["total_students"])
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/courses - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock courses data
		mockCourses := []services.Course{
			{
				ID:          "course1",
				Name:        "Mathematics",
				Description: "Advanced Math",
				Section:     "A",
				Room:        "Room 101",
				OwnerID:     "teacher1",
				CourseState: "ACTIVE",
			},
			{
				ID:          "course2",
				Name:        "Science",
				Description: "Physics and Chemistry",
				Section:     "B",
				Room:        "Room 102",
				OwnerID:     "teacher1",
				CourseState: "ACTIVE",
			},
		}
		
		mockGoogleService.On("ListCourses", "teacher1").Return(mockCourses, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/courses", handler.GetGoogleCourses)
		
		// Create request
		req := createTestRequest("GET", "/api/google/courses", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Add user ID to context
		c.Set("user_id", "teacher1")
		
		// Execute
		err := handler.GetGoogleCourses(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "courses")
		
		courses := response["courses"].([]interface{})
		assert.Len(t, courses, 2)
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/students/:courseId - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock students data
		mockStudents := []services.Student{
			{
				ID:       "student1",
				Name:     "John Doe",
				Email:    "john@example.com",
				PhotoURL: "https://example.com/photo1.jpg",
			},
			{
				ID:       "student2",
				Name:     "Jane Smith",
				Email:    "jane@example.com",
				PhotoURL: "https://example.com/photo2.jpg",
			},
		}
		
		mockGoogleService.On("ListStudents", "course123").Return(mockStudents, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/students/:courseId", handler.GetGoogleStudents)
		
		// Create request
		req := createTestRequest("GET", "/api/google/students/course123", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Set course ID parameter
		c.SetParamNames("courseId")
		c.SetParamValues("course123")
		
		// Execute
		err := handler.GetGoogleStudents(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "students")
		
		students := response["students"].([]interface{})
		assert.Len(t, students, 2)
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/assignments/:courseId - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock assignments data
		mockAssignments := []services.Assignment{
			{
				ID:          "assignment1",
				Title:       "Math Homework",
				Description: "Complete exercises 1-10",
				DueDate:     "2025-10-15",
				MaxPoints:   100,
				State:       "PUBLISHED",
			},
			{
				ID:          "assignment2",
				Title:       "Science Project",
				Description: "Research project on physics",
				DueDate:     "2025-10-20",
				MaxPoints:   150,
				State:       "DRAFT",
			},
		}
		
		mockGoogleService.On("ListAssignments", "course123").Return(mockAssignments, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/assignments/:courseId", handler.GetGoogleAssignments)
		
		// Create request
		req := createTestRequest("GET", "/api/google/assignments/course123", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Set course ID parameter
		c.SetParamNames("courseId")
		c.SetParamValues("course123")
		
		// Execute
		err := handler.GetGoogleAssignments(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "assignments")
		
		assignments := response["assignments"].([]interface{})
		assert.Len(t, assignments, 2)
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("POST /api/google/mock-mode - toggle mock mode", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock mock mode toggle
		mockGoogleService.On("SetMockMode", true).Return()
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.POST("/api/google/mock-mode", handler.ToggleMockMode)
		
		// Create request body
		requestBody := map[string]interface{}{
			"enabled": true,
		}
		
		req := createTestRequest("POST", "/api/google/mock-mode", requestBody)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Execute
		err := handler.ToggleMockMode(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Equal(t, true, response["mock_mode_enabled"])
		
		mockGoogleService.AssertExpectations(t)
	})
}

func TestDashboardAPI_ErrorHandling(t *testing.T) {
	t.Run("GET /api/dashboard/admin - service error", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock service error
		mockDashboardService.On("GetAdminMetrics").Return(nil, fmt.Errorf("database connection failed"))
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/admin", handler.GetAdminDashboard)
		
		// Create request
		req := createTestRequest("GET", "/api/dashboard/admin", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Execute
		err := handler.GetAdminDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusInternalServerError, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response["error"], "database connection failed")
		
		mockDashboardService.AssertExpectations(t)
	})

	t.Run("GET /api/dashboard/teacher - missing user ID", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/teacher", handler.GetTeacherDashboard)
		
		// Create request
		req := createTestRequest("GET", "/api/dashboard/teacher", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Don't set user ID in context
		
		// Execute
		err := handler.GetTeacherDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusUnauthorized, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response["error"], "user not authenticated")
	})

	t.Run("POST /api/dashboard/export - invalid format", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.POST("/api/dashboard/export", handler.ExportDashboard)
		
		// Create request body with invalid format
		requestBody := map[string]interface{}{
			"format": "invalid_format",
		}
		
		req := createTestRequest("POST", "/api/dashboard/export", requestBody)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Add user ID and role to context
		c.Set("user_id", "1")
		c.Set("user_role", "admin")
		
		// Execute
		err := handler.ExportDashboard(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusBadRequest, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response["error"], "invalid export format")
	})

	t.Run("GET /api/metrics/course-stats - course not found", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock course not found error
		mockGoogleService.On("GetCourseStats", "nonexistent").Return(nil, fmt.Errorf("course not found"))
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/metrics/course-stats/:courseId", handler.GetCourseStats)
		
		// Create request
		req := createTestRequest("GET", "/api/metrics/course-stats/nonexistent", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Set course ID parameter
		c.SetParamNames("courseId")
		c.SetParamValues("nonexistent")
		
		// Execute
		err := handler.GetCourseStats(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusNotFound, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response["error"], "course not found")
		
		mockGoogleService.AssertExpectations(t)
	})
}

func TestDashboardAPI_ConcurrentAccess(t *testing.T) {
	t.Run("concurrent dashboard requests", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock data for concurrent requests
		mockData := map[string]interface{}{
			"user": map[string]interface{}{
				"id":    1,
				"name":  "Test User",
				"email": "test@test.com",
				"role":  "admin",
			},
			"timestamp": time.Now().Format(time.RFC3339),
			"dashboard": map[string]interface{}{
				"type": "admin",
				"stats": map[string]interface{}{
					"total_users": 150,
				},
			},
		}
		
		mockDashboardService.On("GetAdminMetrics").Return(mockData, nil).Times(5)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/admin", handler.GetAdminDashboard)
		
		// Create channel for results
		results := make(chan int, 5)
		errors := make(chan error, 5)
		
		// Launch concurrent requests
		for i := 0; i < 5; i++ {
			go func() {
				req := createTestRequest("GET", "/api/dashboard/admin", nil)
				c, rec := createTestContextWithUser(e, req, "1", "admin")
				
				err := handler.GetAdminDashboard(c)
				results <- rec.Code
				errors <- err
			}()
		}
		
		// Collect results
		for i := 0; i < 5; i++ {
			code := <-results
			err := <-errors
			
			assert.NoError(t, err)
			assert.Equal(t, http.StatusOK, code)
		}
		
		mockDashboardService.AssertExpectations(t)
	})
}

func TestDashboardAPI_Performance(t *testing.T) {
	t.Run("dashboard response time", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockDashboardService := &MockDashboardService{}
		mockGoogleService := &MockGoogleService{}
		
		// Mock data
		mockData := map[string]interface{}{
			"user": map[string]interface{}{
				"id":    1,
				"name":  "Test User",
				"email": "test@test.com",
				"role":  "admin",
			},
			"timestamp": time.Now().Format(time.RFC3339),
			"dashboard": map[string]interface{}{
				"type": "admin",
				"stats": map[string]interface{}{
					"total_users": 150,
				},
			},
		}
		
		mockDashboardService.On("GetAdminMetrics").Return(mockData, nil)
		
		// Create handler
		handler := &DashboardHandler{
			dashboardService: mockDashboardService,
			googleService:    mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/dashboard/admin", handler.GetAdminDashboard)
		
		// Create request
		req := createTestRequest("GET", "/api/dashboard/admin", nil)
		c, rec := createTestContextWithUser(e, req, "1", "admin")
		
		// Measure response time
		start := time.Now()
		err := handler.GetAdminDashboard(c)
		duration := time.Since(start)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		assert.Less(t, duration, 100*time.Millisecond, "Response time should be less than 100ms")
		
		mockDashboardService.AssertExpectations(t)
	})
}
