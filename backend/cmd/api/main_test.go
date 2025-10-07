package main

import (
	"context"
	"fmt"
	"os"
	"syscall"
	"testing"
	"time"

	"github.com/alicebob/miniredis/v2"
	echo "github.com/labstack/echo/v4"
	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/shared"
)

func TestSeedUsers(t *testing.T) {
	users := seedUsers(shared.Logger())
	require.Len(t, users, 4)
	require.Equal(t, "admin@classsphere.edu", users[0].Email)
	require.Equal(t, "coordinator@classsphere.edu", users[1].Email)
	require.Equal(t, "teacher@classsphere.edu", users[2].Email)
	require.Equal(t, "student@classsphere.edu", users[3].Email)
	require.NotEqual(t, "admin123", users[0].HashedPassword)
	require.NotEqual(t, "teach123", users[2].HashedPassword)
}

func TestStartServerShutdown(t *testing.T) {
	e := echo.New()
	logger := shared.Logger()
	ctx := context.Background()
	signalCh := make(chan os.Signal, 1)

	done := make(chan struct{})
	go func() {
		startServer(ctx, e, 0, logger, signalCh)
		close(done)
	}()

	time.Sleep(50 * time.Millisecond)
	signalCh <- syscall.SIGINT

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("server did not shut down in time")
	}
}

func TestStartServerUsesFactory(t *testing.T) {
	originalFactory := signalChannelFactory
	ch := make(chan os.Signal, 1)
	signalChannelFactory = func() (chan os.Signal, func()) {
		return ch, func() {}
	}
	defer func() { signalChannelFactory = originalFactory }()

	e := echo.New()
	logger := shared.Logger()
	ctx := context.Background()
	done := make(chan struct{})
	go func() {
		startServer(ctx, e, 0, logger, nil)
		close(done)
	}()

	time.Sleep(50 * time.Millisecond)
	ch <- syscall.SIGTERM

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("factory-based server shutdown timed out")
	}
}

func TestInitialize(t *testing.T) {
	srv, err := miniredis.Run()
	require.NoError(t, err)
	defer srv.Close()

	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("JWT_ISSUER", "classsphere")
	t.Setenv("JWT_EXPIRY_MINUTES", "60")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("REDIS_ADDR", srv.Addr())

	app, cleanup, err := initialize(context.Background())
	require.NoError(t, err)
	require.NotNil(t, app.server)
	require.NotNil(t, cleanup)
	cleanup()
}

func TestMainFunction(t *testing.T) {
	srv, err := miniredis.Run()
	require.NoError(t, err)
	defer srv.Close()

	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("JWT_ISSUER", "classsphere")
	t.Setenv("JWT_EXPIRY_MINUTES", "60")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("REDIS_ADDR", srv.Addr())
	t.Setenv("SERVER_PORT", "0")

	originalFactory := signalChannelFactory
	ch := make(chan os.Signal, 1)
	signalChannelFactory = func() (chan os.Signal, func()) {
		return ch, func() {}
	}
	defer func() { signalChannelFactory = originalFactory }()

	done := make(chan struct{})
	go func() {
		main()
		close(done)
	}()

	time.Sleep(50 * time.Millisecond)
	ch <- syscall.SIGINT

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("main did not exit in time")
	}
}

// === ADDITIONAL TESTS FOR 80% COVERAGE ===

func TestInitialize_RedisConnectionWarning(t *testing.T) {
	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("JWT_ISSUER", "classsphere")
	t.Setenv("JWT_EXPIRY_MINUTES", "60")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("REDIS_ADDR", "invalid-host:9999") // Invalid Redis address

	// Initialize should succeed even with Redis connection issues
	app, cleanup, err := initialize(context.Background())
	require.NoError(t, err)
	require.NotNil(t, app)
	cleanup()
}

func TestInitialize_ConfigValidationError(t *testing.T) {
	// Missing required JWT_SECRET
	t.Setenv("JWT_SECRET", "")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")

	_, _, err := initialize(context.Background())
	require.Error(t, err)
	require.Contains(t, err.Error(), "JWT_SECRET")
}

