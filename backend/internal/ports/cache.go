package ports

import (
	"context"
	"errors"
)

// Cache outlines simple cache operations required by the application.
type Cache interface {
	Set(ctx context.Context, key string, value []byte, ttlSeconds int) error
	Get(ctx context.Context, key string) ([]byte, error)
	Delete(ctx context.Context, key string) error
	Ping(ctx context.Context) error
	Close() error
}

// Cache errors
var (
	ErrCacheUnavailable = errors.New("cache unavailable")
)
