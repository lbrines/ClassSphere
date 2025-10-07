package shared

import (
	"fmt"
	"os"
	"strconv"
)

const (
	defaultServerPort = 8080
	defaultRedisAddr  = "localhost:6379"
)

// Config groups runtime configuration sourced from environment variables.
type Config struct {
	AppEnv             string
	ServerPort         int
	JWTSecret          string
	JWTIssuer          string
	JWTExpiryMinutes   int
	RedisAddr          string
	RedisPassword      string
	RedisDB            int
	GoogleClientID     string
	GoogleClientSecret string
	GoogleRedirectURL  string
}

// LoadConfig constructs a Config instance using environment variables. It applies
// sane defaults for local development so the service can start without extensive setup.
func LoadConfig() (Config, error) {
	cfg := Config{
		AppEnv:             getEnv("APP_ENV", "development"),
		RedisAddr:          getEnv("REDIS_ADDR", defaultRedisAddr),
		RedisPassword:      os.Getenv("REDIS_PASSWORD"),
		GoogleClientID:     os.Getenv("GOOGLE_CLIENT_ID"),
		GoogleClientSecret: os.Getenv("GOOGLE_CLIENT_SECRET"),
		GoogleRedirectURL:  os.Getenv("GOOGLE_REDIRECT_URL"),
		JWTSecret:          os.Getenv("JWT_SECRET"),
		JWTIssuer:          getEnv("JWT_ISSUER", "classsphere"),
	}

	port, err := parseIntEnv("SERVER_PORT", defaultServerPort)
	if err != nil {
		return Config{}, fmt.Errorf("invalid SERVER_PORT: %w", err)
	}
	cfg.ServerPort = port

	expiryMinutes, err := parseIntEnv("JWT_EXPIRY_MINUTES", 60)
	if err != nil {
		return Config{}, fmt.Errorf("invalid JWT_EXPIRY_MINUTES: %w", err)
	}
	cfg.JWTExpiryMinutes = expiryMinutes

	redisDB, err := parseIntEnv("REDIS_DB", 0)
	if err != nil {
		return Config{}, fmt.Errorf("invalid REDIS_DB: %w", err)
	}
	cfg.RedisDB = redisDB

	return cfg, cfg.Validate()
}

// Validate ensures required configuration is present for secure operation.
func (c Config) Validate() error {
	if c.JWTSecret == "" {
		return fmt.Errorf("JWT_SECRET must be provided")
	}
	if c.GoogleClientID == "" {
		return fmt.Errorf("GOOGLE_CLIENT_ID must be provided")
	}
	if c.GoogleClientSecret == "" {
		return fmt.Errorf("GOOGLE_CLIENT_SECRET must be provided")
	}
	if c.GoogleRedirectURL == "" {
		return fmt.Errorf("GOOGLE_REDIRECT_URL must be provided")
	}
	return nil
}

func getEnv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func parseIntEnv(key string, fallback int) (int, error) {
	raw := os.Getenv(key)
	if raw == "" {
		return fallback, nil
	}
	value, err := strconv.Atoi(raw)
	if err != nil {
		return 0, err
	}
	return value, nil
}
