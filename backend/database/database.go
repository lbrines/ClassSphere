package database

import (
	"classsphere-backend/models"
	"log"
	"os"
	"time"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// NewConnection creates a new database connection
func NewConnection(databasePath string) (*gorm.DB, error) {
	config := GetDatabaseConfig()
	db, err := gorm.Open(sqlite.Open(databasePath), config)
	if err != nil {
		return nil, err
	}

	// Configure connection pool
	sqlDB, err := db.DB()
	if err != nil {
		return nil, err
	}

	// Set maximum number of open connections
	sqlDB.SetMaxOpenConns(25)
	// Set maximum number of idle connections
	sqlDB.SetMaxIdleConns(5)
	// Set maximum lifetime of connections
	sqlDB.SetConnMaxLifetime(5 * time.Minute)

	return db, nil
}

// GetDatabaseConfig returns GORM configuration
func GetDatabaseConfig() *gorm.Config {
	logLevel := logger.Error
	if os.Getenv("APP_ENV") == "development" {
		logLevel = logger.Info
	}

	return &gorm.Config{
		Logger: logger.New(
			log.New(os.Stdout, "\r\n", log.LstdFlags),
			logger.Config{
				SlowThreshold:             time.Second,
				LogLevel:                  logLevel,
				IgnoreRecordNotFoundError: true,
				Colorful:                  true,
			},
		),
		NowFunc: func() time.Time {
			return time.Now().UTC()
		},
	}
}

// AutoMigrate runs database migrations
func AutoMigrate(db *gorm.DB) error {
	return db.AutoMigrate(
		&models.User{},
		// Add other models here as they're created
	)
}

// InitializeDatabase creates connection and runs migrations
func InitializeDatabase(databasePath string) (*gorm.DB, error) {
	db, err := NewConnection(databasePath)
	if err != nil {
		return nil, err
	}

	err = AutoMigrate(db)
	if err != nil {
		return nil, err
	}

	return db, nil
}

// CloseDatabase closes the database connection
func CloseDatabase(db *gorm.DB) error {
	sqlDB, err := db.DB()
	if err != nil {
		return err
	}
	return sqlDB.Close()
}

// HealthCheck performs a database health check
func HealthCheck(db *gorm.DB) error {
	sqlDB, err := db.DB()
	if err != nil {
		return err
	}
	return sqlDB.Ping()
}