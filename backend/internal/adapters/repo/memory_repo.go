package repo

import (
	"context"
	"sync"

	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/shared"
)

// MemoryUserRepository stores users in-memory for development/testing.
type MemoryUserRepository struct {
	mu      sync.RWMutex
	byID    map[string]domain.User
	byEmail map[string]domain.User
}

// NewMemoryUserRepository constructs the repository with optional seed data.
func NewMemoryUserRepository(seed []domain.User) *MemoryUserRepository {
	repo := &MemoryUserRepository{
		byID:    make(map[string]domain.User),
		byEmail: make(map[string]domain.User),
	}
	for _, user := range seed {
		repo.save(user)
	}
	return repo
}

func (r *MemoryUserRepository) save(user domain.User) {
	r.byID[user.ID] = user
	r.byEmail[user.Email] = user
}

// FindByEmail retrieves a user by email.
func (r *MemoryUserRepository) FindByEmail(_ context.Context, email string) (domain.User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	if user, ok := r.byEmail[email]; ok {
		return user, nil
	}
	return domain.User{}, shared.ErrUserNotFound
}

// FindByID retrieves a user by ID.
func (r *MemoryUserRepository) FindByID(_ context.Context, id string) (domain.User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	if user, ok := r.byID[id]; ok {
		return user, nil
	}
	return domain.User{}, shared.ErrUserNotFound
}

// Upsert stores a user.
func (r *MemoryUserRepository) Upsert(_ context.Context, user domain.User) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.save(user)
	return nil
}
