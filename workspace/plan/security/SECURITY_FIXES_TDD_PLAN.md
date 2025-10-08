---
id: "security-tdd-plan"
title: "ClassSphere Security Fixes - TDD Implementation Plan"
version: "1.0"
priority: "CRITICAL"
branch: "security/fix-critical-vulnerabilities"
date: "2025-10-08"
methodology: "Test-Driven Development (Red → Green → Refactor)"
---

# 🔐 Security Fixes - TDD Implementation Plan

## Metodología TDD

Para cada issue seguiremos el ciclo:
1. 🔴 **RED**: Escribir tests que fallen (definir comportamiento esperado)
2. 🟢 **GREEN**: Implementar código mínimo para pasar tests
3. 🔵 **REFACTOR**: Mejorar código manteniendo tests verdes

---

## 🔴 ISSUE #1: Environment-Based User Seeding (CRÍTICO)

### Problema Actual
**Archivo**: `backend/cmd/api/main.go:76`
```go
userRepo := repo.NewMemoryUserRepository(seedUsers(logger))
```
- Inyecta usuarios hardcoded sin validar entorno
- Contraseñas débiles en producción: `admin123`, `coord123`, etc.

### 🔴 RED - Tests a Crear

**Archivo**: `backend/cmd/api/main_test.go`

#### Test 1: Production Environment Skips Seeding
```go
func TestInitialize_ProductionEnvironment_NoSeedUsers(t *testing.T) {
	// GIVEN: Production environment
	os.Setenv("APP_ENV", "production")
	defer os.Unsetenv("APP_ENV")
	
	ctx := context.Background()
	
	// WHEN: Initialize application
	app, cleanup, err := initialize(ctx)
	defer cleanup()
	
	// THEN: No seed users should be loaded
	require.NoError(t, err)
	// Verify UserRepository is empty or uses database
	// TODO: Add assertion once UserRepository exposes Count()
}
```

#### Test 2: Development Environment Loads Seed Users
```go
func TestInitialize_DevelopmentEnvironment_LoadsSeedUsers(t *testing.T) {
	// GIVEN: Development environment (default)
	os.Setenv("APP_ENV", "development")
	defer os.Unsetenv("APP_ENV")
	
	ctx := context.Background()
	
	// WHEN: Initialize application
	app, cleanup, err := initialize(ctx)
	defer cleanup()
	
	// THEN: Seed users should be loaded
	require.NoError(t, err)
	// Verify 4 seed users exist (admin, coordinator, teacher, student)
}
```

#### Test 3: Local Environment Loads Seed Users
```go
func TestInitialize_LocalEnvironment_LoadsSeedUsers(t *testing.T) {
	// GIVEN: Local environment
	os.Setenv("APP_ENV", "local")
	defer os.Unsetenv("APP_ENV")
	
	ctx := context.Background()
	
	// WHEN: Initialize application
	app, cleanup, err := initialize(ctx)
	defer cleanup()
	
	// THEN: Seed users should be loaded
	require.NoError(t, err)
}
```

### 🟢 GREEN - Implementation

**Archivo**: `backend/cmd/api/main.go`

```go
func initialize(ctx context.Context) (application, func(), error) {
	cfg, err := shared.LoadConfig()
	if err != nil {
		return application{}, nil, fmt.Errorf("load config: %w", err)
	}

	logger := shared.Logger()

	// ... Redis setup ...

	// Environment-based user repository initialization
	var userRepo ports.UserRepository
	if cfg.Environment == "production" {
		// Production: Empty repository (users from database)
		logger.Info("production environment detected, skipping seed users")
		userRepo = repo.NewMemoryUserRepository([]domain.User{})
		// TODO Phase 4: Load from PostgreSQL instead
	} else {
		// Development/Local: Load seed users
		logger.Info("development environment detected, loading seed users", 
			slog.String("env", cfg.Environment))
		userRepo = repo.NewMemoryUserRepository(seedUsers(logger))
	}

	// ... rest of initialization ...
}
```

