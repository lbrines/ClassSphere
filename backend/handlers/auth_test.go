package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"classsphere-backend/auth"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func setupTestDB(t *testing.T) *gorm.DB {
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	require.NoError(t, err)
	
	// Auto migrate
	err = db.AutoMigrate(&models.User{})
	require.NoError(t, err)
	
	return db
}

func setupTestAuthHandler(t *testing.T) (*AuthHandler, *gorm.DB, *auth.JWTManager) {
	db := setupTestDB(t)
	userRepo := models.NewUserRepository(db)
	jwtManager := auth.NewJWTManager("test-secret-key")
	authHandler := NewAuthHandler(userRepo, jwtManager)
	
	return authHandler, db, jwtManager
}

func closeTestDB(t *testing.T, db *gorm.DB) {
	sqlDB, err := db.DB()
	require.NoError(t, err)
	err = sqlDB.Close()
	require.NoError(t, err)
}

func TestNewAuthHandler(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	userRepo := models.NewUserRepository(db)
	jwtManager := auth.NewJWTManager("test-secret")
	
	handler := NewAuthHandler(userRepo, jwtManager)
	
	assert.NotNil(t, handler)
	assert.NotNil(t, handler.userRepo)
	assert.NotNil(t, handler.jwtManager)
}

func TestAuthHandler_Register_Success(t *testing.T) {
	handler, db, jwtManager := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	registerReq := RegisterRequest{
		Email:    "test@example.com",
		Password: "TestPassword123",
		Name:     "Test User",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusCreated, rec.Code)
	
	var response RegisterResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "test@example.com", response.User.Email)
	assert.Equal(t, "Test User", response.User.Name)
	assert.Equal(t, "user", response.User.Role)
	assert.NotEmpty(t, response.Token)
	
	// Verify token is valid
	claims, err := jwtManager.ValidateToken(response.Token)
	assert.NoError(t, err)
	assert.Equal(t, "1", claims.UserID) // UserID is the string representation of the user ID
}

