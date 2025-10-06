package main

import (
	"log"

	"classsphere-backend/auth"
	"classsphere-backend/config"
	"classsphere-backend/database"
	"classsphere-backend/models"
)

func main() {
	// Load configuration
	cfg := config.Load()

	// Initialize database
	db, err := database.InitializeDatabase(cfg.DatabasePath)
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	// Initialize repository
	userRepo := models.NewUserRepository(db)

	// Test users with proper roles
	testUsers := []struct {
		Email    string
		Password string
		Name     string
		Role     string
	}{
		{"student@test.com", "StrongPassword123!", "Test Student", "student"},
		{"teacher@test.com", "StrongPassword123!", "Test Teacher", "teacher"},
		{"coordinator@test.com", "StrongPassword123!", "Test Coordinator", "coordinator"},
		{"admin@test.com", "StrongPassword123!", "Test Admin", "admin"},
	}

	for _, userData := range testUsers {
		// Check if user exists
		existingUser, err := userRepo.GetUserByEmail(userData.Email)
		if err == nil && existingUser != nil {
			// Update existing user with correct role and password
			hashedPassword, err := auth.HashPassword(userData.Password)
			if err != nil {
				log.Printf("Failed to hash password for %s: %v", userData.Email, err)
				continue
			}
			
			existingUser.Password = hashedPassword
			existingUser.Role = userData.Role
			existingUser.Name = userData.Name
			
			if err := userRepo.UpdateUser(existingUser); err != nil {
				log.Printf("Failed to update user %s: %v", userData.Email, err)
			} else {
				log.Printf("Updated user: %s (%s) - Role: %s", userData.Name, userData.Email, userData.Role)
			}
		} else {
			// Create new user
			hashedPassword, err := auth.HashPassword(userData.Password)
			if err != nil {
				log.Printf("Failed to hash password for %s: %v", userData.Email, err)
				continue
			}

			user := &models.User{
				Email:    userData.Email,
				Password: hashedPassword,
				Name:     userData.Name,
				Role:     userData.Role,
				IsActive: true,
			}

			if err := userRepo.CreateUser(user); err != nil {
				log.Printf("Failed to create user %s: %v", userData.Email, err)
			} else {
				log.Printf("Created user: %s (%s) - Role: %s", userData.Name, userData.Email, userData.Role)
			}
		}
	}

	log.Println("Test users with proper roles setup completed!")
}
