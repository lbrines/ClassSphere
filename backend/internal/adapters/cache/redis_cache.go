package cache

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

// RedisCache implements ports.Cache backed by Redis.
type RedisCache struct {
	client redis.UniversalClient
}

// NewRedisCache accepts a configured redis client.
func NewRedisCache(client redis.UniversalClient) *RedisCache {
	return &RedisCache{client: client}
}

func (c *RedisCache) Set(ctx context.Context, key string, value []byte, ttlSeconds int) error {
	return c.client.Set(ctx, key, value, time.Duration(ttlSeconds)*time.Second).Err()
}

func (c *RedisCache) Get(ctx context.Context, key string) ([]byte, error) {
	cmd := c.client.Get(ctx, key)
	value, err := cmd.Bytes()
	if err == redis.Nil {
		return nil, nil
	}
	return value, err
}

func (c *RedisCache) Delete(ctx context.Context, key string) error {
	return c.client.Del(ctx, key).Err()
}

func (c *RedisCache) Ping(ctx context.Context) error {
	return c.client.Ping(ctx).Err()
}

func (c *RedisCache) Close() error {
	return c.client.Close()
}