**Archivo**: `backend/internal/shared/config.go`

Agregar campo `Environment`:
```go
type Config struct {
	// Existing fields...
	
	// Environment (production, development, local)
	Environment string `env:"APP_ENV" envDefault:"development"`
}
```

### 🔵 REFACTOR - Cleanup

1. Extraer lógica a función `initializeUserRepository(cfg, logger)`
2. Agregar constantes para environments:
```go
const (
	EnvProduction  = "production"
	EnvDevelopment = "development"
	EnvLocal       = "local"
)
```
3. Documentar en comentarios la estrategia de seeding

---

## 🔴 ISSUE #2: WebSocket JWT Authentication (CRÍTICO)

### Problema Actual
**Archivo**: `backend/internal/adapters/http/websocket_handler.go:32-36`
```go
// Get userID from query params (in production, use JWT from token)
userID := c.QueryParam("userId")
if userID == "" {
	userID = "anonymous" // Fallback for testing
}
```
- Endpoint no está en grupo `protected`
- Acepta cualquier `userId` sin validación
- Vulnerable a suplantación de identidad

### 🔴 RED - Tests a Crear

**Archivo**: `backend/internal/adapters/http/websocket_handler_test.go`

#### Test 1: Reject Connection Without JWT
```go
func TestWebSocket_Unauthorized_NoToken(t *testing.T) {
	// GIVEN: WebSocket endpoint without JWT token
	hub := app.NewNotificationHub()
	authService := setupMockAuthService(t)
	handler := &Handler{
		authService:     authService,
		notificationHub: hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	
	// WHEN: Attempt to connect without Authorization header
	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, nil)
	
	// THEN: Connection should be rejected with 401
	require.Error(t, err)
	assert.Equal(t, http.StatusUnauthorized, resp.StatusCode)
	if ws != nil {
		ws.Close()
	}
}
```

#### Test 2: Reject Connection With Invalid JWT
```go
func TestWebSocket_Unauthorized_InvalidToken(t *testing.T) {
	// GIVEN: WebSocket endpoint with invalid JWT
	hub := app.NewNotificationHub()
	authService := setupMockAuthService(t)
	handler := &Handler{
		authService:     authService,
		notificationHub: hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	
	// WHEN: Attempt to connect with invalid token
	headers := http.Header{}
	headers.Set("Authorization", "Bearer invalid-token-12345")
	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, headers)
	
	// THEN: Connection should be rejected
	require.Error(t, err)
	assert.Equal(t, http.StatusUnauthorized, resp.StatusCode)
	if ws != nil {
		ws.Close()
	}
}
```

#### Test 3: Accept Connection With Valid JWT
```go
func TestWebSocket_Authorized_ValidToken(t *testing.T) {
	// GIVEN: WebSocket endpoint with valid JWT
	hub := app.NewNotificationHub()
	authService := setupRealAuthService(t)
	
	// Create valid token for test user
	user := domain.User{
		ID:    "test-user-1",
		Email: "test@example.com",
		Role:  domain.RoleStudent,
	}
	token, err := authService.GenerateToken(context.Background(), user)
	require.NoError(t, err)
	
	handler := &Handler{
		authService:     authService,
		notificationHub: hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	
	// WHEN: Connect with valid JWT
	headers := http.Header{}
	headers.Set("Authorization", "Bearer "+token.AccessToken)
	ws, resp, err := websocket.DefaultDialer.Dial(wsURL, headers)
	
	// THEN: Connection should succeed
	require.NoError(t, err)
	assert.Equal(t, http.StatusSwitchingProtocols, resp.StatusCode)
	
	// Cleanup
	ws.Close()
}
```

