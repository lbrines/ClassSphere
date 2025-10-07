package app

import (
	"context"
	"fmt"

	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

// UserService exposes user related use cases.
type UserService struct {
	users ports.UserRepository
}

// NewUserService constructs a UserService instance.
func NewUserService(users ports.UserRepository) (*UserService, error) {
	if users == nil {
		return nil, fmt.Errorf("users repository is required")
	}
	return &UserService{users: users}, nil
}

// GetByID fetches a user.
func (s *UserService) GetByID(ctx context.Context, id string) (domain.User, error) {
	user, err := s.users.FindByID(ctx, id)
	if err != nil {
		return domain.User{}, shared.ErrUserNotFound
	}
	return user, nil
}
