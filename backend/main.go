package main

import (
	"log"
	"os"

	"classsphere-backend/auth"
	"classsphere-backend/cache"
	"classsphere-backend/config"
	"classsphere-backend/database"
	"classsphere-backend/handlers"
	"classsphere-backend/models"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	// Load configuration
	cfg := config.Load()

	// Initialize database
	db, err := database.InitializeDatabase(cfg.DatabasePath)
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	// Initialize cache (for future use)
	redisClient := cache.NewRedisClient(cfg.RedisAddr, cfg.RedisPassword, cfg.RedisDB)
	_ = cache.NewRedisCache(redisClient) // Cache client ready for future features

	// Initialize JWT manager
	jwtManager := auth.NewJWTManager(cfg.JWTSecret)

	// Initialize repositories
	userRepo := models.NewUserRepository(db)

	// Initialize handlers
	authHandler := handlers.NewAuthHandler(userRepo, jwtManager)
	dashboardHandler := handlers.NewDashboardHandler(userRepo)

	// Setup Echo
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	// Public routes
	e.GET("/", handleWelcome)
	e.GET("/health", handleHealth)

	// Auth routes
	authGroup := e.Group("/auth")
	authGroup.POST("/register", authHandler.Register)
	authGroup.POST("/login", authHandler.Login)
	authGroup.POST("/refresh", authHandler.RefreshToken)
	authGroup.POST("/logout", authHandler.Logout)

	// Protected routes
	protectedGroup := e.Group("/api")
	protectedGroup.Use(auth.JWTMiddleware(jwtManager))
	
	// Dashboard routes (more specific routes first)
	protectedGroup.GET("/dashboard/student", dashboardHandler.GetStudentDashboard)
	protectedGroup.GET("/dashboard/teacher", dashboardHandler.GetTeacherDashboard)
	protectedGroup.GET("/dashboard/coordinator", dashboardHandler.GetCoordinatorDashboard)
	protectedGroup.GET("/dashboard/admin", dashboardHandler.GetAdminDashboard)
	
	// General profile route
	protectedGroup.GET("/profile", authHandler.GetProfile)

	// Admin routes (require admin role)
	adminGroup := e.Group("/admin")
	adminGroup.Use(auth.JWTMiddleware(jwtManager))
	adminGroup.Use(auth.RequireRole("admin"))
	// Add admin routes here later

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Starting ClassSphere API server on port %s", port)
	e.Logger.Fatal(e.Start(":" + port))
}

func handleWelcome(c echo.Context) error {
	return c.JSON(200, map[string]string{
		"message": "ClassSphere API",
		"version": "1.0.0",
		"status":  "running",
	})
}

func handleHealth(c echo.Context) error {
	return c.JSON(200, map[string]string{
		"status":    "healthy",
		"service":   "classsphere-backend",
		"timestamp": "2025-10-06",
	})
}

func setupTestApp() *echo.Echo {
	e := echo.New()
	e.GET("/", handleWelcome)
	e.GET("/health", handleHealth)
	return e
}