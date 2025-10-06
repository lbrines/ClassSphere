package handlers

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"classsphere-backend/auth"
	"classsphere-backend/services"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// MockGoogleClassroomService is a mock implementation for testing
type MockGoogleClassroomService struct {
	mock.Mock
}

func (m *MockGoogleClassroomService) ListCourses(userID string) ([]services.Course, error) {
	args := m.Called(userID)
	return args.Get(0).([]services.Course), args.Error(1)
}

func (m *MockGoogleClassroomService) ListStudents(courseID string) ([]services.Student, error) {
	args := m.Called(courseID)
	return args.Get(0).([]services.Student), args.Error(1)
}

func (m *MockGoogleClassroomService) ListAssignments(courseID string) ([]services.Assignment, error) {
	args := m.Called(courseID)
	return args.Get(0).([]services.Assignment), args.Error(1)
}

func (m *MockGoogleClassroomService) SetMockMode(enabled bool) {
	m.Called(enabled)
}

func (m *MockGoogleClassroomService) GetCourseStats(courseID string) (map[string]interface{}, error) {
	args := m.Called(courseID)
	return args.Get(0).(map[string]interface{}), args.Error(1)
}

// MockMetricsService is a mock implementation for testing
type MockMetricsService struct {
	mock.Mock
}

func (m *MockMetricsService) CalculateCourseMetrics(courses []services.Course) services.CourseMetrics {
	args := m.Called(courses)
	return args.Get(0).(services.CourseMetrics)
}

func (m *MockMetricsService) CalculateStudentMetrics(students []services.Student) services.StudentMetrics {
	args := m.Called(students)
	return args.Get(0).(services.StudentMetrics)
}

func (m *MockMetricsService) CalculateAssignmentMetrics(assignments []services.Assignment) services.AssignmentMetrics {
	args := m.Called(assignments)
	return args.Get(0).(services.AssignmentMetrics)
}

func (m *MockMetricsService) GetDashboardMetrics(courses []services.Course, students []services.Student, assignments []services.Assignment) services.DashboardMetrics {
	args := m.Called(courses, students, assignments)
	return args.Get(0).(services.DashboardMetrics)
}

func (m *MockMetricsService) GetRoleSpecificMetrics(role string, courses []services.Course, students []services.Student, assignments []services.Assignment) map[string]interface{} {
	args := m.Called(role, courses, students, assignments)
	return args.Get(0).(map[string]interface{})
}

func TestGoogleHandler_GetCourses(t *testing.T) {
	tests := []struct {
		name           string
		userID         string
		mockCourses    []services.Course
		mockError      error
		expectedStatus int
		expectedError  bool
	}{
		{
			name:   "successful course listing",
			userID: "user123",
			mockCourses: []services.Course{
				{
					ID:          "course1",
					Name:        "Mathematics",
					Description: "Advanced Math",
					Section:     "A",
					Room:        "Room 101",
					OwnerID:     "user123",
					CourseState: "ACTIVE",
				},
				{
					ID:          "course2",
					Name:        "Science",
					Description: "Physics",
					Section:     "B",
					Room:        "Room 102",
					OwnerID:     "user123",
					CourseState: "ACTIVE",
				},
			},
			mockError:      nil,
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "empty course list",
			userID:         "user456",
			mockCourses:    []services.Course{},
			mockError:      nil,
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "service error",
			userID:         "user789",
			mockCourses:    nil,
			mockError:      assert.AnError,
			expectedStatus: http.StatusInternalServerError,
			expectedError:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}
			
		// Setup mock expectations
		mockGoogleService.On("ListCourses", tt.userID).Return(tt.mockCourses, tt.mockError)
		
		// Setup metrics service expectations
		courseMetrics := services.CourseMetrics{
			TotalCourses:     len(tt.mockCourses),
			ActiveCourses:    len(tt.mockCourses),
			ArchivedCourses:  0,
			TotalStudents:    len(tt.mockCourses) * 8, // Mock calculation
			AverageGrade:     85.5,
			TotalAssignments: len(tt.mockCourses) * 6, // Mock calculation
		}
		mockMetricsService.On("CalculateCourseMetrics", tt.mockCourses).Return(courseMetrics)

			// Create handler
			handler := &GoogleHandler{
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

		// Setup test context
		e := echo.New()
		req := httptest.NewRequest(http.MethodGet, "/api/google/courses", nil)
		rec := httptest.NewRecorder()
		c := e.NewContext(req, rec)
		
		// Mock user context with auth.Claims
		claims := &auth.Claims{
			UserID: tt.userID,
			Role:   "student",
		}
		c.Set("user", claims)

		// Test the method
		err := handler.GetCourses(c)

		// Assertions
		if tt.expectedError {
			assert.NoError(t, err) // Echo returns nil when using c.JSON with error status
			assert.Equal(t, tt.expectedStatus, rec.Code)
		} else {
			assert.NoError(t, err)
			assert.Equal(t, tt.expectedStatus, rec.Code)
		}

		// Verify mock was called
		mockGoogleService.AssertExpectations(t)
		})
	}
}

