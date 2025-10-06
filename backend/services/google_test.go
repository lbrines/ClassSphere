package services

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// MockGoogleClient is a mock implementation of Google API client
type MockGoogleClient struct {
	mock.Mock
}

func (m *MockGoogleClient) ListCourses(userID string) ([]Course, error) {
	args := m.Called(userID)
	return args.Get(0).([]Course), args.Error(1)
}

func (m *MockGoogleClient) ListStudents(courseID string) ([]Student, error) {
	args := m.Called(courseID)
	return args.Get(0).([]Student), args.Error(1)
}

func (m *MockGoogleClient) ListAssignments(courseID string) ([]Assignment, error) {
	args := m.Called(courseID)
	return args.Get(0).([]Assignment), args.Error(1)
}



func TestGoogleClassroomService_ListCourses(t *testing.T) {
	tests := []struct {
		name           string
		userID         string
		mockCourses    []Course
		mockError      error
		expectedError  bool
		expectedCount  int
	}{
		{
			name:   "successful course listing",
			userID: "user123",
			mockCourses: []Course{
				{ID: "course1", Name: "Mathematics", Description: "Advanced Math", Section: "A", Room: "Room 101", OwnerID: "user123", CourseState: "ACTIVE"},
				{ID: "course2", Name: "Science", Description: "Physics and Chemistry", Section: "B", Room: "Room 102", OwnerID: "user123", CourseState: "ACTIVE"},
				{ID: "course3", Name: "English", Description: "Literature", Section: "C", Room: "Room 103", OwnerID: "user123", CourseState: "ACTIVE"},
			},
			mockError:     nil,
			expectedError: false,
			expectedCount: 3,
		},
		{
			name:           "empty course list",
			userID:         "user456",
			mockCourses:    []Course{},
			mockError:      nil,
			expectedError:  false,
			expectedCount:  0,
		},
		{
			name:           "API error",
			userID:         "user789",
			mockCourses:    nil,
			mockError:      assert.AnError,
			expectedError:  true,
			expectedCount:  0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock client
			mockClient := &MockGoogleClient{}
			mockClient.On("ListCourses", tt.userID).Return(tt.mockCourses, tt.mockError)

			// Create service with mock client
			service := &GoogleClassroomService{
				client:   mockClient,
				mockMode: false,
			}

			// Test the method
			courses, err := service.ListCourses(tt.userID)

			// Assertions
			if tt.expectedError {
				assert.Error(t, err)
				assert.Nil(t, courses)
			} else {
				assert.NoError(t, err)
				assert.Len(t, courses, tt.expectedCount)
				assert.Equal(t, tt.mockCourses, courses)
			}

			// Verify mock was called
			mockClient.AssertExpectations(t)
		})
	}
}

func TestGoogleClassroomService_ListCoursesWithMockMode(t *testing.T) {
	service := &GoogleClassroomService{
		client:   nil, // No real client in mock mode
		mockMode: true,
	}

	courses, err := service.ListCourses("user123")

	assert.NoError(t, err)
	assert.Len(t, courses, 5) // Mock data should return 5 courses

	// Verify mock data structure
	for _, course := range courses {
		assert.NotEmpty(t, course.ID)
		assert.NotEmpty(t, course.Name)
		assert.NotEmpty(t, course.Description)
		assert.NotEmpty(t, course.OwnerID)
		assert.Equal(t, "ACTIVE", course.CourseState)
	}
}

func TestGoogleClassroomService_ListStudents(t *testing.T) {
	tests := []struct {
		name            string
		courseID        string
		mockStudents    []Student
		mockError       error
		expectedError   bool
		expectedCount   int
	}{
		{
			name:     "successful student listing",
			courseID: "course1",
			mockStudents: []Student{
				{ID: "student1", Name: "John Doe", Email: "john@example.com", PhotoURL: "https://example.com/photo1.jpg"},
				{ID: "student2", Name: "Jane Smith", Email: "jane@example.com", PhotoURL: "https://example.com/photo2.jpg"},
				{ID: "student3", Name: "Bob Johnson", Email: "bob@example.com", PhotoURL: "https://example.com/photo3.jpg"},
			},
			mockError:     nil,
			expectedError: false,
			expectedCount: 3,
		},
		{
			name:           "empty student list",
			courseID:       "course2",
			mockStudents:   []Student{},
			mockError:      nil,
			expectedError:  false,
			expectedCount:  0,
		},
		{
			name:           "API error",
			courseID:       "course3",
			mockStudents:   nil,
			mockError:      assert.AnError,
			expectedError:  true,
			expectedCount:  0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock client
			mockClient := &MockGoogleClient{}
			mockClient.On("ListStudents", tt.courseID).Return(tt.mockStudents, tt.mockError)

			// Create service with mock client
			service := &GoogleClassroomService{
				client:   mockClient,
				mockMode: false,
			}

			// Test the method
			students, err := service.ListStudents(tt.courseID)

			// Assertions
			if tt.expectedError {
				assert.Error(t, err)
				assert.Nil(t, students)
			} else {
				assert.NoError(t, err)
				assert.Len(t, students, tt.expectedCount)
				assert.Equal(t, tt.mockStudents, students)
			}

			// Verify mock was called
			mockClient.AssertExpectations(t)
		})
	}
}

