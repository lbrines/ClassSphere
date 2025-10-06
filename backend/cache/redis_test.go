package cache

import (
	"context"
	"testing"
	"time"

	"github.com/alicebob/miniredis/v2"
	"github.com/go-redis/redis/v8"
	"github.com/stretchr/testify/assert"
)

func TestRedisConnection(t *testing.T) {
	// Mock Redis server with miniredis
	mockRedis := miniredis.RunT(t)
	defer mockRedis.Close()

	client := redis.NewClient(&redis.Options{
		Addr: mockRedis.Addr(),
	})
	defer client.Close()

	cache := NewRedisCache(client)

	// Test Set/Get
	ctx := context.Background()
	err := cache.Set(ctx, "key1", "value1", 5*time.Minute)
	assert.NoError(t, err)

	val, err := cache.Get(ctx, "key1")
	assert.NoError(t, err)
	assert.Equal(t, "value1", val)
}

func TestRedisSetExpiration(t *testing.T) {
	mockRedis := miniredis.RunT(t)
	defer mockRedis.Close()

	client := redis.NewClient(&redis.Options{
		Addr: mockRedis.Addr(),
	})
	defer client.Close()

	cache := NewRedisCache(client)
	ctx := context.Background()

	// Set with 1 second expiration
	err := cache.Set(ctx, "expire_key", "expire_value", 1*time.Second)
	assert.NoError(t, err)

	// Fast forward time in miniredis
	mockRedis.FastForward(2 * time.Second)

	// Key should be expired
	val, err := cache.Get(ctx, "expire_key")
	assert.Error(t, err)
	assert.Equal(t, "", val)
	assert.Equal(t, redis.Nil, err)
}

func TestRedisDelete(t *testing.T) {
	mockRedis := miniredis.RunT(t)
	defer mockRedis.Close()

	client := redis.NewClient(&redis.Options{
		Addr: mockRedis.Addr(),
	})
	defer client.Close()

	cache := NewRedisCache(client)
	ctx := context.Background()

	// Set and then delete
	err := cache.Set(ctx, "delete_key", "delete_value", 5*time.Minute)
	assert.NoError(t, err)

	err = cache.Delete(ctx, "delete_key")
	assert.NoError(t, err)

	// Key should not exist
	val, err := cache.Get(ctx, "delete_key")
	assert.Error(t, err)
	assert.Equal(t, "", val)
	assert.Equal(t, redis.Nil, err)
}

func TestRedisConnectionFailure(t *testing.T) {
	// Test connection failure handling
	client := redis.NewClient(&redis.Options{
		Addr: "invalid:6379",
	})
	defer client.Close()

	cache := NewRedisCache(client)
	ctx := context.Background()

	// Should handle connection error gracefully
	err := cache.Set(ctx, "key", "value", time.Minute)
	assert.Error(t, err)
}

func TestRedisExists(t *testing.T) {
	mockRedis := miniredis.RunT(t)
	defer mockRedis.Close()

	client := redis.NewClient(&redis.Options{
		Addr: mockRedis.Addr(),
	})
	defer client.Close()

	cache := NewRedisCache(client)
	ctx := context.Background()

	// Test key doesn't exist
	exists, err := cache.Exists(ctx, "nonexistent")
	assert.NoError(t, err)
	assert.False(t, exists)

	// Set key and test it exists
	err = cache.Set(ctx, "exists_key", "value", 5*time.Minute)
	assert.NoError(t, err)

	exists, err = cache.Exists(ctx, "exists_key")
	assert.NoError(t, err)
	assert.True(t, exists)
}

func TestRedisExistsConnectionError(t *testing.T) {
	// Test connection error for Exists method
	client := redis.NewClient(&redis.Options{
		Addr: "invalid:6379",
	})
	defer client.Close()

	cache := NewRedisCache(client)
	ctx := context.Background()

	// Should handle connection error gracefully in Exists
	exists, err := cache.Exists(ctx, "key")
	assert.Error(t, err)
	assert.False(t, exists)
}

func TestNewRedisClient(t *testing.T) {
	// Test NewRedisClient function
	client := NewRedisClient("localhost:6379", "", 0)
	assert.NotNil(t, client)

	// Verify client configuration
	opts := client.Options()
	assert.Equal(t, "localhost:6379", opts.Addr)
	assert.Equal(t, "", opts.Password)
	assert.Equal(t, 0, opts.DB)

	client.Close()
}

func TestNewRedisClientWithAuth(t *testing.T) {
	// Test NewRedisClient with authentication
	client := NewRedisClient("localhost:6379", "password123", 1)
	assert.NotNil(t, client)

	// Verify client configuration with auth
	opts := client.Options()
	assert.Equal(t, "localhost:6379", opts.Addr)
	assert.Equal(t, "password123", opts.Password)
	assert.Equal(t, 1, opts.DB)

	client.Close()
}