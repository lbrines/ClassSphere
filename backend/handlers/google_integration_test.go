package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"classsphere-backend/services"
)


func TestGoogleAPI_Integration(t *testing.T) {
	t.Run("GET /api/google/courses - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
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
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/courses", handler.GetCourses)
		
		// Create request
		req := createTestRequest("GET", "/api/google/courses", nil)
		c, rec := createTestContext(e, req)
		
		// Add user ID to context
		c.Set("user_id", "teacher1")
		
		// Execute
		err := handler.GetCourses(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "courses")
		
		courses := response["courses"].([]interface{})
		assert.Len(t, courses, 2)
		
		// Verify course data
		course1 := courses[0].(map[string]interface{})
		assert.Equal(t, "course1", course1["id"])
		assert.Equal(t, "Mathematics", course1["name"])
		assert.Equal(t, "ACTIVE", course1["courseState"])
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/students/:courseId - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
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
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/students/:courseId", handler.GetStudents)
		
		// Create request
		req := createTestRequest("GET", "/api/google/students/course123", nil)
		c, rec := createTestContext(e, req)
		
		// Set course ID parameter
		c.SetParamNames("courseId")
		c.SetParamValues("course123")
		
		// Execute
		err := handler.GetStudents(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "students")
		
		students := response["students"].([]interface{})
		assert.Len(t, students, 2)
		
		// Verify student data
		student1 := students[0].(map[string]interface{})
		assert.Equal(t, "student1", student1["id"])
		assert.Equal(t, "John Doe", student1["name"])
		assert.Equal(t, "john@example.com", student1["email"])
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/assignments/:courseId - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
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
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/assignments/:courseId", handler.GetAssignments)
		
		// Create request
		req := createTestRequest("GET", "/api/google/assignments/course123", nil)
		c, rec := createTestContext(e, req)
		
		// Set course ID parameter
		c.SetParamNames("courseId")
		c.SetParamValues("course123")
		
		// Execute
		err := handler.GetAssignments(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "assignments")
		
		assignments := response["assignments"].([]interface{})
		assert.Len(t, assignments, 2)
		
		// Verify assignment data
		assignment1 := assignments[0].(map[string]interface{})
		assert.Equal(t, "assignment1", assignment1["id"])
		assert.Equal(t, "Math Homework", assignment1["title"])
		assert.Equal(t, "PUBLISHED", assignment1["state"])
		assert.Equal(t, float64(100), assignment1["maxPoints"])
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/course-stats/:courseId - successful response", func(t *testing.T) {
		// Setup
		e := createTestServer()
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
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/course-stats/:courseId", handler.GetCourseStats)
		
		// Create request
		req := createTestRequest("GET", "/api/google/course-stats/course123", nil)
		c, rec := createTestContext(e, req)
		
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
		assert.Equal(t, 25, response["total_students"])
		assert.Equal(t, 10, response["total_assignments"])
		assert.Equal(t, 8, response["published_assignments"])
		assert.Equal(t, 2, response["draft_assignments"])
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("POST /api/google/mock-mode - toggle mock mode", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Mock mock mode toggle
		mockGoogleService.On("SetMockMode", true).Return()
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.POST("/api/google/mock-mode", handler.ToggleMockMode)
		
		// Create request body
		requestBody := map[string]interface{}{
			"enabled": true,
		}
		
		req := createTestRequest("POST", "/api/google/mock-mode", requestBody)
		c, rec := createTestContext(e, req)
		
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

	t.Run("GET /api/google/random-data - get random data", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Mock random data
		mockCourse := services.Course{
			ID:          "random_course",
			Name:        "Random Course",
			Description: "Random Description",
			Section:     "R",
			Room:        "Random Room",
			OwnerID:     "random_teacher",
			CourseState: "ACTIVE",
		}
		
		mockStudent := services.Student{
			ID:       "random_student",
			Name:     "Random Student",
			Email:    "random@example.com",
			PhotoURL: "https://example.com/random.jpg",
		}
		
		mockAssignment := services.Assignment{
			ID:          "random_assignment",
			Title:       "Random Assignment",
			Description: "Random Description",
			DueDate:     "2025-12-31",
			MaxPoints:   100,
			State:       "PUBLISHED",
		}
		
		mockGoogleService.On("GetRandomCourse").Return(mockCourse)
		mockGoogleService.On("GetRandomStudent").Return(mockStudent)
		mockGoogleService.On("GetRandomAssignment").Return(mockAssignment)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/random-data", handler.GetRandomData)
		
		// Create request
		req := createTestRequest("GET", "/api/google/random-data", nil)
		c, rec := createTestContext(e, req)
		
		// Execute
		err := handler.GetRandomData(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "course")
		assert.Contains(t, response, "student")
		assert.Contains(t, response, "assignment")
		
		// Verify random data
		course := response["course"].(map[string]interface{})
		assert.Equal(t, "random_course", course["id"])
		assert.Equal(t, "Random Course", course["name"])
		
		student := response["student"].(map[string]interface{})
		assert.Equal(t, "random_student", student["id"])
		assert.Equal(t, "Random Student", student["name"])
		
		assignment := response["assignment"].(map[string]interface{})
		assert.Equal(t, "random_assignment", assignment["id"])
		assert.Equal(t, "Random Assignment", assignment["title"])
		
		mockGoogleService.AssertExpectations(t)
	})
}

func TestGoogleAPI_ErrorHandling(t *testing.T) {
	t.Run("GET /api/google/courses - service error", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Mock service error
		mockGoogleService.On("ListCourses", "teacher1").Return(nil, assert.AnError)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/courses", handler.GetCourses)
		
		// Create request
		req := createTestRequest("GET", "/api/google/courses", nil)
		c, rec := createTestContext(e, req)
		
		// Add user ID to context
		c.Set("user_id", "teacher1")
		
		// Execute
		err := handler.GetCourses(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusInternalServerError, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "error")
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/students/:courseId - course not found", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Mock course not found error
		mockGoogleService.On("ListStudents", "nonexistent").Return(nil, assert.AnError)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/students/:courseId", handler.GetStudents)
		
		// Create request
		req := createTestRequest("GET", "/api/google/students/nonexistent", nil)
		c, rec := createTestContext(e, req)
		
		// Set course ID parameter
		c.SetParamNames("courseId")
		c.SetParamValues("nonexistent")
		
		// Execute
		err := handler.GetStudents(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusInternalServerError, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "error")
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("GET /api/google/courses - missing user ID", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/courses", handler.GetCourses)
		
		// Create request
		req := createTestRequest("GET", "/api/google/courses", nil)
		c, rec := createTestContext(e, req)
		
		// Don't set user ID in context
		
		// Execute
		err := handler.GetCourses(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusUnauthorized, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response["error"], "user not authenticated")
	})

	t.Run("POST /api/google/mock-mode - invalid request body", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.POST("/api/google/mock-mode", handler.ToggleMockMode)
		
		// Create request with invalid body
		req := httptest.NewRequest("POST", "/api/google/mock-mode", bytes.NewReader([]byte("invalid json")))
		req.Header.Set("Content-Type", "application/json")
		c, rec := createTestContext(e, req)
		
		// Execute
		err := handler.ToggleMockMode(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusBadRequest, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Contains(t, response, "error")
	})
}

func TestGoogleAPI_ConcurrentAccess(t *testing.T) {
	t.Run("concurrent course requests", func(t *testing.T) {
		// Setup
		e := createTestServer()
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
		}
		
		mockGoogleService.On("ListCourses", "teacher1").Return(mockCourses, nil).Times(5)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/courses", handler.GetCourses)
		
		// Create channel for results
		results := make(chan int, 5)
		errors := make(chan error, 5)
		
		// Launch concurrent requests
		for i := 0; i < 5; i++ {
			go func() {
				req := createTestRequest("GET", "/api/google/courses", nil)
				c, rec := createTestContext(e, req)
				c.Set("user_id", "teacher1")
				
				err := handler.GetCourses(c)
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
		
		mockGoogleService.AssertExpectations(t)
	})
}

func TestGoogleAPI_Performance(t *testing.T) {
	t.Run("course listing response time", func(t *testing.T) {
		// Setup
		e := createTestServer()
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
		}
		
		mockGoogleService.On("ListCourses", "teacher1").Return(mockCourses, nil)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/courses", handler.GetCourses)
		
		// Create request
		req := createTestRequest("GET", "/api/google/courses", nil)
		c, rec := createTestContext(e, req)
		c.Set("user_id", "teacher1")
		
		// Measure response time
		start := time.Now()
		err := handler.GetCourses(c)
		duration := time.Since(start)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		assert.Less(t, duration, 100*time.Millisecond, "Response time should be less than 100ms")
		
		mockGoogleService.AssertExpectations(t)
	})
}

func TestGoogleAPI_DataValidation(t *testing.T) {
	t.Run("course data validation", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Mock courses data with various states
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
				CourseState: "ARCHIVED",
			},
		}
		
		mockGoogleService.On("ListCourses", "teacher1").Return(mockCourses, nil)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/courses", handler.GetCourses)
		
		// Create request
		req := createTestRequest("GET", "/api/google/courses", nil)
		c, rec := createTestContext(e, req)
		c.Set("user_id", "teacher1")
		
		// Execute
		err := handler.GetCourses(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		
		courses := response["courses"].([]interface{})
		assert.Len(t, courses, 2)
		
		// Validate course data structure
		for _, courseInterface := range courses {
			course := courseInterface.(map[string]interface{})
			
			// Required fields
			assert.Contains(t, course, "id")
			assert.Contains(t, course, "name")
			assert.Contains(t, course, "description")
			assert.Contains(t, course, "section")
			assert.Contains(t, course, "room")
			assert.Contains(t, course, "ownerId")
			assert.Contains(t, course, "courseState")
			
			// Validate course state
			courseState := course["courseState"].(string)
			assert.Contains(t, []string{"ACTIVE", "ARCHIVED", "PROVISIONED", "DECLINED"}, courseState)
		}
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("student data validation", func(t *testing.T) {
		// Setup
		e := createTestServer()
		mockGoogleService := &MockGoogleService{}
		
		// Mock students data
		mockStudents := []services.Student{
			{
				ID:       "student1",
				Name:     "John Doe",
				Email:    "john@example.com",
				PhotoURL: "https://example.com/photo1.jpg",
			},
		}
		
		mockGoogleService.On("ListStudents", "course123").Return(mockStudents, nil)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/students/:courseId", handler.GetStudents)
		
		// Create request
		req := createTestRequest("GET", "/api/google/students/course123", nil)
		c, rec := createTestContext(e, req)
		c.SetParamNames("courseId")
		c.SetParamValues("course123")
		
		// Execute
		err := handler.GetStudents(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		
		students := response["students"].([]interface{})
		assert.Len(t, students, 1)
		
		// Validate student data structure
		student := students[0].(map[string]interface{})
		
		// Required fields
		assert.Contains(t, student, "id")
		assert.Contains(t, student, "name")
		assert.Contains(t, student, "email")
		assert.Contains(t, student, "photoUrl")
		
		// Validate email format
		email := student["email"].(string)
		assert.Contains(t, email, "@")
		assert.Contains(t, email, ".")
		
		// Validate photo URL format
		photoURL := student["photoUrl"].(string)
		assert.Contains(t, photoURL, "http")
		
		mockGoogleService.AssertExpectations(t)
	})

	t.Run("assignment data validation", func(t *testing.T) {
		// Setup
		e := createTestServer()
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
		}
		
		mockGoogleService.On("ListAssignments", "course123").Return(mockAssignments, nil)
		
		// Create handler
		handler := &GoogleHandler{
			googleService: mockGoogleService,
		}
		
		// Setup route
		e.GET("/api/google/assignments/:courseId", handler.GetAssignments)
		
		// Create request
		req := createTestRequest("GET", "/api/google/assignments/course123", nil)
		c, rec := createTestContext(e, req)
		c.SetParamNames("courseId")
		c.SetParamValues("course123")
		
		// Execute
		err := handler.GetAssignments(c)
		
		// Assertions
		assert.NoError(t, err)
		assert.Equal(t, http.StatusOK, rec.Code)
		
		var response map[string]interface{}
		err = json.Unmarshal(rec.Body.Bytes(), &response)
		assert.NoError(t, err)
		
		assignments := response["assignments"].([]interface{})
		assert.Len(t, assignments, 1)
		
		// Validate assignment data structure
		assignment := assignments[0].(map[string]interface{})
		
		// Required fields
		assert.Contains(t, assignment, "id")
		assert.Contains(t, assignment, "title")
		assert.Contains(t, assignment, "description")
		assert.Contains(t, assignment, "dueDate")
		assert.Contains(t, assignment, "maxPoints")
		assert.Contains(t, assignment, "state")
		
		// Validate assignment state
		state := assignment["state"].(string)
		assert.Contains(t, []string{"PUBLISHED", "DRAFT", "DELETED"}, state)
		
		// Validate max points
		maxPoints := assignment["maxPoints"].(float64)
		assert.Greater(t, maxPoints, 0.0)
		
		mockGoogleService.AssertExpectations(t)
	})
}