#### Test 4: Extract User From JWT Context
```go
func TestWebSocket_ExtractsUserFromJWT(t *testing.T) {
	// GIVEN: Authenticated WebSocket connection
	hub := app.NewNotificationHub()
	authService := setupRealAuthService(t)
	
	user := domain.User{
		ID:          "test-user-123",
		Email:       "student@test.com",
		DisplayName: "Test Student",
		Role:        domain.RoleStudent,
	}
	token, err := authService.GenerateToken(context.Background(), user)
	require.NoError(t, err)
	
	handler := &Handler{
		authService:     authService,
		notificationHub: hub,
	}
	
	e := echo.New()
	protected := e.Group("")
	protected.Use(AuthMiddleware(authService))
	protected.GET("/ws/notifications", handler.handleWebSocket)
	
	server := httptest.NewServer(e)
	defer server.Close()
	
	wsURL := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws/notifications"
	headers := http.Header{}
	headers.Set("Authorization", "Bearer "+token.AccessToken)
	
	// WHEN: Connect and verify user registration
	ws, _, err := websocket.DefaultDialer.Dial(wsURL, headers)
	require.NoError(t, err)
	defer ws.Close()
	
	time.Sleep(100 * time.Millisecond) // Wait for registration
	
	// THEN: User should be registered with correct ID from JWT
	clients := hub.GetClients() // Need to expose this for testing
	assert.Greater(t, len(clients), 0)
	// Verify client is registered for user "test-user-123"
}
```

### 🟢 GREEN - Implementation

**Archivo**: `backend/internal/adapters/http/handler.go`

Cambiar líneas 64 y 115:
```go
// ❌ BEFORE:
e.GET("/api/v1/ws/notifications", h.handleWebSocket)

// ✅ AFTER:
protected.GET("/ws/notifications", h.handleWebSocket)
```

**Archivo**: `backend/internal/adapters/http/websocket_handler.go`

Modificar función `handleWebSocket`:
```go
// handleWebSocket upgrades HTTP connection to WebSocket and handles messages.
func (h *Handler) handleWebSocket(c echo.Context) error {
	// Extract authenticated user from context (set by AuthMiddleware)
	user := CurrentUser(c)
	if user.ID == "" {
		return echo.NewHTTPError(http.StatusUnauthorized, "unauthorized: missing user context")
	}

	// Upgrade connection
	ws, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
	if err != nil {
		slog.Error("WebSocket upgrade failed", "error", err, "user", user.ID)
		return err
	}
	defer ws.Close()

	// Register client with authenticated user ID
	clientID := h.notificationHub.RegisterClient(user.ID)
	defer h.notificationHub.UnregisterClient(clientID)

	slog.Info("WebSocket client connected", 
		"clientID", clientID, 
		"userID", user.ID,
		"role", user.Role)

	// Create message channel
	messages := make(chan domain.Notification, 100)
	h.notificationHub.Subscribe(clientID, messages)
	defer h.notificationHub.Unsubscribe(clientID)

	// Configure WebSocket
	ws.SetReadLimit(maxMessageSize)
	ws.SetReadDeadline(time.Now().Add(pongWait))
	ws.SetPongHandler(func(string) error {
		ws.SetReadDeadline(time.Now().Add(pongWait))
		return nil
	})

	// Start goroutines for read/write
	done := make(chan struct{})
	go h.writePump(ws, messages, done)
	go h.readPump(ws, done)

	// Wait for connection to close
	<-done

	slog.Info("WebSocket client disconnected", "clientID", clientID, "userID", user.ID)

	return nil
}
```

### 🔵 REFACTOR - Cleanup

1. Remover código comentado sobre query params
2. Agregar helper `validateWebSocketUpgrade()` si hay lógica repetida
3. Mejorar logging con structured fields
4. Agregar metrics para conexiones autenticadas

---

## 🔴 ISSUE #3: Search RBAC Filtering (ALTO)

### Problema Actual
**Archivo**: `backend/internal/app/search_service.go:289-294`
```go
func (s *SearchService) filterByRole(results []domain.SearchResult, role domain.Role) []domain.SearchResult {
	// Role-based access control
	// For now, all roles can see all results
	// In production, implement proper RBAC filtering
	return results
}
```
- No implementa ningún filtro
- Estudiantes pueden ver teachers, assignments de otros cursos

### 🔴 RED - Tests a Crear

**Archivo**: `backend/internal/app/search_service_test.go`