func TestGoogleHandler_GetCourseStudents(t *testing.T) {
	tests := []struct {
		name            string
		courseID        string
		mockStudents    []services.Student
		mockError       error
		expectedStatus  int
		expectedError   bool
	}{
		{
			name:     "successful student listing",
			courseID: "course1",
			mockStudents: []services.Student{
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
			},
			mockError:      nil,
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "empty student list",
			courseID:       "course2",
			mockStudents:   []services.Student{},
			mockError:      nil,
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "service error",
			courseID:       "course3",
			mockStudents:   nil,
			mockError:      assert.AnError,
			expectedStatus: http.StatusInternalServerError,
			expectedError:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}
			
		// Setup mock expectations
		mockGoogleService.On("ListStudents", tt.courseID).Return(tt.mockStudents, tt.mockError)
		
		// Setup metrics service expectations
		studentMetrics := services.StudentMetrics{
			TotalStudents:  len(tt.mockStudents),
			ActiveStudents: len(tt.mockStudents),
		}
		mockMetricsService.On("CalculateStudentMetrics", tt.mockStudents).Return(studentMetrics)

			// Create handler
			handler := &GoogleHandler{
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Setup test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodGet, "/api/google/courses/"+tt.courseID+"/students", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			c.SetParamNames("courseId")
			c.SetParamValues(tt.courseID)

		// Test the method
		err := handler.GetCourseStudents(c)

		// Assertions
		if tt.expectedError {
			assert.NoError(t, err) // Echo returns nil when using c.JSON with error status
			assert.Equal(t, tt.expectedStatus, rec.Code)
		} else {
			assert.NoError(t, err)
			assert.Equal(t, tt.expectedStatus, rec.Code)
		}

			// Verify mock was called
			mockGoogleService.AssertExpectations(t)
		})
	}
}

func TestGoogleHandler_GetCourseAssignments(t *testing.T) {
	tests := []struct {
		name              string
		courseID          string
		mockAssignments   []services.Assignment
		mockError         error
		expectedStatus    int
		expectedError     bool
	}{
		{
			name:     "successful assignment listing",
			courseID: "course1",
			mockAssignments: []services.Assignment{
				{
					ID:          "assignment1",
					Title:       "Math Homework",
					Description: "Solve equations",
					DueDate:     "2025-10-10",
					MaxPoints:   100,
					State:       "PUBLISHED",
				},
				{
					ID:          "assignment2",
					Title:       "Science Project",
					Description: "Lab report",
					DueDate:     "2025-10-15",
					MaxPoints:   150,
					State:       "PUBLISHED",
				},
			},
			mockError:      nil,
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "empty assignment list",
			courseID:       "course2",
			mockAssignments: []services.Assignment{},
			mockError:      nil,
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "service error",
			courseID:       "course3",
			mockAssignments: nil,
			mockError:      assert.AnError,
			expectedStatus: http.StatusInternalServerError,
			expectedError:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}
			
		// Setup mock expectations
		mockGoogleService.On("ListAssignments", tt.courseID).Return(tt.mockAssignments, tt.mockError)
		
		// Setup metrics service expectations
		assignmentMetrics := services.AssignmentMetrics{
			TotalAssignments:     len(tt.mockAssignments),
			PublishedAssignments: len(tt.mockAssignments), // All are published in mock data
			DraftAssignments:     0,
			TotalPoints:          0, // Will be calculated
			AveragePoints:        0.0,
		}
		
		// Calculate total points for mock data
		for _, assignment := range tt.mockAssignments {
			assignmentMetrics.TotalPoints += assignment.MaxPoints
		}
		
		if len(tt.mockAssignments) > 0 {
			assignmentMetrics.AveragePoints = float64(assignmentMetrics.TotalPoints) / float64(len(tt.mockAssignments))
		}
		
		mockMetricsService.On("CalculateAssignmentMetrics", tt.mockAssignments).Return(assignmentMetrics)

			// Create handler
			handler := &GoogleHandler{
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Setup test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodGet, "/api/google/courses/"+tt.courseID+"/assignments", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			c.SetParamNames("courseId")
			c.SetParamValues(tt.courseID)

		// Test the method
		err := handler.GetCourseAssignments(c)

		// Assertions
		if tt.expectedError {
			assert.NoError(t, err) // Echo returns nil when using c.JSON with error status
			assert.Equal(t, tt.expectedStatus, rec.Code)
		} else {
			assert.NoError(t, err)
			assert.Equal(t, tt.expectedStatus, rec.Code)
		}

			// Verify mock was called
			mockGoogleService.AssertExpectations(t)
		})
	}
}

