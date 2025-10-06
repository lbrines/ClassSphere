package auth

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestHashPassword(t *testing.T) {
	password := "testSecurePass123"

	hashedPassword, err := HashPassword(password)
	assert.NoError(t, err)
	assert.NotEmpty(t, hashedPassword)
	assert.NotEqual(t, password, hashedPassword)

	// Test that the same password produces different hashes (due to salt)
	hashedPassword2, err := HashPassword(password)
	assert.NoError(t, err)
	assert.NotEqual(t, hashedPassword, hashedPassword2)
}

func TestCheckPassword(t *testing.T) {
	password := "testSecurePass123"
	wrongPassword := "wrongpassword"

	hashedPassword, err := HashPassword(password)
	assert.NoError(t, err)

	// Test correct password
	isValid := CheckPassword(password, hashedPassword)
	assert.True(t, isValid)

	// Test wrong password
	isValid = CheckPassword(wrongPassword, hashedPassword)
	assert.False(t, isValid)

	// Test empty password
	isValid = CheckPassword("", hashedPassword)
	assert.False(t, isValid)

	// Test empty hash
	isValid = CheckPassword(password, "")
	assert.False(t, isValid)
}

func TestHashPasswordEmpty(t *testing.T) {
	// Test empty password
	hashedPassword, err := HashPassword("")
	assert.NoError(t, err)
	assert.NotEmpty(t, hashedPassword)

	// Should be able to verify empty password
	isValid := CheckPassword("", hashedPassword)
	assert.True(t, isValid)
}

func TestCheckPasswordInvalidHash(t *testing.T) {
	password := "testSecurePass123"

	// Test with invalid hash
	isValid := CheckPassword(password, "invalid_hash")
	assert.False(t, isValid)

	// Test with malformed hash
	isValid = CheckPassword(password, "$2a$10$invalid")
	assert.False(t, isValid)
}

func TestPasswordStrength(t *testing.T) {
	// Test weak password
	err := ValidatePasswordStrength("123")
	assert.Error(t, err)

	// Test password too short
	err = ValidatePasswordStrength("short")
	assert.Error(t, err)

	// Test strong password
	err = ValidatePasswordStrength("StrongPassword123!")
	assert.NoError(t, err)

	// Test minimum acceptable password
	err = ValidatePasswordStrength("ValidPass123")
	assert.NoError(t, err)
}

func TestPasswordComplexity(t *testing.T) {
	// Test password with only lowercase
	err := ValidatePasswordStrength("lowercase")
	assert.Error(t, err)

	// Test password with only numbers
	err = ValidatePasswordStrength("12345678")
	assert.Error(t, err)

	// Test password with letters and numbers
	err = ValidatePasswordStrength("ValidPass123")
	assert.NoError(t, err)

	// Test password with special characters
	err = ValidatePasswordStrength("Password123!")
	assert.NoError(t, err)
}