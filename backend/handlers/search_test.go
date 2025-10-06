package handlers

import (
	"bytes"
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

// MockSearchService is a mock implementation of SearchService
type MockSearchService struct {
	mock.Mock
}

func (m *MockSearchService) SearchStudents(query string, filters services.SearchFilters) []services.SearchResult {
	args := m.Called(query, filters)
	return args.Get(0).([]services.SearchResult)
}

func (m *MockSearchService) SearchCourses(query string, filters services.SearchFilters) []services.SearchResult {
	args := m.Called(query, filters)
	return args.Get(0).([]services.SearchResult)
}

func (m *MockSearchService) SearchAssignments(query string, filters services.SearchFilters) []services.SearchResult {
	args := m.Called(query, filters)
	return args.Get(0).([]services.SearchResult)
}

func (m *MockSearchService) SearchAll(request services.SearchRequest) services.SearchResponse {
	args := m.Called(request)
	return args.Get(0).(services.SearchResponse)
}

// MockSearchUserRepository is a mock implementation of UserRepository for search tests
type MockSearchUserRepository struct {
	mock.Mock
}

func (m *MockSearchUserRepository) GetUserByID(id uint) (*models.User, error) {
	args := m.Called(id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*models.User), args.Error(1)
}

func (m *MockSearchUserRepository) GetUserByEmail(email string) (*models.User, error) {
	args := m.Called(email)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*models.User), args.Error(1)
}

func (m *MockSearchUserRepository) CreateUser(user *models.User) error {
	args := m.Called(user)
	return args.Error(0)
}

func (m *MockSearchUserRepository) UpdateUser(user *models.User) error {
	args := m.Called(user)
	return args.Error(0)
}

func (m *MockSearchUserRepository) DeleteUser(id uint) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockSearchUserRepository) ListUsers(offset, limit int) ([]*models.User, error) {
	args := m.Called(offset, limit)
	return args.Get(0).([]*models.User), args.Error(1)
}

func (m *MockSearchUserRepository) GetUserCount() (int64, error) {
	args := m.Called()
	return args.Get(0).(int64), args.Error(1)
}

func (m *MockSearchUserRepository) DeactivateUser(id uint) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockSearchUserRepository) ActivateUser(id uint) error {
	args := m.Called(id)
	return args.Error(0)
}

