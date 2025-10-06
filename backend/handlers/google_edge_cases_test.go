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

// Test GetCourses edge cases
func TestGoogleHandler_GetCourses_EdgeCases(t *testing.T) {
	tests := []struct {
		name           string
		setupMocks     func(*MockGoogleClassroomService, *MockMetricsService)
		expectedStatus int
		description    string
	}{
		{
			name: "Invalid user context type",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				// No mocks needed for this test
			},
			expectedStatus: http.StatusUnauthorized,
			description:    "Should return unauthorized for invalid user context",
		},
		{
			name: "Service returns error",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				googleService.On("ListCourses", "123").Return([]services.Course{}, assert.AnError)
			},
			expectedStatus: http.StatusInternalServerError,
			description:    "Should return internal server error when service fails",
		},
		{
			name: "Service returns empty courses",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				emptyCourses := []services.Course{}
				googleService.On("ListCourses", "123").Return(emptyCourses, nil)
				metricsService.On("CalculateCourseMetrics", emptyCourses).Return(services.CourseMetrics{TotalCourses: 0})
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle empty courses list gracefully",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockUserRepo := &models.UserRepository{}
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}

			// Setup mocks
			tt.setupMocks(mockGoogleService, mockMetricsService)

			// Create handler
			handler := &GoogleHandler{
				userRepo:       mockUserRepo,
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Create test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodGet, "/api/google/courses", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)

			// Set user context based on test case
			if tt.name == "Invalid user context type" {
				c.Set("user", "invalid_user_context")
			} else {
				claims := &auth.Claims{
					UserID: "123",
					Role:   "student",
				}
				c.Set("user", claims)
			}

			// Test the function
			err := handler.GetCourses(c)

			// Assertions
			assert.NoError(t, err, tt.description)
			assert.Equal(t, tt.expectedStatus, rec.Code, tt.description)

			// Verify response structure for successful cases
			if tt.expectedStatus == http.StatusOK {
				var response map[string]interface{}
				err = json.Unmarshal(rec.Body.Bytes(), &response)
				assert.NoError(t, err, tt.description)
				assert.Contains(t, response, "courses", tt.description)
			}

			// Verify mock expectations
			mockGoogleService.AssertExpectations(t)
			mockMetricsService.AssertExpectations(t)
		})
	}
}

// Test GetCourseStudents edge cases
func TestGoogleHandler_GetCourseStudents_EdgeCases(t *testing.T) {
	tests := []struct {
		name           string
		courseID       string
		setupMocks     func(*MockGoogleClassroomService, *MockMetricsService)
		expectedStatus int
		description    string
	}{
		{
			name:     "Empty course ID",
			courseID: "",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				// No mocks needed - should fail validation
			},
			expectedStatus: http.StatusBadRequest,
			description:    "Should return bad request for empty course ID",
		},
		{
			name:     "Service returns error",
			courseID: "course123",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				googleService.On("ListStudents", "course123").Return([]services.Student{}, assert.AnError)
			},
			expectedStatus: http.StatusInternalServerError,
			description:    "Should return internal server error when service fails",
		},
		{
			name:     "Service returns empty students",
			courseID: "course123",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				emptyStudents := []services.Student{}
				googleService.On("ListStudents", "course123").Return(emptyStudents, nil)
				metricsService.On("CalculateStudentMetrics", emptyStudents).Return(services.StudentMetrics{TotalStudents: 0})
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle empty students list gracefully",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockUserRepo := &models.UserRepository{}
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}

			// Setup mocks
			tt.setupMocks(mockGoogleService, mockMetricsService)

			// Create handler
			handler := &GoogleHandler{
				userRepo:       mockUserRepo,
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Create test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodGet, "/api/google/courses/"+tt.courseID+"/students", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			
			// Set course ID parameter
			c.SetParamNames("courseId")
			c.SetParamValues(tt.courseID)

			// Set user context
			claims := &auth.Claims{
				UserID: "123",
				Role:   "teacher",
			}
			c.Set("user", claims)

			// Test the function
			err := handler.GetCourseStudents(c)

			// Assertions
			assert.NoError(t, err, tt.description)
			assert.Equal(t, tt.expectedStatus, rec.Code, tt.description)

			// Verify response structure for successful cases
			if tt.expectedStatus == http.StatusOK {
				var response map[string]interface{}
				err = json.Unmarshal(rec.Body.Bytes(), &response)
				assert.NoError(t, err, tt.description)
				assert.Contains(t, response, "students", tt.description)
			}

			// Verify mock expectations
			mockGoogleService.AssertExpectations(t)
			mockMetricsService.AssertExpectations(t)
		})
	}
}

