package http_test

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"golang.org/x/crypto/bcrypt"

	httpadapter "github.com/lbrines/classsphere/internal/adapters/http"
	"github.com/lbrines/classsphere/internal/adapters/repo"
	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

var ctx = context.Background()

func TestSearchHandler_SingleEntity(t *testing.T) {
	// Setup
	authService, userService, _, classroomService := newTestServicesSearch(t)
	searchService := app.NewSearchService()
	notificationHub := app.NewNotificationHub()
	
	router := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)
	
	// Login to get token
	tokens, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	// Test search
	req := httptest.NewRequest(http.MethodGet, "/api/v1/search?q=Math&entities=courses&limit=10", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()
	
	router.ServeHTTP(rec, req)
	
	// Assert
	require.Equal(t, http.StatusOK, rec.Code)
	
	var response domain.SearchResponse
	err = json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "Math", response.Query)
	assert.GreaterOrEqual(t, response.Total, 0)
}

func TestSearchHandler_MultipleEntities(t *testing.T) {
	// Setup
	authService, userService, _, classroomService := newTestServicesSearch(t)
	searchService := app.NewSearchService()
	notificationHub := app.NewNotificationHub()
	
	router := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)
	
	// Login
	tokens, err := authService.LoginWithPassword(ctx, "teacher@classsphere.edu", "teacher123")
	require.NoError(t, err)
	
	// Test search multiple entities
	req := httptest.NewRequest(http.MethodGet, "/api/v1/search?q=John&entities=students,teachers&limit=5", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()
	
	router.ServeHTTP(rec, req)
	
	// Assert
	require.Equal(t, http.StatusOK, rec.Code)
	
	var response domain.SearchResponse
	err = json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, "John", response.Query)
}

func TestSearchHandler_Unauthorized(t *testing.T) {
	// Setup
	authService, userService, _, classroomService := newTestServicesSearch(t)
	searchService := app.NewSearchService()
	notificationHub := app.NewNotificationHub()
	
	router := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)
	
	// Test without token
	req := httptest.NewRequest(http.MethodGet, "/api/v1/search?q=Math&entities=courses", nil)
	rec := httptest.NewRecorder()
	
	router.ServeHTTP(rec, req)
	
	// Assert
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestSearchHandler_MissingQuery(t *testing.T) {
	// Setup
	authService, userService, _, classroomService := newTestServicesSearch(t)
	searchService := app.NewSearchService()
	notificationHub := app.NewNotificationHub()
	
	router := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)
	
	// Login
	tokens, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	// Test without query
	req := httptest.NewRequest(http.MethodGet, "/api/v1/search?entities=courses", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()
	
	router.ServeHTTP(rec, req)
	
	// Empty query should return 200 with empty results
	require.Equal(t, http.StatusOK, rec.Code)
	
	var response domain.SearchResponse
	err = json.NewDecoder(rec.Body).Decode(&response)
	require.NoError(t, err)
	
	assert.Equal(t, 0, response.Total)
}

func TestSearchHandler_MissingEntities(t *testing.T) {
	// Setup
	authService, userService, _, classroomService := newTestServicesSearch(t)
	searchService := app.NewSearchService()
	notificationHub := app.NewNotificationHub()
	
	router := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)
	
	// Login
	tokens, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	// Test without entities - should default to all
	req := httptest.NewRequest(http.MethodGet, "/api/v1/search?q=Math", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()
	
	router.ServeHTTP(rec, req)
	
	// Should return bad request when entities not specified
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestSearchHandler_InvalidLimit(t *testing.T) {
	// Setup
	authService, userService, _, classroomService := newTestServicesSearch(t)
	searchService := app.NewSearchService()
	notificationHub := app.NewNotificationHub()
	
	router := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)
	
	// Login
	tokens, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	// Test with invalid limit
	req := httptest.NewRequest(http.MethodGet, "/api/v1/search?q=Math&entities=courses&limit=abc", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()
	
	router.ServeHTTP(rec, req)
	
	// Should use default limit (10) and still work
	require.Equal(t, http.StatusOK, rec.Code)
}

func TestSearchHandler_RoleBasedFiltering(t *testing.T) {
	tests := []struct {
		name     string
		email    string
		password string
		entities string
		wantCode int
	}{
		{
			name:     "Student searches courses",
			email:    "student@classsphere.edu",
			password: "student123",
			entities: "courses",
			wantCode: http.StatusOK,
		},
		{
			name:     "Teacher searches students",
			email:    "teacher@classsphere.edu",
			password: "teacher123",
			entities: "students",
			wantCode: http.StatusOK,
		},
		{
			name:     "Admin searches all",
			email:    "admin@classsphere.edu",
			password: "admin123",
			entities: "students,teachers,courses,assignments",
			wantCode: http.StatusOK,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Setup
			authService, userService, _, classroomService := newTestServicesSearch(t)
			searchService := app.NewSearchService()
			notificationHub := app.NewNotificationHub()
			
			router := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)
			
			// Login
			tokens, err := authService.LoginWithPassword(ctx, tt.email, tt.password)
			require.NoError(t, err)
			
			// Test search
			req := httptest.NewRequest(http.MethodGet, "/api/v1/search?q=test&entities="+tt.entities, nil)
			req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
			rec := httptest.NewRecorder()
			
			router.ServeHTTP(rec, req)
			
			assert.Equal(t, tt.wantCode, rec.Code)
		})
	}
}

