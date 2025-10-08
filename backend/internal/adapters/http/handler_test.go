package http_test

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	echo "github.com/labstack/echo/v4"
	"github.com/stretchr/testify/require"
	"golang.org/x/crypto/bcrypt"

	httpadapter "github.com/lbrines/classsphere/internal/adapters/http"
	"github.com/lbrines/classsphere/internal/adapters/repo"
	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

func TestLoginHandler(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	payload := map[string]string{
		"email":    "admin@classsphere.edu",
		"password": "admin123",
	}
	body, err := json.Marshal(payload)
	require.NoError(t, err)

	req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(body))
	req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
	rec := httptest.NewRecorder()

	router.ServeHTTP(rec, req)

	require.Equal(t, http.StatusOK, rec.Code)
}

func TestAuthMiddleware(t *testing.T) {
	authService, _, _, _ := newTestServices(t)
	ctx := context.Background()
	tokens, err := authService.LoginWithPassword(ctx, "admin@classsphere.edu", "admin123")
	require.NoError(t, err)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/users/me", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	handler := func(c echo.Context) error {
		user := httpadapter.CurrentUser(c)
		require.Equal(t, "admin@classsphere.edu", user.Email)
		return c.NoContent(http.StatusOK)
	}

	err = httpadapter.AuthMiddleware(authService)(handler)(c)
	require.NoError(t, err)
	require.Equal(t, http.StatusOK, rec.Code)
}

func TestRequireRole(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	ctx := context.Background()
	tokens, err := authService.LoginWithPassword(ctx, "admin@classsphere.edu", "admin123")
	require.NoError(t, err)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/admin/ping", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()

	notificationHub := app.NewNotificationHub()
	e := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())
	e.ServeHTTP(rec, req)

	require.Equal(t, http.StatusOK, rec.Code)
}

func TestHealthEndpoint(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	require.Equal(t, http.StatusOK, rec.Code)
}

func TestOAuthEndpoints(t *testing.T) {
	authService, userService, cache, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	req := httptest.NewRequest(http.MethodGet, "/api/v1/auth/oauth/google", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)
	require.Equal(t, http.StatusOK, rec.Code)

	var startResp map[string]string
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &startResp))
	state := startResp["state"]
	require.NotEmpty(t, state)
	require.Contains(t, cache.store, "oauth_state:"+state)

	callbackReq := httptest.NewRequest(http.MethodGet, "/api/v1/auth/oauth/callback?code=abc&state="+state, nil)
	callbackRec := httptest.NewRecorder()
	router.ServeHTTP(callbackRec, callbackReq)
	require.Equal(t, http.StatusOK, callbackRec.Code)
}

func TestMeEndpoint(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	loginPayload := map[string]string{
		"email":    "admin@classsphere.edu",
		"password": "admin123",
	}
	body, err := json.Marshal(loginPayload)
	require.NoError(t, err)

	loginReq := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(body))
	loginReq.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
	loginRec := httptest.NewRecorder()
	router.ServeHTTP(loginRec, loginReq)
	require.Equal(t, http.StatusOK, loginRec.Code)

	var loginResp map[string]any
	require.NoError(t, json.Unmarshal(loginRec.Body.Bytes(), &loginResp))
	token, _ := loginResp["accessToken"].(string)
	require.NotEmpty(t, token)

	meReq := httptest.NewRequest(http.MethodGet, "/api/v1/users/me", nil)
	meReq.Header.Set("Authorization", "Bearer "+token)
	meRec := httptest.NewRecorder()
	router.ServeHTTP(meRec, meReq)
	require.Equal(t, http.StatusOK, meRec.Code)
}

func TestCoursesEndpoint(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	ctx := context.Background()
	tokens, err := authService.LoginWithPassword(ctx, "admin@classsphere.edu", "admin123")
	require.NoError(t, err)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/google/courses", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()

	router.ServeHTTP(rec, req)
	require.Equal(t, http.StatusOK, rec.Code)

	var resp struct {
		Mode           string           `json:"mode"`
		Courses        []map[string]any `json:"courses"`
		AvailableModes []string         `json:"availableModes"`
	}
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &resp))
	require.Contains(t, resp.Mode, "mock")
	require.NotEmpty(t, resp.Courses)
	require.NotEmpty(t, resp.AvailableModes)
}

func TestAdminDashboardEndpoint(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	ctx := context.Background()
	tokens, err := authService.LoginWithPassword(ctx, "admin@classsphere.edu", "admin123")
	require.NoError(t, err)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/dashboard/admin", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()

	router.ServeHTTP(rec, req)
	require.Equal(t, http.StatusOK, rec.Code)

	var resp map[string]any
	require.NoError(t, json.Unmarshal(rec.Body.Bytes(), &resp))
	require.Equal(t, "admin", resp["role"])
}