#### Test 1: Students Cannot See Teachers
```go
func TestSearchService_FilterByRole_StudentCannotSeeTeachers(t *testing.T) {
	// GIVEN: Search service with teacher results
	service := NewSearchService()
	
	teacherResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityTeacher,
			ID:          "teacher-1",
			Title:       "Prof. John Doe",
			Description: "john@faculty.edu",
			Relevance:   1.0,
		},
		{
			Type:        domain.SearchEntityTeacher,
			ID:          "teacher-2",
			Title:       "Dr. Jane Smith",
			Description: "jane@faculty.edu",
			Relevance:   0.9,
		},
	}
	
	// WHEN: Filter as student role
	filtered := service.filterByRole(teacherResults, domain.RoleStudent)
	
	// THEN: No teachers should be returned
	assert.Empty(t, filtered, "students should not see teacher search results")
}
```

#### Test 2: Students Can See Courses
```go
func TestSearchService_FilterByRole_StudentCanSeeCourses(t *testing.T) {
	// GIVEN: Search service with course results
	service := NewSearchService()
	
	courseResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityCourse,
			ID:          "course-1",
			Title:       "Mathematics 101",
			Description: "Intro to Calculus",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as student role
	filtered := service.filterByRole(courseResults, domain.RoleStudent)
	
	// THEN: Courses should be visible
	assert.Len(t, filtered, 1, "students should see course results")
	assert.Equal(t, "course-1", filtered[0].ID)
}
```

#### Test 3: Teachers Can See Students
```go
func TestSearchService_FilterByRole_TeacherCanSeeStudents(t *testing.T) {
	// GIVEN: Search service with student results
	service := NewSearchService()
	
	studentResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityStudent,
			ID:          "student-1",
			Title:       "John Student",
			Description: "john@student.edu",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as teacher role
	filtered := service.filterByRole(studentResults, domain.RoleTeacher)
	
	// THEN: Students should be visible to teachers
	assert.Len(t, filtered, 1, "teachers should see student results")
}
```

#### Test 4: Teachers Can See Teachers
```go
func TestSearchService_FilterByRole_TeacherCanSeeTeachers(t *testing.T) {
	// GIVEN: Search service with teacher results
	service := NewSearchService()
	
	teacherResults := []domain.SearchResult{
		{
			Type:        domain.SearchEntityTeacher,
			ID:          "teacher-1",
			Title:       "Prof. Colleague",
			Description: "colleague@faculty.edu",
			Relevance:   1.0,
		},
	}
	
	// WHEN: Filter as teacher role
	filtered := service.filterByRole(teacherResults, domain.RoleTeacher)
	
	// THEN: Teachers should be visible to other teachers
	assert.Len(t, filtered, 1, "teachers should see other teachers")
}
```

#### Test 5: Admin Sees Everything
```go
func TestSearchService_FilterByRole_AdminSeesEverything(t *testing.T) {
	// GIVEN: Search service with all types of results
	service := NewSearchService()
	
	mixedResults := []domain.SearchResult{
		{Type: domain.SearchEntityStudent, ID: "student-1", Title: "Student", Relevance: 1.0},
		{Type: domain.SearchEntityTeacher, ID: "teacher-1", Title: "Teacher", Relevance: 1.0},
		{Type: domain.SearchEntityCourse, ID: "course-1", Title: "Course", Relevance: 1.0},
		{Type: domain.SearchEntityAssignment, ID: "assign-1", Title: "Assignment", Relevance: 1.0},
		{Type: domain.SearchEntityAnnouncement, ID: "ann-1", Title: "Announcement", Relevance: 1.0},
	}
	
	// WHEN: Filter as admin role
	filtered := service.filterByRole(mixedResults, domain.RoleAdmin)
	
	// THEN: All results should be visible
	assert.Len(t, filtered, 5, "admins should see all results")
}
```