// Test GetCourseAssignments edge cases
func TestGoogleHandler_GetCourseAssignments_EdgeCases(t *testing.T) {
	tests := []struct {
		name           string
		courseID       string
		setupMocks     func(*MockGoogleClassroomService, *MockMetricsService)
		expectedStatus int
		description    string
	}{
		{
			name:     "Invalid course ID format",
			courseID: "invalid-course-id-format",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				googleService.On("ListAssignments", "invalid-course-id-format").Return([]services.Assignment{}, assert.AnError)
			},
			expectedStatus: http.StatusInternalServerError,
			description:    "Should handle invalid course ID format",
		},
		{
			name:     "Service returns mixed results",
			courseID: "course123",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				assignments := []services.Assignment{
					{ID: "assignment1", Title: "HW1", State: "PUBLISHED", MaxPoints: 100},
					{ID: "assignment2", Title: "HW2", State: "DRAFT", MaxPoints: 150},
				}
				googleService.On("ListAssignments", "course123").Return(assignments, nil)
				metricsService.On("CalculateAssignmentMetrics", assignments).Return(services.AssignmentMetrics{TotalAssignments: 2})
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle mixed assignment states",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockUserRepo := &models.UserRepository{}
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}

			// Setup mocks
			tt.setupMocks(mockGoogleService, mockMetricsService)

			// Create handler
			handler := &GoogleHandler{
				userRepo:       mockUserRepo,
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Create test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodGet, "/api/google/courses/"+tt.courseID+"/assignments", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			
			// Set course ID parameter
			c.SetParamNames("courseId")
			c.SetParamValues(tt.courseID)

			// Set user context
			claims := &auth.Claims{
				UserID: "123",
				Role:   "teacher",
			}
			c.Set("user", claims)

			// Test the function
			err := handler.GetCourseAssignments(c)

			// Assertions
			assert.NoError(t, err, tt.description)
			assert.Equal(t, tt.expectedStatus, rec.Code, tt.description)

			// Verify response structure for successful cases
			if tt.expectedStatus == http.StatusOK {
				var response map[string]interface{}
				err = json.Unmarshal(rec.Body.Bytes(), &response)
				assert.NoError(t, err, tt.description)
				assert.Contains(t, response, "assignments", tt.description)
			}

			// Verify mock expectations
			mockGoogleService.AssertExpectations(t)
			mockMetricsService.AssertExpectations(t)
		})
	}
}

// Test ToggleMockMode edge cases
func TestGoogleHandler_ToggleMockMode_EdgeCases(t *testing.T) {
	tests := []struct {
		name           string
		enabledParam   string
		setupMocks     func(*MockGoogleClassroomService)
		expectedStatus int
		description    string
	}{
		{
			name:           "Empty enabled parameter",
			enabledParam:   "",
			setupMocks:     func(googleService *MockGoogleClassroomService) {},
			expectedStatus: http.StatusBadRequest,
			description:    "Should return bad request for empty parameter",
		},
		{
			name:           "Invalid boolean value",
			enabledParam:   "invalid",
			setupMocks:     func(googleService *MockGoogleClassroomService) {},
			expectedStatus: http.StatusBadRequest,
			description:    "Should return bad request for invalid boolean",
		},
		{
			name:         "Valid true value",
			enabledParam: "true",
			setupMocks: func(googleService *MockGoogleClassroomService) {
				googleService.On("SetMockMode", true).Return()
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle valid true value",
		},
		{
			name:         "Valid false value",
			enabledParam: "false",
			setupMocks: func(googleService *MockGoogleClassroomService) {
				googleService.On("SetMockMode", false).Return()
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle valid false value",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock services
			mockUserRepo := &models.UserRepository{}
			mockGoogleService := &MockGoogleClassroomService{}
			mockMetricsService := &MockMetricsService{}

			// Setup mocks
			tt.setupMocks(mockGoogleService)

			// Create handler
			handler := &GoogleHandler{
				userRepo:       mockUserRepo,
				googleService:  mockGoogleService,
				metricsService: mockMetricsService,
			}

			// Create test context
			e := echo.New()
			req := httptest.NewRequest(http.MethodPost, "/api/google/mock-mode/"+tt.enabledParam, nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			
			// Set enabled parameter
			c.SetParamNames("enabled")
			c.SetParamValues(tt.enabledParam)

			// Test the function
			err := handler.ToggleMockMode(c)

			// Assertions
			assert.NoError(t, err, tt.description)
			assert.Equal(t, tt.expectedStatus, rec.Code, tt.description)

			// Verify response structure for successful cases
			if tt.expectedStatus == http.StatusOK {
				var response map[string]interface{}
				err = json.Unmarshal(rec.Body.Bytes(), &response)
				assert.NoError(t, err, tt.description)
				assert.Contains(t, response, "message", tt.description)
			}

			// Verify mock expectations
			mockGoogleService.AssertExpectations(t)
		})
	}
}
