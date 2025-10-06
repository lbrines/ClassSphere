package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"classsphere-backend/auth"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

// Test GetCourseStats edge cases
func TestGoogleHandler_GetCourseStats_EdgeCases(t *testing.T) {
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
				googleService.On("GetCourseStats", "course123").Return(map[string]interface{}{}, assert.AnError)
			},
			expectedStatus: http.StatusInternalServerError,
			description:    "Should return internal server error when service fails",
		},
		{
			name:     "Service returns empty stats",
			courseID: "course123",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				emptyStats := map[string]interface{}{}
				googleService.On("GetCourseStats", "course123").Return(emptyStats, nil)
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle empty stats gracefully",
		},
		{
			name:     "Service returns valid stats",
			courseID: "course123",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				stats := map[string]interface{}{
					"course_id":             "course123",
					"total_students":        25,
					"total_assignments":     10,
					"published_assignments": 8,
					"draft_assignments":     2,
					"average_grade":         85.5,
				}
				googleService.On("GetCourseStats", "course123").Return(stats, nil)
			},
			expectedStatus: http.StatusOK,
			description:    "Should handle valid stats correctly",
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
			req := httptest.NewRequest(http.MethodGet, "/api/google/courses/"+tt.courseID+"/stats", nil)
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
			err := handler.GetCourseStats(c)

			// Assertions
			assert.NoError(t, err, tt.description)
			assert.Equal(t, tt.expectedStatus, rec.Code, tt.description)

			// Verify response structure for successful cases
			if tt.expectedStatus == http.StatusOK {
				var response map[string]interface{}
				err = json.Unmarshal(rec.Body.Bytes(), &response)
				assert.NoError(t, err, tt.description)
				// GetCourseStats returns the stats directly, not wrapped in a "stats" key
				// For empty stats case, we just verify the response is valid JSON
				if tt.name == "Service returns empty stats" {
					assert.NotNil(t, response, tt.description)
				} else {
					assert.NotEmpty(t, response, tt.description)
				}
			}

			// Verify mock expectations
			mockGoogleService.AssertExpectations(t)
		})
	}
}

// Test GetPerformanceMetrics edge cases
func TestGoogleHandler_GetPerformanceMetrics_EdgeCases(t *testing.T) {
	tests := []struct {
		name           string
		setupMocks     func(*MockGoogleClassroomService, *MockMetricsService)
		expectedStatus int
		description    string
	}{
		{
			name: "No user context",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				// No mocks needed
			},
			expectedStatus: http.StatusUnauthorized,
			description:    "Should return unauthorized for no user context",
		},
		{
			name: "Invalid user context type",
			setupMocks: func(googleService *MockGoogleClassroomService, metricsService *MockMetricsService) {
				// No mocks needed
			},
			expectedStatus: http.StatusUnauthorized,
			description:    "Should return unauthorized for invalid user context",
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
			req := httptest.NewRequest(http.MethodGet, "/api/google/performance/metrics", nil)
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)

			// Set user context based on test case
			if tt.name == "Invalid user context type" {
				c.Set("user", "invalid_user_context")
			}
			// For "No user context", we don't set any user

			// Test the function
			err := handler.GetPerformanceMetrics(c)

			// Assertions
			assert.NoError(t, err, tt.description)
			assert.Equal(t, tt.expectedStatus, rec.Code, tt.description)

			// Verify response structure for error cases
			if tt.expectedStatus == http.StatusUnauthorized {
				var response map[string]interface{}
				err = json.Unmarshal(rec.Body.Bytes(), &response)
				assert.NoError(t, err, tt.description)
				assert.Contains(t, response, "error", tt.description)
			}

			// Verify mock expectations
			mockGoogleService.AssertExpectations(t)
		})
	}
}
