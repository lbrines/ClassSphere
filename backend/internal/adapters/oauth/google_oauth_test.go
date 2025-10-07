package oauth_test

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/go-resty/resty/v2"
	"github.com/stretchr/testify/require"
	"golang.org/x/oauth2"

	"github.com/lbrines/classsphere/internal/adapters/oauth"
)

func TestGoogleOAuthAuthURL(t *testing.T) {
	provider := oauth.NewGoogleOAuth("client", "secret", "http://localhost/callback")
	url, err := provider.AuthURL("state123")
	require.NoError(t, err)
	require.Contains(t, url, "state123")
}

func TestGoogleOAuthAuthURLError(t *testing.T) {
	provider := oauth.NewGoogleOAuth("client", "secret", "http://localhost/callback")
	_, err := provider.AuthURL("")
	require.Error(t, err)
}

func TestGoogleOAuthExchangeValidation(t *testing.T) {
	provider := oauth.NewGoogleOAuth("client", "secret", "http://localhost/callback")
	_, err := provider.Exchange(nil, "")
	require.Error(t, err)
}

func TestGoogleOAuthExchangeSuccess(t *testing.T) {
	tokenSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		require.NoError(t, r.ParseForm())
		w.Header().Set("Content-Type", "application/json")
		response := map[string]any{
			"access_token": "token123",
			"token_type":   "Bearer",
			"expires_in":   3600,
		}
		_ = json.NewEncoder(w).Encode(response)
	}))
	defer tokenSrv.Close()

	userSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]string{
			"sub":   "user123",
			"email": "user@test.com",
			"name":  "Test User",
		})
	}))
	defer userSrv.Close()

	cfg := &oauth2.Config{
		ClientID:     "client",
		ClientSecret: "secret",
		RedirectURL:  "http://localhost/callback",
		Scopes:       []string{"openid", "email"},
		Endpoint: oauth2.Endpoint{
			AuthURL:  tokenSrv.URL + "/auth",
			TokenURL: tokenSrv.URL,
		},
	}

	restyClient := resty.New().SetRetryCount(0)

	provider := oauth.NewGoogleOAuth("client", "secret", "http://localhost/callback",
		oauth.WithOAuth2Config(cfg),
		oauth.WithUserInfoURL(userSrv.URL),
		oauth.WithRestyClient(restyClient),
	)

	user, err := provider.Exchange(context.Background(), "code123")
	require.NoError(t, err)
	require.Equal(t, "user123", user.ID)
	require.Equal(t, "user@test.com", user.Email)
}

// === ADDITIONAL TESTS FOR 90% COVERAGE ===

func TestGoogleOAuthExchangeTokenError(t *testing.T) {
	// Server that returns an error
	tokenSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("invalid request"))
	}))
	defer tokenSrv.Close()

	cfg := &oauth2.Config{
		ClientID:     "client",
		ClientSecret: "secret",
		RedirectURL:  "http://localhost/callback",
		Endpoint: oauth2.Endpoint{
			TokenURL: tokenSrv.URL,
		},
	}

	provider := oauth.NewGoogleOAuth("client", "secret", "http://localhost/callback",
		oauth.WithOAuth2Config(cfg),
	)

	_, err := provider.Exchange(context.Background(), "invalid-code")
	require.Error(t, err)
}

func TestGoogleOAuthExchangeUserInfoError(t *testing.T) {
	// Token server that works
	tokenSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		response := map[string]any{
			"access_token": "token123",
			"token_type":   "Bearer",
			"expires_in":   3600,
		}
		_ = json.NewEncoder(w).Encode(response)
	}))
	defer tokenSrv.Close()

	// User info server that returns error
	userSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("server error"))
	}))
	defer userSrv.Close()

	cfg := &oauth2.Config{
		ClientID:     "client",
		ClientSecret: "secret",
		RedirectURL:  "http://localhost/callback",
		Endpoint: oauth2.Endpoint{
			TokenURL: tokenSrv.URL,
		},
	}

	restyClient := resty.New().SetRetryCount(0)

	provider := oauth.NewGoogleOAuth("client", "secret", "http://localhost/callback",
		oauth.WithOAuth2Config(cfg),
		oauth.WithUserInfoURL(userSrv.URL),
		oauth.WithRestyClient(restyClient),
	)

	_, err := provider.Exchange(context.Background(), "code123")
	require.Error(t, err)
	require.Contains(t, err.Error(), "userinfo error")
}

func TestGoogleOAuthExchangeInvalidJSON(t *testing.T) {
	tokenSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		response := map[string]any{
			"access_token": "token123",
			"token_type":   "Bearer",
			"expires_in":   3600,
		}
		_ = json.NewEncoder(w).Encode(response)
	}))
	defer tokenSrv.Close()

	// User server that returns invalid JSON
	userSrv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte("invalid-json{"))
	}))
	defer userSrv.Close()

	cfg := &oauth2.Config{
		ClientID:     "client",
		ClientSecret: "secret",
		RedirectURL:  "http://localhost/callback",
		Endpoint: oauth2.Endpoint{
			TokenURL: tokenSrv.URL,
		},
	}

	restyClient := resty.New().SetRetryCount(0)

	provider := oauth.NewGoogleOAuth("client", "secret", "http://localhost/callback",
		oauth.WithOAuth2Config(cfg),
		oauth.WithUserInfoURL(userSrv.URL),
		oauth.WithRestyClient(restyClient),
	)

	_, err := provider.Exchange(context.Background(), "code123")
	require.Error(t, err)
	require.Contains(t, err.Error(), "userinfo")
}
