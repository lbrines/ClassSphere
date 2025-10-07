package app

import (
	"context"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"

	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

const (
	oauthStatePrefix = "oauth_state:"
	oauthStateTTL    = 300 // 5 minutes
)

// AuthService coordinates authentication flows (password and OAuth based).
type AuthService struct {
	users   ports.UserRepository
	cache   ports.Cache
	oauth   ports.OAuthProvider
	nowFunc func() time.Time
	cfg     shared.Config
}

// NewAuthService constructs an AuthService.
func NewAuthService(users ports.UserRepository, cache ports.Cache, oauth ports.OAuthProvider, cfg shared.Config) (*AuthService, error) {
	if users == nil {
		return nil, fmt.Errorf("users repository is required")
	}
	if cache == nil {
		return nil, fmt.Errorf("cache is required")
	}
	if oauth == nil {
		return nil, fmt.Errorf("oauth provider is required")
	}
	return &AuthService{
		users:   users,
		cache:   cache,
		oauth:   oauth,
		nowFunc: time.Now,
		cfg:     cfg,
	}, nil
}

// AuthTokens represents the authentication outcome.
type AuthTokens struct {
	AccessToken string
	ExpiresAt   time.Time
	User        domain.User
}

// LoginWithPassword authenticates a user using email and password credentials.
func (a *AuthService) LoginWithPassword(ctx context.Context, email, password string) (AuthTokens, error) {
	user, err := a.users.FindByEmail(ctx, email)
	if err != nil {
		return AuthTokens{}, shared.ErrInvalidCredentials
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.HashedPassword), []byte(password)); err != nil {
		return AuthTokens{}, shared.ErrInvalidCredentials
	}

	token, expiresAt, err := a.generateToken(user)
	if err != nil {
		return AuthTokens{}, err
	}

	return AuthTokens{
		AccessToken: token,
		ExpiresAt:   expiresAt,
		User:        user,
	}, nil
}

// StartOAuth generates a state parameter, persists it, and returns the authorization URL.
func (a *AuthService) StartOAuth(ctx context.Context) (string, string, error) {
	state, err := generateState()
	if err != nil {
		return "", "", err
	}
	if err := a.cache.Set(ctx, oauthStatePrefix+state, []byte("1"), oauthStateTTL); err != nil {
		return "", "", fmt.Errorf("store oauth state: %w", err)
	}
	url, err := a.oauth.AuthURL(state)
	if err != nil {
		return "", "", err
	}
	return state, url, nil
}

// CompleteOAuth processes the OAuth callback and returns signed tokens.
func (a *AuthService) CompleteOAuth(ctx context.Context, code, state string) (AuthTokens, error) {
	if state == "" {
		return AuthTokens{}, fmt.Errorf("state is required")
	}
	value, err := a.cache.Get(ctx, oauthStatePrefix+state)
	if err != nil {
		return AuthTokens{}, fmt.Errorf("validate oauth state: %w", err)
	}
	if len(value) == 0 {
		return AuthTokens{}, shared.ErrUnauthorized
	}
	defer func() {
		_ = a.cache.Delete(ctx, oauthStatePrefix+state)
	}()

	oauthUser, err := a.oauth.Exchange(ctx, code)
	if err != nil {
		return AuthTokens{}, err
	}

	user, err := a.users.FindByEmail(ctx, oauthUser.Email)
	if err != nil {
		user = domain.User{
			ID:          oauthUser.ID,
			Email:       oauthUser.Email,
			DisplayName: oauthUser.DisplayName,
			Role:        domain.RoleTeacher,
			CreatedAt:   a.nowFunc(),
			UpdatedAt:   a.nowFunc(),
		}
		if err := a.users.Upsert(ctx, user); err != nil {
			return AuthTokens{}, fmt.Errorf("save oauth user: %w", err)
		}
	}

	token, expiresAt, err := a.generateToken(user)
	if err != nil {
		return AuthTokens{}, err
	}

	return AuthTokens{
		AccessToken: token,
		ExpiresAt:   expiresAt,
		User:        user,
	}, nil
}

// ValidateToken verifies the JWT and returns the associated user.
func (a *AuthService) ValidateToken(ctx context.Context, tokenString string) (domain.User, error) {
	if tokenString == "" {
		return domain.User{}, shared.ErrUnauthorized
	}

	claims := &jwt.RegisteredClaims{}
	_, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(a.cfg.JWTSecret), nil
	})
	if err != nil {
		return domain.User{}, shared.ErrUnauthorized
	}

	user, err := a.users.FindByID(ctx, claims.Subject)
	if err != nil {
		return domain.User{}, shared.ErrUnauthorized
	}
	return user, nil
}

func (a *AuthService) generateToken(user domain.User) (string, time.Time, error) {
	exp := a.nowFunc().Add(time.Minute * time.Duration(a.cfg.JWTExpiryMinutes))
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.RegisteredClaims{
		Subject:   user.ID,
		Issuer:    a.cfg.JWTIssuer,
		ExpiresAt: jwt.NewNumericDate(exp),
		IssuedAt:  jwt.NewNumericDate(a.nowFunc()),
	})

	tokenString, err := token.SignedString([]byte(a.cfg.JWTSecret))
	if err != nil {
		return "", time.Time{}, fmt.Errorf("sign token: %w", err)
	}
	return tokenString, exp, nil
}

func generateState() (string, error) {
	buf := make([]byte, 32)
	if _, err := rand.Read(buf); err != nil {
		return "", fmt.Errorf("generate state: %w", err)
	}
	return base64.RawURLEncoding.EncodeToString(buf), nil
}

// SetNowFunc allows tests to control the time provider.
func (a *AuthService) SetNowFunc(fn func() time.Time) {
	if fn != nil {
		a.nowFunc = fn
	}
}
