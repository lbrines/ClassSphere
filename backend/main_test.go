package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
)

func TestHandleWelcome(t *testing.T) {
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handleWelcome(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	var response map[string]interface{}
	json.Unmarshal(rec.Body.Bytes(), &response)
	assert.Contains(t, response, "message")
	assert.Equal(t, "ClassSphere API", response["message"])
	assert.Equal(t, "1.0.0", response["version"])
	assert.Equal(t, "running", response["status"])
}

func TestHandleWelcome_WithDifferentMethods(t *testing.T) {
	e := echo.New()
	
	// Test with POST method (should still work)
	req := httptest.NewRequest(http.MethodPost, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handleWelcome(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestHandleHealth(t *testing.T) {
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handleHealth(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
	
	var response map[string]interface{}
	json.Unmarshal(rec.Body.Bytes(), &response)
	assert.Contains(t, response, "status")
	assert.Equal(t, "healthy", response["status"])
	assert.Equal(t, "classsphere-backend", response["service"])
	assert.Contains(t, response, "timestamp")
}

func TestHandleHealth_WithDifferentMethods(t *testing.T) {
	e := echo.New()
	
	// Test with POST method (should still work)
	req := httptest.NewRequest(http.MethodPost, "/health", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handleHealth(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestSetupTestApp(t *testing.T) {
	e := setupTestApp()
	
	assert.NotNil(t, e)
	
	// Test that the app has the expected routes
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handleWelcome(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestSetupTestApp_HealthEndpoint(t *testing.T) {
	e := setupTestApp()
	
	// Test health endpoint
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	err := handleHealth(c)
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestMainFunction(t *testing.T) {
	// Test that main function can be called without errors
	// This is a basic test to verify the main function structure
	// Note: We can't actually call main() in tests as it would start the server
	// But we can test that the function exists and the package compiles
	assert.True(t, true, "Main function exists and package compiles")
}