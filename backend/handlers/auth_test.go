package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"classsphere-backend/auth"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func setupTestHandler() (*AuthHandler, *gorm.DB, func()) {
	// Setup test database
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// Migrate the schema
	db.AutoMigrate(&models.User{})

	// Create repositories and services
	userRepo := models.NewUserRepository(db)
	jwtManager := auth.NewJWTManager("test-secret-key")

	// Create handler
	handler := NewAuthHandler(userRepo, jwtManager)

	// Cleanup function
	cleanup := func() {
		sqlDB, _ := db.DB()
		sqlDB.Close()
	}

	return handler, db, cleanup
}

func TestRegister(t *testing.T) {
	handler, _, cleanup := setupTestHandler()
	defer cleanup()

	// Test successful registration
	registerReq := RegisterRequest{
		Email:    "test@example.com",
		Password: "SecurePass123",
		Name:     "Test User",
	}

	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/register", bytes.NewBuffer(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	err := handler.Register(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusCreated, rec.Code)

	var response RegisterResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "test@example.com", response.User.Email)
	assert.Equal(t, "Test User", response.User.Name)
	assert.NotEmpty(t, response.Token)
}

func TestRegisterValidationErrors(t *testing.T) {
	handler, _, cleanup := setupTestHandler()
	defer cleanup()

	tests := []struct {
		name    string
		request RegisterRequest
		status  int
	}{
		{
			name: "empty email",
			request: RegisterRequest{
				Email:    "",
				Password: "SecurePass123",
				Name:     "Test User",
			},
			status: http.StatusBadRequest,
		},
		{
			name: "invalid email",
			request: RegisterRequest{
				Email:    "invalid-email",
				Password: "SecurePass123",
				Name:     "Test User",
			},
			status: http.StatusBadRequest,
		},
		{
			name: "weak password",
			request: RegisterRequest{
				Email:    "test@example.com",
				Password: "123",
				Name:     "Test User",
			},
			status: http.StatusBadRequest,
		},
		{
			name: "empty name",
			request: RegisterRequest{
				Email:    "test@example.com",
				Password: "SecurePass123",
				Name:     "",
			},
			status: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			reqBody, _ := json.Marshal(tt.request)
			req := httptest.NewRequest(http.MethodPost, "/register", bytes.NewBuffer(reqBody))
			req.Header.Set("Content-Type", "application/json")
			rec := httptest.NewRecorder()

			e := echo.New()
			c := e.NewContext(req, rec)

			err := handler.Register(c)
			assert.NoError(t, err)
			assert.Equal(t, tt.status, rec.Code)
		})
	}
}

