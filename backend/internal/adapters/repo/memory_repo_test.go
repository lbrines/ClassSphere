package repo_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/require"

	"github.com/lbrines/classsphere/internal/adapters/repo"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/shared"
)

func TestMemoryUserRepository(t *testing.T) {
	ctx := context.Background()
	seed := []domain.User{{
		ID:    "user-1",
		Email: "user@classsphere.edu",
		Role:  domain.RoleTeacher,
	}}

	repository := repo.NewMemoryUserRepository(seed)

	user, err := repository.FindByID(ctx, "user-1")
	require.NoError(t, err)
	require.Equal(t, seed[0].Email, user.Email)

	user, err = repository.FindByEmail(ctx, "user@classsphere.edu")
	require.NoError(t, err)
	require.Equal(t, "user-1", user.ID)

	user.Role = domain.RoleAdmin
	require.NoError(t, repository.Upsert(ctx, user))

	updated, err := repository.FindByID(ctx, "user-1")
	require.NoError(t, err)
	require.Equal(t, domain.RoleAdmin, updated.Role)

	_, err = repository.FindByID(ctx, "missing")
	require.ErrorIs(t, err, shared.ErrUserNotFound)
}
