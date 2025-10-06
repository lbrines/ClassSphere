package config

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestLoadConfig(t *testing.T) {
	// Test environment variables
	os.Setenv("JWT_SECRET", "test-secret")
	os.Setenv("REDIS_URL", "localhost:6379")
	os.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	os.Setenv("GOOGLE_SECRET", "test-secret")

	cfg := LoadConfig()

	assert.Equal(t, "test-secret", cfg.JWTSecret)
	assert.Equal(t, "localhost:6379", cfg.RedisURL)
	assert.Equal(t, "test-client-id", cfg.GoogleClientID)
	assert.Equal(t, "test-secret", cfg.GoogleSecret)

	// Cleanup
	os.Unsetenv("JWT_SECRET")
	os.Unsetenv("REDIS_URL")
	os.Unsetenv("GOOGLE_CLIENT_ID")
	os.Unsetenv("GOOGLE_SECRET")
}

func TestConfigValidation(t *testing.T) {
	// Test missing required config
	os.Unsetenv("JWT_SECRET")

	assert.Panics(t, func() {
		LoadConfig()
	})
}

func TestGetEnvDefault(t *testing.T) {
	// Test default value when env var not set
	os.Unsetenv("TEST_VAR")
	value := getEnv("TEST_VAR", "default-value")
	assert.Equal(t, "default-value", value)

	// Test actual value when env var is set
	os.Setenv("TEST_VAR", "actual-value")
	value = getEnv("TEST_VAR", "default-value")
	assert.Equal(t, "actual-value", value)

	// Cleanup
	os.Unsetenv("TEST_VAR")
}