package oauth

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"time"

	"classsphere-backend/auth"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
)

// GoogleOAuthService handles Google OAuth authentication
type GoogleOAuthService struct {
	clientID     string
	clientSecret string
	redirectURI  string
	authURL      string
	tokenURL     string
	userInfoURL  string
}

// GoogleTokenResponse represents the response from Google's token endpoint
type GoogleTokenResponse struct {
	AccessToken  string `json:"access_token"`
	TokenType    string `json:"token_type"`
	ExpiresIn    int    `json:"expires_in"`
	RefreshToken string `json:"refresh_token"`
	Scope        string `json:"scope"`
}

// GoogleUserInfo represents user information from Google
type GoogleUserInfo struct {
	ID            string `json:"id"`
	Email         string `json:"email"`
	VerifiedEmail bool   `json:"verified_email"`
	Name          string `json:"name"`
	GivenName     string `json:"given_name"`
	FamilyName    string `json:"family_name"`
	Picture       string `json:"picture"`
	Locale        string `json:"locale"`
}

// NewGoogleOAuthService creates a new Google OAuth service
func NewGoogleOAuthService() *GoogleOAuthService {
	return &GoogleOAuthService{
		clientID:     os.Getenv("GOOGLE_CLIENT_ID"),
		clientSecret: os.Getenv("GOOGLE_CLIENT_SECRET"),
		redirectURI:  os.Getenv("GOOGLE_REDIRECT_URI"),
		authURL:      "https://accounts.google.com/o/oauth2/v2/auth",
		tokenURL:     "https://oauth2.googleapis.com/token",
		userInfoURL:  "https://www.googleapis.com/oauth2/v2/userinfo",
	}
}

// GetAuthURL generates the Google OAuth authorization URL
func (g *GoogleOAuthService) GetAuthURL(state string) string {
	params := url.Values{}
	params.Add("client_id", g.clientID)
	params.Add("redirect_uri", g.redirectURI)
	params.Add("scope", "openid email profile")
	params.Add("response_type", "code")
	params.Add("state", state)
	params.Add("access_type", "offline")
	params.Add("prompt", "consent")

	return fmt.Sprintf("%s?%s", g.authURL, params.Encode())
}

// ExchangeCode exchanges authorization code for access token
func (g *GoogleOAuthService) ExchangeCode(code string) (*GoogleTokenResponse, error) {
	data := url.Values{}
	data.Set("client_id", g.clientID)
	data.Set("client_secret", g.clientSecret)
	data.Set("code", code)
	data.Set("grant_type", "authorization_code")
	data.Set("redirect_uri", g.redirectURI)

	resp, err := http.PostForm(g.tokenURL, data)
	if err != nil {
		return nil, fmt.Errorf("failed to exchange code: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("token exchange failed: %s", string(body))
	}

	var tokenResp GoogleTokenResponse
	if err := json.NewDecoder(resp.Body).Decode(&tokenResp); err != nil {
		return nil, fmt.Errorf("failed to decode token response: %v", err)
	}

	return &tokenResp, nil
}

// GetUserInfo retrieves user information from Google
func (g *GoogleOAuthService) GetUserInfo(accessToken string) (*GoogleUserInfo, error) {
	req, err := http.NewRequest("GET", g.userInfoURL, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %v", err)
	}

	req.Header.Set("Authorization", "Bearer "+accessToken)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to get user info: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("user info request failed: %s", string(body))
	}

	var userInfo GoogleUserInfo
	if err := json.NewDecoder(resp.Body).Decode(&userInfo); err != nil {
		return nil, fmt.Errorf("failed to decode user info: %v", err)
	}

	return &userInfo, nil
}

// GoogleOAuthHandler handles Google OAuth requests
type GoogleOAuthHandler struct {
	oauthService *GoogleOAuthService
	userRepo     *models.UserRepository
	jwtManager   *auth.JWTManager
}

// NewGoogleOAuthHandler creates a new Google OAuth handler
func NewGoogleOAuthHandler(userRepo *models.UserRepository, jwtManager *auth.JWTManager) *GoogleOAuthHandler {
	return &GoogleOAuthHandler{
		oauthService: NewGoogleOAuthService(),
		userRepo:     userRepo,
		jwtManager:   jwtManager,
	}
}

// InitiateGoogleAuth initiates Google OAuth flow
func (h *GoogleOAuthHandler) InitiateGoogleAuth(c echo.Context) error {
	// Generate a random state for security
	state := fmt.Sprintf("state_%d", time.Now().Unix())
	
	// Store state in session/cache for validation (simplified for now)
	// In production, store this in Redis or session store
	
	authURL := h.oauthService.GetAuthURL(state)
	return c.Redirect(http.StatusTemporaryRedirect, authURL)
}

// HandleGoogleCallback handles Google OAuth callback
func (h *GoogleOAuthHandler) HandleGoogleCallback(c echo.Context) error {
	code := c.QueryParam("code")
	_ = c.QueryParam("state") // State validation would be implemented here
	error := c.QueryParam("error")

	if error != "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "OAuth error: " + error,
		})
	}

	if code == "" {
		return c.JSON(http.StatusBadRequest, map[string]string{
			"error": "Authorization code not provided",
		})
	}

	// Exchange code for token
	tokenResp, err := h.oauthService.ExchangeCode(code)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to exchange authorization code",
		})
	}

	// Get user info from Google
	userInfo, err := h.oauthService.GetUserInfo(tokenResp.AccessToken)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to get user information",
		})
	}

	// Check if user exists in our database
	user, err := h.userRepo.GetUserByEmail(userInfo.Email)
	if err != nil {
		// User doesn't exist, create new user
		user = &models.User{
			Email:    userInfo.Email,
			Name:     userInfo.Name,
			Role:     "user", // Default role
			IsActive: true,
			// No password for OAuth users
		}

		if err := h.userRepo.CreateUser(user); err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{
				"error": "Failed to create user",
			})
		}
	}

	// Generate JWT token
	token, err := h.jwtManager.GenerateToken(fmt.Sprintf("%d", user.ID), user.Role, 24*time.Hour)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Failed to generate token",
		})
	}

	// Redirect to frontend with token
	// In production, use a secure method to pass the token
	frontendURL := os.Getenv("FRONTEND_URL")
	if frontendURL == "" {
		frontendURL = "http://localhost:4200"
	}

	redirectURL := fmt.Sprintf("%s/auth/callback?token=%s", frontendURL, token)
	return c.Redirect(http.StatusTemporaryRedirect, redirectURL)
}
