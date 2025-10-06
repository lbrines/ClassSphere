package handlers

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"classsphere-backend/auth"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func setupTestDashboardHandler(t *testing.T) (*DashboardHandler, *gorm.DB) {
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	require.NoError(t, err)
	
	// Auto migrate
	err = db.AutoMigrate(&models.User{})
	require.NoError(t, err)
	
	userRepo := models.NewUserRepository(db)
	handler := NewDashboardHandler(userRepo)
	
	return handler, db
}

func closeTestDashboardDB(t *testing.T, db *gorm.DB) {
	sqlDB, err := db.DB()
	require.NoError(t, err)
	err = sqlDB.Close()
	require.NoError(t, err)
}

func TestNewDashboardHandler(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	assert.NotNil(t, handler)
	assert.NotNil(t, handler.userRepo)
}

func TestGetStudentDashboard(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	// Create a user in the database
	user := &models.User{
		Email:    "student@example.com",
		Password: "hashedpassword",
		Name:     "Test Student",
		Role:     "student",
		IsActive: true,
	}
	err := db.Create(user).Error
	require.NoError(t, err)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context (simulating JWT middleware)
	c.Set("user", &auth.Claims{UserID: "1", Role: "student"})
	
	err = handler.GetStudentDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestGetTeacherDashboard(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	// Create a user in the database
	user := &models.User{
		Email:    "teacher@example.com",
		Password: "hashedpassword",
		Name:     "Test Teacher",
		Role:     "teacher",
		IsActive: true,
	}
	err := db.Create(user).Error
	require.NoError(t, err)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context (simulating JWT middleware)
	c.Set("user", &auth.Claims{UserID: "1", Role: "teacher"})
	
	err = handler.GetTeacherDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestGetCoordinatorDashboard(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	// Create a user in the database
	user := &models.User{
		Email:    "coordinator@example.com",
		Password: "hashedpassword",
		Name:     "Test Coordinator",
		Role:     "coordinator",
		IsActive: true,
	}
	err := db.Create(user).Error
	require.NoError(t, err)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/coordinator", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context (simulating JWT middleware)
	c.Set("user", &auth.Claims{UserID: "1", Role: "coordinator"})
	
	err = handler.GetCoordinatorDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestGetAdminDashboard(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	// Create a user in the database
	user := &models.User{
		Email:    "admin@example.com",
		Password: "hashedpassword",
		Name:     "Test Admin",
		Role:     "admin",
		IsActive: true,
	}
	err := db.Create(user).Error
	require.NoError(t, err)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	
	// Set user in context (simulating JWT middleware)
	c.Set("user", &auth.Claims{UserID: "1", Role: "admin"})
	
	err = handler.GetAdminDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusOK, rec.Code)
}

func TestGetStudentDashboard_NoUserInContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	// No user set in context
	
	err := handler.GetStudentDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetStudentDashboard_InvalidUserContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", "invalid-claims-type") // Wrong type
	
	err := handler.GetStudentDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetStudentDashboard_InvalidUserID(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "invalid-id", Role: "student"})
	
	err := handler.GetStudentDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestGetStudentDashboard_UserNotFound(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/student", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "999", Role: "student"})
	
	err := handler.GetStudentDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusNotFound, rec.Code)
}

func TestGetTeacherDashboard_NoUserInContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	// No user set in context
	
	err := handler.GetTeacherDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetTeacherDashboard_InvalidUserContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", "invalid-claims-type") // Wrong type
	
	err := handler.GetTeacherDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetTeacherDashboard_InvalidUserID(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "invalid-id", Role: "teacher"})
	
	err := handler.GetTeacherDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestGetTeacherDashboard_UserNotFound(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/teacher", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "999", Role: "teacher"})
	
	err := handler.GetTeacherDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusNotFound, rec.Code)
}

func TestGetCoordinatorDashboard_NoUserInContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/coordinator", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	// No user set in context
	
	err := handler.GetCoordinatorDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetCoordinatorDashboard_InvalidUserContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/coordinator", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", "invalid-claims-type") // Wrong type
	
	err := handler.GetCoordinatorDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetCoordinatorDashboard_InvalidUserID(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/coordinator", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "invalid-id", Role: "coordinator"})
	
	err := handler.GetCoordinatorDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestGetCoordinatorDashboard_UserNotFound(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/coordinator", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "999", Role: "coordinator"})
	
	err := handler.GetCoordinatorDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusNotFound, rec.Code)
}

func TestGetAdminDashboard_NoUserInContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	// No user set in context
	
	err := handler.GetAdminDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetAdminDashboard_InvalidUserContext(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", "invalid-claims-type") // Wrong type
	
	err := handler.GetAdminDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusUnauthorized, rec.Code)
}

func TestGetAdminDashboard_InvalidUserID(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "invalid-id", Role: "admin"})
	
	err := handler.GetAdminDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusBadRequest, rec.Code)
}

func TestGetAdminDashboard_UserNotFound(t *testing.T) {
	handler, db := setupTestDashboardHandler(t)
	defer closeTestDashboardDB(t, db)
	
	e := echo.New()
	req := httptest.NewRequest(http.MethodGet, "/api/dashboard/admin", nil)
	rec := httptest.NewRecorder()
	c := e.NewContext(req, rec)
	c.Set("user", &auth.Claims{UserID: "999", Role: "admin"})
	
	err := handler.GetAdminDashboard(c)
	
	assert.NoError(t, err)
	assert.Equal(t, http.StatusNotFound, rec.Code)
}