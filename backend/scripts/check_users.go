//go:build ignore
// +build ignore

package main

import (
	"log"

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

	// List all users
	users, err := userRepo.ListUsers(0, 100)
	if err != nil {
		log.Fatalf("Failed to list users: %v", err)
	}

	log.Printf("Found %d users in database:", len(users))
	for _, user := range users {
		log.Printf("- %s (%s) - Role: %s - Active: %t", user.Name, user.Email, user.Role, user.IsActive)
	}
}