func TestGoogleHandler_GetCourseStats(t *testing.T) {
	tests := []struct {
		name           string
		courseID       string
		mockStats      map[string]interface{}
		mockError      error
		expectedStatus int
		expectedError  bool
	}{
		{
			name:     "successful stats retrieval",
			courseID: "course1",
			mockStats: map[string]interface{}{
				"course_id":             "course1",
				"total_students":        25,
				"total_assignments":     10,
				"published_assignments": 8,
				"draft_assignments":     2,
			},
			mockError:      nil,
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "service error",
			courseID:       "course2",
			mockStats:      nil,
			mockError:      assert.AnError,
			expectedStatus: http.StatusInternalServerError,
			expectedError:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}
			
			// Setup mock expectations
			mockGoogleService.On("GetCourseStats", tt.courseID).Return(tt.mockStats, tt.mockError)

			// Create handler
			handler := &GoogleHandler{
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Setup test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodGet, "/api/google/courses/"+tt.courseID+"/stats", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			c.SetParamNames("courseId")
			c.SetParamValues(tt.courseID)

		// Test the method
		err := handler.GetCourseStats(c)

		// Assertions
		if tt.expectedError {
			assert.NoError(t, err) // Echo returns nil when using c.JSON with error status
			assert.Equal(t, tt.expectedStatus, rec.Code)
		} else {
			assert.NoError(t, err)
			assert.Equal(t, tt.expectedStatus, rec.Code)
		}

			// Verify mock was called
			mockGoogleService.AssertExpectations(t)
		})
	}
}

func TestGoogleHandler_ToggleMockMode(t *testing.T) {
	tests := []struct {
		name           string
		mockMode       string
		expectedStatus int
		expectedError  bool
	}{
		{
			name:           "enable mock mode",
			mockMode:       "true",
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "disable mock mode",
			mockMode:       "false",
			expectedStatus: http.StatusOK,
			expectedError:  false,
		},
		{
			name:           "invalid mock mode",
			mockMode:       "invalid",
			expectedStatus: http.StatusBadRequest,
			expectedError:  true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}
			
			// Setup mock expectations
			if tt.mockMode == "true" || tt.mockMode == "false" {
				mockGoogleService.On("SetMockMode", tt.mockMode == "true").Return()
			}

			// Create handler
			handler := &GoogleHandler{
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Setup test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodPost, "/api/google/mock-mode", nil)
			req.Header.Set("Content-Type", "application/json")
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			c.SetParamNames("enabled")
			c.SetParamValues(tt.mockMode)

			// Test the method
			err := handler.ToggleMockMode(c)

		// Assertions
		if tt.expectedError {
			assert.NoError(t, err) // Echo returns nil when using c.JSON with error status
			assert.Equal(t, tt.expectedStatus, rec.Code)
		} else {
			assert.NoError(t, err)
			assert.Equal(t, tt.expectedStatus, rec.Code)
		}

			// Verify mock was called
			mockGoogleService.AssertExpectations(t)
		})
	}
}
