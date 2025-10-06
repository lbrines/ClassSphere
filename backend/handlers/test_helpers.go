package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/mock"
	"classsphere-backend/services"
)

// MockDashboardService for testing
type MockDashboardService struct {
	mock.Mock
}

func (m *MockDashboardService) GetDashboardData(userID string, role string) (map[string]interface{}, error) {
	args := m.Called(userID, role)
	return args.Get(0).(map[string]interface{}), args.Error(1)
}

func (m *MockDashboardService) GetAdminMetrics() (map[string]interface{}, error) {
	args := m.Called()
	return args.Get(0).(map[string]interface{}), args.Error(1)
}

func (m *MockDashboardService) GetTeacherMetrics(userID string) (map[string]interface{}, error) {
	args := m.Called(userID)
	return args.Get(0).(map[string]interface{}), args.Error(1)
}

func (m *MockDashboardService) GetStudentMetrics(userID string) (map[string]interface{}, error) {
	args := m.Called(userID)
	return args.Get(0).(map[string]interface{}), args.Error(1)
}

func (m *MockDashboardService) GetCoordinatorMetrics(userID string) (map[string]interface{}, error) {
	args := m.Called(userID)
	return args.Get(0).(map[string]interface{}), args.Error(1)
}

func (m *MockDashboardService) ExportDashboardData(userID string, role string, format string) ([]byte, error) {
	args := m.Called(userID, role, format)
	return args.Get(0).([]byte), args.Error(1)
}

// MockGoogleService for testing
type MockGoogleService struct {
	mock.Mock
}

func (m *MockGoogleService) ListCourses(userID string) ([]services.Course, error) {
	args := m.Called(userID)
	return args.Get(0).([]services.Course), args.Error(1)
}

func (m *MockGoogleService) ListStudents(courseID string) ([]services.Student, error) {
	args := m.Called(courseID)
	return args.Get(0).([]services.Student), args.Error(1)
}

func (m *MockGoogleService) ListAssignments(courseID string) ([]services.Assignment, error) {
	args := m.Called(courseID)
	return args.Get(0).([]services.Assignment), args.Error(1)
}

func (m *MockGoogleService) GetCourseStats(courseID string) (map[string]interface{}, error) {
	args := m.Called(courseID)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(map[string]interface{}), args.Error(1)
}

func (m *MockGoogleService) SetMockMode(enabled bool) {
	m.Called(enabled)
}

func (m *MockGoogleService) GetRandomCourse() services.Course {
	args := m.Called()
	return args.Get(0).(services.Course)
}

func (m *MockGoogleService) GetRandomStudent() services.Student {
	args := m.Called()
	return args.Get(0).(services.Student)
}

func (m *MockGoogleService) GetRandomAssignment() services.Assignment {
	args := m.Called()
	return args.Get(0).(services.Assignment)
}

// Test helper function to create test server
func createTestServer() *echo.Echo {
	e := echo.New()
	return e
}

// Test helper function to create test request
func createTestRequest(method, url string, body interface{}) *http.Request {
	var reqBody []byte
	if body != nil {
		reqBody, _ = json.Marshal(body)
	}
	
	req := httptest.NewRequest(method, url, bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	return req
}

// Test helper function to create test context
func createTestContext(e *echo.Echo, req *http.Request) (echo.Context, *httptest.ResponseRecorder) {
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	return c, rec
}

// Test helper function to create test context with user
func createTestContextWithUser(e *echo.Echo, req *http.Request, userID, userRole string) (echo.Context, *httptest.ResponseRecorder) {
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user_id", userID)
	c.Set("user_role", userRole)
	return c, rec
}