func TestGoogleClassroomService_ListStudentsWithMockMode(t *testing.T) {
	service := &GoogleClassroomService{
		client:   nil, // No real client in mock mode
		mockMode: true,
	}

	students, err := service.ListStudents("course1")

	assert.NoError(t, err)
	assert.Len(t, students, 8) // Mock data should return 8 students

	// Verify mock data structure
	for _, student := range students {
		assert.NotEmpty(t, student.ID)
		assert.NotEmpty(t, student.Name)
		assert.NotEmpty(t, student.Email)
	}
}

func TestGoogleClassroomService_ListAssignments(t *testing.T) {
	tests := []struct {
		name              string
		courseID          string
		mockAssignments   []Assignment
		mockError         error
		expectedError     bool
		expectedCount     int
	}{
		{
			name:     "successful assignment listing",
			courseID: "course1",
			mockAssignments: []Assignment{
				{ID: "assignment1", Title: "Math Homework", Description: "Solve equations", DueDate: "2025-10-10", MaxPoints: 100, State: "PUBLISHED"},
				{ID: "assignment2", Title: "Science Project", Description: "Lab report", DueDate: "2025-10-15", MaxPoints: 150, State: "PUBLISHED"},
			},
			mockError:     nil,
			expectedError: false,
			expectedCount: 2,
		},
		{
			name:           "empty assignment list",
			courseID:       "course2",
			mockAssignments: []Assignment{},
			mockError:      nil,
			expectedError:  false,
			expectedCount:  0,
		},
		{
			name:           "API error",
			courseID:       "course3",
			mockAssignments: nil,
			mockError:      assert.AnError,
			expectedError:  true,
			expectedCount:  0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock client
			mockClient := &MockGoogleClient{}
			mockClient.On("ListAssignments", tt.courseID).Return(tt.mockAssignments, tt.mockError)

			// Create service with mock client
			service := &GoogleClassroomService{
				client:   mockClient,
				mockMode: false,
			}

			// Test the method
			assignments, err := service.ListAssignments(tt.courseID)

			// Assertions
			if tt.expectedError {
				assert.Error(t, err)
				assert.Nil(t, assignments)
			} else {
				assert.NoError(t, err)
				assert.Len(t, assignments, tt.expectedCount)
				assert.Equal(t, tt.mockAssignments, assignments)
			}

			// Verify mock was called
			mockClient.AssertExpectations(t)
		})
	}
}

func TestGoogleClassroomService_ListAssignmentsWithMockMode(t *testing.T) {
	service := &GoogleClassroomService{
		client:   nil, // No real client in mock mode
		mockMode: true,
	}

	assignments, err := service.ListAssignments("course1")

	assert.NoError(t, err)
	assert.Len(t, assignments, 6) // Mock data should return 6 assignments

	// Verify mock data structure
	for _, assignment := range assignments {
		assert.NotEmpty(t, assignment.ID)
		assert.NotEmpty(t, assignment.Title)
		assert.NotEmpty(t, assignment.DueDate)
		assert.Greater(t, assignment.MaxPoints, 0)
		assert.Equal(t, "PUBLISHED", assignment.State)
	}
}

func TestGoogleClassroomService_SetMockMode(t *testing.T) {
	service := &GoogleClassroomService{
		client:   &MockGoogleClient{},
		mockMode: false,
	}

	// Test setting mock mode to true
	service.SetMockMode(true)
	assert.True(t, service.mockMode)

	// Test setting mock mode to false
	service.SetMockMode(false)
	assert.False(t, service.mockMode)
}