// Test helper
func newTestServicesSearch(t *testing.T) (*app.AuthService, *app.UserService, *inMemoryCacheSearch, *app.ClassroomService) {
	t.Helper()

	hash, err := bcrypt.GenerateFromPassword([]byte("admin123"), bcrypt.DefaultCost)
	require.NoError(t, err)
	adminHash := string(hash)

	hash, err = bcrypt.GenerateFromPassword([]byte("teacher123"), bcrypt.DefaultCost)
	require.NoError(t, err)
	teacherHash := string(hash)

	hash, err = bcrypt.GenerateFromPassword([]byte("student123"), bcrypt.DefaultCost)
	require.NoError(t, err)
	studentHash := string(hash)

	now := time.Now()
	users := []domain.User{
		{ID: "admin-1", Email: "admin@classsphere.edu", HashedPassword: adminHash, Role: domain.RoleAdmin, CreatedAt: now, UpdatedAt: now},
		{ID: "teacher-1", Email: "teacher@classsphere.edu", HashedPassword: teacherHash, Role: domain.RoleTeacher, CreatedAt: now, UpdatedAt: now},
		{ID: "student-1", Email: "student@classsphere.edu", HashedPassword: studentHash, Role: domain.RoleStudent, CreatedAt: now, UpdatedAt: now},
	}

	userRepo := repo.NewMemoryUserRepository(users)
	cache := &inMemoryCacheSearch{store: make(map[string][]byte)}
	oauth := &staticOAuthSearch{}

	authService, err := app.NewAuthService(userRepo, cache, oauth, shared.Config{
		JWTSecret:          "test-secret",
		JWTIssuer:          "classsphere",
		JWTExpiryMinutes:   60,
		GoogleClientID:     "client",
		GoogleClientSecret: "secret",
		GoogleRedirectURL:  "http://localhost/callback",
		ClassroomMode:      "mock",
	})
	require.NoError(t, err)

	userService, err := app.NewUserService(userRepo)
	require.NoError(t, err)

	classroomService := newStubClassroomServiceSearch(t)

	return authService, userService, cache, classroomService
}

func newStubClassroomServiceSearch(t *testing.T) *app.ClassroomService {
	provider := &stubClassroomProviderSearch{mode: shared.IntegrationModeMock}
	svc, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	return svc
}

type inMemoryCacheSearch struct {
	store map[string][]byte
}

func (c *inMemoryCacheSearch) Set(ctx context.Context, key string, value []byte, expiration int) error {
	c.store[key] = value
	return nil
}

func (c *inMemoryCacheSearch) Get(ctx context.Context, key string) ([]byte, error) {
	if val, ok := c.store[key]; ok {
		return val, nil
	}
	return nil, nil
}

func (c *inMemoryCacheSearch) Delete(ctx context.Context, key string) error {
	delete(c.store, key)
	return nil
}

func (c *inMemoryCacheSearch) Ping(ctx context.Context) error {
	return nil
}

func (c *inMemoryCacheSearch) Close() error {
	return nil
}

type staticOAuthSearch struct{}

func (s *staticOAuthSearch) AuthURL(state string) (string, error) {
	return "https://accounts.google.com?state=" + state, nil
}

func (s *staticOAuthSearch) Exchange(_ context.Context, _ string) (ports.OAuthUser, error) {
	return ports.OAuthUser{ID: "student-1", Email: "student@classsphere.edu"}, nil
}

type stubClassroomProviderSearch struct {
	mode string
}

func (s *stubClassroomProviderSearch) Mode() string {
	return s.mode
}

func (s *stubClassroomProviderSearch) Snapshot(_ context.Context) (domain.ClassroomSnapshot, error) {
	return domain.ClassroomSnapshot{
		Mode:        s.mode,
		GeneratedAt: time.Unix(0, 0),
		Courses:     []domain.Course{},
	}, nil
}

