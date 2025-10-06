package models

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func setupTestDB(t *testing.T) *gorm.DB {
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	require.NoError(t, err)
	
	// Auto migrate
	err = db.AutoMigrate(&User{})
	require.NoError(t, err)
	
	return db
}

func closeTestDB(t *testing.T, db *gorm.DB) {
	sqlDB, err := db.DB()
	require.NoError(t, err)
	err = sqlDB.Close()
	require.NoError(t, err)
}

func TestUser_TableName(t *testing.T) {
	user := &User{}
	assert.Equal(t, "users", user.TableName())
}

func TestUser_IsAdmin(t *testing.T) {
	user := &User{Role: "admin"}
	assert.True(t, user.IsAdmin())
	
	user.Role = "user"
	assert.False(t, user.IsAdmin())
}

func TestUser_IsInstructor(t *testing.T) {
	user := &User{Role: "instructor"}
	assert.True(t, user.IsInstructor())
	
	user.Role = "teacher"
	assert.False(t, user.IsInstructor())
	
	user.Role = "student"
	assert.False(t, user.IsInstructor())
}

func TestNewUserRepository(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	assert.NotNil(t, repo)
	assert.NotNil(t, repo.db)
}

func TestUserRepository_CreateUser(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.CreateUser(user)
	assert.NoError(t, err)
	assert.NotZero(t, user.ID)
	assert.NotZero(t, user.CreatedAt)
	assert.NotZero(t, user.UpdatedAt)
}

func TestUserRepository_GetUserByEmail(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Create a user first
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.CreateUser(user)
	require.NoError(t, err)
	
	// Test getting user by email
	foundUser, err := repo.GetUserByEmail("test@example.com")
	assert.NoError(t, err)
	assert.NotNil(t, foundUser)
	assert.Equal(t, "test@example.com", foundUser.Email)
	assert.Equal(t, "Test User", foundUser.Name)
	assert.Equal(t, "user", foundUser.Role)
	assert.True(t, foundUser.IsActive)
}

func TestUserRepository_GetUserByEmail_NotFound(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Test getting non-existent user
	foundUser, err := repo.GetUserByEmail("nonexistent@example.com")
	assert.Error(t, err)
	assert.Nil(t, foundUser)
}

func TestUserRepository_GetUserByID(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Create a user first
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.CreateUser(user)
	require.NoError(t, err)
	
	// Test getting user by ID
	foundUser, err := repo.GetUserByID(user.ID)
	assert.NoError(t, err)
	assert.NotNil(t, foundUser)
	assert.Equal(t, user.ID, foundUser.ID)
	assert.Equal(t, "test@example.com", foundUser.Email)
}

func TestUserRepository_GetUserByID_NotFound(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Test getting non-existent user
	foundUser, err := repo.GetUserByID(999)
	assert.Error(t, err)
	assert.Nil(t, foundUser)
}

func TestUserRepository_UpdateUser(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Create a user first
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.CreateUser(user)
	require.NoError(t, err)
	
	// Update user
	user.Name = "Updated Name"
	user.Role = "admin"
	
	err = repo.UpdateUser(user)
	assert.NoError(t, err)
	
	// Verify update
	updatedUser, err := repo.GetUserByID(user.ID)
	assert.NoError(t, err)
	assert.Equal(t, "Updated Name", updatedUser.Name)
	assert.Equal(t, "admin", updatedUser.Role)
}