func TestGoogleClassroomService_GetCourseStats(t *testing.T) {
	tests := []struct {
		name           string
		courseID       string
		mockStudents   []Student
		mockAssignments []Assignment
		mockError      error
		expectedError  bool
		expectedStats  map[string]interface{}
	}{
		{
			name:     "successful stats calculation",
			courseID: "course1",
			mockStudents: []Student{
				{ID: "student1", Name: "John Doe", Email: "john@example.com"},
				{ID: "student2", Name: "Jane Smith", Email: "jane@example.com"},
			},
			mockAssignments: []Assignment{
				{ID: "assignment1", Title: "Homework 1", State: "PUBLISHED", MaxPoints: 100},
				{ID: "assignment2", Title: "Homework 2", State: "PUBLISHED", MaxPoints: 150},
				{ID: "assignment3", Title: "Homework 3", State: "DRAFT", MaxPoints: 120},
			},
			mockError:     nil,
			expectedError: false,
			expectedStats: map[string]interface{}{
				"course_id":             "course1",
				"total_students":        2,
				"total_assignments":     3,
				"published_assignments": 2,
				"draft_assignments":     1,
			},
		},
		{
			name:           "error getting students",
			courseID:       "course2",
			mockStudents:   nil,
			mockAssignments: []Assignment{},
			mockError:      assert.AnError,
			expectedError:  true,
			expectedStats:  nil,
		},
		{
			name:           "error getting assignments",
			courseID:       "course3",
			mockStudents:   []Student{},
			mockAssignments: nil,
			mockError:      assert.AnError,
			expectedError:  true,
			expectedStats:  nil,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create mock client
			mockClient := &MockGoogleClient{}
			
			// Setup mock expectations
			mockClient.On("ListStudents", tt.courseID).Return(tt.mockStudents, tt.mockError)
			if tt.mockError == nil {
				mockClient.On("ListAssignments", tt.courseID).Return(tt.mockAssignments, tt.mockError)
			}

			// Create service with mock client
			service := &GoogleClassroomService{
				client:   mockClient,
				mockMode: false,
			}

			// Test the method
			stats, err := service.GetCourseStats(tt.courseID)

			// Assertions
			if tt.expectedError {
				assert.Error(t, err)
				assert.Nil(t, stats)
			} else {
				assert.NoError(t, err)
				assert.Equal(t, tt.expectedStats["course_id"], stats["course_id"])
				assert.Equal(t, tt.expectedStats["total_students"], stats["total_students"])
				assert.Equal(t, tt.expectedStats["total_assignments"], stats["total_assignments"])
				assert.Equal(t, tt.expectedStats["published_assignments"], stats["published_assignments"])
				assert.Equal(t, tt.expectedStats["draft_assignments"], stats["draft_assignments"])
			}

			// Verify mock was called
			mockClient.AssertExpectations(t)
		})
	}
}

func TestGoogleClassroomService_GetRandomMethods(t *testing.T) {
	service := &GoogleClassroomService{
		client:   nil,
		mockMode: true,
	}

	// Test GetRandomCourse
	course := service.GetRandomCourse()
	assert.NotEmpty(t, course.ID)
	assert.NotEmpty(t, course.Name)

	// Test GetRandomStudent
	student := service.GetRandomStudent()
	assert.NotEmpty(t, student.ID)
	assert.NotEmpty(t, student.Name)

	// Test GetRandomAssignment
	assignment := service.GetRandomAssignment()
	assert.NotEmpty(t, assignment.ID)
	assert.NotEmpty(t, assignment.Title)
}

func TestGoogleClassroomService_NewGoogleClassroomService(t *testing.T) {
	// Test with nil client (should enable mock mode)
	service := NewGoogleClassroomService(nil)
	assert.NotNil(t, service)
	assert.Nil(t, service.client)
	assert.True(t, service.mockMode) // Mock mode should be enabled when client is nil

	// Test with mock client (should disable mock mode)
	mockClient := &MockGoogleClient{}
	service = NewGoogleClassroomService(mockClient)
	assert.NotNil(t, service)
	assert.Equal(t, mockClient, service.client)
	assert.False(t, service.mockMode) // Mock mode should be disabled when client is provided
}

func TestGoogleClassroomService_ListCourses_EdgeCases(t *testing.T) {
	// Test ListCourses with nil client in non-mock mode
	service := &GoogleClassroomService{
		client:   nil,
		mockMode: false,
	}

	courses, err := service.ListCourses("user123")
	assert.Error(t, err)
	assert.Nil(t, courses)
	assert.Contains(t, err.Error(), "Google client not initialized")
}

func TestGoogleClassroomService_ListStudents_EdgeCases(t *testing.T) {
	// Test ListStudents with nil client in non-mock mode
	service := &GoogleClassroomService{
		client:   nil,
		mockMode: false,
	}

	students, err := service.ListStudents("course123")
	assert.Error(t, err)
	assert.Nil(t, students)
	assert.Contains(t, err.Error(), "Google client not initialized")
}

func TestGoogleClassroomService_ListAssignments_EdgeCases(t *testing.T) {
	// Test ListAssignments with nil client in non-mock mode
	service := &GoogleClassroomService{
		client:   nil,
		mockMode: false,
	}

	assignments, err := service.ListAssignments("course123")
	assert.Error(t, err)
	assert.Nil(t, assignments)
	assert.Contains(t, err.Error(), "Google client not initialized")
}

func TestGoogleClassroomService_GetCourseStats_EdgeCases(t *testing.T) {
	// Test GetCourseStats with nil client in non-mock mode
	service := &GoogleClassroomService{
		client:   nil,
		mockMode: false,
	}

	stats, err := service.GetCourseStats("course123")
	assert.Error(t, err)
	assert.Nil(t, stats)
	assert.Contains(t, err.Error(), "Google client not initialized")
}

// Test helper function to create a test HTTP server
func createTestServer(responseData interface{}, statusCode int) *httptest.Server {
	return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(statusCode)
		json.NewEncoder(w).Encode(responseData)
	}))
}
