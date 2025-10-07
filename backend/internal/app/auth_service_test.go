package app_test

import (
	"context"
	"testing"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"golang.org/x/crypto/bcrypt"

	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

func TestLoginWithPassword(t *testing.T) {
	ctx := context.Background()

	hash, err := bcrypt.GenerateFromPassword([]byte("secret"), bcrypt.DefaultCost)
	require.NoError(t, err)

	repo := newFakeRepo()
	repo.upsert(domain.User{
		ID:             "user-1",
		Email:          "user@test.com",
		HashedPassword: string(hash),
		Role:           domain.RoleTeacher,
	})

	cache := newFakeCache()
	oauth := &fakeOAuth{
		authURL: "https://auth",
		user: ports.OAuthUser{
			ID:    "oauth-1",
			Email: "user@test.com",
		},
	}

	cfg := shared.Config{
		JWTSecret:          "test-secret",
		JWTIssuer:          "classsphere",
		JWTExpiryMinutes:   60,
		GoogleClientID:     "client",
		GoogleClientSecret: "secret",
		GoogleRedirectURL:  "http://localhost/callback",
	}

	service, err := app.NewAuthService(repo, cache, oauth, cfg)
	require.NoError(t, err)

	result, err := service.LoginWithPassword(ctx, "user@test.com", "secret")
	require.NoError(t, err)

	assert.NotEmpty(t, result.AccessToken)
	assert.Equal(t, "user-1", result.User.ID)

	_, err = service.LoginWithPassword(ctx, "user@test.com", "wrong")
	assert.Error(t, err)
}

func TestOAuthFlow(t *testing.T) {
	ctx := context.Background()
	repo := newFakeRepo()
	cache := newFakeCache()
	oauth := &fakeOAuth{
		authURL: "https://accounts.google.com",
		user: ports.OAuthUser{
			ID:          "oauth-1",
			Email:       "new@test.com",
			DisplayName: "OAuth User",
		},
	}

	cfg := shared.Config{
		JWTSecret:          "test-secret",
		JWTIssuer:          "classsphere",
		JWTExpiryMinutes:   60,
		GoogleClientID:     "client",
		GoogleClientSecret: "secret",
		GoogleRedirectURL:  "http://localhost/callback",
	}

	service, err := app.NewAuthService(repo, cache, oauth, cfg)
	require.NoError(t, err)
	fixedNow := time.Now().Add(-time.Minute)
	service.SetNowFunc(func() time.Time { return fixedNow })

	state, url, err := service.StartOAuth(ctx)
	require.NoError(t, err)
	assert.NotEmpty(t, state)
	assert.Equal(t, oauth.authURL, url)
	require.Contains(t, cache.data, "oauth_state:"+state)
	require.NotNil(t, cache.data["oauth_state:"+state])
	value, err := cache.Get(ctx, "oauth_state:"+state)
	require.NoError(t, err)
	require.NotEmpty(t, value)
	cache.lastGetKey = ""
	result, err := service.CompleteOAuth(ctx, "code", state)
	if err != nil {
		t.Fatalf("CompleteOAuth error: %v, cache key: %s, keys: %v", err, cache.lastGetKey, cache.keys())
	}
	assert.Equal(t, "oauth-1", result.User.ID)

	user, err := service.ValidateToken(ctx, result.AccessToken)
	require.NoError(t, err)
	assert.Equal(t, result.User.ID, user.ID)
}

// Helpers

type fakeRepo struct {
	users map[string]domain.User
}

func newFakeRepo() *fakeRepo {
	return &fakeRepo{users: make(map[string]domain.User)}
}

func (f *fakeRepo) FindByEmail(_ context.Context, email string) (domain.User, error) {
	for _, u := range f.users {
		if u.Email == email {
			return u, nil
		}
	}
	return domain.User{}, shared.ErrUserNotFound
}

func (f *fakeRepo) FindByID(_ context.Context, id string) (domain.User, error) {
	if user, ok := f.users[id]; ok {
		return user, nil
	}
	return domain.User{}, shared.ErrUserNotFound
}

func (f *fakeRepo) Upsert(_ context.Context, user domain.User) error {
	f.users[user.ID] = user
	return nil
}

func (f *fakeRepo) upsert(user domain.User) {
	f.users[user.ID] = user
}

type fakeCache struct {
	data       map[string][]byte
	lastGetKey string
}

func newFakeCache() *fakeCache {
	return &fakeCache{data: make(map[string][]byte)}
}

func (f *fakeCache) Set(_ context.Context, key string, value []byte, _ int) error {
	f.data[key] = value
	return nil
}

func (f *fakeCache) Get(_ context.Context, key string) ([]byte, error) {
	f.lastGetKey = key
	return f.data[key], nil
}

func (f *fakeCache) Delete(_ context.Context, key string) error {
	delete(f.data, key)
	return nil
}

func (f *fakeCache) Ping(_ context.Context) error {
	return nil
}

func (f *fakeCache) Close() error {
	return nil
}

func (f *fakeCache) keys() []string {
	keys := make([]string, 0, len(f.data))
	for k := range f.data {
		keys = append(keys, k)
	}
	return keys
}

type fakeOAuth struct {
	authURL string
	user    ports.OAuthUser
}

func (f *fakeOAuth) AuthURL(state string) (string, error) {
	if state == "" {
		return "", assert.AnError
	}
	return f.authURL, nil
}

func (f *fakeOAuth) Exchange(_ context.Context, _ string) (ports.OAuthUser, error) {
	return f.user, nil
}

// === ADDITIONAL TESTS FOR 90% COVERAGE ===

// TestNewAuthService_Validation tests parameter validation
func TestNewAuthService_Validation(t *testing.T) {
	cfg := shared.Config{
		JWTSecret:        "test-secret",
		JWTIssuer:        "classsphere",
		JWTExpiryMinutes: 60,
	}

	t.Run("nil repository", func(t *testing.T) {
		_, err := app.NewAuthService(nil, newFakeCache(), &fakeOAuth{}, cfg)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "users repository is required")
	})

	t.Run("nil cache", func(t *testing.T) {
		_, err := app.NewAuthService(newFakeRepo(), nil, &fakeOAuth{}, cfg)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "cache is required")
	})

	t.Run("nil oauth", func(t *testing.T) {
		_, err := app.NewAuthService(newFakeRepo(), newFakeCache(), nil, cfg)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "oauth provider is required")
	})

	t.Run("valid parameters", func(t *testing.T) {
		svc, err := app.NewAuthService(newFakeRepo(), newFakeCache(), &fakeOAuth{}, cfg)
		assert.NoError(t, err)
		assert.NotNil(t, svc)
	})
}

