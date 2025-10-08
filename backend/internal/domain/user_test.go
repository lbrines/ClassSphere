package domain_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/lbrines/classsphere/internal/domain"
)

func TestUserCanAccessRole(t *testing.T) {
	user := domain.User{Role: domain.RoleCoordinator}
	assert.True(t, user.CanAccessRole(domain.RoleTeacher))
	assert.False(t, user.CanAccessRole(domain.RoleAdmin))
}