func TestSearchHandler_SearchAll(t *testing.T) {
	e := echo.New()
	
	tests := []struct {
		name           string
		requestBody    SearchRequest
		mockUser       *models.User
		mockUserError  error
		mockResponse   services.SearchResponse
		expectedStatus int
		expectedError  string
	}{
		{
			name: "successful search",
			requestBody: SearchRequest{
				Query: "math",
				Filters: services.SearchFilters{},
				Limit: 10,
				Offset: 0,
			},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResponse: services.SearchResponse{
				Results: []services.SearchResult{
					{Type: "course", ID: "1", Title: "Math 101", Score: 0.9},
				},
				Total: 1,
				Query: "math",
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "unauthorized - no user",
			requestBody: SearchRequest{
				Query: "math",
				Filters: services.SearchFilters{},
				Limit: 10,
				Offset: 0,
			},
			mockUser:       nil,
			mockUserError:  assert.AnError,
			expectedStatus: http.StatusUnauthorized,
			expectedError:  "User not found",
		},
		{
			name: "invalid request body",
			requestBody: SearchRequest{},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			expectedStatus: http.StatusOK, // Should use defaults
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Setup mocks
			mockUserRepo := new(MockSearchUserRepository)
			mockSearchService := new(MockSearchService)
			
			// Setup expectations
			if tt.mockUser != nil {
				mockUserRepo.On("GetUserByID", uint(1)).Return(tt.mockUser, tt.mockUserError)
			}
			
			if tt.expectedStatus == http.StatusOK {
				mockSearchService.On("SearchAll", mock.AnythingOfType("services.SearchRequest")).Return(tt.mockResponse)
			}
			
			// Create handler
			handler := NewSearchHandler(mockUserRepo, mockSearchService)
			
			// Create request
			reqBody, _ := json.Marshal(tt.requestBody)
			req := httptest.NewRequest(http.MethodPost, "/search", bytes.NewReader(reqBody))
			req.Header.Set("Content-Type", "application/json")
			rec := httptest.NewRecorder()
			
			// Add user to context (simulating JWT middleware)
			c := e.NewContext(req, rec)
			if tt.name != "unauthorized - no user" {
				claims := &auth.Claims{UserID: "1", Role: "admin"}
				c.Set("user", claims)
			}
			
			// Execute
			err := handler.SearchAll(c)
			
			// Assertions
			if tt.expectedStatus == http.StatusUnauthorized {
				// For unauthorized, check HTTP status code
				assert.NoError(t, err) // Echo doesn't return error for HTTP responses
				assert.Equal(t, tt.expectedStatus, rec.Code)
			} else if tt.expectedError != "" {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
			
			mockUserRepo.AssertExpectations(t)
			mockSearchService.AssertExpectations(t)
		})
	}
}

func TestSearchHandler_SearchStudents(t *testing.T) {
	e := echo.New()
	
	tests := []struct {
		name           string
		queryParams    map[string]string
		mockUser       *models.User
		mockResults    []services.SearchResult
		expectedStatus int
	}{
		{
			name: "successful student search",
			queryParams: map[string]string{
				"q": "john",
			},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResults: []services.SearchResult{
				{Type: "student", ID: "1", Title: "John Doe", Score: 0.9},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "search with filters",
			queryParams: map[string]string{
				"q": "jane",
				"course": "math",
				"grade": "A",
			},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResults: []services.SearchResult{
				{Type: "student", ID: "2", Title: "Jane Smith", Score: 0.8},
			},
			expectedStatus: http.StatusOK,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Setup mocks
			mockUserRepo := new(MockSearchUserRepository)
			mockSearchService := new(MockSearchService)
			
			// Setup expectations
			mockUserRepo.On("GetUserByID", uint(1)).Return(tt.mockUser, nil)
			mockSearchService.On("SearchStudents", mock.AnythingOfType("string"), mock.AnythingOfType("services.SearchFilters")).Return(tt.mockResults)
			
			// Create handler
			handler := NewSearchHandler(mockUserRepo, mockSearchService)
			
			// Create request
			req := httptest.NewRequest(http.MethodGet, "/search/students", nil)
			
			// Add query parameters
			q := req.URL.Query()
			for key, value := range tt.queryParams {
				q.Add(key, value)
			}
			req.URL.RawQuery = q.Encode()
			
			// Add user to context
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			claims := &auth.Claims{UserID: "1", Role: "admin"}
			c.Set("user", claims)
			
			// Execute
			err := handler.SearchStudents(c)
			
			// Assertions
			assert.NoError(t, err)
			mockUserRepo.AssertExpectations(t)
			mockSearchService.AssertExpectations(t)
		})
	}
}

func TestSearchHandler_SearchCourses(t *testing.T) {
	e := echo.New()
	
	tests := []struct {
		name           string
		queryParams    map[string]string
		mockUser       *models.User
		mockResults    []services.SearchResult
		expectedStatus int
	}{
		{
			name: "successful course search",
			queryParams: map[string]string{
				"q": "math",
			},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResults: []services.SearchResult{
				{Type: "course", ID: "1", Title: "Math 101", Score: 0.9},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "search with course filter",
			queryParams: map[string]string{
				"q": "physics",
				"course": "physics",
				"state": "ACTIVE",
			},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResults: []services.SearchResult{
				{Type: "course", ID: "2", Title: "Physics 201", Score: 0.8},
			},
			expectedStatus: http.StatusOK,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Setup mocks
			mockUserRepo := new(MockSearchUserRepository)
			mockSearchService := new(MockSearchService)
			
			// Setup expectations
			mockUserRepo.On("GetUserByID", uint(1)).Return(tt.mockUser, nil)
			mockSearchService.On("SearchCourses", mock.AnythingOfType("string"), mock.AnythingOfType("services.SearchFilters")).Return(tt.mockResults)
			
			// Create handler
			handler := NewSearchHandler(mockUserRepo, mockSearchService)
			
			// Create request
			req := httptest.NewRequest(http.MethodGet, "/search/courses", nil)
			
			// Add query parameters
			q := req.URL.Query()
			for key, value := range tt.queryParams {
				q.Add(key, value)
			}
			req.URL.RawQuery = q.Encode()
			
			// Add user to context
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			claims := &auth.Claims{UserID: "1", Role: "admin"}
			c.Set("user", claims)
			
			// Execute
			err := handler.SearchCourses(c)
			
			// Assertions
			assert.NoError(t, err)
			mockUserRepo.AssertExpectations(t)
			mockSearchService.AssertExpectations(t)
		})
	}
}

func TestSearchHandler_SearchAssignments(t *testing.T) {
	e := echo.New()
	
	tests := []struct {
		name           string
		queryParams    map[string]string
		mockUser       *models.User
		mockResults    []services.SearchResult
		expectedStatus int
	}{
		{
			name: "successful assignment search",
			queryParams: map[string]string{
				"q": "homework",
			},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResults: []services.SearchResult{
				{Type: "assignment", ID: "1", Title: "Math Homework", Score: 0.9},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name: "search with points filter",
			queryParams: map[string]string{
				"q": "quiz",
				"min_points": "50",
				"max_points": "100",
				"state": "PUBLISHED",
			},
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResults: []services.SearchResult{
				{Type: "assignment", ID: "2", Title: "Physics Quiz", Score: 0.8},
			},
			expectedStatus: http.StatusOK,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Setup mocks
			mockUserRepo := new(MockSearchUserRepository)
			mockSearchService := new(MockSearchService)
			
			// Setup expectations
			mockUserRepo.On("GetUserByID", uint(1)).Return(tt.mockUser, nil)
			mockSearchService.On("SearchAssignments", mock.AnythingOfType("string"), mock.AnythingOfType("services.SearchFilters")).Return(tt.mockResults)
			
			// Create handler
			handler := NewSearchHandler(mockUserRepo, mockSearchService)
			
			// Create request
			req := httptest.NewRequest(http.MethodGet, "/search/assignments", nil)
			
			// Add query parameters
			q := req.URL.Query()
			for key, value := range tt.queryParams {
				q.Add(key, value)
			}
			req.URL.RawQuery = q.Encode()
			
			// Add user to context
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			claims := &auth.Claims{UserID: "1", Role: "admin"}
			c.Set("user", claims)
			
			// Execute
			err := handler.SearchAssignments(c)
			
			// Assertions
			assert.NoError(t, err)
			mockUserRepo.AssertExpectations(t)
			mockSearchService.AssertExpectations(t)
		})
	}
}

func TestSearchHandler_GetSearchSuggestions(t *testing.T) {
	e := echo.New()
	
	tests := []struct {
		name           string
		query          string
		mockUser       *models.User
		mockResults    []services.SearchResult
		expectedStatus int
	}{
		{
			name:  "successful suggestions",
			query: "math",
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			mockResults: []services.SearchResult{
				{Type: "course", ID: "1", Title: "Math 101", Score: 0.9},
				{Type: "student", ID: "2", Title: "Math Student", Score: 0.8},
			},
			expectedStatus: http.StatusOK,
		},
		{
			name:  "query too short",
			query: "m",
			mockUser: &models.User{ID: 1, Email: "test@example.com", Name: "Test User"},
			expectedStatus: http.StatusOK,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Setup mocks
			mockUserRepo := new(MockSearchUserRepository)
			mockSearchService := new(MockSearchService)
			
			// Setup expectations
			mockUserRepo.On("GetUserByID", uint(1)).Return(tt.mockUser, nil)
			
			if len(tt.query) >= 2 {
				mockSearchService.On("SearchStudents", tt.query, mock.AnythingOfType("services.SearchFilters")).Return(tt.mockResults)
				mockSearchService.On("SearchCourses", tt.query, mock.AnythingOfType("services.SearchFilters")).Return(tt.mockResults)
				mockSearchService.On("SearchAssignments", tt.query, mock.AnythingOfType("services.SearchFilters")).Return(tt.mockResults)
			}
			
			// Create handler
			handler := NewSearchHandler(mockUserRepo, mockSearchService)
			
			// Create request
			req := httptest.NewRequest(http.MethodGet, "/search/suggestions", nil)
			
			// Add query parameter
			q := req.URL.Query()
			q.Add("q", tt.query)
			req.URL.RawQuery = q.Encode()
			
			// Add user to context
			rec := httptest.NewRecorder()
			c := e.NewContext(req, rec)
			claims := &auth.Claims{UserID: "1", Role: "admin"}
			c.Set("user", claims)
			
			// Execute
			err := handler.GetSearchSuggestions(c)
			
			// Assertions
			assert.NoError(t, err)
			mockUserRepo.AssertExpectations(t)
			mockSearchService.AssertExpectations(t)
		})
	}
}

