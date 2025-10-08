package cache_test

import (
	"context"
	"testing"
	"time"

	"github.com/alicebob/miniredis/v2"
	"github.com/redis/go-redis/v9"
	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/adapters/cache"
)

func TestRedisCache(t *testing.T) {
	srv, err := miniredis.Run()
	require.NoError(t, err)
	defer srv.Close()

	client := redis.NewClient(&redis.Options{Addr: srv.Addr()})
	cacheAdapter := cache.NewRedisCache(client)

	ctx := context.Background()
	require.NoError(t, cacheAdapter.Ping(ctx))

	require.NoError(t, cacheAdapter.Set(ctx, "token", []byte("value"), 1))
	value, err := cacheAdapter.Get(ctx, "token")
	require.NoError(t, err)
	require.Equal(t, []byte("value"), value)

	srv.FastForward(2 * time.Second)
	value, err = cacheAdapter.Get(ctx, "token")
	require.NoError(t, err)
	require.Nil(t, value)

	require.NoError(t, cacheAdapter.Set(ctx, "token", []byte("value"), 10))
	require.NoError(t, cacheAdapter.Delete(ctx, "token"))
	value, err = cacheAdapter.Get(ctx, "token")
	require.NoError(t, err)
	require.Nil(t, value)

	require.NoError(t, cacheAdapter.Close())
}