// Helpers

// newTestConfig returns a test configuration with default values
func newTestConfig() shared.Config {
	return shared.Config{
		JWTSecret:          "test-secret",
		JWTIssuer:          "classsphere",
		JWTExpiryMinutes:   60,
		GoogleClientID:     "client",
		GoogleClientSecret: "secret",
		GoogleRedirectURL:  "http://localhost/callback",
		FrontendURL:        "http://localhost:4200",
		AllowedOrigins:     []string{"http://localhost:4200"},
	}
}

func newTestServices(t *testing.T) (*app.AuthService, *app.UserService, *inMemoryCache, *app.ClassroomService) {
	t.Helper()

	hash, err := bcrypt.GenerateFromPassword([]byte("admin123"), bcrypt.DefaultCost)
	require.NoError(t, err)

	repository := repo.NewMemoryUserRepository([]domain.User{{
		ID:             "admin-1",
		Email:          "admin@classsphere.edu",
		HashedPassword: string(hash),
		Role:           domain.RoleAdmin,
		CreatedAt:      time.Now(),
		UpdatedAt:      time.Now(),
	}})

	cache := &inMemoryCache{store: make(map[string][]byte)}
	oauth := &staticOAuth{}

	cfg := newTestConfig()

	authService, err := app.NewAuthService(repository, cache, oauth, cfg)
	require.NoError(t, err)
	userService, err := app.NewUserService(repository)
	require.NoError(t, err)

	classroomService := newStubClassroomService(t)

	return authService, userService, cache, classroomService
}

func newStubClassroomService(t *testing.T) *app.ClassroomService {
	provider := &stubClassroomProvider{mode: shared.IntegrationModeMock}
	svc, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	svc.WithClock(func() time.Time { return time.Unix(0, 0) })
	return svc
}

type inMemoryCache struct {
	store map[string][]byte
}

func (c *inMemoryCache) Set(_ context.Context, key string, value []byte, _ int) error {
	c.store[key] = value
	return nil
}

func (c *inMemoryCache) Get(_ context.Context, key string) ([]byte, error) {
	return c.store[key], nil
}

func (c *inMemoryCache) Delete(_ context.Context, key string) error {
	delete(c.store, key)
	return nil
}

func (c *inMemoryCache) Ping(_ context.Context) error { return nil }

func (c *inMemoryCache) Close() error { return nil }

type staticOAuth struct{}

func (s *staticOAuth) AuthURL(state string) (string, error) {
	return "https://accounts.google.com?state=" + state, nil
}

func (s *staticOAuth) Exchange(_ context.Context, _ string) (ports.OAuthUser, error) {
	return ports.OAuthUser{ID: "admin-1", Email: "admin@classsphere.edu"}, nil
}

type stubClassroomProvider struct {
	mode string
}

func (s *stubClassroomProvider) Mode() string {
	return s.mode
}

func (s *stubClassroomProvider) Snapshot(_ context.Context) (domain.ClassroomSnapshot, error) {
	now := time.Unix(0, 0)
	return domain.ClassroomSnapshot{
		Mode:        s.mode,
		GeneratedAt: now,
		Courses: []domain.Course{
			{
				ID:               "course-test",
				Name:             "Test Course",
				Program:          "STEM",
				CoordinatorEmail: "coordinator@classsphere.edu",
				Teachers: []domain.CourseTeacher{{
					ID:    "teacher-1",
					Name:  "Teacher",
					Email: "teacher@classsphere.edu",
				}},
				Students: []domain.CourseStudent{},
				Assignments: []domain.CourseAssignment{{
					ID:        "assign-1",
					Title:     "Assignment",
					DueDate:   now.Add(48 * time.Hour),
					Status:    domain.AssignmentStatusOpen,
					Completed: 10,
					Pending:   5,
				}},
				LastActivity: now,
			},
		},
	}, nil
}

// === ADDITIONAL TESTS FOR 90% COVERAGE ===

func TestLoginHandler_Errors(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	t.Run("invalid json", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader([]byte("invalid-json")))
		req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		require.Equal(t, http.StatusBadRequest, rec.Code)
	})

	t.Run("missing email", func(t *testing.T) {
		payload := map[string]string{"password": "test"}
		body, _ := json.Marshal(payload)

		req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(body))
		req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		// Missing email results in unauthorized (treated as invalid credentials)
		require.Equal(t, http.StatusUnauthorized, rec.Code)
	})

	t.Run("invalid credentials", func(t *testing.T) {
		payload := map[string]string{
			"email":    "admin@classsphere.edu",
			"password": "wrong",
		}
		body, _ := json.Marshal(payload)

		req := httptest.NewRequest(http.MethodPost, "/api/v1/auth/login", bytes.NewReader(body))
		req.Header.Set(echo.HeaderContentType, echo.MIMEApplicationJSON)
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		require.Equal(t, http.StatusUnauthorized, rec.Code)
	})
}