func TestRegisterDuplicateEmail(t *testing.T) {
	handler, db, cleanup := setupTestHandler()
	defer cleanup()

	// Create existing user
	hashedPassword, _ := auth.HashPassword("SecurePass123")
	existingUser := &models.User{
		Email:    "existing@example.com",
		Password: hashedPassword,
		Name:     "Existing User",
		Role:     "user",
	}
	db.Create(existingUser)

	// Try to register with same email
	registerReq := RegisterRequest{
		Email:    "existing@example.com",
		Password: "NewSecurePass123",
		Name:     "New User",
	}

	reqBody, _ := json.Marshal(registerReq)
	req := httptest.NewRequest(http.MethodPost, "/register", bytes.NewBuffer(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	err := handler.Register(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusConflict, rec.Code)
}

func TestLogin(t *testing.T) {
	handler, db, cleanup := setupTestHandler()
	defer cleanup()

	// Create test user
	hashedPassword, _ := auth.HashPassword("SecurePass123")
	user := &models.User{
		Email:    "login@example.com",
		Password: hashedPassword,
		Name:     "Login User",
		Role:     "user",
	}
	db.Create(user)

	// Test successful login
	loginReq := LoginRequest{
		Email:    "login@example.com",
		Password: "SecurePass123",
	}

	reqBody, _ := json.Marshal(loginReq)
	req := httptest.NewRequest(http.MethodPost, "/login", bytes.NewBuffer(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	err := handler.Login(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response LoginResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "login@example.com", response.User.Email)
	assert.NotEmpty(t, response.Token)
}

func TestLoginInvalidCredentials(t *testing.T) {
	handler, db, cleanup := setupTestHandler()
	defer cleanup()

	// Create test user
	hashedPassword, _ := auth.HashPassword("SecurePass123")
	user := &models.User{
		Email:    "login@example.com",
		Password: hashedPassword,
		Name:     "Login User",
		Role:     "user",
	}
	db.Create(user)

	tests := []struct {
		name    string
		request LoginRequest
		status  int
	}{
		{
			name: "wrong password",
			request: LoginRequest{
				Email:    "login@example.com",
				Password: "wrongpassword",
			},
			status: http.StatusUnauthorized,
		},
		{
			name: "non-existent email",
			request: LoginRequest{
				Email:    "nonexistent@example.com",
				Password: "SecurePass123",
			},
			status: http.StatusUnauthorized,
		},
		{
			name: "empty email",
			request: LoginRequest{
				Email:    "",
				Password: "SecurePass123",
			},
			status: http.StatusBadRequest,
		},
		{
			name: "empty password",
			request: LoginRequest{
				Email:    "login@example.com",
				Password: "",
			},
			status: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			reqBody, _ := json.Marshal(tt.request)
			req := httptest.NewRequest(http.MethodPost, "/login", bytes.NewBuffer(reqBody))
			req.Header.Set("Content-Type", "application/json")
			rec := httptest.NewRecorder()

			e := echo.New()
			c := e.NewContext(req, rec)

			err := handler.Login(c)
			assert.NoError(t, err)
			assert.Equal(t, tt.status, rec.Code)
		})
	}
}

func TestGetProfile(t *testing.T) {
	handler, db, cleanup := setupTestHandler()
	defer cleanup()

	// Create test user
	user := &models.User{
		Email: "profile@example.com",
		Name:  "Profile User",
		Role:  "user",
	}
	db.Create(user)

	req := httptest.NewRequest(http.MethodGet, "/profile", nil)
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	// Set user context (simulating middleware)
	claims := &auth.Claims{
		UserID: "1",
		Role:   "user",
	}
	c.Set("user", claims)

	err := handler.GetProfile(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response UserResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "profile@example.com", response.Email)
}

func TestGetProfileUnauthorized(t *testing.T) {
	handler, _, cleanup := setupTestHandler()
	defer cleanup()

	req := httptest.NewRequest(http.MethodGet, "/profile", nil)
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	// No user context set
	err := handler.GetProfile(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestRefreshToken(t *testing.T) {
	handler, _, cleanup := setupTestHandler()
	defer cleanup()

	// Create a valid token
	jwtManager := auth.NewJWTManager("test-secret-key")
	originalToken, _ := jwtManager.GenerateToken("1", "user", 1*time.Hour)

	refreshReq := RefreshTokenRequest{
		Token: originalToken,
	}

	reqBody, _ := json.Marshal(refreshReq)
	req := httptest.NewRequest(http.MethodPost, "/refresh", bytes.NewBuffer(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	err := handler.RefreshToken(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	var response RefreshTokenResponse
	err = json.Unmarshal(rec.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.NotEmpty(t, response.Token)
	assert.NotEqual(t, originalToken, response.Token)
}

func TestRefreshTokenInvalid(t *testing.T) {
	handler, _, cleanup := setupTestHandler()
	defer cleanup()

	refreshReq := RefreshTokenRequest{
		Token: "invalid.token.here",
	}

	reqBody, _ := json.Marshal(refreshReq)
	req := httptest.NewRequest(http.MethodPost, "/refresh", bytes.NewBuffer(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rec := httptest.NewRecorder()

	e := echo.New()
	c := e.NewContext(req, rec)

	err := handler.RefreshToken(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}