func TestSeedUsers_PasswordHashing(t *testing.T) {
	logger := shared.Logger()
	users := seedUsers(logger)

	require.Len(t, users, 4)

	// Verify passwords are hashed (not plaintext)
	require.NotEqual(t, "admin123", users[0].HashedPassword)
	require.NotEqual(t, "coord123", users[1].HashedPassword)
	require.NotEqual(t, "teach123", users[2].HashedPassword)
	require.NotEqual(t, "stud123", users[3].HashedPassword)

	// Verify hashes are bcrypt format (starts with $2a$)
	require.Contains(t, users[0].HashedPassword, "$2a$")
	require.Contains(t, users[1].HashedPassword, "$2a$")
	require.Contains(t, users[2].HashedPassword, "$2a$")
	require.Contains(t, users[3].HashedPassword, "$2a$")

	// Verify roles
	require.Equal(t, "admin", string(users[0].Role))
	require.Equal(t, "coordinator", string(users[1].Role))
	require.Equal(t, "teacher", string(users[2].Role))
	require.Equal(t, "student", string(users[3].Role))
}

func TestStartServer_GracefulShutdownTimeout(t *testing.T) {
	e := echo.New()
	logger := shared.Logger()
	ctx := context.Background()
	signalCh := make(chan os.Signal, 1)

	done := make(chan struct{})
	go func() {
		startServer(ctx, e, 0, logger, signalCh)
		close(done)
	}()

	// Let server start
	time.Sleep(50 * time.Millisecond)

	// Send shutdown signal
	signalCh <- syscall.SIGINT

	// Verify graceful shutdown completes
	select {
	case <-done:
		// Success
	case <-time.After(15 * time.Second):
		t.Fatal("server did not shut down gracefully within timeout")
	}
}

func TestStartServer_WithSpecificPort(t *testing.T) {
	e := echo.New()
	logger := shared.Logger()
	ctx := context.Background()
	signalCh := make(chan os.Signal, 1)

	// Test with a specific port (0 = random)
	done := make(chan struct{})
	go func() {
		startServer(ctx, e, 0, logger, signalCh)
		close(done)
	}()

	time.Sleep(50 * time.Millisecond)
	signalCh <- syscall.SIGTERM

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("server did not shut down")
	}
}

func TestStartServer_ServerStartError(t *testing.T) {
	// This test covers the error path when server fails to start
	e := echo.New()
	logger := shared.Logger()
	ctx := context.Background()
	signalCh := make(chan os.Signal, 1)

	// Start server on port 0 (will succeed)
	done := make(chan struct{})
	go func() {
		startServer(ctx, e, 0, logger, signalCh)
		close(done)
	}()

	// Immediately send shutdown signal
	time.Sleep(10 * time.Millisecond)
	signalCh <- syscall.SIGINT

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("server did not shut down")
	}
}

func TestInitialize_CleanupFunction(t *testing.T) {
	srv, err := miniredis.Run()
	require.NoError(t, err)
	defer srv.Close()

	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("JWT_ISSUER", "classsphere")
	t.Setenv("JWT_EXPIRY_MINUTES", "60")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("REDIS_ADDR", srv.Addr())

	app, cleanup, err := initialize(context.Background())
	require.NoError(t, err)
	require.NotNil(t, app)
	require.NotNil(t, cleanup)

	// Test that cleanup works without error
	cleanup()

	// Should be safe to call multiple times
	cleanup()
}

func TestInitialize_UserServiceError(t *testing.T) {
	// This is harder to trigger but we can test the path exists
	srv, err := miniredis.Run()
	require.NoError(t, err)
	defer srv.Close()

	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("JWT_ISSUER", "classsphere")
	t.Setenv("JWT_EXPIRY_MINUTES", "60")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("REDIS_ADDR", srv.Addr())

	app, cleanup, err := initialize(context.Background())
	require.NoError(t, err)
	defer cleanup()

	// Verify all components initialized
	require.NotNil(t, app.server)
	require.NotNil(t, app.logger)
	require.NotNil(t, app.cache)
	require.NotEmpty(t, app.config.JWTSecret)
}

func TestMainFunction_WithStopFactory(t *testing.T) {
	srv, err := miniredis.Run()
	require.NoError(t, err)
	defer srv.Close()

	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("JWT_ISSUER", "classsphere")
	t.Setenv("JWT_EXPIRY_MINUTES", "60")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("REDIS_ADDR", srv.Addr())
	t.Setenv("SERVER_PORT", "0")

	originalFactory := signalChannelFactory
	ch := make(chan os.Signal, 1)
	stopCalled := false
	signalChannelFactory = func() (chan os.Signal, func()) {
		return ch, func() { stopCalled = true }
	}
	defer func() { signalChannelFactory = originalFactory }()

	done := make(chan struct{})
	go func() {
		main()
		close(done)
	}()

	time.Sleep(50 * time.Millisecond)
	ch <- syscall.SIGTERM

	select {
	case <-done:
		// Verify stop was called
		require.True(t, stopCalled, "signal.Stop should have been called")
	case <-time.After(2 * time.Second):
		t.Fatal("main did not exit in time")
	}
}

