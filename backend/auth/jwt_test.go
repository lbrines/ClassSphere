package auth

import (
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestGenerateToken(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Test successful token generation
	token, err := jwtManager.GenerateToken("user123", "admin", 24*time.Hour)
	assert.NoError(t, err)
	assert.NotEmpty(t, token)

	// Verify token format (should be JWT format with 3 parts)
	parts := len(strings.Split(token, "."))
	assert.Equal(t, 3, parts)
}

func TestValidateToken(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Generate a token first
	token, err := jwtManager.GenerateToken("user123", "admin", 24*time.Hour)
	assert.NoError(t, err)

	// Test successful validation
	claims, err := jwtManager.ValidateToken(token)
	assert.NoError(t, err)
	assert.NotNil(t, claims)
	assert.Equal(t, "user123", claims.Subject)
	assert.Equal(t, "admin", claims.Role)
}

func TestValidateTokenInvalid(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Test invalid token
	claims, err := jwtManager.ValidateToken("invalid.token.here")
	assert.Error(t, err)
	assert.Nil(t, claims)
}

func TestValidateTokenWrongSecret(t *testing.T) {
	jwtManager1 := NewJWTManager("secret1")
	jwtManager2 := NewJWTManager("secret2")

	// Generate token with first manager
	token, err := jwtManager1.GenerateToken("user123", "admin", 24*time.Hour)
	assert.NoError(t, err)

	// Try to validate with different secret
	claims, err := jwtManager2.ValidateToken(token)
	assert.Error(t, err)
	assert.Nil(t, claims)
}

func TestValidateTokenExpired(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Generate token with very short expiration
	token, err := jwtManager.GenerateToken("user123", "admin", 1*time.Nanosecond)
	assert.NoError(t, err)

	// Wait for token to expire
	time.Sleep(1 * time.Millisecond)

	// Test expired token validation
	claims, err := jwtManager.ValidateToken(token)
	assert.Error(t, err)
	assert.Nil(t, claims)
}

func TestRefreshToken(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Generate original token
	originalToken, err := jwtManager.GenerateToken("user123", "admin", 1*time.Hour)
	assert.NoError(t, err)

	// Test token refresh
	newToken, err := jwtManager.RefreshToken(originalToken, 2*time.Hour)
	assert.NoError(t, err)
	assert.NotEmpty(t, newToken)
	assert.NotEqual(t, originalToken, newToken)

	// Validate new token
	claims, err := jwtManager.ValidateToken(newToken)
	assert.NoError(t, err)
	assert.Equal(t, "user123", claims.Subject)
	assert.Equal(t, "admin", claims.Role)
}

func TestRefreshTokenInvalid(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Test refresh with invalid token
	newToken, err := jwtManager.RefreshToken("invalid.token.here", 1*time.Hour)
	assert.Error(t, err)
	assert.Empty(t, newToken)
}

func TestGetTokenClaims(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Generate token
	token, err := jwtManager.GenerateToken("user123", "admin", 1*time.Hour)
	assert.NoError(t, err)

	// Test getting claims without validation
	claims, err := jwtManager.GetTokenClaims(token)
	assert.NoError(t, err)
	assert.NotNil(t, claims)
	assert.Equal(t, "user123", claims.Subject)
	assert.Equal(t, "admin", claims.Role)
}

func TestJWTManagerEmptySecret(t *testing.T) {
	// Test that empty secret still creates manager but tokens won't validate properly
	jwtManager := NewJWTManager("")
	assert.NotNil(t, jwtManager)

	// Generate token with empty secret
	token, err := jwtManager.GenerateToken("user123", "admin", 1*time.Hour)
	assert.NoError(t, err)
	assert.NotEmpty(t, token)
}

func TestGenerateTokenEmptyUserID(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Test with empty user ID
	token, err := jwtManager.GenerateToken("", "admin", 1*time.Hour)
	assert.NoError(t, err)
	assert.NotEmpty(t, token)

	// Validate claims
	claims, err := jwtManager.ValidateToken(token)
	assert.NoError(t, err)
	assert.Equal(t, "", claims.Subject)
}

func TestGenerateTokenEmptyRole(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Test with empty role
	token, err := jwtManager.GenerateToken("user123", "", 1*time.Hour)
	assert.NoError(t, err)
	assert.NotEmpty(t, token)

	// Validate claims
	claims, err := jwtManager.ValidateToken(token)
	assert.NoError(t, err)
	assert.Equal(t, "", claims.Role)
}

func TestGenerateTokenZeroDuration(t *testing.T) {
	jwtManager := NewJWTManager("test-secret-key")

	// Test with zero duration (should create immediately expired token)
	token, err := jwtManager.GenerateToken("user123", "admin", 0)
	assert.NoError(t, err)
	assert.NotEmpty(t, token)

	// Token should be expired immediately
	claims, err := jwtManager.ValidateToken(token)
	assert.Error(t, err)
	assert.Nil(t, claims)
}

func TestValidateTokenWithRSASigningMethod(t *testing.T) {
	// Test validation with a token using RSA signing method instead of HMAC
	jwtManager := NewJWTManager("test-secret-key")

	// Create a token string manually with RSA prefix to test signing method validation
	// This will fail when jwt.ParseWithClaims checks the signing method
	invalidTokenWithRSA := "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.invalid_signature_for_rsa"

	// This should fail due to wrong signing method
	validatedClaims, err := jwtManager.ValidateToken(invalidTokenWithRSA)
	assert.Error(t, err)
	assert.Nil(t, validatedClaims)
}