// TestLoginWithPassword_UserNotFound tests login with non-existent user
func TestLoginWithPassword_UserNotFound(t *testing.T) {
	ctx := context.Background()
	cfg := shared.Config{
		JWTSecret:        "test-secret",
		JWTIssuer:        "classsphere",
		JWTExpiryMinutes: 60,
	}

	service, err := app.NewAuthService(newFakeRepo(), newFakeCache(), &fakeOAuth{}, cfg)
	require.NoError(t, err)

	_, err = service.LoginWithPassword(ctx, "nonexistent@test.com", "password")
	assert.Error(t, err)
	assert.Equal(t, shared.ErrInvalidCredentials, err)
}

// TestStartOAuth_Errors tests error scenarios in OAuth initialization
func TestStartOAuth_Errors(t *testing.T) {
	ctx := context.Background()
	cfg := shared.Config{
		JWTSecret:        "test-secret",
		JWTIssuer:        "classsphere",
		JWTExpiryMinutes: 60,
	}

	t.Run("cache set error", func(t *testing.T) {
		cache := &fakeCacheWithErrors{setError: assert.AnError}
		oauth := &fakeOAuth{authURL: "https://auth"}
		
		service, err := app.NewAuthService(newFakeRepo(), cache, oauth, cfg)
		require.NoError(t, err)

		_, _, err = service.StartOAuth(ctx)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "store oauth state")
	})

	t.Run("oauth authURL error", func(t *testing.T) {
		oauth := &fakeOAuthWithErrors{authURLError: assert.AnError}
		
		service, err := app.NewAuthService(newFakeRepo(), newFakeCache(), oauth, cfg)
		require.NoError(t, err)

		_, _, err = service.StartOAuth(ctx)
		assert.Error(t, err)
	})
}

// TestCompleteOAuth_Errors tests error scenarios in OAuth callback
func TestCompleteOAuth_Errors(t *testing.T) {
	ctx := context.Background()
	cfg := shared.Config{
		JWTSecret:        "test-secret",
		JWTIssuer:        "classsphere",
		JWTExpiryMinutes: 60,
	}

	t.Run("empty state", func(t *testing.T) {
		service, err := app.NewAuthService(newFakeRepo(), newFakeCache(), &fakeOAuth{}, cfg)
		require.NoError(t, err)

		_, err = service.CompleteOAuth(ctx, "code", "")
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "state is required")
	})

	t.Run("invalid state not in cache", func(t *testing.T) {
		cache := newFakeCache()
		service, err := app.NewAuthService(newFakeRepo(), cache, &fakeOAuth{}, cfg)
		require.NoError(t, err)

		_, err = service.CompleteOAuth(ctx, "code", "invalid-state")
		assert.Error(t, err)
	})

	t.Run("oauth exchange error", func(t *testing.T) {
		cache := newFakeCache()
		cache.Set(ctx, "oauth_state:valid", []byte("1"), 300)
		
		oauth := &fakeOAuthWithErrors{exchangeError: assert.AnError}
		service, err := app.NewAuthService(newFakeRepo(), cache, oauth, cfg)
		require.NoError(t, err)

		_, err = service.CompleteOAuth(ctx, "code", "valid")
		assert.Error(t, err)
	})

	t.Run("upsert new user error", func(t *testing.T) {
		cache := newFakeCache()
		cache.Set(ctx, "oauth_state:valid", []byte("1"), 300)
		
		repo := &fakeRepoWithErrors{upsertError: assert.AnError}
		oauth := &fakeOAuth{
			user: ports.OAuthUser{
				ID:          "new-user",
				Email:       "new@test.com",
				DisplayName: "New User",
			},
		}
		
		service, err := app.NewAuthService(repo, cache, oauth, cfg)
		require.NoError(t, err)

		_, err = service.CompleteOAuth(ctx, "code", "valid")
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "save oauth user")
	})
}