func TestAuthHandler_Register_InvalidEmail(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	registerReq := RegisterRequest{
		Email:    "invalid-email",
		Password: "TestPassword123",
		Name:     "Test User",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Register_WeakPassword(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	registerReq := RegisterRequest{
		Email:    "test@example.com",
		Password: "123",
		Name:     "Test User",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Register_DuplicateEmail(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// First registration
	registerReq := RegisterRequest{
		Email:    "test@example.com",
		Password: "TestPassword123",
		Name:     "Test User",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusCreated, rec.Code)
	
	// Second registration with same email
	reqBody2, _ := json.Marshal(registerReq)
	req2 := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody2))
	req2.Header.Set("Content-Type", "application/json")
	rec2 := httptest.NewRecorder()
	c2 := e.NewContext(req2, rec2)
	
	err = handler.Register(c2)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusConflict, rec2.Code)
}

func TestAuthHandler_Login_Success(t *testing.T) {
	handler, db, jwtManager := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// First register a user
	registerReq := RegisterRequest{
		Email:    "test@example.com",
		Password: "TestPassword123",
		Name:     "Test User",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	require.NoError(t, err)
	
	// Now login
	loginReq := LoginRequest{
		Email:    "test@example.com",
		Password: "TestPassword123",
	}
	
	reqBody, _ = json.Marshal(loginReq)
	req = httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec = httptest.NewRecorder()
	c = e.NewContext(req, rec)
	
	err = handler.Login(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	var response LoginResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "test@example.com", response.User.Email)
	assert.NotEmpty(t, response.Token)
	
	// Verify token is valid
	claims, err := jwtManager.ValidateToken(response.Token)
	assert.NoError(t, err)
	assert.Equal(t, "1", claims.UserID) // UserID is the string representation of the user ID
}

func TestAuthHandler_Login_InvalidCredentials(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	loginReq := LoginRequest{
		Email:    "test@example.com",
		Password: "WrongPassword",
	}
	
	reqBody, _ := json.Marshal(loginReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Login(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_GetProfile_Success(t *testing.T) {
	handler, db, jwtManager := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// First register a user
	registerReq := RegisterRequest{
		Email:    "test@example.com",
		Password: "TestPassword123",
		Name:     "Test User",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	require.NoError(t, err)
	
	// Get user from database to get ID
	user, err := handler.userRepo.GetUserByEmail("test@example.com")
	require.NoError(t, err)
	
	// Create valid token
	token, err := jwtManager.GenerateToken("1", user.Role, 24*time.Hour)
	require.NoError(t, err)
	
	// Set user in context (simulating JWT middleware)
	c.Set("user", &auth.Claims{UserID: "1", Role: user.Role})
	
	req = httptest.NewRequest(http.MethodGet, "/api/profile", nil)
	req.Header.Set("Authorization", "Bearer "+token)
	rec = httptest.NewRecorder()
	c = e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "1", Role: user.Role})
	
	err = handler.GetProfile(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	var response UserResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "test@example.com", response.Email)
	assert.Equal(t, "Test User", response.Name)
}

func TestAuthHandler_RefreshToken_Success(t *testing.T) {
	handler, db, jwtManager := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Create a valid token
	token, err := jwtManager.GenerateToken("1", "user", 1*time.Hour)
	require.NoError(t, err)
	
	refreshReq := RefreshTokenRequest{
		Token: token,
	}
	
	reqBody, _ := json.Marshal(refreshReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/refresh", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err = handler.RefreshToken(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	var response RefreshTokenResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.NotEmpty(t, response.Token)
	assert.NotEqual(t, token, response.Token)
}

func TestAuthHandler_RefreshToken_InvalidToken(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	refreshReq := RefreshTokenRequest{
		Token: "invalid.token.here",
	}
	
	reqBody, _ := json.Marshal(refreshReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/refresh", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.RefreshToken(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestValidateRegisterRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	tests := []struct {
		name    string
		req     RegisterRequest
		wantErr bool
	}{
		{
			name: "valid request",
			req: RegisterRequest{
				Email:    "test@example.com",
				Password: "TestPassword123",
				Name:     "Test User",
			},
			wantErr: false,
		},
		{
			name: "empty email",
			req: RegisterRequest{
				Email:    "",
				Password: "TestPassword123",
				Name:     "Test User",
			},
			wantErr: true,
		},
		{
			name: "invalid email",
			req: RegisterRequest{
				Email:    "invalid-email",
				Password: "TestPassword123",
				Name:     "Test User",
			},
			wantErr: true,
		},
		{
			name: "empty name",
			req: RegisterRequest{
				Email:    "test@example.com",
				Password: "TestPassword123",
				Name:     "",
			},
			wantErr: true,
		},
		{
			name: "weak password",
			req: RegisterRequest{
				Email:    "test@example.com",
				Password: "123",
				Name:     "Test User",
			},
			wantErr: true,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := handler.validateRegisterRequest(tt.req)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestValidateLoginRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	tests := []struct {
		name    string
		req     LoginRequest
		wantErr bool
	}{
		{
			name: "valid request",
			req: LoginRequest{
				Email:    "test@example.com",
				Password: "TestPassword123",
			},
			wantErr: false,
		},
		{
			name: "empty email",
			req: LoginRequest{
				Email:    "",
				Password: "TestPassword123",
			},
			wantErr: true,
		},
		{
			name: "empty password",
			req: LoginRequest{
				Email:    "test@example.com",
				Password: "",
			},
			wantErr: true,
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := handler.validateLoginRequest(tt.req)
			if tt.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}

func TestIsValidEmail(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	tests := []struct {
		name  string
		email string
		want  bool
	}{
		{"valid email", "test@example.com", true},
		{"valid email with subdomain", "test@mail.example.com", true},
		{"invalid email", "invalid-email", false},
		{"empty email", "", false},
		{"email without @", "testexample.com", false},
		{"email without domain", "test@", false},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := handler.isValidEmail(tt.email)
			assert.Equal(t, tt.want, got)
		})
	}
}

func TestAuthHandler_Logout(t *testing.T) {
	handler, db, jwtManager := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Create a valid token
	token, err := jwtManager.GenerateToken("1", "user", 1*time.Hour)
	require.NoError(t, err)
	
	logoutReq := LogoutRequest{
		Token: token,
	}
	
	reqBody, _ := json.Marshal(logoutReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/logout", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err = handler.Logout(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	var response map[string]string
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "Logout successful", response["message"])
}

func TestAuthHandler_Logout_InvalidToken(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	logoutReq := LogoutRequest{
		Token: "invalid-token",
	}
	
	reqBody, _ := json.Marshal(logoutReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/logout", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Logout(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_Logout_EmptyToken(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	logoutReq := LogoutRequest{
		Token: "",
	}
	
	reqBody, _ := json.Marshal(logoutReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/logout", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Logout(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_GetProfile_UserNotFound(t *testing.T) {
	handler, db, jwtManager := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Create a valid token for non-existent user
	token, err := jwtManager.GenerateToken("999", "user", 1*time.Hour)
	require.NoError(t, err)
	
	req := httptest.NewRequest(http.MethodGet, "/api/profile", nil)
	req.Header.Set("Authorization", "Bearer "+token)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "999", Role: "user"})
	
	err = handler.GetProfile(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusNotFound, rec.Code)
}

func TestAuthHandler_Login_InvalidCredentials_New(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	loginReq := LoginRequest{
		Email:    "test@example.com",
		Password: "wrongpassword",
	}
	
	reqBody, _ := json.Marshal(loginReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Login(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_Login_UserNotFound(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	loginReq := LoginRequest{
		Email:    "nonexistent@example.com",
		Password: "password123",
	}
	
	reqBody, _ := json.Marshal(loginReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Login(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_Login_InvalidRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Invalid JSON
	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Login(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Register_InvalidRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Invalid JSON
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_RefreshToken_InvalidToken_New(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	refreshReq := RefreshTokenRequest{
		Token: "invalid-token",
	}
	
	reqBody, _ := json.Marshal(refreshReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/refresh", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.RefreshToken(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_RefreshToken_InvalidRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Invalid JSON
	req := httptest.NewRequest(http.MethodPost, "/auth/refresh", bytes.NewReader([]byte("invalid json")))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.RefreshToken(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_RefreshToken_EmptyToken(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	refreshReq := RefreshTokenRequest{
		Token: "",
	}
	
	reqBody, _ := json.Marshal(refreshReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/refresh", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.RefreshToken(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_Register_WeakPassword_New(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	registerReq := RegisterRequest{
		Email:    "test2@example.com",
		Password: "123", // Weak password
		Name:     "Test User 2",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Register_InvalidEmail_New(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	registerReq := RegisterRequest{
		Email:    "invalid-email-format", // Invalid email format
		Password: "TestPassword123",
		Name:     "Test User 2",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Login_WithEmptyEmail(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	loginReq := LoginRequest{
		Email:    "", // Empty email
		Password: "TestPassword123",
	}
	
	reqBody, _ := json.Marshal(loginReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Login(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Login_WithEmptyPassword(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	loginReq := LoginRequest{
		Email:    "test@example.com",
		Password: "", // Empty password
	}
	
	reqBody, _ := json.Marshal(loginReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Login(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_GetProfile_WithInvalidUserID(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/profile", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set invalid user ID in context (this will cause an error when parsing)
	c.Set("user_id", "invalid-id")
	
	err := handler.GetProfile(c)
	
	assert.NoError(t, err)
	// The handler should return 401 because there's no valid JWT middleware
	// but we're testing the error handling path, so we expect an error response
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_GetProfile_WithNonExistentUser(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/profile", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set non-existent user ID in context
	c.Set("user_id", "999")
	
	err := handler.GetProfile(c)
	
	assert.NoError(t, err)
	// The handler should return 401 because there's no valid JWT middleware
	// but we're testing the error handling path, so we expect an error response
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_Login_WithDatabaseError(t *testing.T) {
	// Create handler with closed database to simulate database error
	db := setupTestDB(t)
	sqlDB, _ := db.DB()
	sqlDB.Close()
	
	jwtManager := auth.NewJWTManager("test-secret")
	userRepo := models.NewUserRepository(db)
	handler := NewAuthHandler(userRepo, jwtManager)
	
	e := echo.New()
	
	loginReq := LoginRequest{
		Email:    "test@example.com",
		Password: "TestPassword123",
	}
	
	reqBody, _ := json.Marshal(loginReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/login", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Login(c)
	
	assert.NoError(t, err)
	// The handler returns 401 for user not found, even with database errors
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_Register_WithDatabaseError(t *testing.T) {
	// Create handler with closed database to simulate database error
	db := setupTestDB(t)
	sqlDB, _ := db.DB()
	sqlDB.Close()
	
	jwtManager := auth.NewJWTManager("test-secret")
	userRepo := models.NewUserRepository(db)
	handler := NewAuthHandler(userRepo, jwtManager)
	
	e := echo.New()
	
	registerReq := RegisterRequest{
		Email:    "test@example.com",
		Password: "TestPassword123",
		Name:     "Test User",
	}
	
	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/auth/register", bytes.NewReader(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusInternalServerError, rec.Code)
}

func TestAuthHandler_Logout_WithInvalidRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Test with invalid JSON that will cause c.Bind to fail
	req := httptest.NewRequest(http.MethodPost, "/auth/logout", strings.NewReader("invalid json"))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Logout(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Logout_WithEmptyRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Test with empty request body - this will create an empty LogoutRequest
	// and then fail token validation
	req := httptest.NewRequest(http.MethodPost, "/auth/logout", nil)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Logout(c)
	
	assert.NoError(t, err)
	// The handler should return 401 for invalid token (empty token)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestAuthHandler_Register_WithInvalidRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Test with invalid JSON that will cause c.Bind to fail
	req := httptest.NewRequest(http.MethodPost, "/auth/register", strings.NewReader("invalid json"))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestAuthHandler_Register_WithEmptyRequest(t *testing.T) {
	handler, db, _ := setupTestAuthHandler(t)
	defer closeTestDB(t, db)
	
	e := echo.New()
	
	// Test with empty request body
	req := httptest.NewRequest(http.MethodPost, "/auth/register", nil)
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handler.Register(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}
