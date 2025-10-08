package ports

import (
	"context"

	"github.com/lbrines/classsphere/internal/domain"
)

// UserRepository defines persistence behaviour for users.
type UserRepository interface {
	FindByEmail(ctx context.Context, email string) (domain.User, error)
	FindByID(ctx context.Context, id string) (domain.User, error)
	Upsert(ctx context.Context, user domain.User) error
}