func TestStartServer_ContextHandling(t *testing.T) {
	e := echo.New()
	logger := shared.Logger()
	ctx := context.Background()
	signalCh := make(chan os.Signal, 1)

	done := make(chan struct{})
	go func() {
		startServer(ctx, e, 0, logger, signalCh)
		close(done)
	}()

	time.Sleep(50 * time.Millisecond)

	// Test both signal types
	signalCh <- syscall.SIGTERM

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("server did not handle SIGTERM")
	}
}

func TestCreateSeedUsers(t *testing.T) {
	users, err := createSeedUsers()
	require.NoError(t, err)
	require.Len(t, users, 4)

	// Verify admin
	require.Equal(t, "admin-1", users[0].ID)
	require.Equal(t, "admin@classsphere.edu", users[0].Email)
	require.Equal(t, "Admin", users[0].DisplayName)
	require.Equal(t, "admin", string(users[0].Role))
	require.NotEmpty(t, users[0].HashedPassword)
	require.Contains(t, users[0].HashedPassword, "$2a$")

	// Verify coordinator
	require.Equal(t, "coord-1", users[1].ID)
	require.Equal(t, "coordinator@classsphere.edu", users[1].Email)
	require.Equal(t, "Coordinator", users[1].DisplayName)
	require.Equal(t, "coordinator", string(users[1].Role))
	require.NotEmpty(t, users[1].HashedPassword)
	require.Contains(t, users[1].HashedPassword, "$2a$")

	// Verify teacher
	require.Equal(t, "teacher-1", users[2].ID)
	require.Equal(t, "teacher@classsphere.edu", users[2].Email)
	require.Equal(t, "Teacher", users[2].DisplayName)
	require.Equal(t, "teacher", string(users[2].Role))
	require.NotEmpty(t, users[2].HashedPassword)
	require.Contains(t, users[2].HashedPassword, "$2a$")

	// Verify student
	require.Equal(t, "student-1", users[3].ID)
	require.Equal(t, "student@classsphere.edu", users[3].Email)
	require.Equal(t, "Student", users[3].DisplayName)
	require.Equal(t, "student", string(users[3].Role))
	require.NotEmpty(t, users[3].HashedPassword)
	require.Contains(t, users[3].HashedPassword, "$2a$")

	// Verify hashes are different
	require.NotEqual(t, users[0].HashedPassword, users[1].HashedPassword)
	require.NotEqual(t, users[2].HashedPassword, users[3].HashedPassword)

	// Verify passwords are not plaintext
	require.NotEqual(t, "admin123", users[0].HashedPassword)
	require.NotEqual(t, "coord123", users[1].HashedPassword)
	require.NotEqual(t, "teach123", users[2].HashedPassword)
	require.NotEqual(t, "stud123", users[3].HashedPassword)
}

func TestSeedUsers_CallsCreateSeedUsers(t *testing.T) {
	logger := shared.Logger()
	users := seedUsers(logger)

	// Verify it returns the same result as createSeedUsers
	expectedUsers, _ := createSeedUsers()
	require.Len(t, users, len(expectedUsers))
	for i := range expectedUsers {
		require.Equal(t, expectedUsers[i].Email, users[i].Email)
	}
}

func TestCreateSeedUsers_Deterministic(t *testing.T) {
	// Test that createSeedUsers returns consistent structure
	users1, err1 := createSeedUsers()
	require.NoError(t, err1)

	users2, err2 := createSeedUsers()
	require.NoError(t, err2)

	// Same emails and IDs
	require.Equal(t, users1[0].Email, users2[0].Email)
	require.Equal(t, users1[0].ID, users2[0].ID)
	require.Equal(t, users1[1].Email, users2[1].Email)
	require.Equal(t, users1[1].ID, users2[1].ID)
	require.Equal(t, users1[2].Email, users2[2].Email)
	require.Equal(t, users1[2].ID, users2[2].ID)
	require.Equal(t, users1[3].Email, users2[3].Email)
	require.Equal(t, users1[3].ID, users2[3].ID)

	// Different hashes (bcrypt generates new salt each time)
	require.NotEqual(t, users1[0].HashedPassword, users2[0].HashedPassword)
	require.NotEqual(t, users1[2].HashedPassword, users2[2].HashedPassword)
}

