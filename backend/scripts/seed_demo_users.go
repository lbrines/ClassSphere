//go:build ignore
// +build ignore

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

	// Initialize user repository
	userRepo := models.NewUserRepository(db)

	// Demo users to create
	demoUsers := []struct {
		Email    string
		Password string
		Name     string
		Role     string
	}{
		{
			Email:    "admin@classsphere.com",
			Password: "admin123",
			Name:     "Admin User",
			Role:     "admin",
		},
		{
			Email:    "teacher@classsphere.com",
			Password: "teacher123",
			Name:     "Teacher Demo",
			Role:     "instructor",
		},
		{
			Email:    "student@classsphere.com",
			Password: "student123",
			Name:     "Student Demo",
			Role:     "user",
		},
		{
			Email:    "parent@classsphere.com",
			Password: "parent123",
			Name:     "Parent Demo",
			Role:     "user",
		},
	}

	// Create demo users
	for _, demoUser := range demoUsers {
		// Check if user already exists
		existingUser, err := userRepo.GetUserByEmail(demoUser.Email)
		if err == nil && existingUser != nil {
			log.Printf("User %s already exists, skipping...", demoUser.Email)
			continue
		}

		// Hash password
		hashedPassword, err := auth.HashPassword(demoUser.Password)
		if err != nil {
			log.Printf("Failed to hash password for %s: %v", demoUser.Email, err)
			continue
		}

		// Create user
		user := &models.User{
			Email:    demoUser.Email,
			Password: hashedPassword,
			Name:     demoUser.Name,
			Role:     demoUser.Role,
			IsActive: true,
		}

		if err := userRepo.CreateUser(user); err != nil {
			log.Printf("Failed to create user %s: %v", demoUser.Email, err)
			continue
		}

		log.Printf("Successfully created demo user: %s (%s)", demoUser.Name, demoUser.Email)
	}

	log.Println("Demo users seeding completed!")
}