func TestNewSearchHandler(t *testing.T) {
	mockUserRepo := new(MockSearchUserRepository)
	mockSearchService := new(MockSearchService)
	
	handler := NewSearchHandler(mockUserRepo, mockSearchService)
	
	assert.NotNil(t, handler)
	assert.Equal(t, mockUserRepo, handler.userRepo)
	assert.Equal(t, mockSearchService, handler.searchService)
}

func TestSearchRequest_DefaultValues(t *testing.T) {
	req := SearchRequest{
		Query: "test",
		Filters: services.SearchFilters{},
		Limit: 10,
		Offset: 0,
	}
	
	assert.Equal(t, "test", req.Query)
	assert.Equal(t, 10, req.Limit)
	assert.Equal(t, 0, req.Offset)
	assert.NotNil(t, req.Filters)
}

func TestSearchResponse_Structure(t *testing.T) {
	response := SearchResponse{
		Results:    []services.SearchResult{},
		Total:      0,
		Query:      "test",
		Filters:    services.SearchFilters{},
		SearchTime: "100ms",
	}
	
	assert.NotNil(t, response.Results)
	assert.Equal(t, 0, response.Total)
	assert.Equal(t, "test", response.Query)
	assert.NotNil(t, response.Filters)
	assert.Equal(t, "100ms", response.SearchTime)
}
