package ports

import "context"

// OAuthUser contains the minimal information returned by an OAuth provider.
type OAuthUser struct {
	ID          string
	Email       string
	DisplayName string
}

// OAuthProvider declares the operations needed for OAuth flows.
type OAuthProvider interface {
	AuthURL(state string) (string, error)
	Exchange(ctx context.Context, code string) (OAuthUser, error)
}
