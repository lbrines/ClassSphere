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

// Test GetCourseAssignments additional edge cases
func TestGoogleHandler_GetCourseAssignments_AdditionalEdgeCases(t *testing.T) {
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
				googleService.On("ListAssignments", "course123").Return([]services.Assignment{}, assert.AnError)
			},
			expectedStatus: http.StatusInternalServerError,
			description:    "Should return internal server error when service fails",
		},
		{
			name:     "Service returns assignments with mixed states",
			courseID: "course123",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				assignments := []services.Assignment{
					{ID: "assignment1", Title: "HW1", State: "PUBLISHED", MaxPoints: 100},
					{ID: "assignment2", Title: "HW2", State: "DRAFT", MaxPoints: 150},
					{ID: "assignment3", Title: "HW3", State: "COMPLETED", MaxPoints: 120},
				}
				googleService.On("ListAssignments", "course123").Return(assignments, nil)
				metricsService.On("CalculateAssignmentMetrics", assignments).Return(services.AssignmentMetrics{TotalAssignments: 3})
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle assignments with mixed states correctly",
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

// Test GetCourses edge cases for better coverage
func TestGoogleHandler_GetCourses_AdditionalEdgeCases(t *testing.T) {
	tests := []struct {
		name           string
		setupMocks     func(*MockGoogleClassroomService, *MockMetricsService)
		expectedStatus int
		description    string
	}{
		{
			name: "Service returns courses with mixed states",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				courses := []services.Course{
					{ID: "course1", Name: "Math", CourseState: "ACTIVE"},
					{ID: "course2", Name: "Science", CourseState: "ARCHIVED"},
					{ID: "course3", Name: "History", CourseState: "ACTIVE"},
				}
				googleService.On("ListCourses", "123").Return(courses, nil)
				metricsService.On("CalculateCourseMetrics", courses).Return(services.CourseMetrics{TotalCourses: 3})
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle courses with mixed states correctly",
		},
		{
			name: "Service returns single course",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				courses := []services.Course{
					{ID: "course1", Name: "Math", CourseState: "ACTIVE"},
				}
				googleService.On("ListCourses", "123").Return(courses, nil)
				metricsService.On("CalculateCourseMetrics", courses).Return(services.CourseMetrics{TotalCourses: 1})
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle single course correctly",
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

			// Set user context
			claims := &auth.Claims{
				UserID: "123",
				Role:   "student",
			}
			c.Set("user", claims)

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
