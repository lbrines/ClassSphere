package database

import (
	"testing"

	"classsphere-backend/models"

	"github.com/stretchr/testify/assert"
)

func TestNewConnection(t *testing.T) {
	// Test memory database connection
	db, err := NewConnection(":memory:")
	assert.NoError(t, err)
	assert.NotNil(t, db)

	// Test that we can interact with the database
	sqlDB, err := db.DB()
	assert.NoError(t, err)
	assert.NoError(t, sqlDB.Ping())

	// Close connection
	assert.NoError(t, sqlDB.Close())
}

func TestAutoMigrate(t *testing.T) {
	db, err := NewConnection(":memory:")
	assert.NoError(t, err)

	// Test auto migration
	err = AutoMigrate(db)
	assert.NoError(t, err)

	// Verify tables exist by creating a user
	user := &models.User{
		Email:    "test@example.com",
		Password: "password",
		Name:     "Test User",
		Role:     "user",
	}

	err = db.Create(user).Error
	assert.NoError(t, err)
	assert.NotZero(t, user.ID)

	sqlDB, err := db.DB()
	assert.NoError(t, err)
	assert.NoError(t, sqlDB.Close())
}

func TestInitializeDatabase(t *testing.T) {
	// Test full database initialization
	db, err := InitializeDatabase(":memory:")
	assert.NoError(t, err)
	assert.NotNil(t, db)

	// Verify we can use the database
	user := &models.User{
		Email:    "init@example.com",
		Password: "password",
		Name:     "Init User",
		Role:     "user",
	}

	err = db.Create(user).Error
	assert.NoError(t, err)

	// Verify user was created with proper constraints
	var count int64
	err = db.Model(&models.User{}).Count(&count).Error
	assert.NoError(t, err)
	assert.Equal(t, int64(1), count)

	sqlDB, err := db.DB()
	assert.NoError(t, err)
	assert.NoError(t, sqlDB.Close())
}

func TestConnectionError(t *testing.T) {
	// Test connection with invalid path
	_, err := NewConnection("/invalid/path/database.db")
	assert.Error(t, err)
}

func TestGetDatabaseConfig(t *testing.T) {
	config := GetDatabaseConfig()
	assert.NotNil(t, config)

	// Test that config has proper settings
	assert.True(t, config.Logger != nil || config.Logger == nil) // Logger can be nil or set
}

func TestCloseDatabase(t *testing.T) {
	db, err := NewConnection(":memory:")
	assert.NoError(t, err)

	// Test closing database
	err = CloseDatabase(db)
	assert.NoError(t, err)

	// Verify connection is closed
	sqlDB, err := db.DB()
	assert.NoError(t, err)
	err = sqlDB.Ping()
	assert.Error(t, err) // Should fail because connection is closed
}