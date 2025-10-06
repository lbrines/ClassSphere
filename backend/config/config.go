package config

import (
	"os"
)

type Config struct {
	JWTSecret      string
	DatabasePath   string
	RedisAddr      string
	RedisPassword  string
	RedisDB        int
	GoogleClientID string
	GoogleSecret   string
	Port           string
}

func Load() *Config {
	return &Config{
		JWTSecret:      getEnv("JWT_SECRET", "default-secret-key-for-development"),
		DatabasePath:   getEnv("DATABASE_PATH", "./classsphere.db"),
		RedisAddr:      getEnv("REDIS_ADDR", "localhost:6379"),
		RedisPassword:  getEnv("REDIS_PASSWORD", ""),
		RedisDB:        0,
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