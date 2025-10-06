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
}

func TestSetupTestApp(t *testing.T) {
	e := setupTestApp()
	
	assert.NotNil(t, e)
}