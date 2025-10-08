package http

import (
	"context"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/gorilla/websocket"
	echo "github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"golang.org/x/crypto/bcrypt"

	"github.com/lbrines/classsphere/internal/adapters/repo"
	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

// ==============================================================================
// WebSocket JWT Authentication Tests
// All WebSocket tests now require JWT authentication for security
// ==============================================================================

// TestWebSocketHandler_Unauthorized_NoToken tests that connection is rejected without JWT
func TestWebSocketHandler_Unauthorized_NoToken(t *testing.T) {
	// GIVEN: WebSocket endpoint requiring JWT authentication
	hub := app.NewNotificationHub()
	authService, userService, _, classroomService := newTestServicesWebSocket(t)
	
	handler := &Handler{
		authService:      authService,
		userService:      userService,
		classroomService: classroomService,
		notificationHub:  hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	
	// WHEN: Attempt to connect without Authorization header
	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, nil)
	
	// THEN: Connection should be rejected with 401
	require.Error(t, err)
	assert.Equal(t, http.StatusUnauthorized, resp.StatusCode)
	if ws != nil {
		ws.Close()
	}
}

// TestWebSocketHandler_Unauthorized_InvalidToken tests rejection of invalid JWT
func TestWebSocketHandler_Unauthorized_InvalidToken(t *testing.T) {
	// GIVEN: WebSocket endpoint with auth middleware
	hub := app.NewNotificationHub()
	authService, userService, _, classroomService := newTestServicesWebSocket(t)
	
	handler := &Handler{
		authService:      authService,
		userService:      userService,
		classroomService: classroomService,
		notificationHub:  hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	
	// WHEN: Attempt to connect with invalid token
	headers := http.Header{}
	headers.Set("Authorization", "Bearer invalid-token-12345")
	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, headers)
	
	// THEN: Connection should be rejected
	require.Error(t, err)
	assert.Equal(t, http.StatusUnauthorized, resp.StatusCode)
	if ws != nil {
		ws.Close()
	}
}

// TestWebSocketHandler_Authorized_ValidToken tests acceptance of valid JWT
func TestWebSocketHandler_Authorized_ValidToken(t *testing.T) {
	// GIVEN: WebSocket endpoint with valid JWT
	hub := app.NewNotificationHub()
	authService, userService, _, classroomService := newTestServicesWebSocket(t)
	
	// Create valid token for test user
	ctx := context.Background()
	loginResult, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	handler := &Handler{
		authService:      authService,
		userService:      userService,
		classroomService: classroomService,
		notificationHub:  hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	
	// WHEN: Connect with valid JWT
	headers := http.Header{}
	headers.Set("Authorization", "Bearer "+loginResult.AccessToken)
	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, headers)
	
	// THEN: Connection should succeed
	require.NoError(t, err)
	assert.Equal(t, http.StatusSwitchingProtocols, resp.StatusCode)
	
	// Cleanup
	if ws != nil {
		ws.Close()
	}
}

// TestWebSocketHandler_ExtractsUserFromJWT tests user extraction from JWT context
func TestWebSocketHandler_ExtractsUserFromJWT(t *testing.T) {
	// GIVEN: Authenticated WebSocket connection
	hub := app.NewNotificationHub()
	authService, userService, _, classroomService := newTestServicesWebSocket(t)
	
	// Login to get valid token
	ctx := context.Background()
	loginResult, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	handler := &Handler{
		authService:      authService,
		userService:      userService,
		classroomService: classroomService,
		notificationHub:  hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	headers := http.Header{}
	headers.Set("Authorization", "Bearer "+loginResult.AccessToken)
	
	// WHEN: Connect and verify user registration
	ws, _, err := websocket.DefaultDialer.Dial(wsURL, headers)
	require.NoError(t, err)
	defer ws.Close()
	
	time.Sleep(100 * time.Millisecond) // Wait for registration
	
	// THEN: User should be registered with correct ID from JWT
	assert.Greater(t, hub.ClientCount(), 0, "Client should be registered")
	
	// Send user-specific notification
	notification := domain.Notification{
		ID:      "test-notif-1",
		UserID:  "student-1",
		Type:    "info",
		Title:   "Test",
		Message: "For student",
	}
	
	hub.SendToUser("student-1", notification)
	
	// User should receive the notification
	ws.SetReadDeadline(time.Now().Add(2 * time.Second))
	var received domain.Notification
	err = ws.ReadJSON(&received)
	require.NoError(t, err)
	assert.Equal(t, "test-notif-1", received.ID)
}

// newTestServicesWebSocket creates test services with student user for WebSocket tests
func newTestServicesWebSocket(t *testing.T) (*app.AuthService, *app.UserService, *inMemoryCache, *app.ClassroomService) {
	t.Helper()
	
	// Create test users with hashed passwords
	adminHash, err := bcrypt.GenerateFromPassword([]byte("admin123"), bcrypt.DefaultCost)
	require.NoError(t, err)
	studentHash, err := bcrypt.GenerateFromPassword([]byte("student123"), bcrypt.DefaultCost)
	require.NoError(t, err)
	
	repository := repo.NewMemoryUserRepository([]domain.User{
		{
			ID:             "admin-1",
			Email:          "admin@classsphere.edu",
			HashedPassword: string(adminHash),
			Role:           domain.RoleAdmin,
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
		{
			ID:             "student-1",
			Email:          "student@classsphere.edu",
			HashedPassword: string(studentHash),
			Role:           domain.RoleStudent,
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
	})
	
	cache := &inMemoryCache{store: make(map[string][]byte)}
	oauth := &staticOAuth{}
	
	cfg := shared.Config{
		JWTSecret:          "test-secret-websocket",
		JWTIssuer:          "classsphere",
		JWTExpiryMinutes:   60,
		GoogleClientID:     "client",
		GoogleClientSecret: "secret",
		GoogleRedirectURL:  "http://localhost/callback",
	}
	
	authService, err := app.NewAuthService(repository, cache, oauth, cfg)
	require.NoError(t, err)
	userService, err := app.NewUserService(repository)
	require.NoError(t, err)
	
	classroomService := newStubClassroomService(t)
	
	return authService, userService, cache, classroomService
}

// Test stubs for WebSocket tests

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

func newStubClassroomService(t *testing.T) *app.ClassroomService {
	provider := &stubClassroomProvider{mode: shared.IntegrationModeMock}
	svc, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	svc.WithClock(func() time.Time { return time.Unix(0, 0) })
	return svc
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
		Courses:     []domain.Course{},
	}, nil
}

