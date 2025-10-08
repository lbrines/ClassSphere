package main

import (
	"context"
	"fmt"
	"log"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/redis/go-redis/v9"
	"golang.org/x/crypto/bcrypt"

	"github.com/lbrines/classsphere/internal/adapters/cache"
	googleadapter "github.com/lbrines/classsphere/internal/adapters/google"
	httpadapter "github.com/lbrines/classsphere/internal/adapters/http"
	"github.com/lbrines/classsphere/internal/adapters/oauth"
	"github.com/lbrines/classsphere/internal/adapters/repo"
	"github.com/lbrines/classsphere/internal/app"
	"github.com/lbrines/classsphere/internal/domain"
	"github.com/lbrines/classsphere/internal/ports"
	"github.com/lbrines/classsphere/internal/shared"
)

var signalChannelFactory = func() (chan os.Signal, func()) {
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	return ch, func() { signal.Stop(ch) }
}

func main() {
	ctx := context.Background()

	app, cleanup, err := initialize(ctx)
	if err != nil {
		log.Fatalf("initialization error: %v", err)
	}
	defer cleanup()

	signalCh, stop := signalChannelFactory()
	defer stop()

	startServer(ctx, app.server, app.config.ServerPort, app.logger, signalCh)
}

type application struct {
	server *echo.Echo
	logger *slog.Logger
	config shared.Config
	cache  ports.Cache
}

func initialize(ctx context.Context) (application, func(), error) {
	cfg, err := shared.LoadConfig()
	if err != nil {
		return application{}, nil, fmt.Errorf("load config: %w", err)
	}

	logger := shared.Logger()

	redisClient := redis.NewClient(&redis.Options{
		Addr:     cfg.RedisAddr,
		Password: cfg.RedisPassword,
		DB:       cfg.RedisDB,
	})

	cacheAdapter := cache.NewRedisCache(redisClient)
	if err := cacheAdapter.Ping(ctx); err != nil {
		logger.Error("redis ping failed", slog.String("error", err.Error()))
	}

	userRepo := repo.NewMemoryUserRepository(seedUsers(logger))
	oauthProvider := oauth.NewGoogleOAuth(cfg.GoogleClientID, cfg.GoogleClientSecret, cfg.GoogleRedirectURL)

	authService, err := app.NewAuthService(userRepo, cacheAdapter, oauthProvider, cfg)
	if err != nil {
		return application{}, nil, fmt.Errorf("auth service: %w", err)
	}
	userService, err := app.NewUserService(userRepo)
	if err != nil {
		return application{}, nil, fmt.Errorf("user service: %w", err)
	}

	classroomProviders := []ports.ClassroomProvider{}
	mockProvider, err := googleadapter.NewClassroomService("", shared.IntegrationModeMock)
	if err != nil {
		return application{}, nil, fmt.Errorf("init mock classroom provider: %w", err)
	}
	classroomProviders = append(classroomProviders, mockProvider)

	if cfg.GoogleCredentials != "" {
		googleProvider, err := googleadapter.NewClassroomService(cfg.GoogleCredentials, shared.IntegrationModeGoogle)
		if err != nil {
			logger.Warn("google classroom provider unavailable", slog.String("error", err.Error()))
		} else {
			classroomProviders = append(classroomProviders, googleProvider)
		}
	}

	classroomService, err := app.NewClassroomService(cfg.ClassroomMode, classroomProviders...)
	if err != nil {
		return application{}, nil, fmt.Errorf("classroom service: %w", err)
	}

	notificationHub := app.NewNotificationHub()
	searchService := app.NewSearchService()

	server := httpadapter.NewWithSearch(authService, userService, classroomService, notificationHub, searchService)

	cleanup := func() {
		_ = cacheAdapter.Close()
	}

	return application{
		server: server,
		logger: logger,
		config: cfg,
		cache:  cacheAdapter,
	}, cleanup, nil
}

func startServer(ctx context.Context, e *echo.Echo, port int, logger *slog.Logger, signalCh <-chan os.Signal) {
	addr := fmt.Sprintf(":%d", port)
	go func() {
		if err := e.Start(addr); err != nil && err != http.ErrServerClosed {
			logger.Error("server failed", slog.String("error", err.Error()))
			os.Exit(1)
		}
	}()

	logger.Info("server started", slog.String("addr", addr))

	if signalCh == nil {
		ch, stop := signalChannelFactory()
		defer stop()
		signalCh = ch
	}

	<-signalCh

	ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()

	if err := e.Shutdown(ctx); err != nil {
		logger.Error("server shutdown failed", slog.String("error", err.Error()))
	}
	logger.Info("server stopped gracefully")
}

func seedUsers(logger *slog.Logger) []domain.User {
	users, err := createSeedUsers()
	if err != nil {
		logger.Error("failed to create seed users", slog.String("error", err.Error()))
		os.Exit(1)
	}
	return users
}

// hashPasswordFunc allows mocking in tests
var hashPasswordFunc = bcrypt.GenerateFromPassword

// createSeedUsers generates the initial users. Separated for testability.
func createSeedUsers() ([]domain.User, error) {
	adminHash, err := hashPasswordFunc([]byte("admin123"), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("hash admin password: %w", err)
	}
	coordinatorHash, err := hashPasswordFunc([]byte("coord123"), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("hash coordinator password: %w", err)
	}
	teacherHash, err := hashPasswordFunc([]byte("teach123"), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("hash teacher password: %w", err)
	}
	studentHash, err := hashPasswordFunc([]byte("stud123"), bcrypt.DefaultCost)
	if err != nil {
		return nil, fmt.Errorf("hash student password: %w", err)
	}

	return []domain.User{
		{
			ID:             "admin-1",
			Email:          "admin@classsphere.edu",
			DisplayName:    "Admin",
			HashedPassword: string(adminHash),
			Role:           domain.RoleAdmin,
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
		{
			ID:             "coord-1",
			Email:          "coordinator@classsphere.edu",
			DisplayName:    "Coordinator",
			HashedPassword: string(coordinatorHash),
			Role:           domain.RoleCoordinator,
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
		{
			ID:             "teacher-1",
			Email:          "teacher@classsphere.edu",
			DisplayName:    "Teacher",
			HashedPassword: string(teacherHash),
			Role:           domain.RoleTeacher,
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
		{
			ID:             "student-1",
			Email:          "student@classsphere.edu",
			DisplayName:    "Student",
			HashedPassword: string(studentHash),
			Role:           domain.RoleStudent,
			CreatedAt:      time.Now(),
			UpdatedAt:      time.Now(),
		},
	}, nil
}