func TestUserRepository_UpdateUser_NotFound(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to update non-existent user
	user := &User{
		ID:       999,
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.UpdateUser(user)
	assert.Error(t, err)
}

func TestUserRepository_DeleteUser(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Create a user first
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.CreateUser(user)
	require.NoError(t, err)
	
	// Delete user (soft delete)
	err = repo.DeleteUser(user.ID)
	assert.NoError(t, err)
	
	// Verify user is soft deleted (should not be found)
	_, err = repo.GetUserByID(user.ID)
	assert.Error(t, err)
}

func TestUserRepository_DeleteUser_NotFound(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to delete non-existent user
	err := repo.DeleteUser(999)
	assert.Error(t, err)
}

func TestUserRepository_ListUsers(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Create multiple users
	users := []*User{
		{Email: "user1@example.com", Password: "hash1", Name: "User 1", Role: "user", IsActive: true},
		{Email: "user2@example.com", Password: "hash2", Name: "User 2", Role: "user", IsActive: true},
		{Email: "user3@example.com", Password: "hash3", Name: "User 3", Role: "admin", IsActive: true},
	}
	
	for _, user := range users {
		err := repo.CreateUser(user)
		require.NoError(t, err)
	}
	
	// Test listing users
	list, err := repo.ListUsers(0, 10)
	assert.NoError(t, err)
	assert.Len(t, list, 3)
	
	// Test pagination
	list, err = repo.ListUsers(0, 2)
	assert.NoError(t, err)
	assert.Len(t, list, 2)
	
	list, err = repo.ListUsers(2, 2)
	assert.NoError(t, err)
	assert.Len(t, list, 1)
}

func TestUserRepository_GetUserCount(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Initially should be 0
	count, err := repo.GetUserCount()
	assert.NoError(t, err)
	assert.Equal(t, int64(0), count)
	
	// Create users
	users := []*User{
		{Email: "user1@example.com", Password: "hash1", Name: "User 1", Role: "user", IsActive: true},
		{Email: "user2@example.com", Password: "hash2", Name: "User 2", Role: "user", IsActive: true},
	}
	
	for _, user := range users {
		err := repo.CreateUser(user)
		require.NoError(t, err)
	}
	
	// Should be 2 now
	count, err = repo.GetUserCount()
	assert.NoError(t, err)
	assert.Equal(t, int64(2), count)
}

func TestUserRepository_DeactivateUser(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Create a user first
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.CreateUser(user)
	require.NoError(t, err)
	
	// Deactivate user
	err = repo.DeactivateUser(user.ID)
	assert.NoError(t, err)
	
	// Verify user is deactivated (should not be found by GetUserByEmail)
	_, err = repo.GetUserByEmail("test@example.com")
	assert.Error(t, err)
}

func TestUserRepository_DeactivateUser_NotFound(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to deactivate non-existent user
	err := repo.DeactivateUser(999)
	assert.Error(t, err)
}

func TestUserRepository_ActivateUser(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Create a user first
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.CreateUser(user)
	require.NoError(t, err)
	
	// Deactivate user first
	err = repo.DeactivateUser(user.ID)
	require.NoError(t, err)
	
	// Activate user
	err = repo.ActivateUser(user.ID)
	assert.NoError(t, err)
	
	// Verify user is activated (should be found by GetUserByEmail)
	foundUser, err := repo.GetUserByEmail("test@example.com")
	assert.NoError(t, err)
	assert.NotNil(t, foundUser)
	assert.True(t, foundUser.IsActive)
}

func TestUserRepository_ActivateUser_NotFound(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to activate non-existent user
	err := repo.ActivateUser(999)
	assert.Error(t, err)
}

func TestUserRepository_UpdateUser_WithZeroID(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to update user with zero ID
	user := &User{
		ID:       0,
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	err := repo.UpdateUser(user)
	assert.Error(t, err)
}

func TestUserRepository_DeleteUser_WithZeroID(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to delete user with zero ID
	err := repo.DeleteUser(0)
	assert.Error(t, err)
}

func TestUserRepository_DeactivateUser_WithZeroID(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to deactivate user with zero ID
	err := repo.DeactivateUser(0)
	assert.Error(t, err)
}

func TestUserRepository_ActivateUser_WithZeroID(t *testing.T) {
	db := setupTestDB(t)
	defer closeTestDB(t, db)
	
	repo := NewUserRepository(db)
	
	// Try to activate user with zero ID
	err := repo.ActivateUser(0)
	assert.Error(t, err)
}

func TestUserRepository_DeactivateUser_WithDatabaseError(t *testing.T) {
	// Create a repository with a closed database to simulate database error
	db := setupTestDB(t)
	
	// Close the database to simulate error
	sqlDB, _ := db.DB()
	sqlDB.Close()
	
	repo := NewUserRepository(db)
	
	// This should trigger the error path in DeactivateUser
	err := repo.DeactivateUser(1)
	assert.Error(t, err)
}

func TestUserRepository_ActivateUser_WithDatabaseError(t *testing.T) {
	// Create a repository with a closed database to simulate database error
	db := setupTestDB(t)
	
	// Close the database to simulate error
	sqlDB, _ := db.DB()
	sqlDB.Close()
	
	repo := NewUserRepository(db)
	
	// This should trigger the error path in ActivateUser
	err := repo.ActivateUser(1)
	assert.Error(t, err)
}

func TestUserRepository_DeleteUser_WithDatabaseError(t *testing.T) {
	// Create a repository with a closed database to simulate database error
	db := setupTestDB(t)
	
	// Close the database to simulate error
	sqlDB, _ := db.DB()
	sqlDB.Close()
	
	repo := NewUserRepository(db)
	
	// This should trigger the error path in DeleteUser
	err := repo.DeleteUser(1)
	assert.Error(t, err)
}

func TestUserRepository_UpdateUser_WithDatabaseError(t *testing.T) {
	// Create a repository with a closed database to simulate database error
	db := setupTestDB(t)
	
	// Close the database to simulate error
	sqlDB, _ := db.DB()
	sqlDB.Close()
	
	repo := NewUserRepository(db)
	
	// Create a user to update
	user := &User{
		ID:       1,
		Email:    "test@example.com",
		Password: "hashedpassword",
		Name:     "Test User",
		Role:     "user",
		IsActive: true,
	}
	
	// This should trigger the error path in UpdateUser
	err := repo.UpdateUser(user)
	assert.Error(t, err)
}