func TestAuthMiddleware_Errors(t *testing.T) {
	t.Run("missing authorization header", func(t *testing.T) {
		authService, userService, _, classroomService := newTestServices(t)
		notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

		req := httptest.NewRequest(http.MethodGet, "/api/v1/users/me", nil)
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		require.Equal(t, http.StatusUnauthorized, rec.Code)
	})

	t.Run("invalid token format", func(t *testing.T) {
		authService, userService, _, classroomService := newTestServices(t)
		notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

		req := httptest.NewRequest(http.MethodGet, "/api/v1/users/me", nil)
		req.Header.Set("Authorization", "InvalidFormat")
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		require.Equal(t, http.StatusUnauthorized, rec.Code)
	})

	t.Run("invalid token", func(t *testing.T) {
		authService, userService, _, classroomService := newTestServices(t)
		notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

		req := httptest.NewRequest(http.MethodGet, "/api/v1/users/me", nil)
		req.Header.Set("Authorization", "Bearer invalid-token")
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		require.Equal(t, http.StatusUnauthorized, rec.Code)
	})
}

func TestCurrentUser_NoUser(t *testing.T) {
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	user := httpadapter.CurrentUser(c)
	require.Equal(t, "", user.ID)
	require.Equal(t, "", user.Email)
}

func TestRequireRole_Unauthorized(t *testing.T) {
	// Create a combined repo with both admin and teacher
	hash1, _ := bcrypt.GenerateFromPassword([]byte("admin123"), bcrypt.DefaultCost)
	hash2, _ := bcrypt.GenerateFromPassword([]byte("teacher123"), bcrypt.DefaultCost)

	combinedRepo := repo.NewMemoryUserRepository([]domain.User{
		{
			ID:             "admin-1",
			Email:          "admin@classsphere.edu",
			HashedPassword: string(hash1),
			Role:           domain.RoleAdmin,
			DisplayName:    "Admin",
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
		{
			ID:             "teacher-1",
			Email:          "teacher@classsphere.edu",
			HashedPassword: string(hash2),
			Role:           domain.RoleTeacher,
			DisplayName:    "Teacher",
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
	})

	cache := &inMemoryCache{store: make(map[string][]byte)}
	oauth := &staticOAuth{}
	cfg := shared.Config{
		JWTSecret:        "test-secret",
		JWTIssuer:        "classsphere",
		JWTExpiryMinutes: 60,
	}

	sharedAuthService, _ := app.NewAuthService(combinedRepo, cache, oauth, cfg)
	sharedUserService, _ := app.NewUserService(combinedRepo)
	classroomService := newStubClassroomService(t)

	ctx := context.Background()
	tokens, err := sharedAuthService.LoginWithPassword(ctx, "teacher@classsphere.edu", "teacher123")
	require.NoError(t, err)

	// Try to access admin endpoint with teacher token
	req := httptest.NewRequest(http.MethodGet, "/api/v1/admin/ping", nil)
	req.Header.Set("Authorization", "Bearer "+tokens.AccessToken)
	rec := httptest.NewRecorder()

	notificationHub := app.NewNotificationHub()
	e := httpadapter.New(sharedAuthService, sharedUserService, classroomService, notificationHub, newTestConfig())
	e.ServeHTTP(rec, req)

	require.Equal(t, http.StatusForbidden, rec.Code)
}

func TestOAuthCallback_Errors(t *testing.T) {
	authService, userService, _, classroomService := newTestServices(t)
	notificationHub := app.NewNotificationHub()
	router := httpadapter.New(authService, userService, classroomService, notificationHub, newTestConfig())

	t.Run("missing state", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/api/v1/auth/oauth/callback?code=test", nil)
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		require.Equal(t, http.StatusBadRequest, rec.Code)
	})

	t.Run("missing code", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/api/v1/auth/oauth/callback?state=test", nil)
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		// Missing code results in unauthorized because it can't complete OAuth
		require.True(t, rec.Code == http.StatusBadRequest || rec.Code == http.StatusUnauthorized)
	})

	t.Run("invalid state", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/api/v1/auth/oauth/callback?code=test&state=invalid", nil)
		rec := httptest.NewRecorder()

		router.ServeHTTP(rec, req)
		require.Equal(t, http.StatusUnauthorized, rec.Code)
	})
}
