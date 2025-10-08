package app_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/shared"
)

func TestUserService(t *testing.T) {
	repo := newFakeRepo()
	repo.upsert(domain.User{ID: "user-1", Email: "user@classsphere.edu", Role: domain.RoleTeacher})

	service, err := app.NewUserService(repo)
	require.NoError(t, err)

	ctx := context.Background()
	user, err := service.GetByID(ctx, "user-1")
	require.NoError(t, err)
	require.Equal(t, "user@classsphere.edu", user.Email)

	_, err = service.GetByID(ctx, "missing")
	require.ErrorIs(t, err, shared.ErrUserNotFound)

	_, err = app.NewUserService(nil)
	require.Error(t, err)
}
