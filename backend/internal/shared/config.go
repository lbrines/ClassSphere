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
	
	// Parse multiple origins with smart defaults based on environment
	cfg.AllowedOrigins = parseAllowedOrigins(cfg.Environment, cfg.FrontendURL)

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

// parseAllowedOrigins determines allowed CORS origins based on environment.
//
// This function implements a three-tier priority system for CORS configuration:
//
// 1. Explicit Configuration (Highest Priority):
//    If ALLOWED_ORIGINS environment variable is set, it takes precedence.
//    Format: Comma-separated list of origins (e.g., "http://localhost,https://example.com")
//
// 2. Environment-Specific Defaults (Medium Priority):
//    - Production: Only allows the configured FrontendURL (most restrictive)
//    - Development/Test/Local: Allows common local development origins:
//      * http://localhost (browser default, no port)
//      * http://localhost:80 (explicit port 80, Docker frontend container)
//      * http://localhost:4200 (Angular dev server default)
//      * http://localhost:8080 (backend, for testing)
//
// 3. Fallback (Lowest Priority):
//    Falls back to FrontendURL for unknown environments
//
// This design fixes the CORS issue where the frontend container (running on port 80)
// couldn't communicate with the backend. It also supports multiple deployment modes:
// mock, test, development, and production.
//
// Security Considerations:
// - Production mode is restrictive by design (single origin only)
// - Development modes allow multiple localhost variations for flexibility
// - Explicit ALLOWED_ORIGINS always overrides defaults for custom setups
//
// TDD Implementation: Tests in cors_test.go verify all scenarios
func parseAllowedOrigins(environment, frontendURL string) []string {
	// 1. If ALLOWED_ORIGINS is explicitly set, use it
	if originsStr := os.Getenv("ALLOWED_ORIGINS"); originsStr != "" {
		origins := strings.Split(originsStr, ",")
		result := make([]string, 0, len(origins))
		for _, origin := range origins {
			trimmed := strings.TrimSpace(origin)
			if trimmed != "" {
				result = append(result, trimmed)
			}
		}
		return result
	}
	
	// 2. Use environment-specific defaults
	switch environment {
	case EnvProduction:
		// Production: Only allow explicitly configured frontend URL
		return []string{frontendURL}
		
	case EnvDevelopment, EnvLocal, "test":
		// Development/Test: Allow common local development origins
		// This fixes the localhost:80 CORS issue
		return []string{
			"http://localhost",         // Browser default
			"http://localhost:80",      // Explicit port 80 (frontend container)
			"http://localhost:4200",    // Angular dev server
			"http://localhost:8080",    // Backend (for testing)
		}
		
	default:
		// Unknown environment: fallback to FrontendURL only
		return []string{frontendURL}
	}
}