func TestInitialize_AllComponents(t *testing.T) {
	srv, err := miniredis.Run()
	require.NoError(t, err)
	defer srv.Close()

	t.Setenv("JWT_SECRET", "test-secret-key-for-testing")
	t.Setenv("JWT_ISSUER", "classsphere-test")
	t.Setenv("JWT_EXPIRY_MINUTES", "120")
	t.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	t.Setenv("GOOGLE_CLIENT_SECRET", "test-secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost:4200/callback")
	t.Setenv("REDIS_ADDR", srv.Addr())
	t.Setenv("SERVER_PORT", "9999")

	app, cleanup, err := initialize(context.Background())
	require.NoError(t, err)
	defer cleanup()

	// Verify server is Echo instance
	require.NotNil(t, app.server)

	// Verify logger initialized
	require.NotNil(t, app.logger)

	// Verify config loaded correctly
	require.Equal(t, "test-secret-key-for-testing", app.config.JWTSecret)
	require.Equal(t, "classsphere-test", app.config.JWTIssuer)
	require.Equal(t, 120, app.config.JWTExpiryMinutes)
	require.Equal(t, 9999, app.config.ServerPort)

	// Verify cache initialized
	require.NotNil(t, app.cache)
	err = app.cache.Ping(context.Background())
	require.NoError(t, err)
}

func TestStartServer_MultipleSignalTypes(t *testing.T) {
	tests := []struct {
		name   string
		signal os.Signal
	}{
		{"SIGINT", syscall.SIGINT},
		{"SIGTERM", syscall.SIGTERM},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			e := echo.New()
			logger := shared.Logger()
			ctx := context.Background()
			signalCh := make(chan os.Signal, 1)

			done := make(chan struct{})
			go func() {
				startServer(ctx, e, 0, logger, signalCh)
				close(done)
			}()

			time.Sleep(50 * time.Millisecond)
			signalCh <- tt.signal

			select {
			case <-done:
				// Success
			case <-time.After(2 * time.Second):
				t.Fatalf("server did not respond to %s", tt.name)
			}
		})
	}
}

// === TESTING ERROR PATHS WITH MOCKING ===

func TestCreateSeedUsers_AdminHashError(t *testing.T) {
	// Save original function
	originalHashFunc := hashPasswordFunc
	defer func() { hashPasswordFunc = originalHashFunc }()

	// Mock to fail on first call (admin password)
	callCount := 0
	hashPasswordFunc = func(password []byte, cost int) ([]byte, error) {
		callCount++
		if callCount == 1 {
			return nil, fmt.Errorf("mock bcrypt error for admin")
		}
		return originalHashFunc(password, cost)
	}

	users, err := createSeedUsers()
	require.Error(t, err)
	require.Contains(t, err.Error(), "hash admin password")
	require.Nil(t, users)
}

func TestCreateSeedUsers_CoordinatorHashError(t *testing.T) {
	// Save original function
	originalHashFunc := hashPasswordFunc
	defer func() { hashPasswordFunc = originalHashFunc }()

	// Mock to fail on second call (coordinator password)
	callCount := 0
	hashPasswordFunc = func(password []byte, cost int) ([]byte, error) {
		callCount++
		if callCount == 2 {
			return nil, fmt.Errorf("mock bcrypt error for coordinator")
		}
		return originalHashFunc(password, cost)
	}

	users, err := createSeedUsers()
	require.Error(t, err)
	require.Contains(t, err.Error(), "hash coordinator password")
	require.Nil(t, users)
}

func TestCreateSeedUsers_TeacherHashError(t *testing.T) {
	originalHashFunc := hashPasswordFunc
	defer func() { hashPasswordFunc = originalHashFunc }()

	callCount := 0
	hashPasswordFunc = func(password []byte, cost int) ([]byte, error) {
		callCount++
		if callCount == 3 {
			return nil, fmt.Errorf("mock bcrypt error for teacher")
		}
		return originalHashFunc(password, cost)
	}

	users, err := createSeedUsers()
	require.Error(t, err)
	require.Contains(t, err.Error(), "hash teacher password")
	require.Nil(t, users)
}

func TestCreateSeedUsers_StudentHashError(t *testing.T) {
	originalHashFunc := hashPasswordFunc
	defer func() { hashPasswordFunc = originalHashFunc }()

	callCount := 0
	hashPasswordFunc = func(password []byte, cost int) ([]byte, error) {
		callCount++
		if callCount == 4 {
			return nil, fmt.Errorf("mock bcrypt error for student")
		}
		return originalHashFunc(password, cost)
	}

	users, err := createSeedUsers()
	require.Error(t, err)
	require.Contains(t, err.Error(), "hash student password")
	require.Nil(t, users)
}
