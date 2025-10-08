package domain

import "time"

// User represents an authenticated platform member.
type User struct {
	ID             string    `json:"id"`
	Email          string    `json:"email"`
	HashedPassword string    `json:"-"`
	Role           Role      `json:"role"`
	DisplayName    string    `json:"displayName"`
	CreatedAt      time.Time `json:"createdAt"`
	UpdatedAt      time.Time `json:"updatedAt"`
}

// CanAccessRole determines if the user can access resources requiring the given role.
func (u User) CanAccessRole(role Role) bool {
	return u.Role.Allows(role)
}
