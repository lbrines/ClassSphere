package auth

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGenerateRandomPassword(t *testing.T) {
	// Test password generation
	password, err := GenerateRandomPassword(12)
	assert.NoError(t, err)
	assert.Len(t, password, 12)
	assert.NotEmpty(t, password)

	// Test different lengths
	password8, err := GenerateRandomPassword(8)
	assert.NoError(t, err)
	assert.Len(t, password8, 8)

	password16, err := GenerateRandomPassword(16)
	assert.NoError(t, err)
	assert.Len(t, password16, 16)

	// Test that passwords are different
	assert.NotEqual(t, password, password8)
	assert.NotEqual(t, password, password16)
	assert.NotEqual(t, password8, password16)
}

func TestValidatePasswordStrength_EdgeCases(t *testing.T) {
	// Test empty password
	err := ValidatePasswordStrength("")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Password is required")

	// Test very short password
	err = ValidatePasswordStrength("123")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "at least 8 characters")

	// Test password without uppercase
	err = ValidatePasswordStrength("password123")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "uppercase letter")

	// Test password without lowercase
	err = ValidatePasswordStrength("PASSWORD123")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "lowercase letter")

	// Test password without number
	err = ValidatePasswordStrength("Password")
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "number")

	// Test valid password
	err = ValidatePasswordStrength("Password123")
	assert.NoError(t, err)

	// Test very strong password
	err = ValidatePasswordStrength("MyStr0ng!P@ssw0rd")
	assert.NoError(t, err)
}