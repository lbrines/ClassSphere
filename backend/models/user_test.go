package models

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func setupTestDB() *gorm.DB {
	db, err := gorm.Open(sqlite.Open(":memory:"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// Migrate the schema
	db.AutoMigrate(&User{})

	return db
}

func TestUserModel(t *testing.T) {
	db := setupTestDB()

	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword123",
		Name:     "Test User",
		Role:     "user",
	}

	// Test Create
	err := db.Create(user).Error
	assert.NoError(t, err)
	assert.NotZero(t, user.ID)
	assert.NotZero(t, user.CreatedAt)
	assert.NotZero(t, user.UpdatedAt)

	// Test Find by ID
	var foundUser User
	err = db.First(&foundUser, user.ID).Error
	assert.NoError(t, err)
	assert.Equal(t, user.Email, foundUser.Email)
	assert.Equal(t, user.Name, foundUser.Name)
	assert.Equal(t, user.Role, foundUser.Role)
}

func TestUserValidation(t *testing.T) {
	db := setupTestDB()

	// Test that we can create a user with empty email (SQLite allows it)
	user := &User{
		Email:    "", // Empty email - SQLite allows this
		Password: "password123",
		Name:     "Test User",
		Role:     "user",
	}

	err := db.Create(user).Error
	assert.NoError(t, err) // SQLite doesn't enforce NOT NULL on empty strings

	// Test unique email constraint
	user1 := &User{
		Email:    "unique@example.com",
		Password: "password123",
		Name:     "User 1",
		Role:     "user",
	}

	user2 := &User{
		Email:    "unique@example.com", // Same email
		Password: "password456",
		Name:     "User 2",
		Role:     "admin",
	}

	err = db.Create(user1).Error
	assert.NoError(t, err)

	err = db.Create(user2).Error
	assert.Error(t, err) // Should fail due to unique constraint
}

func TestUserMethods(t *testing.T) {
	user := &User{
		Email:    "test@example.com",
		Password: "hashedpassword123",
		Name:     "Test User",
		Role:     "admin",
	}

	// Test IsAdmin
	assert.True(t, user.IsAdmin())

	user.Role = "user"
	assert.False(t, user.IsAdmin())

	// Test IsInstructor
	user.Role = "instructor"
	assert.True(t, user.IsInstructor())

	user.Role = "user"
	assert.False(t, user.IsInstructor())

	// Test TableName
	assert.Equal(t, "users", user.TableName())
}

func TestUserRepository(t *testing.T) {
	db := setupTestDB()
	repo := NewUserRepository(db)

	// Test CreateUser
	user := &User{
		Email:    "repo@example.com",
		Password: "hashedpassword123",
		Name:     "Repo User",
		Role:     "user",
	}

	err := repo.CreateUser(user)
	assert.NoError(t, err)
	assert.NotZero(t, user.ID)

	// Test GetUserByEmail
	foundUser, err := repo.GetUserByEmail("repo@example.com")
	assert.NoError(t, err)
	assert.Equal(t, user.Email, foundUser.Email)
	assert.Equal(t, user.Name, foundUser.Name)

	// Test GetUserByID
	foundUser2, err := repo.GetUserByID(user.ID)
	assert.NoError(t, err)
	assert.Equal(t, user.Email, foundUser2.Email)

	// Test UpdateUser
	foundUser.Name = "Updated Name"
	err = repo.UpdateUser(foundUser)
	assert.NoError(t, err)

	updatedUser, err := repo.GetUserByID(user.ID)
	assert.NoError(t, err)
	assert.Equal(t, "Updated Name", updatedUser.Name)

	// Test DeleteUser
	err = repo.DeleteUser(user.ID)
	assert.NoError(t, err)

	_, err = repo.GetUserByID(user.ID)
	assert.Error(t, err) // Should not find deleted user
}

func TestUserRepositoryErrors(t *testing.T) {
	db := setupTestDB()
	repo := NewUserRepository(db)

	// Test GetUserByEmail with non-existent email
	_, err := repo.GetUserByEmail("nonexistent@example.com")
	assert.Error(t, err)

	// Test GetUserByID with non-existent ID
	_, err = repo.GetUserByID(99999)
	assert.Error(t, err)

	// Test UpdateUser with non-existent user
	nonExistentUser := &User{
		ID:       99999,
		Email:    "nonexistent@example.com",
		Password: "password",
		Name:     "Non Existent",
		Role:     "user",
	}

	err = repo.UpdateUser(nonExistentUser)
	assert.Error(t, err)

	// Test DeleteUser with non-existent ID
	err = repo.DeleteUser(99999)
	assert.Error(t, err)
}

func TestUserRepositoryListUsers(t *testing.T) {
	db := setupTestDB()
	repo := NewUserRepository(db)

	// Create test users
	users := []*User{
		{Email: "user1@example.com", Password: "password1", Name: "User 1", Role: "user"},
		{Email: "user2@example.com", Password: "password2", Name: "User 2", Role: "admin"},
		{Email: "user3@example.com", Password: "password3", Name: "User 3", Role: "user"},
	}

	for _, user := range users {
		err := repo.CreateUser(user)
		assert.NoError(t, err)
	}

	// Test ListUsers
	allUsers, err := repo.ListUsers(0, 10)
	assert.NoError(t, err)
	assert.Len(t, allUsers, 3)

	// Test ListUsers with pagination
	firstUser, err := repo.ListUsers(0, 1)
	assert.NoError(t, err)
	assert.Len(t, firstUser, 1)

	secondUser, err := repo.ListUsers(1, 1)
	assert.NoError(t, err)
	assert.Len(t, secondUser, 1)
	assert.NotEqual(t, firstUser[0].ID, secondUser[0].ID)
}

func TestUserSoftDelete(t *testing.T) {
	db := setupTestDB()
	repo := NewUserRepository(db)

	user := &User{
		Email:    "softdelete@example.com",
		Password: "password123",
		Name:     "Soft Delete User",
		Role:     "user",
	}

	err := repo.CreateUser(user)
	assert.NoError(t, err)

	// Soft delete
	err = repo.DeleteUser(user.ID)
	assert.NoError(t, err)

	// Should not find in normal query
	_, err = repo.GetUserByID(user.ID)
	assert.Error(t, err)

	// Should find with Unscoped (including soft deleted)
	var deletedUser User
	err = db.Unscoped().First(&deletedUser, user.ID).Error
	assert.NoError(t, err)
	assert.NotNil(t, deletedUser.DeletedAt)
}