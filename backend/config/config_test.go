package config

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestLoadConfig(t *testing.T) {
	// Test environment variables
	os.Setenv("JWT_SECRET", "test-secret")
	os.Setenv("DATABASE_PATH", "./test.db")
	os.Setenv("REDIS_ADDR", "localhost:6379")
	os.Setenv("GOOGLE_CLIENT_ID", "test-client-id")
	os.Setenv("GOOGLE_SECRET", "test-secret")

	cfg := Load()

	assert.Equal(t, "test-secret", cfg.JWTSecret)
	assert.Equal(t, "./test.db", cfg.DatabasePath)
	assert.Equal(t, "localhost:6379", cfg.RedisAddr)
	assert.Equal(t, "test-client-id", cfg.GoogleClientID)
	assert.Equal(t, "test-secret", cfg.GoogleSecret)

	// Cleanup
	os.Unsetenv("JWT_SECRET")
	os.Unsetenv("DATABASE_PATH")
	os.Unsetenv("REDIS_ADDR")
	os.Unsetenv("GOOGLE_CLIENT_ID")
	os.Unsetenv("GOOGLE_SECRET")
}

func TestConfigDefaults(t *testing.T) {
	// Test default values
	os.Unsetenv("JWT_SECRET")
	os.Unsetenv("DATABASE_PATH")
	os.Unsetenv("REDIS_ADDR")

	cfg := Load()

	assert.Equal(t, "default-secret-key-for-development", cfg.JWTSecret)
	assert.Equal(t, "./classsphere.db", cfg.DatabasePath)
	assert.Equal(t, "localhost:6379", cfg.RedisAddr)
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