// TestValidateToken_Errors tests token validation edge cases
func TestValidateToken_Errors(t *testing.T) {
	ctx := context.Background()
	cfg := shared.Config{
		JWTSecret:        "test-secret",
		JWTIssuer:        "classsphere",
		JWTExpiryMinutes: 60,
	}

	hash, _ := bcrypt.GenerateFromPassword([]byte("secret"), bcrypt.DefaultCost)
	repo := newFakeRepo()
	repo.upsert(domain.User{
		ID:             "user-1",
		Email:          "user@test.com",
		HashedPassword: string(hash),
		Role:           domain.RoleTeacher,
	})

	service, err := app.NewAuthService(repo, newFakeCache(), &fakeOAuth{}, cfg)
	require.NoError(t, err)

	t.Run("empty token", func(t *testing.T) {
		_, err := service.ValidateToken(ctx, "")
		assert.Error(t, err)
		assert.Equal(t, shared.ErrUnauthorized, err)
	})

	t.Run("invalid token format", func(t *testing.T) {
		_, err := service.ValidateToken(ctx, "invalid-token")
		assert.Error(t, err)
		assert.Equal(t, shared.ErrUnauthorized, err)
	})

	t.Run("expired token", func(t *testing.T) {
		// Create expired token
		expiredSvc, _ := app.NewAuthService(repo, newFakeCache(), &fakeOAuth{}, cfg)
		pastTime := time.Now().Add(-2 * time.Hour)
		expiredSvc.SetNowFunc(func() time.Time { return pastTime })

		result, err := expiredSvc.LoginWithPassword(ctx, "user@test.com", "secret")
		require.NoError(t, err)

		// Try to validate with current time
		_, err = service.ValidateToken(ctx, result.AccessToken)
		assert.Error(t, err)
		assert.Equal(t, shared.ErrUnauthorized, err)
	})

	t.Run("user not found", func(t *testing.T) {
		// Create token for non-existent user
		emptyRepo := newFakeRepo()
		tempService, _ := app.NewAuthService(emptyRepo, newFakeCache(), &fakeOAuth{}, cfg)
		
		// Manually create a token with non-existent user ID
		token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.RegisteredClaims{
			Subject:   "non-existent-user",
			Issuer:    cfg.JWTIssuer,
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour)),
		})
		tokenString, _ := token.SignedString([]byte(cfg.JWTSecret))

		_, err := tempService.ValidateToken(ctx, tokenString)
		assert.Error(t, err)
		assert.Equal(t, shared.ErrUnauthorized, err)
	})
}

// === HELPER TYPES WITH ERRORS ===

type fakeCacheWithErrors struct {
	*fakeCache
	setError error
}

func (f *fakeCacheWithErrors) Set(_ context.Context, _ string, _ []byte, _ int) error {
	if f.setError != nil {
		return f.setError
	}
	return nil
}

type fakeOAuthWithErrors struct {
	authURLError  error
	exchangeError error
}

func (f *fakeOAuthWithErrors) AuthURL(_ string) (string, error) {
	if f.authURLError != nil {
		return "", f.authURLError
	}
	return "https://auth", nil
}

func (f *fakeOAuthWithErrors) Exchange(_ context.Context, _ string) (ports.OAuthUser, error) {
	if f.exchangeError != nil {
		return ports.OAuthUser{}, f.exchangeError
	}
	return ports.OAuthUser{}, nil
}

type fakeRepoWithErrors struct {
	*fakeRepo
	upsertError error
}

func (f *fakeRepoWithErrors) Upsert(_ context.Context, user domain.User) error {
	if f.upsertError != nil {
		return f.upsertError
	}
	return nil
}

func (f *fakeRepoWithErrors) FindByEmail(_ context.Context, _ string) (domain.User, error) {
	return domain.User{}, shared.ErrUserNotFound
}

func (f *fakeRepoWithErrors) FindByID(_ context.Context, _ string) (domain.User, error) {
	return domain.User{}, shared.ErrUserNotFound
}
