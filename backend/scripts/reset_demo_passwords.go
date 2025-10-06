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

	// Demo users to update
	demoUsers := []struct {
		Email    string
		Password string
		Role     string
	}{
		{
			Email:    "admin@classsphere.com",
			Password: "admin123",
			Role:     "admin",
		},
		{
			Email:    "teacher@classsphere.com",
			Password: "teacher123",
			Role:     "instructor",
		},
		{
			Email:    "student@classsphere.com",
			Password: "student123",
			Role:     "user",
		},
		{
			Email:    "parent@classsphere.com",
			Password: "parent123",
			Role:     "user",
		},
	}

	// Update demo users
	for _, demoUser := range demoUsers {
		// Get existing user
		user, err := userRepo.GetUserByEmail(demoUser.Email)
		if err != nil {
			log.Printf("User %s not found, skipping...", demoUser.Email)
			continue
		}

		// Hash new password
		hashedPassword, err := auth.HashPassword(demoUser.Password)
		if err != nil {
			log.Printf("Failed to hash password for %s: %v", demoUser.Email, err)
			continue
		}

		// Update user
		user.Password = hashedPassword
		user.Role = demoUser.Role

		if err := userRepo.UpdateUser(user); err != nil {
			log.Printf("Failed to update user %s: %v", demoUser.Email, err)
			continue
		}

		log.Printf("Successfully updated demo user: %s (%s) - Role: %s", user.Name, demoUser.Email, demoUser.Role)
	}

	log.Println("Demo users password reset completed!")
}