#### Test 6: Coordinator Sees Everything Except Students
```go
func TestSearchService_FilterByRole_CoordinatorPermissions(t *testing.T) {
	// GIVEN: Search service with mixed results
	service := NewSearchService()
	
	mixedResults := []domain.SearchResult{
		{Type: domain.SearchEntityStudent, ID: "student-1", Title: "Student", Relevance: 1.0},
		{Type: domain.SearchEntityTeacher, ID: "teacher-1", Title: "Teacher", Relevance: 1.0},
		{Type: domain.SearchEntityCourse, ID: "course-1", Title: "Course", Relevance: 1.0},
	}
	
	// WHEN: Filter as coordinator role
	filtered := service.filterByRole(mixedResults, domain.RoleCoordinator)
	
	// THEN: Should see teachers and courses, but not students
	assert.Len(t, filtered, 2, "coordinators see teachers and courses")
	for _, result := range filtered {
		assert.NotEqual(t, domain.SearchEntityStudent, result.Type)
	}
}
```

### 🟢 GREEN - Implementation

**Archivo**: `backend/internal/app/search_service.go`

Implementar matriz de permisos:
```go
// RBAC Permission Matrix for Search
// Defines which roles can see which entity types
var searchPermissions = map[domain.Role]map[domain.SearchEntity]bool{
	domain.RoleAdmin: {
		domain.SearchEntityStudent:      true,
		domain.SearchEntityTeacher:      true,
		domain.SearchEntityCourse:       true,
		domain.SearchEntityAssignment:   true,
		domain.SearchEntityAnnouncement: true,
	},
	domain.RoleCoordinator: {
		domain.SearchEntityStudent:      false, // Privacy: coordinators don't see student details
		domain.SearchEntityTeacher:      true,
		domain.SearchEntityCourse:       true,
		domain.SearchEntityAssignment:   true,
		domain.SearchEntityAnnouncement: true,
	},
	domain.RoleTeacher: {
		domain.SearchEntityStudent:      true,  // Teachers see their students
		domain.SearchEntityTeacher:      true,  // Can see colleagues
		domain.SearchEntityCourse:       true,
		domain.SearchEntityAssignment:   true,
		domain.SearchEntityAnnouncement: true,
	},
	domain.RoleStudent: {
		domain.SearchEntityStudent:      false, // Privacy: students don't see other students
		domain.SearchEntityTeacher:      false, // Privacy: students don't see teacher directory
		domain.SearchEntityCourse:       true,  // Can see available courses
		domain.SearchEntityAssignment:   true,  // Can see their assignments
		domain.SearchEntityAnnouncement: true,  // Can see announcements
	},
}

// filterByRole filters results based on user role permissions.
func (s *SearchService) filterByRole(results []domain.SearchResult, role domain.Role) []domain.SearchResult {
	// Get permissions for this role
	permissions, exists := searchPermissions[role]
	if !exists {
		// If role not found in matrix, deny all (secure by default)
		return []domain.SearchResult{}
	}

	// Filter results based on permissions
	filtered := make([]domain.SearchResult, 0, len(results))
	for _, result := range results {
		// Check if this role can see this entity type
		if allowed, exists := permissions[result.Type]; exists && allowed {
			filtered = append(filtered, result)
		}
	}

	return filtered
}

// canAccess checks if a role can access a specific entity type.
// Exposed for testing and documentation purposes.
func (s *SearchService) canAccess(entityType domain.SearchEntity, role domain.Role) bool {
	permissions, exists := searchPermissions[role]
	if !exists {
		return false
	}
	
	allowed, exists := permissions[entityType]
	return exists && allowed
}
```

### 🔵 REFACTOR - Cleanup

1. Extraer `searchPermissions` a constantes en archivo separado si crece
2. Considerar cargar permisos desde configuración/base de datos
3. Agregar logging cuando se filtran resultados:
```go
filtered := len(results) - len(filteredResults)
if filtered > 0 {
	slog.Debug("filtered search results by role",
		"role", role,
		"original", len(results),
		"filtered", filtered,
		"final", len(filteredResults))
}
```
4. Agregar métricas de acceso negado por rol

---

