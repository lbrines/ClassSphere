package shared_test

import (
	"testing"

	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/shared"
)

func TestLoadConfigSuccess(t *testing.T) {
	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "client-secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("SERVER_PORT", "8080")

	cfg, err := shared.LoadConfig()
	require.NoError(t, err)
	require.Equal(t, 8080, cfg.ServerPort)
}

func TestLoadConfigValidation(t *testing.T) {
	t.Setenv("JWT_SECRET", "")
	t.Setenv("GOOGLE_CLIENT_ID", "")
	t.Setenv("GOOGLE_CLIENT_SECRET", "")
	t.Setenv("GOOGLE_REDIRECT_URL", "")

	_, err := shared.LoadConfig()
	require.Error(t, err)
}

// === ADDITIONAL TESTS FOR 80% COVERAGE ===

func TestLoadConfig_InvalidServerPort(t *testing.T) {
	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "client-secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("SERVER_PORT", "invalid")

	_, err := shared.LoadConfig()
	require.Error(t, err)
	require.Contains(t, err.Error(), "invalid SERVER_PORT")
}

func TestLoadConfig_InvalidJWTExpiry(t *testing.T) {
	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "client-secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("JWT_EXPIRY_MINUTES", "invalid")

	_, err := shared.LoadConfig()
	require.Error(t, err)
	require.Contains(t, err.Error(), "invalid JWT_EXPIRY_MINUTES")
}

func TestLoadConfig_InvalidRedisDB(t *testing.T) {
	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "client-secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")
	t.Setenv("REDIS_DB", "invalid")

	_, err := shared.LoadConfig()
	require.Error(t, err)
	require.Contains(t, err.Error(), "invalid REDIS_DB")
}

func TestConfigValidate_MissingFields(t *testing.T) {
	t.Run("missing JWT_SECRET", func(t *testing.T) {
		cfg := shared.Config{
			GoogleClientID:     "client",
			GoogleClientSecret: "secret",
			GoogleRedirectURL:  "http://localhost",
		}
		err := cfg.Validate()
		require.Error(t, err)
		require.Contains(t, err.Error(), "JWT_SECRET")
	})

	t.Run("missing GOOGLE_CLIENT_ID", func(t *testing.T) {
		cfg := shared.Config{
			JWTSecret:          "secret",
			GoogleClientSecret: "secret",
			GoogleRedirectURL:  "http://localhost",
		}
		err := cfg.Validate()
		require.Error(t, err)
		require.Contains(t, err.Error(), "GOOGLE_CLIENT_ID")
	})

	t.Run("missing GOOGLE_CLIENT_SECRET", func(t *testing.T) {
		cfg := shared.Config{
			JWTSecret:         "secret",
			GoogleClientID:    "client",
			GoogleRedirectURL: "http://localhost",
		}
		err := cfg.Validate()
		require.Error(t, err)
		require.Contains(t, err.Error(), "GOOGLE_CLIENT_SECRET")
	})

	t.Run("missing GOOGLE_REDIRECT_URL", func(t *testing.T) {
		cfg := shared.Config{
			JWTSecret:          "secret",
			GoogleClientID:     "client",
			GoogleClientSecret: "secret",
		}
		err := cfg.Validate()
		require.Error(t, err)
		require.Contains(t, err.Error(), "GOOGLE_REDIRECT_URL")
	})
}

func TestLoadConfig_Defaults(t *testing.T) {
	t.Setenv("JWT_SECRET", "secret")
	t.Setenv("GOOGLE_CLIENT_ID", "client")
	t.Setenv("GOOGLE_CLIENT_SECRET", "client-secret")
	t.Setenv("GOOGLE_REDIRECT_URL", "http://localhost/callback")

	cfg, err := shared.LoadConfig()
	require.NoError(t, err)
	
	// Verify defaults
	require.Equal(t, "development", cfg.AppEnv)
	require.Equal(t, "localhost:6379", cfg.RedisAddr)
	require.Equal(t, "classsphere", cfg.JWTIssuer)
	require.Equal(t, 8080, cfg.ServerPort)
	require.Equal(t, 60, cfg.JWTExpiryMinutes)
	require.Equal(t, 0, cfg.RedisDB)
}
