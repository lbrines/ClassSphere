package config

import (
	"os"
)

type Config struct {
	JWTSecret      string
	RedisURL       string
	GoogleClientID string
	GoogleSecret   string
	Port           string
}

func LoadConfig() *Config {
	jwtSecret := os.Getenv("JWT_SECRET")
	if jwtSecret == "" {
		panic("JWT_SECRET is required")
	}

	return &Config{
		JWTSecret:      jwtSecret,
		RedisURL:       getEnv("REDIS_URL", "localhost:6379"),
		GoogleClientID: os.Getenv("GOOGLE_CLIENT_ID"),
		GoogleSecret:   os.Getenv("GOOGLE_SECRET"),
		Port:           getEnv("PORT", "8080"),
	}
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}