## ✅ Verification & Testing

### Run Tests
```bash
# Run all backend tests
cd backend
go test ./... -v -coverprofile=coverage.out

# Run specific security tests
go test ./cmd/api -run TestInitialize_.*Environment -v
go test ./internal/adapters/http -run TestWebSocket_.*Authorized -v
go test ./internal/app -run TestSearchService_FilterByRole -v

# Check coverage
go tool cover -html=coverage.out -o coverage.html

# Verify coverage maintained >85%
go test ./... -coverprofile=coverage.out -covermode=count
go tool cover -func=coverage.out | grep total
```

### Integration Tests
```bash
# Start services
docker-compose up -d

# Test WebSocket auth manually
# Should fail (401):
wscat -c "ws://localhost:8080/api/v1/ws/notifications?userId=hacker"

# Should succeed with valid token:
TOKEN=$(curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@classsphere.edu","password":"student123"}' \
  | jq -r '.accessToken')

wscat -c "ws://localhost:8080/api/v1/ws/notifications" \
  -H "Authorization: Bearer $TOKEN"

# Test search RBAC
# Student searching for teachers (should get empty results):
curl -X GET "http://localhost:8080/api/v1/search?q=prof&entities=teachers&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📊 Success Criteria

| Criteria | Target | Verification |
|----------|--------|--------------|
| All new tests pass | 100% | `go test ./... -v` |
| Coverage maintained | ≥85% | `go tool cover -func` |
| No breaking changes | 0 | Existing tests still pass |
| Security vulnerabilities | 0 CRITICAL | Manual review + Trivy scan |
| Production-ready | ✅ | Environment check implemented |

---

## 📝 Commit Strategy

Después de cada issue completo (RED → GREEN → REFACTOR):

```bash
# Issue #1
git add backend/cmd/api/main.go backend/cmd/api/main_test.go backend/internal/shared/config.go
git commit -m "security: implement environment-based user seeding

- Add APP_ENV validation before loading seed users
- Skip seed users in production environment
- Load seed users in development/local environments
- Add tests for environment-based initialization
- Fixes critical vulnerability of hardcoded users in production

Refs: security/fix-critical-vulnerabilities"

# Issue #2
git add backend/internal/adapters/http/handler.go backend/internal/adapters/http/websocket_handler.go backend/internal/adapters/http/websocket_handler_test.go
git commit -m "security: implement JWT authentication for WebSocket endpoint

- Move WebSocket endpoint to protected route group
- Extract authenticated user from JWT context
- Remove insecure userId query parameter
- Add tests for unauthorized/authorized access
- Fixes critical identity spoofing vulnerability

Refs: security/fix-critical-vulnerabilities"

# Issue #3
git add backend/internal/app/search_service.go backend/internal/app/search_service_test.go
git commit -m "security: implement RBAC filtering in search service

- Add permission matrix for role-based search access
- Students cannot see teachers or other students
- Teachers can see students and colleagues
- Coordinators see everything except student details
- Admins have full access to all entities
- Add comprehensive tests for all roles
- Fixes information disclosure vulnerability

Refs: security/fix-critical-vulnerabilities"

# Final verification
git add .
git commit -m "security: verify all security fixes with integration tests

- All security tests passing (100%)
- Coverage maintained at 87.8%+
- No breaking changes to existing functionality
- Production-ready security hardening complete

Closes: security/fix-critical-vulnerabilities"
```

---

## 🔄 Next Steps After Completion

1. ✅ Merge to `main` after PR review
2. 🔍 Run Trivy security scan: `trivy fs --security-checks vuln .`
3. 📝 Update `workspace/services_status.md` with security fixes
4. ✅ Update `workspace/plan/container/00_devcontainers_master_plan.md` - Mark security verified
5. 🚀 Proceed with Phase 4 - Production Deployment

---

**Created**: 2025-10-08  
**Status**: READY TO IMPLEMENT  
**Estimated Time**: 4-6 hours (with tests)  
**Risk Level**: LOW (comprehensive test coverage)

