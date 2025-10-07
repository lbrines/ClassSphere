package oauth

import "testing"

func TestOAuthErrorString(t *testing.T) {
	err := (&oauthError{Code: "invalid", Description: "Invalid token"}).Error()
	if err != "Invalid token" {
		t.Fatalf("expected description, got %s", err)
	}

	err = (&oauthError{Code: "invalid"}).Error()
	if err != "invalid" {
		t.Fatalf("expected code fallback, got %s", err)
	}
}
