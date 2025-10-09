package shared

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const (
	defaultServerPort = 8080
	defaultRedisAddr  = "localhost:6379"
)

// Environment constants
const (
	EnvProduction  = "production"
	EnvDevelopment = "development"
	EnvLocal       = "local"
)

// Config groups runtime configuration sourced from environment variables.
type Config struct {
	Environment        string   // Environment: production, development, local
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
	GoogleCredentials  string
	ClassroomMode      string
	FrontendURL        string   // Single frontend URL (for simple setup)
	AllowedOrigins     []string // Multiple allowed origins (for production)
}

// LoadConfig constructs a Config instance using environment variables. It applies
// sane defaults for local development so the service can start without extensive setup.
func LoadConfig() (Config, error) {
	cfg := Config{
		Environment:        getEnv("APP_ENV", "development"),
		RedisAddr:          getEnv("REDIS_ADDR", defaultRedisAddr),
		RedisPassword:      os.Getenv("REDIS_PASSWORD"),
		GoogleClientID:     os.Getenv("GOOGLE_CLIENT_ID"),
		GoogleClientSecret: os.Getenv("GOOGLE_CLIENT_SECRET"),
		GoogleRedirectURL:  os.Getenv("GOOGLE_REDIRECT_URL"),
		JWTSecret:          os.Getenv("JWT_SECRET"),
		JWTIssuer:          getEnv("JWT_ISSUER", "classsphere"),
		GoogleCredentials:  os.Getenv("GOOGLE_CREDENTIALS_FILE"),
		ClassroomMode:      NormalizeIntegrationMode(getEnv("CLASSROOM_MODE", IntegrationModeMock)),
		FrontendURL:        getEnv("FRONTEND_URL", "http://localhost:4200"),
	}
	
	// Parse multiple origins if provided (comma-separated)
	if originsStr := os.Getenv("ALLOWED_ORIGINS"); originsStr != "" {
		origins := strings.Split(originsStr, ",")
		cfg.AllowedOrigins = make([]string, 0, len(origins))
		for _, origin := range origins {
			trimmed := strings.TrimSpace(origin)
			if trimmed != "" {
				cfg.AllowedOrigins = append(cfg.AllowedOrigins, trimmed)
			}
		}
	} else {
		// Default to FrontendURL if ALLOWED_ORIGINS not specified
		cfg.AllowedOrigins = []string{cfg.FrontendURL}
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
	if c.ClassroomMode == IntegrationModeGoogle && c.GoogleCredentials == "" {
		return fmt.Errorf("GOOGLE_CREDENTIALS_FILE must be provided for google classroom mode")
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
