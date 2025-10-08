package shared

import "strings"

// IntegrationMode enumerates supported integration backends.
const (
	IntegrationModeGoogle = "google"
	IntegrationModeMock   = "mock"
)

// NormalizeIntegrationMode sanitizes and normalizes user-provided mode values.
func NormalizeIntegrationMode(mode string) string {
	switch strings.ToLower(strings.TrimSpace(mode)) {
	case IntegrationModeGoogle:
		return IntegrationModeGoogle
	case IntegrationModeMock:
		return IntegrationModeMock
	default:
		return IntegrationModeMock
	}
}
