package domain_test

import (
	"testing"

	"github.com/stretchr/testify/assert"

	"github.com/lbrines/classsphere/internal/domain"
)

func TestRoleAllows(t *testing.T) {
	assert.True(t, domain.RoleAdmin.Allows(domain.RoleTeacher))
	assert.True(t, domain.RoleCoordinator.Allows(domain.RoleTeacher))
	assert.False(t, domain.RoleTeacher.Allows(domain.RoleAdmin))
	assert.True(t, domain.RoleStudent.Allows(domain.RoleStudent))
}

func TestParseRole(t *testing.T) {
	assert.Equal(t, domain.RoleAdmin, domain.ParseRole("ADMIN"))
	assert.Equal(t, domain.RoleStudent, domain.ParseRole("unknown"))
	assert.True(t, domain.RoleTeacher.IsValid())
	assert.False(t, domain.Role("visitor").IsValid())
}
