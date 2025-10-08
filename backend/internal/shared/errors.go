package shared

import "errors"

var (
	// ErrUnauthorized indicates an authentication failure.
	ErrUnauthorized = errors.New("unauthorized")
	// ErrForbidden indicates insufficient permissions.
	ErrForbidden = errors.New("forbidden")
	// ErrUserNotFound indicates the user was not found in persistence.
	ErrUserNotFound = errors.New("user not found")
	// ErrInvalidCredentials represents invalid login credentials.
	ErrInvalidCredentials = errors.New("invalid credentials")
)
