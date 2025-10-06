package handlers

import (
	"net/http"
	"regexp"
	"strconv"
	"time"

	"classsphere-backend/auth"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
)

// AuthHandler handles authentication-related requests
type AuthHandler struct {
	userRepo   *models.UserRepository
	jwtManager *auth.JWTManager
}

// NewAuthHandler creates a new auth handler
func NewAuthHandler(userRepo *models.UserRepository, jwtManager *auth.JWTManager) *AuthHandler {
	return &AuthHandler{
		userRepo:   userRepo,
		jwtManager: jwtManager,
	}
}

// Request/Response types
type RegisterRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required,min=8"`
	Name     string `json:"name" validate:"required"`
}

type LoginRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Password string `json:"password" validate:"required"`
}

type RefreshTokenRequest struct {
	Token string `json:"token" validate:"required"`
}

type UserResponse struct {
	ID       uint   `json:"id"`
	Email    string `json:"email"`
	Name     string `json:"name"`
	Role     string `json:"role"`
	IsActive bool   `json:"is_active"`
}

type RegisterResponse struct {
	User  UserResponse `json:"user"`
	Token string       `json:"token"`
}

type LoginResponse struct {
	User  UserResponse `json:"user"`
	Token string       `json:"token"`
}

type RefreshTokenResponse struct {
	Token string `json:"token"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}

// Register handles user registration
func (h *AuthHandler) Register(c echo.Context) error {
	var req RegisterRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, ErrorResponse{Error: "Invalid request format"})
	}

	// Validate input
	if err := h.validateRegisterRequest(req); err != nil {
		return c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
	}

	// Check if user already exists
	existingUser, err := h.userRepo.GetUserByEmail(req.Email)
	if err == nil && existingUser != nil {
		return c.JSON(http.StatusConflict, ErrorResponse{Error: "User with this email already exists"})
	}

	// Hash password
	hashedPassword, err := auth.HashPassword(req.Password)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, ErrorResponse{Error: "Failed to process password"})
	}

	// Create user
	user := &models.User{
		Email:    req.Email,
		Password: hashedPassword,
		Name:     req.Name,
		Role:     "user", // Default role
		IsActive: true,
	}

	if err := h.userRepo.CreateUser(user); err != nil {
		return c.JSON(http.StatusInternalServerError, ErrorResponse{Error: "Failed to create user"})
	}

	// Generate JWT token
	token, err := h.jwtManager.GenerateToken(strconv.Itoa(int(user.ID)), user.Role, 24*time.Hour)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, ErrorResponse{Error: "Failed to generate token"})
	}

	response := RegisterResponse{
		User: UserResponse{
			ID:       user.ID,
			Email:    user.Email,
			Name:     user.Name,
			Role:     user.Role,
			IsActive: user.IsActive,
		},
		Token: token,
	}

	return c.JSON(http.StatusCreated, response)
}

// Login handles user authentication
func (h *AuthHandler) Login(c echo.Context) error {
	var req LoginRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, ErrorResponse{Error: "Invalid request format"})
	}

	// Validate input
	if err := h.validateLoginRequest(req); err != nil {
		return c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
	}

	// Get user by email
	user, err := h.userRepo.GetUserByEmail(req.Email)
	if err != nil {
		return c.JSON(http.StatusUnauthorized, ErrorResponse{Error: "Invalid credentials"})
	}

	// Check password
	if !auth.CheckPassword(req.Password, user.Password) {
		return c.JSON(http.StatusUnauthorized, ErrorResponse{Error: "Invalid credentials"})
	}

	// Generate JWT token
	token, err := h.jwtManager.GenerateToken(strconv.Itoa(int(user.ID)), user.Role, 24*time.Hour)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, ErrorResponse{Error: "Failed to generate token"})
	}

	response := LoginResponse{
		User: UserResponse{
			ID:       user.ID,
			Email:    user.Email,
			Name:     user.Name,
			Role:     user.Role,
			IsActive: user.IsActive,
		},
		Token: token,
	}

	return c.JSON(http.StatusOK, response)
}

// GetProfile returns the current user's profile
func (h *AuthHandler) GetProfile(c echo.Context) error {
	// Get user from context (set by JWT middleware)
	userClaims, ok := auth.GetCurrentUser(c)
	if !ok {
		return c.JSON(http.StatusUnauthorized, ErrorResponse{Error: "User not authenticated"})
	}

	// Convert user ID from string to uint
	userID, err := strconv.ParseUint(userClaims.UserID, 10, 32)
	if err != nil {
		return c.JSON(http.StatusBadRequest, ErrorResponse{Error: "Invalid user ID"})
	}

	// Get user from database
	user, err := h.userRepo.GetUserByID(uint(userID))
	if err != nil {
		return c.JSON(http.StatusNotFound, ErrorResponse{Error: "User not found"})
	}

	response := UserResponse{
		ID:       user.ID,
		Email:    user.Email,
		Name:     user.Name,
		Role:     user.Role,
		IsActive: user.IsActive,
	}

	return c.JSON(http.StatusOK, response)
}

// RefreshToken generates a new token from an existing valid token
func (h *AuthHandler) RefreshToken(c echo.Context) error {
	var req RefreshTokenRequest
	if err := c.Bind(&req); err != nil {
		return c.JSON(http.StatusBadRequest, ErrorResponse{Error: "Invalid request format"})
	}

	// Refresh the token
	newToken, err := h.jwtManager.RefreshToken(req.Token, 24*time.Hour)
	if err != nil {
		return c.JSON(http.StatusUnauthorized, ErrorResponse{Error: "Invalid or expired token"})
	}

	response := RefreshTokenResponse{
		Token: newToken,
	}

	return c.JSON(http.StatusOK, response)
}

// Helper functions for validation
func (h *AuthHandler) validateRegisterRequest(req RegisterRequest) error {
	if req.Email == "" {
		return echo.NewHTTPError(http.StatusBadRequest, "Email is required")
	}

	if !h.isValidEmail(req.Email) {
		return echo.NewHTTPError(http.StatusBadRequest, "Invalid email format")
	}

	if req.Name == "" {
		return echo.NewHTTPError(http.StatusBadRequest, "Name is required")
	}

	if len(req.Name) < 2 {
		return echo.NewHTTPError(http.StatusBadRequest, "Name must be at least 2 characters long")
	}

	// Validate password strength
	if err := auth.ValidatePasswordStrength(req.Password); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	return nil
}

func (h *AuthHandler) validateLoginRequest(req LoginRequest) error {
	if req.Email == "" {
		return echo.NewHTTPError(http.StatusBadRequest, "Email is required")
	}

	if req.Password == "" {
		return echo.NewHTTPError(http.StatusBadRequest, "Password is required")
	}

	return nil
}

func (h *AuthHandler) isValidEmail(email string) bool {
	emailRegex := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
	return emailRegex.MatchString(email)
}