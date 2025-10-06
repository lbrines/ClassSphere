package oauth

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewGoogleOAuthService(t *testing.T) {
	// Set environment variables for testing
	os.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	os.Setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")
	os.Setenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/auth/google/callback")

	service := NewGoogleOAuthService()

	assert.Equal(t, "test-client-id", service.clientID)
	assert.Equal(t, "test-client-secret", service.clientSecret)
	assert.Equal(t, "http://localhost:8080/auth/google/callback", service.redirectURI)
	assert.Equal(t, "https://accounts.google.com/o/oauth2/v2/auth", service.authURL)
	assert.Equal(t, "https://oauth2.googleapis.com/token", service.tokenURL)
	assert.Equal(t, "https://www.googleapis.com/oauth2/v2/userinfo", service.userInfoURL)
}

func TestGetAuthURL(t *testing.T) {
	os.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	os.Setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")
	os.Setenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/auth/google/callback")

	service := NewGoogleOAuthService()
	state := "test-state-123"

	authURL := service.GetAuthURL(state)

	assert.Contains(t, authURL, "https://accounts.google.com/o/oauth2/v2/auth")
	assert.Contains(t, authURL, "client_id=test-client-id")
	assert.Contains(t, authURL, "redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fauth%2Fgoogle%2Fcallback")
	assert.Contains(t, authURL, "state=test-state-123")
	assert.Contains(t, authURL, "scope=openid+email+profile")
	assert.Contains(t, authURL, "response_type=code")
}

func TestExchangeCode(t *testing.T) {
	// Create a mock server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		assert.Equal(t, "POST", r.Method)
		assert.Equal(t, "application/x-www-form-urlencoded", r.Header.Get("Content-Type"))

		// Mock successful response
		response := GoogleTokenResponse{
			AccessToken:  "mock-access-token",
			TokenType:    "Bearer",
			ExpiresIn:    3600,
			RefreshToken: "mock-refresh-token",
			Scope:        "openid email profile",
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	}))
	defer server.Close()

	os.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	os.Setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")
	os.Setenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/auth/google/callback")

	service := NewGoogleOAuthService()
	service.tokenURL = server.URL

	tokenResp, err := service.ExchangeCode("test-auth-code")

	assert.NoError(t, err)
	assert.Equal(t, "mock-access-token", tokenResp.AccessToken)
	assert.Equal(t, "Bearer", tokenResp.TokenType)
	assert.Equal(t, 3600, tokenResp.ExpiresIn)
}

func TestGetUserInfo(t *testing.T) {
	// Create a mock server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		assert.Equal(t, "GET", r.Method)
		assert.Equal(t, "Bearer mock-access-token", r.Header.Get("Authorization"))

		// Mock user info response
		userInfo := GoogleUserInfo{
			ID:            "123456789",
			Email:         "test@example.com",
			VerifiedEmail: true,
			Name:          "Test User",
			GivenName:     "Test",
			FamilyName:    "User",
			Picture:       "https://example.com/photo.jpg",
			Locale:        "en",
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(userInfo)
	}))
	defer server.Close()

	os.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	os.Setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")
	os.Setenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/auth/google/callback")

	service := NewGoogleOAuthService()
	service.userInfoURL = server.URL

	userInfo, err := service.GetUserInfo("mock-access-token")

	assert.NoError(t, err)
	assert.Equal(t, "123456789", userInfo.ID)
	assert.Equal(t, "test@example.com", userInfo.Email)
	assert.Equal(t, "Test User", userInfo.Name)
	assert.True(t, userInfo.VerifiedEmail)
}

func TestGoogleOAuthService_Integration(t *testing.T) {
	// Test basic service creation and URL generation
	os.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	os.Setenv("GOOGLE_CLIENT_SECRET", "test-client-secret")
	os.Setenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/auth/google/callback")

	service := NewGoogleOAuthService()
	
	// Test auth URL generation
	authURL := service.GetAuthURL("test-state")
	assert.Contains(t, authURL, "accounts.google.com")
	assert.Contains(t, authURL, "test-client-id")
	assert.Contains(t, authURL, "test-state")
}
