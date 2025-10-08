package oauth

import (
	"context"
	"fmt"
	"net/http"

	"github.com/go-resty/resty/v2"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"

	"github.com/lbrines/classsphere/internal/ports"
)

const googleUserInfoEndpoint = "https://www.googleapis.com/oauth2/v3/userinfo"

// GoogleOAuth integrates with Google OAuth 2.0 endpoints.
type GoogleOAuth struct {
	config      *oauth2.Config
	client      *resty.Client
	userInfoURL string
}

// Option configures the GoogleOAuth adapter.
type Option func(*GoogleOAuth)

// NewGoogleOAuth constructs the adapter.
func NewGoogleOAuth(clientID, clientSecret, redirectURL string, opts ...Option) *GoogleOAuth {
	cfg := &oauth2.Config{
		ClientID:     clientID,
		ClientSecret: clientSecret,
		RedirectURL:  redirectURL,
		Scopes: []string{
			"openid",
			"profile",
			"email",
			"https://www.googleapis.com/auth/classroom.courses.readonly",
		},
		Endpoint: google.Endpoint,
	}

	oauthClient := &GoogleOAuth{
		config:      cfg,
		client:      resty.New().SetRetryCount(2),
		userInfoURL: googleUserInfoEndpoint,
	}

	for _, opt := range opts {
		opt(oauthClient)
	}

	return oauthClient
}

// WithOAuth2Config overrides the default OAuth2 configuration.
func WithOAuth2Config(cfg *oauth2.Config) Option {
	return func(g *GoogleOAuth) {
		if cfg != nil {
			g.config = cfg
		}
	}
}

// WithRestyClient overrides the HTTP client used for Google APIs.
func WithRestyClient(client *resty.Client) Option {
	return func(g *GoogleOAuth) {
		if client != nil {
			g.client = client
		}
	}
}

// WithUserInfoURL overrides the user info endpoint (useful for testing).
func WithUserInfoURL(url string) Option {
	return func(g *GoogleOAuth) {
		if url != "" {
			g.userInfoURL = url
		}
	}
}

// AuthURL generates the Google authorization URL.
func (g *GoogleOAuth) AuthURL(state string) (string, error) {
	if state == "" {
		return "", fmt.Errorf("state is required")
	}
	return g.config.AuthCodeURL(state, oauth2.AccessTypeOffline), nil
}

// Exchange exchanges the authorization code for user info.
func (g *GoogleOAuth) Exchange(ctx context.Context, code string) (ports.OAuthUser, error) {
	if code == "" {
		return ports.OAuthUser{}, fmt.Errorf("authorization code is required")
	}

	token, err := g.config.Exchange(ctx, code)
	if err != nil {
		return ports.OAuthUser{}, fmt.Errorf("exchange code: %w", err)
	}

	resp, err := g.client.R().
		SetContext(ctx).
		SetHeader("Authorization", "Bearer "+token.AccessToken).
		SetError(&oauthError{}).
		SetResult(&googleUser{}).
		Get(g.userInfoURL)
	if err != nil {
		return ports.OAuthUser{}, fmt.Errorf("request userinfo: %w", err)
	}

	if resp.IsError() {
		if apiErr, ok := resp.Error().(*oauthError); ok {
			return ports.OAuthUser{}, fmt.Errorf("userinfo error: %s", apiErr.Error())
		}
		return ports.OAuthUser{}, fmt.Errorf("userinfo error: status %d", resp.StatusCode())
	}

	userInfo, ok := resp.Result().(*googleUser)
	if !ok {
		return ports.OAuthUser{}, fmt.Errorf("unexpected userinfo response")
	}

	return ports.OAuthUser{
		ID:          userInfo.Sub,
		Email:       userInfo.Email,
		DisplayName: userInfo.Name,
	}, nil
}

type googleUser struct {
	Sub   string `json:"sub"`
	Email string `json:"email"`
	Name  string `json:"name"`
}

type oauthError struct {
	Code        string `json:"error"`
	Description string `json:"error_description"`
}

func (e *oauthError) Error() string {
	if e == nil {
		return http.StatusText(http.StatusInternalServerError)
	}
	if e.Description != "" {
		return e.Description
	}
	return e.Code
}
