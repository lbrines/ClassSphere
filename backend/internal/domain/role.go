package domain

import "strings"

// Role models access levels within the platform.
type Role string

const (
	RoleAdmin       Role = "admin"
	RoleCoordinator Role = "coordinator"
	RoleTeacher     Role = "teacher"
	RoleStudent     Role = "student"
)

var roleHierarchy = map[Role]int{
	RoleAdmin:       4,
	RoleCoordinator: 3,
	RoleTeacher:     2,
	RoleStudent:     1,
}

// ParseRole converts string input into a valid Role.
func ParseRole(raw string) Role {
	role := Role(strings.ToLower(strings.TrimSpace(raw)))
	if _, ok := roleHierarchy[role]; !ok {
		return RoleStudent
	}
	return role
}

// Allows returns true when the current role grants access to the requested role.
func (r Role) Allows(target Role) bool {
	return roleHierarchy[r] >= roleHierarchy[target]
}

// IsValid returns true when the role exists in the hierarchy map.
func (r Role) IsValid() bool {
	_, ok := roleHierarchy[r]
	return ok
}
