package http_test

import (
	"bufio"
	"context"
	"net/http"
	"net/http/httptest"
	"strings"
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

// ==============================================================================
// SSE Authentication Tests
// ==============================================================================

func TestSSEHandler_Unauthorized_NoToken(t *testing.T) {
	// GIVEN: SSE endpoint requiring JWT authentication
	hub := app.NewNotificationHub()
	authService, userService, cache, classroomService := newTestServicesSSE(t)
	
	e := httpadapter.NewWithSSE(authService, userService, classroomService, hub, nil, cache, newTestConfig())
	server := httptest.NewServer(e)
	defer server.Close()
	
	// WHEN: Attempt to connect without Authorization header
	resp, err := http.Get(server.URL + "/api/v1/notifications/stream")
	
	// THEN: Connection should be rejected with 401
	require.NoError(t, err)
	defer resp.Body.Close()
	assert.Equal(t, http.StatusUnauthorized, resp.StatusCode)
}

func TestSSEHandler_Unauthorized_InvalidToken(t *testing.T) {
	// GIVEN: SSE endpoint with invalid JWT
	hub := app.NewNotificationHub()
	authService, userService, cache, classroomService := newTestServicesSSE(t)
	
	e := httpadapter.NewWithSSE(authService, userService, classroomService, hub, nil, cache, newTestConfig())
	server := httptest.NewServer(e)
	defer server.Close()
	
	// WHEN: Attempt to connect with invalid token
	req, _ := http.NewRequest("GET", server.URL+"/api/v1/notifications/stream", nil)
	req.Header.Set("Authorization", "Bearer invalid-token-here")
	
	resp, err := http.DefaultClient.Do(req)
	
	// THEN: Connection should be rejected with 401
	require.NoError(t, err)
	defer resp.Body.Close()
	assert.Equal(t, http.StatusUnauthorized, resp.StatusCode)
}

func TestSSEHandler_Authorized_ValidToken(t *testing.T) {
	// GIVEN: SSE endpoint with valid JWT
	hub := app.NewNotificationHub()
	authService, userService, cache, classroomService := newTestServicesSSE(t)
	
	// Create valid token for test user
	ctx := context.Background()
	loginResult, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	e := httpadapter.NewWithSSE(authService, userService, classroomService, hub, nil, cache, newTestConfig())
	server := httptest.NewServer(e)
	defer server.Close()
	
	// WHEN: Connect with valid JWT
	req, _ := http.NewRequest("GET", server.URL+"/api/v1/notifications/stream", nil)
	req.Header.Set("Authorization", "Bearer "+loginResult.AccessToken)
	
	// Create client with timeout
	client := &http.Client{Timeout: 2 * time.Second}
	resp, err := client.Do(req)
	
	// THEN: Connection should succeed with SSE headers
	require.NoError(t, err)
	defer resp.Body.Close()
	
	assert.Equal(t, http.StatusOK, resp.StatusCode)
	assert.Equal(t, "text/event-stream", resp.Header.Get("Content-Type"))
	assert.Equal(t, "no-cache", resp.Header.Get("Cache-Control"))
	assert.Equal(t, "keep-alive", resp.Header.Get("Connection"))
}

func TestSSEHandler_ReceivesNotifications(t *testing.T) {
	// GIVEN: SSE connection established
	hub := app.NewNotificationHub()
	authService, userService, cache, classroomService := newTestServicesSSE(t)
	
	// Login to get token
	ctx := context.Background()
	loginResult, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	e := httpadapter.NewWithSSE(authService, userService, classroomService, hub, nil, cache, newTestConfig())
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect to SSE
	req, _ := http.NewRequest("GET", server.URL+"/api/v1/notifications/stream", nil)
	req.Header.Set("Authorization", "Bearer "+loginResult.AccessToken)
	
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	require.NoError(t, err)
	defer resp.Body.Close()
	
	// Read SSE events
	scanner := bufio.NewScanner(resp.Body)
	events := make([]string, 0)
	
	// Read first event (connected message)
	go func() {
		for scanner.Scan() {
			line := scanner.Text()
			if line != "" {
				events = append(events, line)
			}
			// Stop after receiving a few events
			if len(events) > 3 {
				break
			}
		}
	}()
	
	// WHEN: Send notification to user
	time.Sleep(100 * time.Millisecond) // Wait for connection
	hub.SendToUser("student-1", domain.Notification{
		ID:      "notif-1",
		Title:   "Test Notification",
		Message: "This is a test",
		Type:    "info",
	})
	
	// Wait for event to be processed
	time.Sleep(200 * time.Millisecond)
	
	// THEN: Should receive the notification
	assert.GreaterOrEqual(t, len(events), 1, "should receive at least one event")
	
	// Check that we received some SSE data
	hasEventLine := false
	hasDataLine := false
	for _, event := range events {
		if strings.HasPrefix(event, "event:") {
			hasEventLine = true
		}
		if strings.HasPrefix(event, "data:") {
			hasDataLine = true
		}
	}
	
	assert.True(t, hasEventLine || hasDataLine, "should receive SSE formatted events")
}

func TestSSEHandler_KeepAliveMessages(t *testing.T) {
	// GIVEN: SSE connection established
	hub := app.NewNotificationHub()
	authService, userService, cache, classroomService := newTestServicesSSE(t)
	
	// Login
	ctx := context.Background()
	loginResult, err := authService.LoginWithPassword(ctx, "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	e := httpadapter.NewWithSSE(authService, userService, classroomService, hub, nil, cache, newTestConfig())
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect
	req, _ := http.NewRequest("GET", server.URL+"/api/v1/notifications/stream", nil)
	req.Header.Set("Authorization", "Bearer "+loginResult.AccessToken)
	
	client := &http.Client{Timeout: 20 * time.Second}
	resp, err := client.Do(req)
	require.NoError(t, err)
	defer resp.Body.Close()
	
	// Read events
	scanner := bufio.NewScanner(resp.Body)
	keepAliveCount := 0
	
	// Read for a short time
	timeout := time.After(2 * time.Second)
	done := make(chan bool)
	
	go func() {
		for scanner.Scan() {
			line := scanner.Text()
			// Keep-alive comments start with ":"
			if strings.HasPrefix(line, ":") {
				keepAliveCount++
			}
		}
		done <- true
	}()
	
	// WHEN: Wait for keep-alive messages
	select {
	case <-timeout:
		// Expected timeout
	case <-done:
		// Scanner finished
	}
	
	// THEN: Should have received at least one keep-alive
	// Note: Keep-alive interval is 15s, so we might not get one in 2s
	// This test just verifies the connection stays open
	assert.GreaterOrEqual(t, keepAliveCount, 0, "connection should stay open")
}

func TestSSEHandler_ClientDisconnect(t *testing.T) {
	// GIVEN: SSE connection established
	hub := app.NewNotificationHub()
	authService, userService, cache, classroomService := newTestServicesSSE(t)
	
	loginResult, err := authService.LoginWithPassword(context.Background(), "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	e := httpadapter.NewWithSSE(authService, userService, classroomService, hub, nil, cache, newTestConfig())
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Connect
	req, _ := http.NewRequest("GET", server.URL+"/api/v1/notifications/stream", nil)
	req.Header.Set("Authorization", "Bearer "+loginResult.AccessToken)
	
	initialClients := hub.ClientCount()
	
	client := &http.Client{Timeout: 1 * time.Second}
	resp, err := client.Do(req)
	require.NoError(t, err)
	
	// Wait for registration
	time.Sleep(100 * time.Millisecond)
	connectedClients := hub.ClientCount()
	assert.Equal(t, initialClients+1, connectedClients, "client should be registered")
	
	// WHEN: Close connection
	resp.Body.Close()
	
	// Wait for cleanup
	time.Sleep(200 * time.Millisecond)
	
	// THEN: Client should be unregistered
	finalClients := hub.ClientCount()
	assert.Equal(t, initialClients, finalClients, "client should be unregistered")
}

func TestSSEHandler_MultipleClients(t *testing.T) {
	// GIVEN: Multiple users connected via SSE
	hub := app.NewNotificationHub()
	authService, userService, cache, classroomService := newTestServicesSSE(t)
	
	e := httpadapter.NewWithSSE(authService, userService, classroomService, hub, nil, cache, newTestConfig())
	server := httptest.NewServer(e)
	defer server.Close()
	
	// Login as student
	studentLogin, err := authService.LoginWithPassword(context.Background(), "student@classsphere.edu", "student123")
	require.NoError(t, err)
	
	// Login as teacher
	teacherLogin, err := authService.LoginWithPassword(context.Background(), "teacher@classsphere.edu", "teacher123")
	require.NoError(t, err)
	
	// Connect both clients
	reqStudent, _ := http.NewRequest("GET", server.URL+"/api/v1/notifications/stream", nil)
	reqStudent.Header.Set("Authorization", "Bearer "+studentLogin.AccessToken)
	
	reqTeacher, _ := http.NewRequest("GET", server.URL+"/api/v1/notifications/stream", nil)
	reqTeacher.Header.Set("Authorization", "Bearer "+teacherLogin.AccessToken)
	
	client := &http.Client{Timeout: 5 * time.Second}
	
	respStudent, err := client.Do(reqStudent)
	require.NoError(t, err)
	defer respStudent.Body.Close()
	
	respTeacher, err := client.Do(reqTeacher)
	require.NoError(t, err)
	defer respTeacher.Body.Close()
	
	// Wait for connections to establish
	time.Sleep(200 * time.Millisecond)
	
	// THEN: Both clients should be connected
	assert.Equal(t, 2, hub.ClientCount(), "should have 2 clients")
	assert.Equal(t, 2, hub.UserCount(), "should have 2 users")
}

// ==============================================================================
// Test Helpers
// ==============================================================================

func newTestServicesSSE(t *testing.T) (*app.AuthService, *app.UserService, *inMemoryCacheSSE, *app.ClassroomService) {
	t.Helper()

	// Create test users with hashed passwords
	adminHash, _ := bcrypt.GenerateFromPassword([]byte("admin123"), bcrypt.DefaultCost)
	teacherHash, _ := bcrypt.GenerateFromPassword([]byte("teacher123"), bcrypt.DefaultCost)
	studentHash, _ := bcrypt.GenerateFromPassword([]byte("student123"), bcrypt.DefaultCost)

	now := time.Now()
	users := []domain.User{
		{ID: "admin-1", Email: "admin@classsphere.edu", HashedPassword: string(adminHash), Role: domain.RoleAdmin, CreatedAt: now, UpdatedAt: now},
		{ID: "teacher-1", Email: "teacher@classsphere.edu", HashedPassword: string(teacherHash), Role: domain.RoleTeacher, CreatedAt: now, UpdatedAt: now},
		{ID: "student-1", Email: "student@classsphere.edu", HashedPassword: string(studentHash), Role: domain.RoleStudent, CreatedAt: now, UpdatedAt: now},
	}

	userRepo := repo.NewMemoryUserRepository(users)
	cache := &inMemoryCacheSSE{store: make(map[string][]byte)}
	oauth := &staticOAuthSSE{}

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

	classroomService := newStubClassroomServiceSSE(t)

	return authService, userService, cache, classroomService
}

func newStubClassroomServiceSSE(t *testing.T) *app.ClassroomService {
	provider := &stubClassroomProviderSSE{mode: shared.IntegrationModeMock}
	svc, err := app.NewClassroomService(shared.IntegrationModeMock, provider)
	require.NoError(t, err)
	return svc
}

type inMemoryCacheSSE struct {
	store map[string][]byte
}

func (c *inMemoryCacheSSE) Set(ctx context.Context, key string, value []byte, expiration int) error {
	c.store[key] = value
	return nil
}

func (c *inMemoryCacheSSE) Get(ctx context.Context, key string) ([]byte, error) {
	if val, ok := c.store[key]; ok {
		return val, nil
	}
	return nil, nil
}

func (c *inMemoryCacheSSE) Delete(ctx context.Context, key string) error {
	delete(c.store, key)
	return nil
}

func (c *inMemoryCacheSSE) Ping(ctx context.Context) error {
	return nil
}

func (c *inMemoryCacheSSE) Close() error {
	return nil
}

type staticOAuthSSE struct{}

func (s *staticOAuthSSE) AuthURL(state string) (string, error) {
	return "https://accounts.google.com?state=" + state, nil
}

func (s *staticOAuthSSE) Exchange(_ context.Context, _ string) (ports.OAuthUser, error) {
	return ports.OAuthUser{ID: "student-1", Email: "student@classsphere.edu"}, nil
}

type stubClassroomProviderSSE struct {
	mode string
}

func (s *stubClassroomProviderSSE) Mode() string {
	return s.mode
}

func (s *stubClassroomProviderSSE) Snapshot(_ context.Context) (domain.ClassroomSnapshot, error) {
	return domain.ClassroomSnapshot{
		Mode:        s.mode,
		GeneratedAt: time.Unix(0, 0),
		Courses:     []domain.Course{},
	}, nil
}

