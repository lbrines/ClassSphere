package shared_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/shared"
)

func TestLoggerSingleton(t *testing.T) {
	logger1 := shared.Logger()
	logger2 := shared.Logger()
	require.NotNil(t, logger1)
	require.Equal(t, logger1, logger2)
}

func TestWithContext(t *testing.T) {
	ctx := context.WithValue(context.Background(), "request_id", "abc123")
	logger := shared.WithContext(ctx)
	require.NotNil(t, logger)
}
