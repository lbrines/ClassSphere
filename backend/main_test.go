package main

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMain(t *testing.T) {
	// Test that main function exists and doesn't panic
	// In a real test, we would test the main function setup
	// For now, we test the helper functions

	e := setupTestApp()
	assert.NotNil(t, e)

	// Test welcome endpoint
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)

	err := handleWelcome(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)

	// Test health endpoint
	req2 := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec2 := httptest.NewRecorder()
	c2 := e.NewContext(req2, rec2)

	err = handleHealth(c2)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec2.Code)
}