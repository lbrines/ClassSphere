package shared

import (
	"context"
	"log/slog"
	"os"
	"sync"
)

var (
	logger     *slog.Logger
	loggerOnce sync.Once
)

// Logger returns a shared structured logger configured for the current environment.
func Logger() *slog.Logger {
	loggerOnce.Do(func() {
		handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
			Level: slog.LevelInfo,
		})
		logger = slog.New(handler)
	})
	return logger
}

// WithContext enriches a logger with the provided context.
func WithContext(ctx context.Context) *slog.Logger {
	return Logger().With(slog.Any("context", ctx.Value("request_id")))
}
