package models

import (
	"time"

	"gorm.io/gorm"
)

// User represents a user in the system
type User struct {
	ID        uint           `json:"id" gorm:"primaryKey"`
	Email     string         `json:"email" gorm:"uniqueIndex;not null"`
	Password  string         `json:"-" gorm:"not null"` // JSON tag "-" excludes from JSON serialization
	Name      string         `json:"name" gorm:"not null"`
	Role      string         `json:"role" gorm:"not null;default:'user'"` // 'user', 'admin', 'instructor'
	IsActive  bool           `json:"is_active" gorm:"default:true"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `json:"-" gorm:"index"` // Soft delete
}

// TableName sets the table name for GORM
func (User) TableName() string {
	return "users"
}

// IsAdmin checks if the user has admin role
func (u *User) IsAdmin() bool {
	return u.Role == "admin"
}

// IsInstructor checks if the user has instructor role
func (u *User) IsInstructor() bool {
	return u.Role == "instructor"
}

// UserRepository handles database operations for users
type UserRepository struct {
	db *gorm.DB
}

// NewUserRepository creates a new user repository
func NewUserRepository(db *gorm.DB) *UserRepository {
	return &UserRepository{db: db}
}

// CreateUser creates a new user in the database
func (r *UserRepository) CreateUser(user *User) error {
	return r.db.Create(user).Error
}

// GetUserByEmail retrieves a user by email
func (r *UserRepository) GetUserByEmail(email string) (*User, error) {
	var user User
	err := r.db.Where("email = ? AND is_active = ?", email, true).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// GetUserByID retrieves a user by ID
func (r *UserRepository) GetUserByID(id uint) (*User, error) {
	var user User
	err := r.db.Where("is_active = ?", true).First(&user, id).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// UpdateUser updates an existing user
func (r *UserRepository) UpdateUser(user *User) error {
	// First check if the user exists
	var existingUser User
	err := r.db.First(&existingUser, user.ID).Error
	if err != nil {
		return err
	}

	// Update the user
	result := r.db.Save(user)
	if result.Error != nil {
		return result.Error
	}
	return nil
}

// DeleteUser soft deletes a user by ID
func (r *UserRepository) DeleteUser(id uint) error {
	result := r.db.Delete(&User{}, id)
	if result.Error != nil {
		return result.Error
	}
	if result.RowsAffected == 0 {
		return gorm.ErrRecordNotFound
	}
	return nil
}

// ListUsers retrieves users with pagination
func (r *UserRepository) ListUsers(offset, limit int) ([]*User, error) {
	var users []*User
	err := r.db.Where("is_active = ?", true).
		Offset(offset).
		Limit(limit).
		Order("created_at DESC").
		Find(&users).Error
	return users, err
}

// GetUserCount returns the total count of active users
func (r *UserRepository) GetUserCount() (int64, error) {
	var count int64
	err := r.db.Model(&User{}).Where("is_active = ?", true).Count(&count).Error
	return count, err
}

// DeactivateUser deactivates a user instead of deleting
func (r *UserRepository) DeactivateUser(id uint) error {
	result := r.db.Model(&User{}).Where("id = ?", id).Update("is_active", false)
	if result.Error != nil {
		return result.Error
	}
	if result.RowsAffected == 0 {
		return gorm.ErrRecordNotFound
	}
	return nil
}

// ActivateUser activates a deactivated user
func (r *UserRepository) ActivateUser(id uint) error {
	result := r.db.Model(&User{}).Where("id = ?", id).Update("is_active", true)
	if result.Error != nil {
		return result.Error
	}
	if result.RowsAffected == 0 {
		return gorm.ErrRecordNotFound
	}
	return nil
}